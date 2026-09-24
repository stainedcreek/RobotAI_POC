import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32, String


class DecisionNode(Node):
    """
    任務決策 node,含故障處理(fault handling)。

    正常規則(依優先順序):
      confidence < 0.8              -> HOLD          (AI 信心不足)
      detected_object == 'none'     -> SEARCH         (沒偵測到目標)
      distance <= 1.0m              -> STOP           (太近,安全距離)
      distance > 1.0m               -> MOVE_FORWARD

    故障規則(優先級最高,蓋過上面所有規則):
      任一輸入來源(object / confidence / distance)超過 TIMEOUT_SEC
      沒有更新資料 -> SAFE_STOP
      模擬情境:sensor_node 或 lidar_node 當機、斷線、被 kill 掉。

    輸入:
      /detected_object (String)  <- ai_node
      /confidence (Float32)      <- ai_node
      /distance (Float32)        <- lidar_node
    輸出:
      /move_command (String)
    """

    CONFIDENCE_THRESHOLD = 0.8
    SAFE_DISTANCE = 1.0
    TIMEOUT_SEC = 3.0

    def __init__(self):
        super().__init__('decision_node')

        self.detected_object = None
        self.confidence = None
        self.distance = None

        self.last_object_time = None
        self.last_confidence_time = None
        self.last_distance_time = None

        self.in_safety_stop = False

        self.create_subscription(String, '/detected_object', self.object_callback, 10)
        self.create_subscription(Float32, '/confidence', self.confidence_callback, 10)
        self.create_subscription(Float32, '/distance', self.distance_callback, 10)

        self.command_pub = self.create_publisher(String, '/move_command', 10)

        # 每 0.5 秒檢查一次是否有任何來源逾時沒更新
        self.safety_timer = self.create_timer(0.5, self.check_timeouts)

    def object_callback(self, msg):
        self.detected_object = msg.data
        self.last_object_time = self.get_clock().now()
        self.evaluate()

    def confidence_callback(self, msg):
        self.confidence = msg.data
        self.last_confidence_time = self.get_clock().now()
        self.evaluate()

    def distance_callback(self, msg):
        self.distance = msg.data
        self.last_distance_time = self.get_clock().now()
        self.evaluate()

    def check_timeouts(self):
        """故障監控:任一來源太久沒更新 -> 進入 SAFE_STOP。"""
        now = self.get_clock().now()
        timestamps = {
            'detected_object': self.last_object_time,
            'confidence': self.last_confidence_time,
            'distance': self.last_distance_time,
        }

        timed_out_sources = []
        for name, last_time in timestamps.items():
            if last_time is None:
                # 一次都還沒收過資料,也視為異常(尚未上線 / 已斷線)
                timed_out_sources.append(name)
                continue
            elapsed = (now - last_time).nanoseconds / 1e9
            if elapsed > self.TIMEOUT_SEC:
                timed_out_sources.append(name)

        if timed_out_sources:
            if not self.in_safety_stop:
                self.get_logger().error(
                    f'[SAFETY] Timeout on: {timed_out_sources}. Entering SAFE_STOP.'
                )
            self.in_safety_stop = True
            self.publish_command('SAFE_STOP')
        else:
            if self.in_safety_stop:
                self.get_logger().info('[SAFETY] All sources recovered. Resuming normal operation.')
            self.in_safety_stop = False

    def evaluate(self):
        # 故障中,一切以 check_timeouts 發出的 SAFE_STOP 為準,不再判斷正常邏輯
        if self.in_safety_stop:
            return

        # 資料還沒到齊之前先不下決定
        if self.detected_object is None or self.confidence is None or self.distance is None:
            return

        if self.confidence < self.CONFIDENCE_THRESHOLD:
            command = 'HOLD'
        elif self.detected_object == 'none':
            command = 'SEARCH'
        elif self.distance <= self.SAFE_DISTANCE:
            command = 'STOP'
        else:
            command = 'MOVE_FORWARD'

        self.publish_command(command)
        self.get_logger().info(
            f'[DECISION] {command} '
            f'(object={self.detected_object}, confidence={self.confidence:.2f}, distance={self.distance})'
        )

    def publish_command(self, command: str):
        msg = String()
        msg.data = command
        self.command_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = DecisionNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

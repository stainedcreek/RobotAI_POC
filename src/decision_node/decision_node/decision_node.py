import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32, String


class DecisionNode(Node):
    """
    任務決策 node。

    規則(依優先順序):
      confidence < 0.8              -> HOLD          (AI 信心不足,先不動作)
      detected_object == 'none'     -> SEARCH         (沒偵測到目標)
      distance <= 1.0m              -> STOP           (太近,安全距離)
      distance > 1.0m               -> MOVE_FORWARD

    輸入:
      /detected_object (String)  <- ai_node
      /confidence (Float32)      <- ai_node
      /distance (Float32)        <- sensor_node
    輸出:
      /move_command (String)
    """

    CONFIDENCE_THRESHOLD = 0.8
    SAFE_DISTANCE = 1.0

    def __init__(self):
        super().__init__('decision_node')

        self.detected_object = None
        self.confidence = None
        self.distance = None

        self.create_subscription(String, '/detected_object', self.object_callback, 10)
        self.create_subscription(Float32, '/confidence', self.confidence_callback, 10)
        self.create_subscription(Float32, '/distance', self.distance_callback, 10)

        self.command_pub = self.create_publisher(String, '/move_command', 10)

    def object_callback(self, msg):
        self.detected_object = msg.data
        self.evaluate()

    def confidence_callback(self, msg):
        self.confidence = msg.data
        self.evaluate()

    def distance_callback(self, msg):
        self.distance = msg.data
        self.evaluate()

    def evaluate(self):
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

        msg = String()
        msg.data = command
        self.command_pub.publish(msg)
        self.get_logger().info(
            f'[DECISION] {command} '
            f'(object={self.detected_object}, confidence={self.confidence:.2f}, distance={self.distance})'
        )


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

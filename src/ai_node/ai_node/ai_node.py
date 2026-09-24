import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool, Float32, String


class AiNode(Node):
    """
    模擬 AI Perception node。

    重點不是訓練模型,而是示範「AI inference 如何以獨立 ROS2 node
    的形式接進系統」:輸入感測資料,輸出 object 與 confidence,
    跟後面的 decision_node 用 topic 解耦。

    輸入:
      /person_detected (Bool)  <- 來自 sensor_node
    輸出:
      /detected_object (String)  'person' 或 'none'
      /confidence (Float32)

    confidence 是可調的 parameter,模擬 AI 判斷信心值不穩定的情況:
      ros2 param set /ai_node confidence 0.5
    用來測試 decision_node 在低信心時是否正確進入 HOLD。
    """

    def __init__(self):
        super().__init__('ai_node')

        self.declare_parameter('confidence', 0.92)

        self.create_subscription(Bool, '/person_detected', self.on_sensor_data, 10)

        self.object_pub = self.create_publisher(String, '/detected_object', 10)
        self.confidence_pub = self.create_publisher(Float32, '/confidence', 10)

    def on_sensor_data(self, msg: Bool):
        confidence = self.get_parameter('confidence').get_parameter_value().double_value
        detected_object = 'person' if msg.data else 'none'

        object_msg = String()
        object_msg.data = detected_object
        self.object_pub.publish(object_msg)

        confidence_msg = Float32()
        confidence_msg.data = float(confidence)
        self.confidence_pub.publish(confidence_msg)

        self.get_logger().info(f'[AI] object={detected_object} confidence={confidence:.2f}')


def main(args=None):
    rclpy.init(args=args)
    node = AiNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

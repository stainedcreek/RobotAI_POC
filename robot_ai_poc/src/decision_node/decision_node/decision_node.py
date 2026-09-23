import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool, Float32, String


class DecisionNode(Node):
    """
    任務決策 node。

    規則:
      person = False              -> SEARCH
      person = True, distance > 1.0m  -> MOVE_FORWARD
      person = True, distance <= 1.0m -> STOP
    """

    def __init__(self):
        super().__init__('decision_node')

        self.person_detected = False
        self.distance = None

        self.create_subscription(Bool, '/person_detected', self.person_callback, 10)
        self.create_subscription(Float32, '/distance', self.distance_callback, 10)

        self.command_pub = self.create_publisher(String, '/move_command', 10)

    def person_callback(self, msg):
        self.person_detected = msg.data
        self.evaluate()

    def distance_callback(self, msg):
        self.distance = msg.data
        self.evaluate()

    def evaluate(self):
        if not self.person_detected:
            command = 'SEARCH'
        elif self.distance is None:
            return  # 還沒收到 distance,先不下決定
        elif self.distance <= 1.0:
            command = 'STOP'
        else:
            command = 'MOVE_FORWARD'

        msg = String()
        msg.data = command
        self.command_pub.publish(msg)
        self.get_logger().info(f'[DECISION] {command}')


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

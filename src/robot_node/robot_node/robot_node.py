import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class RobotNode(Node):
    """虛擬機器人 node:接收 /move_command,模擬執行動作。"""

    def __init__(self):
        super().__init__('robot_node')
        self.create_subscription(String, '/move_command', self.command_callback, 10)

    def command_callback(self, msg):
        self.get_logger().info(f'[ROBOT] {msg.data}')


def main(args=None):
    rclpy.init(args=args)
    node = RobotNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

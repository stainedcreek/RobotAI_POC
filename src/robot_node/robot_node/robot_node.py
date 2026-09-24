import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist


class RobotNode(Node):
    """
    虛擬機器人 node:接收 /move_command,轉換成 Twist 速度指令,
    發布到 /model/vehicle_blue/cmd_vel 控制 Gazebo 裡的機器人。

    (Day 6 之前這個 node 只會印文字;現在同一份 /move_command
    邏輯不用改,只是多接了一個輸出,讓決策真的能驅動模擬機器人,
    這也是展示「決策層跟執行層解耦」的好例子。)

    對應關係:
      MOVE_FORWARD -> 前進
      SEARCH       -> 原地旋轉(尋找目標)
      STOP / HOLD / SAFE_STOP -> 完全靜止
    """

    LINEAR_SPEED = 0.5
    ANGULAR_SEARCH_SPEED = 0.3

    def __init__(self):
        super().__init__('robot_node')
        self.create_subscription(String, '/move_command', self.command_callback, 10)
        self.cmd_vel_pub = self.create_publisher(Twist, '/model/vehicle_blue/cmd_vel', 10)

    def command_callback(self, msg):
        command = msg.data
        self.get_logger().info(f'[ROBOT] {command}')

        twist = Twist()
        if command == 'MOVE_FORWARD':
            twist.linear.x = self.LINEAR_SPEED
        elif command == 'SEARCH':
            twist.angular.z = self.ANGULAR_SEARCH_SPEED
        # STOP / HOLD / SAFE_STOP 都維持全零(靜止),不用另外設定

        self.cmd_vel_pub.publish(twist)


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

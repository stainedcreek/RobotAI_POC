import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32


class LidarNode(Node):
    """
    虛擬 LiDAR / 距離感測器 node。

    這是系統裡的第二個、完全獨立的感測來源:
    sensor_node(相當於 camera)負責 person_detected,
    lidar_node 只負責 distance,兩者互不知道對方存在。

    真正的「融合」發生在 decision_node:它同時訂閱
    ai_node 的 /detected_object、/confidence 和這裡的 /distance,
    綜合三個來源才下決策。

    數值一樣是可調參數,方便測試:
      ros2 param set /lidar_node distance 0.7
    """

    def __init__(self):
        super().__init__('lidar_node')

        self.declare_parameter('distance', 2.5)

        self.distance_pub = self.create_publisher(Float32, '/distance', 10)
        self.timer = self.create_timer(1.0, self.publish_distance)

    def publish_distance(self):
        distance = self.get_parameter('distance').get_parameter_value().double_value

        msg = Float32()
        msg.data = float(distance)
        self.distance_pub.publish(msg)

        self.get_logger().info(f'[LIDAR] distance={distance}')


def main(args=None):
    rclpy.init(args=args)
    node = LidarNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

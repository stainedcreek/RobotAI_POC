import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool, Float32


class SensorNode(Node):
    """
    虛擬感測器 node。
    每秒發布:
      /person_detected (Bool)
      /distance (Float32)
    數值來自 ROS2 parameter,可以在跑的時候用
    `ros2 param set /sensor_node distance 0.8` 即時改變,
    不用重開 node,方便測試 decision_node 的反應。
    """

    def __init__(self):
        super().__init__('sensor_node')

        self.declare_parameter('person_detected', True)
        self.declare_parameter('distance', 2.5)

        self.person_pub = self.create_publisher(Bool, '/person_detected', 10)
        self.distance_pub = self.create_publisher(Float32, '/distance', 10)

        self.timer = self.create_timer(1.0, self.publish_sensor_data)

    def publish_sensor_data(self):
        person = self.get_parameter('person_detected').get_parameter_value().bool_value
        distance = self.get_parameter('distance').get_parameter_value().double_value

        person_msg = Bool()
        person_msg.data = person
        self.person_pub.publish(person_msg)

        distance_msg = Float32()
        distance_msg.data = float(distance)
        self.distance_pub.publish(distance_msg)

        self.get_logger().info(f'[SENSOR] person={person} distance={distance}')


def main(args=None):
    rclpy.init(args=args)
    node = SensorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool


class SensorNode(Node):
    """
    虛擬感測器 node(相當於 camera 觸發源)。

    Day4 之後只負責:
      /person_detected (Bool)

    distance 已經拆到獨立的 lidar_node,
    兩個感測器互相獨立,是系統裡的第二個資料來源。
    """

    def __init__(self):
        super().__init__('sensor_node')

        self.declare_parameter('person_detected', True)

        self.person_pub = self.create_publisher(Bool, '/person_detected', 10)
        self.timer = self.create_timer(1.0, self.publish_sensor_data)

    def publish_sensor_data(self):
        person = self.get_parameter('person_detected').get_parameter_value().bool_value

        person_msg = Bool()
        person_msg.data = person
        self.person_pub.publish(person_msg)

        self.get_logger().info(f'[SENSOR] person={person}')


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

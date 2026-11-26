import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32


class MonitorNode(Node):
    def __init__(self):
        super().__init__('monitor_node')

        self.subscription = self.create_subscription(
            Float32,
            '/battery_level',
            self.listener_callback,
            10,
        )
        self.get_logger().info('monitor_node started.')

    def listener_callback(self, msg):
        level = msg.data
        if level < 20.0:
            self.get_logger().warn(f'LOW BATTERY WARNING: {level:.1f}%')
        else:
            self.get_logger().info(f'Battery level: {level:.1f}%')


def main(args=None):
    rclpy.init(args=args)
    node = MonitorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
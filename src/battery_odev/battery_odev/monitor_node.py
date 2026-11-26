import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from std_srvs.srv import Trigger


class MonitorNode(Node):
    def __init__(self):
        super().__init__('monitor_node')

        self.subscription = self.create_subscription(
            Float32,
            '/battery_level',
            self.listener_callback,
            10,
        )

        self.recharge_client = self.create_client(Trigger, '/recharge')
        self.recharging = False
        self.get_logger().info('monitor_node started (auto-recharge active).')

    def listener_callback(self, msg):
        level = msg.data
        if level < 20.0:
            self.get_logger().warn(f'LOW BATTERY WARNING: {level:.1f}%')
        else:
            self.get_logger().info(f'Battery level: {level:.1f}%')

        if level < 5.0 and not self.recharging:
            self.call_recharge_service()

    def call_recharge_service(self):
        if not self.recharge_client.service_is_ready():
            self.get_logger().warn('/recharge service is not ready yet.')
            return

        self.recharging = True
        self.get_logger().info('Battery below 5%! Calling /recharge automatically...')

        request = Trigger.Request()
        future = self.recharge_client.call_async(request)
        future.add_done_callback(self.recharge_response_callback)

    def recharge_response_callback(self, future):
        try:
            response = future.result()
            self.get_logger().info(f'Auto-recharge response: {response.message}')
        except Exception as e:
            self.get_logger().error(f'Service call failed: {e}')
        finally:
            self.recharging = False


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
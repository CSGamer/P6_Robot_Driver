# my_publisher_pkg/number_publisher.py

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32

class NumberPublisher(Node):
    def __init__(self):
        super().__init__('number_publisher')
        self.publisher_ = self.create_publisher(Int32, 'number', 10)
        timer_period = 0.1  # seconds (10 times a second)
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        msg = Int32()
        msg.data = 1
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%d"' % msg.data)

def main(args=None):
    rclpy.init(args=args)
    node = NumberPublisher()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

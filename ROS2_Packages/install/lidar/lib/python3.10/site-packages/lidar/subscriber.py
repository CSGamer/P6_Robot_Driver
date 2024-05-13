import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class DistanceSubscriber(Node):
	def __init__(self):
		super().__init__('distance_subscriber')
		self.subscription = self.create_subscription(
			Float32, 
			'distance',
			self.listener_callback,
			10)
		self.subscription
		self.get_logger().info('Distance subscriber node initialized')
		
	def listener_callback(self, msg):
		distance = msg.data
		print(f"Distance: {distance}")
		
def main(args=None):
	rclpy.init(args=args)
	distance_subscriber = DistanceSubscriber()
	try:
		rclpy.spin(distance_subscriber)
	except KeyboardInterrupt:
		pass
	distance_subscriber.destroy_node()
	rclpy.shutdown()
	
if __name__ == '__main__':
	main()

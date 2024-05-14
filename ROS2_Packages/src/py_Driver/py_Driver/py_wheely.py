import os
import select
import sys
import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from geometry_msgs.msg import Twist
from rclpy.qos import QoSProfile

if os.name == 'nt':
	import msvcrt
else:
	import termios
	import tty

TURTLEBOT3_MODEL = os.environ['TURTLEBOT3_MODEL']

msg = """
Controller Test TurtleBot
 ---Put some message here

CTRL-C to quit
"""

e = """
Communications Failed
"""

class MinimalSubscriber(Node):

	def __init__(self):
		super().__init__('minimal_subscriber')
		self.get_logger().warning('goodmorning')
		self.subscription = self.create_subscription(
		String,
			'Cam_Detections',
			self.ang_sub,
			10)
		self.subscription  # prevent unused variable warning
		self.init_Controller
		self.get_logger().warning('goodmorning')

	def ang_sub(self, msg):
		self.get_logger().info('I heard: "%s"' % msg.data)
		self.ang_reg(msg)

	def ang_reg(self, msg):
		# Extract the string data from the message
		values_str = msg.data
		# Remove the square brackets from the string
		values_str = values_str[1:-1]
		# Split the string into individual values
		values = values_str.split(',')
		values[-1] = values[-1].rstrip(']')
		# Convert each value to float
		float_values = [float(value.strip()) for value in values]
		print(float_values)

	def print_vels(self,target_linear_velocity, target_angular_velocity):
		print('currently:\tlinear velocity {0}\t angular velocity {1} '.format(
			target_linear_velocity,
			target_angular_velocity))
	
	def make_simple_profile(self, output, input, slop):
		if input > output:
			output = min(input, output + slop)
		elif input < output:
			output = max(input, output - slop)
		else:
			output = input
		
		return output

	def constrain(self, input_vel, low_bound, high_bound):
		if input_vel < low_bound:
			input_vel = low_bound
		elif input_vel > high_bound:
			input_vel = high_bound
		else:
			input_vel = input_vel

		return input_vel
	
	def init_Controller(self):
		settings = None
		if os.name != 'nt':
			settings = termios.tcgetattr(sys.stdin)

		rclpy.init()

		qos = QoSProfile(depth=10)
		node = rclpy.create_node('teleop_keyboard')
		pub = node.create_publisher(Twist, 'cmd_vel', qos)

		status = 0
		target_linear_velocity = 0.0
		target_angular_velocity = 0.0
		control_linear_velocity = 0.0
		control_angular_velocity = 0.0
		while(1):
			print('im working')



def main(args=None):
	rclpy.init(args=args)
	minimal_subscriber = MinimalSubscriber()
	minimal_subscriber.get_logger().info('yellow')
	rclpy.spin(minimal_subscriber)
	minimal_subscriber.get_logger().info('yoink')
	# Destroy the node explicitly
	# (optional - otherwise it will be done automatically
	# when the garbage collector destroys the node object)
	minimal_subscriber.destroy_node()
	rclpy.shutdown()


if __name__ == '__main__':
    main()

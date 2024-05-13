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
			self.listener_callback,
			10)
		self.subscription  # prevent unused variable warning
		self.init_Controller
		self.get_logger().warning('goodmorning')

	def listener_callback(self, msg):
		self.get_logger().info('I hea rd: "%s"' % msg.data)

	def print_vels(target_linear_velocity, target_angular_velocity):
		print('currently:\tlinear velocity {0}\t angular velocity {1} '.format(
			target_linear_velocity,
			target_angular_velocity))
	def make_simple_profile(output, input, slop):
		if input > output:
			output = min(input, output + slop)
		elif input < output:
			output = max(input, output - slop)
		else:
			output = input
		
		return output


	def constrain(input_vel, low_bound, high_bound):
		if input_vel < low_bound:
			input_vel = low_bound
		elif input_vel > high_bound:
			input_vel = high_bound
		else:
			input_vel = input_vel

		return input_vel
	
	def init_Controller():
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

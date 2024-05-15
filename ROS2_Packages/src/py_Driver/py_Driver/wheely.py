import os
import select
import sys
import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from geometry_msgs.msg import Twist
from rclpy.qos import QoSProfile


LIN_VEL_STEP_SIZE = 0.01

class Controller(Node):
    target_linear_velocity = 0.0
    target_angular_velocity = 2.0
    control_linear_velocity = 0.0
    control_angular_velocity = 0.0
    pub = None
	
    def __init__(self,publisher):
        super().__init__('controller')
        self.pub = publisher
        self.get_logger().info('controller started')

    def make_simple_profile(self,output, input, slop):
        if input > output:
            output = min(input, output + slop)
        elif input < output:
            output = max(input, output - slop)
        else:
            output = input
        return output

    def drive_test(self):
        twist = Twist()
        self.control_linear_velocity = self.make_simple_profile(self.control_linear_velocity, self.target_linear_velocity, (LIN_VEL_STEP_SIZE / 2.0))
        twist.linear.x = self.control_linear_velocity
        twist.linear.y = 0.0
        twist.linear.z = 0.0
        self.control_angular_velocity = self.make_simple_profile(self.control_angular_velocity, self.target_angular_velocity, (LIN_VEL_STEP_SIZE / 2.0))
        twist.angular.x = 0.0
        twist.angular.y = 0.0
        twist.angular.z = self.control_angular_velocity
        self.pub.publish(twist)

class Program(Node):
    contr = None
    def __init__(self,publisher):
        super().__init__('program')
        self.get_logger().info('starting controller ')    
        self.contr = Controller(publisher)
        self.get_logger().info('starting main')
        self.subscription = self.create_subscription(
		String,
			'Cam_Detections',
			self.ang_sub,
			10)
        self.subscription  # prevent unused variable warning
        self.subscription = self.create_subscription(
		String,
			'distance',
			self.dist_sub,
			10)
        self.subscription  # prevent unused variable warning
        self.get_logger().info('main started')


    def ang_sub(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)
        self.ang_reg(msg)

    def ang_reg(self, msg):
        self.contr.drive_test()

    def dist_sub(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)
        self.dist_reg(msg)

    def dist_reg(self, msg):
        self.drive_test()
		


def main(args=None):
    rclpy.init(args=args)
    print("Starting Program")
    qos = QoSProfile(depth=10)
    node = rclpy.create_node('teleop_keyboard')
    pub = node.create_publisher(Twist, 'cmd_vel', qos)

	#node = rclpy.create_node('teleop_keyboard')
    minimal_subscriber = Program(pub)

    rclpy.spin(minimal_subscriber)

	# Destroy the node explicitly
	# (optional - otherwise it will be done automatically
	# when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()





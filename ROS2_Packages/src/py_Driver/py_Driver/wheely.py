import os
import select
import sys
import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist
from rclpy.qos import QoSProfile

TURTLEBOT3_MODEL = os.environ['TURTLEBOT3_MODEL']

LIN_VEL_STEP_SIZE = 0.01

BURGER_MAX_LIN_VEL = 0.22
BURGER_MAX_ANG_VEL = 2.84

WAFFLE_MAX_LIN_VEL = 0.26
WAFFLE_MAX_ANG_VEL = 1.82

ANGLE_SET_POINT = 0 #img x-coordinate
DIST_SET_POINT = 1500 #mm


class Controller(Node):
    target_linear_velocity = 0.0
    target_angular_velocity = 0.0
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

    def constrain(self, input_vel, low_bound, high_bound):
        if input_vel < low_bound:
            input_vel = low_bound
        elif input_vel > high_bound:
            input_vel = high_bound
        else:
            input_vel = input_vel

        return input_vel
        
    def check_linear_limit_velocity(self, velocity):
        if TURTLEBOT3_MODEL == 'burger':
            return self.constrain(velocity, -BURGER_MAX_LIN_VEL, BURGER_MAX_LIN_VEL)
        else:
            return self.constrain(velocity, -WAFFLE_MAX_LIN_VEL, WAFFLE_MAX_LIN_VEL)


    def check_angular_limit_velocity(self, velocity):
        if TURTLEBOT3_MODEL == 'burger':
            return self.constrain(velocity, -BURGER_MAX_ANG_VEL, BURGER_MAX_ANG_VEL)
        else:
            return self.constrain(velocity, -WAFFLE_MAX_ANG_VEL, WAFFLE_MAX_ANG_VEL)

    def set_angle_vel(self, val):
        self.target_angular_velocity = self.check_angular_limit_velocity(val)

    def set_velocity(self, val):
        self.get_logger().warning('speed_val "%s"' % val)
        val = val/1204
        self.target_linear_velocity = self.check_linear_limit_velocity(val)

    def drive(self):
        twist = Twist()
        #self.control_linear_velocity = self.make_simple_profile(self.control_linear_velocity, self.target_linear_velocity, (LIN_VEL_STEP_SIZE / 2.0))
        twist.linear.x = self.target_linear_velocity
        twist.linear.y = 0.0
        twist.linear.z = 0.0
        #self.control_angular_velocity = self.make_simple_profile(self.control_angular_velocity, self.target_angular_velocity, (LIN_VEL_STEP_SIZE / 2.0))
        twist.angular.x = 0.0
        twist.angular.y = 0.0
        twist.angular.z = self.target_angular_velocity
        self.pub.publish(twist)        

    def drive_test(self):
        self.target_angular_velocity = 20
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
		Float32,
			'distance',
			self.dist_sub,
			10)
        self.subscription  # prevent unused variable warning
        self.subscription = self.create_subscription(
		String,
			'Cam_Detections',
			self.ang_sub,
			10)
        self.subscription  # prevent unused variable warning
        self.subscription = self.create_subscription(
		String,
			'looper',
			self.looper,
			10)
        self.subscription  # prevent unused variable warning
        self.get_logger().info('main started')

    def looper(self):
        self.contr.drive()

    def ang_sub(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)

        #Structure [ID, x, y, width, height, FPS] 
        # Remove brackets and split by comma
        elements = msg.data.strip("[]\n").split(", ")
        
        # Convert elements to floats
        float_array = [float(element) for element in elements]

        error = None

        if (float_array[0] == 1): 
            error = float_array[1] + (float_array[3]/2)
            print(error)

        #print([flo for flo in float_array])
        
        self.ang_reg(error)

    def ang_reg(self, error):
        self.contr.set_angle(error)


    def dist_sub(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)
        error =float(msg.data) -  DIST_SET_POINT
        self.dist_reg(error)

    def dist_reg(self, error):
        error = error / 1000 * 86.67
        p = 10
        out = error* p
        self.contr.set_velocity(out)
        self.contr.drive()

    
		


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





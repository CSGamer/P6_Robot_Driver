import serial
import rclpy
import math
from rclpy.node import Node
from sensor_msgs.msg import LaserScan


class LaserPublisher(Node):
	def __init__(self):
		super().__init__('laser_publisher')
		self.publisher_ = self.create_publisher(LaserScan, 'laser_scan', 10)
		timer_period = 0.1 #seconds
		self.timer = self.create_timer(timer_period, self.publish_scan)
		self.serial_port = serial.Serial("/dev/ttyUSB0", baudrate = 230400)
		self.get_logger().info('Laser publisher node initialized')
		
	def publish_scan(self):
		scan_msg = LaserScan()
		scan_msg.header.frame_id = 'laser_frame'
		scan_msg.header.stamp = self.get_clock().now().to_msg()
		scan_msg.angle_min = -math.pi
		scan_msg.angle_max = math.pi
		scan_msg.angle_increment = math.pi / 180  # Assuming one-degree increment
		scan_msg.time_increment = 0.0  # Not specified
		scan_msg.range_min = 0.0  # Assuming minimum range
		scan_msg.range_max = 5000.0  # Assuming maximum range
		scan_msg.ranges = self.grab_data()  # Publish the data obtained from serial port
		self.publisher_.publish(scan_msg)
		
	def grab_data(self):
		while True:
			result = self.serial_port.read(42)
			if result[-1] == result[-2]:
				base_angle = (result[1] - 160) * 6
				for m in range(6):
					angle = base_angle + m
					if (0 <= angle < 30) or (329 <= angle < 360):
						distance = result[(6 * (m + 1)) + 1] * 256 + result[(6 * (m + 1))]
						print(f"Angle: {angle}, Distance: {distance}")  # Debug print
						if (0 <= angle < 30) or (330 <= angle < 360):
							if distance > 0:
								# Do something with the measured distance if needed
								pass
	def destroy_node(self):
		self.serial_port.close()  # Close the serial port
		super().destroy_node()

def main(args=None):
	rclpy.init(args=args)
	laser_publisher = LaserPublisher()
	try:
		rclpy.spin(laser_publisher)
	except KeyboardInterrupt:
		pass
	laser_publisher.destroy_node()
	rclpy.shutdown()

if __name__ == '__main__':
	main()
	

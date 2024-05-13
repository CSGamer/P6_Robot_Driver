import serial
import rclpy
import math
from rclpy.node import Node
from sensor_msgs.msg import LaserScan

class LaserPublisher(Node):
	def __init__(self):
		super().__init__('laser_publisher')
		self.publisher_ = self.create_publisher(LaserScan, 'laser_scan', 10)
		timer_period = 0.1  # seconds
		self.timer = self.create_timer(timer_period, self.publish_scan)
		self.serial_port = serial.Serial("/dev/ttyUSB0", baudrate=230400)
		self.get_logger().info('Laser publisher node initialized')
		self.angles_printed = set()
		self.distance_list = [0.0] * 360

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
		
		result = self.serial_port.read(42)
		if len(result) >= 42 and result[-1] == result[-2]:
			base_angle = (result[1] - 160) * 6
			for m in range(60):
				angle = base_angle + m * 6
				for n in range(6):
					current_angle = int(angle + n)
					if (0 <= current_angle <= 30) or (329 <= current_angle <= 359) or (current_angle <= 4):
						distance_index = (6 * (n + 1)) + 1
						distance = result[distance_index] * 256 + result[distance_index + 1]
						# Print distance in millimeters for every 5th angle
						if current_angle % 5 == 0:
							if 0 < distance < 10000:
								self.angles_printed.discard(current_angle)
								self.distance_list[current_angle] = float(distance)  # Convert to float
								print(f"Angle: {current_angle}, Distance: {distance}")  # Debug print
			scan_msg.ranges = self.distance_list
			self.publisher_.publish(scan_msg)
											
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


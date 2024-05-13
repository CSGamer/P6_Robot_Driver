import os
import serial
import rclpy
import math
from rclpy.node import Node
from std_msgs.msg import Float32

class LaserPublisher(Node):
	def __init__(self):
		super().__init__('laser_publisher')
		self.distance_publisher = self.create_publisher(Float32, 'distance', 10)
		self.serial_port = serial.Serial("/dev/ttyUSB0", baudrate = 230400)
		self.get_logger().info('Laser publisher node initialized')

	def clear_console(self):
		os.system('cls' if os.name == 'nt' else 'clear')
						
	def visualize_distance(self, angle, distance):
		if (329 == angle):
			print("\n\n\n\n\n")
		
		if (0 <= angle < 30) or (329 <= angle < 360):
			distance_chars = '#' * int(distance / 25)  # Adjust the scale as needed
			print(f"Angle: {angle} Distance: {distance} {' ' * (30 - len(distance_chars))}[{distance_chars}]")
		
	def publish_distances(self):
		number = 0
		while number < 5:
			result = self.serial_port.read(42)
			if result[-1] == result[-2]:
				base_angle = (result[1] - 160) * 6
				for m in range(6):
					angle = base_angle + m
					if (0 <= angle < 30) or (329 <= angle < 360):
						distance = result[(6 * (m + 1)) + 1] * 256 + result[(6 * (m + 1))] - 100
						self.distance_publisher.publish(Float32(data=float(distance)))
						#print(f"Angle: {angle}, Distance: {distance}")  # Debug print
						self.visualize_distance(angle,distance)
			number = number + 1


	def destroy_node(self):
		self.serial_port.close()  # Close the serial port
		super().destroy_node()

def main(args=None):
	rclpy.init(args=args)
	laser_publisher = LaserPublisher()
	try:
		laser_publisher.publish_distances()
	except KeyboardInterrupt:
		pass
	laser_publisher.destroy_node()
	rclpy.shutdown()

if __name__ == '__main__':
	main()
	

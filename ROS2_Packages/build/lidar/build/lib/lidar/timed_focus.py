import os
import serial
import rclpy
import math
from rclpy.node import Node
from std_msgs.msg import Float32
import time

class LaserPublisher(Node):
	publish_interval = 1.0 / 20  # 20 Hz
	last_publish_time = time.time()

	def __init__(self):
		super().__init__('laser_publisher')
		self.distance_publisher = self.create_publisher(Float32, 'distance', 10)
		self.serial_port = serial.Serial("/dev/ttyUSB0", baudrate = 230400)
		self.get_logger().info('Laser publisher node initialized')


	def clear_console(self):
		os.system('cls' if os.name == 'nt' else 'clear')
						
	def visualize_distance(self, angle, distance):
		if (329 == angle):
			self.clear_console()
		
		if (0 <= angle < 30) or (329 <= angle < 360):
			distance_chars = '#' * int(distance / 25)  # Adjust the scale as needed
			print(f"Angle: {angle} Distance: {distance} {' ' * (30 - len(distance_chars))}[{distance_chars}]")

	focus = [1,1,1,1,1,1]
	count = 1 

	def publish_distances(self):
		while True:
			result = self.serial_port.read(42) 
			if result[-1] == result[-2]:
				base_angle = (result[1] - 160) * 6
				for m in range(6):
					angle = base_angle + m
					if (0 <= angle <= 2 ) or ( 357 <= angle < 360 ):
						distance = result[(6 * (m + 1)) + 1] * 256 + result[(6 * (m + 1))] - 100
						#print(f"Angle: {angle}, Distance: {distance}")  # Debug print
						if (distance != -100):
							self.focus[self.count-1] = distance

						if (self.count == 6):
							median = sum(self.focus)
							median = median/6
							current_time = time.time()
							if current_time - self.last_publish_time >= self.publish_interval:
								self.distance_publisher.publish(Float32(data=float(median)))
								self.last_publish_time = current_time
							self.count = 0
						
						self.count +=1

						self.visualize_distance(angle,distance)


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
	

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
import os

def generate_launch_description():
    # Path to the robot launch file from turtlebot3_bringup package
    turtlebot3_bringup_dir = FindPackageShare(package='turtlebot3_bringup').find('turtlebot3_bringup')
    robot_launch_file = os.path.join(turtlebot3_bringup_dir, 'launch', 'robot.launch.py')

    return LaunchDescription([
        # Include the turtlebot3 robot.launch.py file
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(robot_launch_file)
        ),
        
        # Node from camera_pack
        Node(
            package='camera_pack',
            executable='Cam_Nano',
            name='Cam_Nano',
            output='screen'
        ),
        
        # Node from lidar
        Node(
            package='lidar',
            executable='timed_focus',
            name='focus_pub',
            output='screen'
        ),
        
        # Node from py_Driver
        Node(
            package='py_Driver',
            executable='routine',
            name='routine',
            output='screen'
        ),
    ])

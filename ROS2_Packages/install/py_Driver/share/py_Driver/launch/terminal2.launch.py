from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.substitutions import FindPackageShare
import os

def generate_launch_description():
    # Absolute path to the robot.launch.py file from turtlebot3_bringup package
    robot_launch_file = os.path.join(
        os.path.expanduser('~'), 'turtlebot3_ws', 'src', 'turtlebot3', 'turtlebot3_bringup', 'launch', 'robot.launch.py'
    )

    return LaunchDescription([
        # Include the turtlebot3 robot.launch.py file in a separate terminal
        ExecuteProcess(
            cmd=['gnome-terminal', '--', 'ros2', 'launch', 'turtlebot3_bringup', 'robot.launch.py'],
            output='screen'
        ),
        
        # Node from camera_pack in the current terminal
        ExecuteProcess(
            cmd=['ros2', 'run', 'camera_pack', 'cam_Nano'],
            output='screen'
        ),
        
        # Node from lidar in a separate terminal
        ExecuteProcess(
            cmd=['gnome-terminal', '--', 'ros2', 'run', 'lidar', 'focus_pub'],
            output='screen'
        ),
        
        # Node from py_Driver in a separate terminal
        ExecuteProcess(
            cmd=['gnome-terminal', '--', 'ros2', 'run', 'py_Driver', 'routine'],
            output='screen'
        ),
    ])
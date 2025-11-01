# gripper_bridge/launch/gripper_bridge.launch.py
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='gripper',
            executable='gripper_bridge_node',
            name='gripper_bridge',
            parameters=[{
                'port': '/dev/ttyUSB0',
                'baud': 115200,
                'command_timeout_s': 8.0,
                'verify_period_s': 0.2,
                'auto_find_usb': True
            }],
            output='screen'
        )
    ])

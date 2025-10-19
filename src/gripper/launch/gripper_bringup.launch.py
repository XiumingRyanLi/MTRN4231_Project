# launch/gripper_bringup.launch.py
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    serial_port_arg = DeclareLaunchArgument('serial_port', default_value='/dev/ttyACM0')
    baudrate_arg = DeclareLaunchArgument('baudrate', default_value='115200')
    action_name_arg = DeclareLaunchArgument('gripper_action_name', default_value='/gripper_controller/gripper_cmd')

    node = Node(
        package='gripper',
        executable='gripper_client',
        name='gripper_client',
        output='screen',
        parameters=[{
            'serial_port': LaunchConfiguration('serial_port'),
            'baudrate': LaunchConfiguration('baudrate'),
            'gripper_action_name': LaunchConfiguration('gripper_action_name'),
        }]
    )

    return LaunchDescription([serial_port_arg, baudrate_arg, action_name_arg, node])

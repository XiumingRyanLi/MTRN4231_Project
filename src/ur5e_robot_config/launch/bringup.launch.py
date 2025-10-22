from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    use_fake = LaunchConfiguration('use_fake_hardware')
    robot_ip  = LaunchConfiguration('robot_ip')
    ur_type   = LaunchConfiguration('ur_type')

    declare_use_fake = DeclareLaunchArgument('use_fake_hardware', default_value='true')
    declare_robot_ip = DeclareLaunchArgument('robot_ip', default_value='192.168.56.101')
    declare_ur_type  = DeclareLaunchArgument('ur_type',  default_value='ur5e')

    ur_driver_share = get_package_share_directory('ur_robot_driver')
    moveit_share    = get_package_share_directory('ur5e_moveit_config')  # created in Step 6
    this_share      = get_package_share_directory('ur5e_robot_moveit')

    real_driver = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(ur_driver_share, 'launch', 'ur_control.launch.py')),
        launch_arguments={
            'ur_type': ur_type,
            'robot_ip': robot_ip,
            'launch_rviz': 'false',
            'use_tool_communication': 'false',
        }.items(),
        condition=UnlessCondition(use_fake)
    )

    fake_control = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(this_share, 'launch', 'fake_control_and_rsp.launch.py')),
        condition=IfCondition(use_fake)
    )

    move_group = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(moveit_share, 'launch', 'move_group.launch.py')),
        launch_arguments={}.items()
    )

    return LaunchDescription([
        declare_use_fake, declare_robot_ip, declare_ur_type,
        real_driver, fake_control, move_group
    ])

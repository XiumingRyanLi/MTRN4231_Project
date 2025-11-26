import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import TimerAction, IncludeLaunchDescription
from launch.substitutions import PathJoinSubstitution
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.substitutions import FindPackageShare

from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

# Toggle between simulated or real UR5e hardware
use_fake = False
use_fake_str = 'false'
ur_type = 'ur5e'
ip_address = '127.0.0.1'

if use_fake:
    ip_address = '127.0.0.1'  # Use localhost for fake hardware
    use_fake_str = 'true'
else:
    print("not fake")
    ip_address = '192.168.0.100'
    use_fake_str = 'false'

def get_ur_control_launch():
    """Configure UR control launch for the UR5e arm."""
    end_effector_path = os.path.join(
        get_package_share_directory('end_effector_description'), 'urdf', 'end_effector_withDriverSupport.xacro'
    )

    ur_control_launch_args = {
        'ur_type': ur_type,
        'robot_ip': ip_address,
        'use_fake_hardware': use_fake_str,
        'launch_rviz': 'false',  
        'description_file': end_effector_path,  # Use full path, not separate package/file
    }

    # Add controller if using simulated hardware
    if use_fake:
        ur_control_launch_args['initial_joint_controller'] = 'joint_trajectory_controller'

    return IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([FindPackageShare('ur_robot_driver'), 'launch', 'ur_control.launch.py'])
        ),
        launch_arguments=ur_control_launch_args.items(),
    )

def get_moveit_launch():
    moveit_launch_args = {
        'ur_type': ur_type,
        'launch_rviz': 'false',  # Set back to true to launch RViz from MoveIt
        'use_fake_hardware': use_fake_str,
    }

    return TimerAction(
        period=4.0,
        actions=[
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    PathJoinSubstitution([FindPackageShare('ur5e_moveit_config_custom'), 'launch', 'move_group.launch.py'])
                ),
                launch_arguments=moveit_launch_args.items(),
            )
        ]
    )


def get_rviz_launch():
    moveit_launch_path = os.path.join(
        get_package_share_directory('ur5e_moveit_config_custom'), 'launch', 'moveit_rviz.launch.py'
    )

    return IncludeLaunchDescription(
        PythonLaunchDescriptionSource(moveit_launch_path)
    )



def get_auxiliary_launch():
    moveit_launch_path = os.path.join(
        get_package_share_directory('end_effector_description'), 'launch', 'auxiliary.launch.py'
    )

    return IncludeLaunchDescription(
        PythonLaunchDescriptionSource(moveit_launch_path)
    )


def generate_launch_description():
    """Main function to generate the complete launch description."""
    launch_description = [
        get_ur_control_launch(),
        # get_moveit_launch(),
        # get_auxiliary_launch(),
        get_rviz_launch()
    ]

    # Only add camera launch if using real hardware
    #if not use_fake:
        #launch_description.append(get_realsense_launch())
        #launch_description.append(get_auxiliary_launch())

    return LaunchDescription(launch_description)
# this script sets up a WSL environment to simulate a UR5e robot with fake hardware using ROS2.
# It does not work yet

#!/usr/bin/env bash

cmd.exe /c start "DriverServer" wsl.exe -d "Ubuntu 22.04.5 LTS" ^
bash -lc 'ros2 launch ur_robot_driver ur_control.launch.py \
    ur_type:=ur5e \
    robot_ip:=yyy.yyy.yyy.yyy \
    initial_joint_controller:=joint_trajectory_controller \
    use_fake_hardware:=true \
    launch_rviz:=false \
    description_package:=ur5e_custom_description \
    description_file:=ur5e_with_tool.urdf.xacro'
sleep 5

cmd.exe /c start "MoveitServer" wsl.exe -d "Ubuntu 22.04.5 LTS" ^
bash -lc 'ros2 launch ur_moveit_config_custom ur_moveit.launch.py \
    ur_type:=ur5e \
    launch_rviz:=true \
    use_fake_hardware:=true \
    description_package:=ur5e_custom_description \
    description_file:=ur5e_with_tool.urdf.xacro'

sleep 5

ros2 launch arm_controller arm_controller.launch.py execute:=true

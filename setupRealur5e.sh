#!/usr/bin/env bash
set -e


source /opt/ros/humble/setup.bash
source install/setup.bash

UR_TYPE=ur5e
DESC_PKG=ur5e_custom_description
DESC_FILE=ur5e_with_tool.urdf.xacro
ROBOT_IP=192.168.0.100    # <<< your real controller IP

# 0) Quick preflight (optional but helpful)
echo "[Preflight] Ensure UR pendant is in 'External Control' / 'Remote Control' and safety is released."
echo "[Preflight] PC and robot must be on same subnet. Consider NTP/time-sync to avoid TF jitter."

# 1) UR driver (real hardware)
gnome-terminal --title="UR Driver (real)" -- bash -lc "
  source /opt/ros/humble/setup.bash
  source install/setup.bash
  ros2 launch ur_robot_driver ur_control.launch.py \
    ur_type:=${UR_TYPE} \
    robot_ip:=${ROBOT_IP} \
    initial_joint_controller:=joint_trajectory_controller \
    use_fake_hardware:=false \
    launch_rviz:=false \
    description_package:=${DESC_PKG} \
    description_file:=${DESC_FILE}
"
sleep 10

# 2) MoveIt + RViz (plan/execute via driver)
gnome-terminal --title="MoveIt + RViz" -- bash -lc "
  source /opt/ros/humble/setup.bash
  source install/setup.bash
  ros2 launch ur_moveit_config ur_moveit.launch.py \
    ur_type:=${UR_TYPE} \
    use_fake_hardware:=false \
    launch_rviz:=true \
    description_package:=${DESC_PKG} \
    description_file:=${DESC_FILE}
"
sleep 8

# 3) Your controller (rename if different)
ros2 launch arm_controller arm_controller.launch.py execute:=true

#!/usr/bin/env bash
set -e

# Workspace root = folder this script lives in
WS_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$WS_ROOT"

echo "[run] Workspace: $WS_ROOT"

# --- config you can tweak ---
UR_TYPE=ur5e
ROBOT_IP=127.0.0.1    # ignored in fake mode

DESC_PKG=ur5e_moveit_config_custom
DESC_FILE=urdf/end_effector_withDriverSupport.xacro

MOVEIT_PKG=ur5e_moveit_config_custom
MOVEIT_SRDF_FILE=config/end_effector_withDriverSupport.srdf
# ----------------------------

# 1) UR driver (fake hardware, no RViz)
gnome-terminal -t "DriverServer" -e 'ros2 launch ur_robot_driver ur_control.launch.py \
    ur_type:=ur5e \
    robot_ip:=127.0.0.1 \
    initial_joint_controller:=joint_trajectory_controller \
    use_fake_hardware:=false \
    launch_rviz:=false'

sleep 5

# 2) MoveIt (move_group + RViz) with your custom URDF + SRDF
gnome-terminal --title="MoveitServer" -- bash -lc "
  set -e
  source /opt/ros/humble/setup.bash
  cd '$WS_ROOT'
  source install/setup.bash || true

  ros2 launch ${MOVEIT_PKG} ur_moveit.launch.py \
    ur_type:=${UR_TYPE} \
    description_package:=${DESC_PKG} \
    description_file:=${DESC_FILE} \
    moveit_config_package:=${MOVEIT_PKG} \
    moveit_config_file:=${MOVEIT_SRDF_FILE} \
    use_fake_hardware:=true \
    launch_rviz:=true

  status=\$?
  echo
  echo 'MoveitServer exited with code' \$status
  echo 'Press Enter to close...'
  read
"



# # 3) Your controller node (same shell so you see its logs)
# source /opt/ros/humble/setup.bash
# source install/setup.bash
# ros2 launch arm_controller arm_controller.launch.py

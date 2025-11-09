#!/usr/bin/env bash
set -e

# --- config you can tweak ---
UR_TYPE=ur5e
ROBOT_IP=127.0.0.1                 # ignored in fake mode
DESC_PKG=ur5e_custom_description
DESC_FILE=ur5e_with_tool.urdf.xacro
MOVEIT_PKG=ur5e_moveit_config_custom   # confirm this package name exists (ros2 pkg list | grep ur5e_moveit_config_custom)

# helper: open a new terminal with a sourced environment
term () {
  local title="$1"; shift
  gnome-terminal --title="$title" -- bash -lc "
    set -e
    source /opt/ros/humble/setup.bash
    source ~/Desktop/MTRN4231_Project/install/setup.bash || true
    $*
    status=\$?
    echo
    echo '=== EXIT CODE:' \$status '==='. 
    echo 'Press Enter to close...'; read _
  "
}

# 1) UR driver (fake hardware with SCALED controller)
term "DriverServer" "
  ros2 launch ur_robot_driver ur_control.launch.py \
    ur_type:=${UR_TYPE} \
    robot_ip:=${ROBOT_IP} \
    use_fake_hardware:=true \
    initial_joint_controller:=scaled_joint_trajectory_controller \
    launch_rviz:=false \
    description_package:=${DESC_PKG} \
    description_file:=${DESC_FILE}
"

sleep 5

# 2) MoveIt (make sure your custom launch accepts these args)
term "MoveItServer" "
  ros2 launch ${MOVEIT_PKG} ur_moveit.launch.py \
    ur_type:=${UR_TYPE} \
    use_fake_hardware:=true \
    launch_rviz:=true \
    description_package:=${DESC_PKG} \
    description_file:=${DESC_FILE}
"

sleep 5

# 3) Your controller node (same shell so you see its logs)
source /opt/ros/humble/setup.bash
source ~/Desktop/MTRN4231_Project/install/setup.bash || true
ros2 launch arm_controller arm_controller.launch.py

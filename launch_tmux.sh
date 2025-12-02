#!/usr/bin/env bash
set -e

SESSION="chessbot"

# --- ROS env ---
ROS_SETUP="source /opt/ros/humble/setup.bash && source ~/MTRN4231_Project/install/setup.bash"

# If session already exists, kill it so we start clean
tmux has-session -t "$SESSION" 2>/dev/null && tmux kill-session -t "$SESSION"

# =========================
# Window 0: RealSense Camera
# =========================
tmux new-session -d -s "$SESSION" -n realsense \
  "bash -lc '$ROS_SETUP; ros2 launch realsense2_camera rs_launch.py align_depth.enable:=true enable_color:=true enable_depth:=true rgb_camera.color_profile:=1920x1080x30 pointcloud.enable:=true; exec bash'"

sleep 5

# =========================
# Window 1: Brain + Master + UI
# =========================
tmux new-window -t "$SESSION" -n brain \
  "bash -lc '$ROS_SETUP; ros2 run brain task_coordinator; exec bash'"

tmux split-window -h -t "$SESSION:brain" \
  "bash -lc '$ROS_SETUP; ros2 run chess_master master; exec bash'"

tmux split-window -v -t "$SESSION:brain.1" \
  "bash -lc '$ROS_SETUP; ros2 run ui user_interface; exec bash'"

tmux select-layout -t "$SESSION:brain" tiled

# =========================
# Window 2: Perception Nodes
# =========================
tmux new-window -t "$SESSION" -n perception \
  "bash -lc '$ROS_SETUP; ros2 run perception chess_detector; exec bash'"

tmux split-window -h -t "$SESSION:perception" \
  "bash -lc '$ROS_SETUP; ros2 run perception state_comparison; exec bash'"

tmux split-window -v -t "$SESSION:perception.0" \
  "bash -lc '$ROS_SETUP; ros2 run perception board_locator; exec bash'"

tmux split-window -v -t "$SESSION:perception.1" \
  "bash -lc '$ROS_SETUP; ros2 run perception board_transformer; exec bash'"

tmux select-layout -t "$SESSION:perception" tiled

# =========================
# Window 3: DriverServer + TF
# =========================
tmux new-window -t "$SESSION" -n driver \
  "bash -lc '$ROS_SETUP; ros2 launch end_effector_description display.launch.py; exec bash'"

tmux split-window -v -t "$SESSION:driver" \
  "bash -lc '$ROS_SETUP; ros2 run tf2_ros static_transform_publisher 0.655 0.25 0.934 0.5 -0.5 -0.5 -0.5 base camera_link; exec bash'"

sleep 5

# =========================
# Window 4: MoveitServer (commented out)
# =========================
# tmux new-window -t "$SESSION" -n moveit \
#   "bash -lc '$ROS_SETUP; ros2 launch ur_moveit_config ur_moveit.launch.py robot_ip:=192.168.0.100 ur_type:=ur5e launch_rviz:=true; exec bash'"

# =========================
# Window 5: Arm Controller + Gripper
# =========================
tmux new-window -t "$SESSION" -n arm_ctrl \
  "bash -lc '$ROS_SETUP; ros2 launch arm_controller arm_controller.launch.py execute:=true; exec bash'"

tmux split-window -v -t "$SESSION:arm_ctrl" \
  "bash -lc '$ROS_SETUP; ros2 run gripper gripper_bridge --ros-args -p port:=/dev/ttyUSB0; exec bash'"

# Attach to session
tmux attach -t "$SESSION"

# TO KILL THE SESSION DO: tmux kill-session -t chessbot
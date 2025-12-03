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
  "bash -lc '$ROS_SETUP; ros2 launch realsense2_camera rs_launch.py enable_color:=true rgb_camera.color_profile:=1920x1080x30; exec bash'"
sleep 5
# =========================
# Window 1: Perception + UI + Brain + Master
# Make task_coordinator the first pane so its logs are always visible.
# =========================
tmux new-window -t "$SESSION" -n core \
  "bash -lc '$ROS_SETUP; ros2 run brain task_coordinator; exec bash'"

tmux split-window -v  -t "$SESSION:core.0" \
  "bash -lc '$ROS_SETUP; ros2 run ui user_interface; exec bash'"

tmux split-window -v  -t "$SESSION:core.1" \
  "bash -lc '$ROS_SETUP; ros2 run chess_master master; exec bash'"

tmux select-layout -t "$SESSION:core" tiled

#perception

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
# Window 2: DriverServer
# =========================
tmux new-window -t "$SESSION" -n driver \
  "bash -lc '$ROS_SETUP; ros2 launch end_effector_description display.launch.py; exec bash'"

# small delay matching your script
sleep 5

# =========================
# Window 3: MoveitServer
# =========================
# tmux new-window -t "$SESSION" -n moveit \
#   "bash -lc '$ROS_SETUP; ros2 launch ur_moveit_config ur_moveit.launch.py robot_ip:=192.168.0.100 ur_type:=ur5e launch_rviz:=true; exec bash'"

# =========================
# Window 4: Arm Controller
# =========================
tmux new-window -t "$SESSION" -n arm_ctrl \
  "bash -lc '$ROS_SETUP; ros2 launch arm_controller arm_controller.launch.py execute:=true; exec bash'"

# =========================
# Window 5: Gripper
# =========================
tmux new-window -t "$SESSION" -n gripper \
  "bash -lc '$ROS_SETUP; ros2 run gripper gripper_bridge --ros-args -p port:=/dev/ttyUSB0; exec bash'"

# Attach to session
tmux attach -t "$SESSION"

# TO KILL THE SESSION DO: tmux kill-session -t chessbot

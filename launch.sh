
source /opt/ros/humble/setup.bash
source ~/MTRN4231_Project/install/setup.bash

gnome-terminal --title="Chess Detector" -- bash -c "ros2 run perception chess_detector; exec bash" &
gnome-terminal --title="State Comparison" -- bash -c "ros2 run perception state_comparison; exec bash" &
gnome-terminal --title="User Interface" -- bash -c "ros2 run ui user_interface; exec bash" &
gnome-terminal --title="Task Coordinator" -- bash -c "ros2 run brain task_coordinator; exec bash" &
gnome-terminal --title="Chess Master" -- bash -c "ros2 run chess_master master; exec bash" &

wait
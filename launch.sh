
source /opt/ros/humble/setup.bash
source ~/MTRN4231_Project/install/setup.bash

gnome-terminal -- bash -c "ros2 run perception chess_detector; exec bash" &
gnome-terminal -- bash -c "ros2 run perception state_comparison; exec bash" &
gnome-terminal -- bash -c "ros2 run ui user_interface; exec bash" &
gnome-terminal -- bash -c "ros2 run brain task_coordinator; exec bash" &
gnome-terminal -- bash -c "ros2 run chess_master master; exec bash" &

wait
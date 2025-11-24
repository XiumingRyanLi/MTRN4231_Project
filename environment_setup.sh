#!/usr/bin/env bash

set -e
set -u

echo "=== Setting up environment ==="

# ---- 1. Install APT dependencies ----
echo "[APT] Updating package index..."
sudo apt update

echo "[APT] Installing ROS MoveIt dependencies..."
sudo apt install -y \
    ros-humble-moveit \
    ros-humble-moveit-ros-planning-interface \
    ros-humble-moveit-visual-tools \
    ros-humble-rviz-visual-tools \
    ros-humble-ur-robot-driver \
    ros-humble-ur-moveit-config \
    wmctrl \
    rviz \


echo "[APT] Installing system pip if missing..."
sudo apt install -y python3-pip

# ---- 2. Install Python packages ----
echo "[PIP] Installing Python dependencies..."
python3 -m pip install --upgrade pip
python3 -m pip install chess cairosvg pyserial

# ---- 3. Make stockfish executable ----
STOCKFISH_PATH="./stockfish/stockfish"
if [ -f "$STOCKFISH_PATH" ]; then
    echo "[CHMOD] Making stockfish executable..."
    chmod +x "$STOCKFISH_PATH"
else
    echo "[WARN] stockfish not found at $STOCKFISH_PATH"
fi

echo "=== Setup complete ==="

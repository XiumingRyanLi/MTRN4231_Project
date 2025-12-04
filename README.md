1. Table of Contents:

2. Project Overview:
   -video

---

# 3. System Architecture:

This section outlines the architecture of our system. It also includes behaviour tree, a description for each node in the system and explanations on custom message type interfaces.   

---

## 3.1 package level architecture diagram
   - behaviour tree showing closed loop
   - description of each node
   - custom message interface explanations

---

# 4. Technical Components:
   - Computer Vision:
   - Custom End-Effector:
   - System Visualisation:

### Closed-Loop Operation:

(will update)

First, the camera is constantly detecting the board’s location. So even if the board is shifted slightly, the system automatically recalibrates and updates the coordinates of all pieces.

Next, the system detects every chess pieces and tracks their changes between moves. This allows it to confirm whether a move has occurred—both from the user or from the robot itself. 

Finally, the chess game state is always kept up to date. Every detected move is applied to the internal game model, which allows the robot to accurately calculate its next response based on the current state of the game.

Together, these three elements form the closed-loop: the robot acts, perception measures the real board, and the system adjusts to the game state in real time.

---

# 5. Installation and Setup

This section explains how to install dependencies, build the workspace, configure the hardware, and prepare the system for running a full chess-playing session with the UR5e robot.

---

## 5.1 Software Prerequisites

The system has been tested on the following stack:

### **Operating System**
- Ubuntu 22.04 LTS  
- Real-time kernel NOT required

### **Robotics Framework**
- ROS 2 Humble Hawksbill  
- MoveIt 2 (installed through apt)

### **Development Tools**
```bash
sudo apt install python3-pip python3-colcon-common-extensions \
  build-essential cmake git python3-opencv
```

### **Python Dependencies**
```bash
pip install numpy opencv-python Pillow pyyaml scipy
```

### **Chess Engine**
- Stockfish (included in `stockfish/` folder)
- No external installation needed

### **Computer Vision**
- Open CV
- Realsense Camera3 Module
  
### **Microcontroller**
- Arduino IDE OR arduino-cli for uploading the end-effector firmware

---

## 5.2 Cloning and Building the Workspace

```bash
# Create workspace
mkdir -p ~/mtrn4231_ws/src
cd ~/mtrn4231_ws/src

# Clone project
git clone <repo-url> chess_robot

# Build
cd ~/mtrn4231_ws
colcon build --symlink-install

# Source the environment
source install/setup.bash
```

Alternatively, the project includes a helper script:

```bash
cd chess_robot
./environment_setup.sh
```

This script:
- Installs required Python dependencies  
- Builds the ROS workspace  
- Sets up Stockfish paths  
- Automatically sources your ROS environment  

---

## 5.3 Hardware Setup

### **UR5e Robot**
- Ensure the UR5e pendant is powered up and ready for movement.
- Connect the UR5e control box to the ROS PC via Ethernet.
- Assign static IPs in the same subnet, check by ping 192.168.0.77.
- Set the system state to Automatic and load the ros.urp file onto the UR5e pendant.
- Set robot → ROS control target IP to the ROS machine.

### **Overhead Camera**
- Set up a beam structure using square beams to create an overhang structure.
- Have a camera mounted to the camera mount by tighening through a M3 bolt.
- Connect the USBC connection to the camera
- Slide the mount onto the beam, it is held securly with friction fit.
![Overhead camera](images/camera.jpg)
- Check camera enumeration:
```bash
ls /dev/video*
```
If it shows up the camera then it is good.

### **End-Effector / Gripper**
- Ensure all the links for the gripper are 3d printed
- Fully assemble the gripper shown as:


![End effector attached](images/End_effector_attached.png)
  
- Mount custom-designed gripper using UR5e flange adapter.
- Upload firmware:
```bash
arduino-cli upload -p /dev/ttyACM0 ArduinoCode.ino
```
- Test motion via serial:
  - `open` → fully open  
  - `close` → close enough to grip standard chess pieces  

### **Electrical**
- Ensure solid grounding between Arduino, UR5e controller, and sensing modules.
- USB isolation is recommended for noise immunity.

![Arduino setup](images/Arduino_setup.jpg)


---

## 5.4 System Calibration

The following calibrations **must** be performed for accurate gameplay.

### **1. Hand–Eye Calibration (Camera → Robot Base TF)**
Defines transform:
```
camera_frame → chessboard_frame → robot_base_frame
```
Store final values in the TF broadcaster.

![Program running on pendant](images/transformed_board.jpg)

### **2. Square Mapping**
`chess_square.py` defines coordinates of all 64 squares.

If board is moved or scaled, update values:
```python
square_coords["e4"] = [x, y, z]
```

### **3. Z-Height Calibration**
Use robot to probe:
- Top of board surface  
- Top of tallest piece  

These define approach heights and safe drop heights.

---
![Grooved chess piece](images/chess_piece.jpg)

# 6. Running the System

This section describes how to launch, test, and interact with the full chess-robot pipeline.

---

## 6.1 Full-System Launch

From project root:

```bash
./tmux_launch.sh
```

This launches:
- UR5e driver  
- MoveIt planner, UR Driver controller and RViz
- Perception stack
- Brain node to coordinate tasks
- Chess master node that runs Stockfish  
- GUI  

To use a multi-window tmux interface:

```bash
./launch_tmux.sh
```

Open the teach pendent and load in the program
![Load ROS2 program on pendant](images/Load_ros2_program_on_pandent.jpg)
---

## 6.2 Component-Level Launch (For Debugging)

### **Terminal 1 — MoveIt + UR5e Control**
```bash
ros2 launch <moveit_package> moveit_rviz.launch.py
```

### **Terminal 2 — Vision**
```bash
ros2 run preception chess_detector
```

### **Terminal 3 — Game Coordinator**
```bash
ros2 run task_coordinator coordinator.py
```

### **Terminal 4 — GUI**
```bash
python3 gui_test.py
```

---

## 6.3 What Should Happen During Execution

- RViz displays live UR5e joint states.
- Vision node detects board grid and pieces.
- GUI shows:
  - Board state  
  - Current turn  
   

### **When a move is executed:**
1. The system verifies legality.
2. The planner generates collision-free pick trajectory.
3. The gripper picks piece from source square.
4. The robot moves to destination.
5. Vision system double-checks placement.
6. Game state updates.

---

## 6.4 Troubleshooting Guide

### **Robot not moving**
- check in Rviz that the robot is simulated, the current position of the robot in real life is accuracte in the simulation
![Program running on pendant](images/running_pendent.jpg)
-    If not the same then check UR5e pandant is in automatic mode.
-    IP mismatch between URCap → ROS driver. Run
```bash
ping 192.168.0.77
```
- If the robot does show up accuractely in RVIZ, check the terminal, if it shows that MoveIt is failing to find a collision-free path, look at which step did it fail at and debug arm_controller_node.cpp.



### **Camera not publishing**
```bash
ros2 topic list | grep image
```
If no result appears:
- Missing drivers --> install realsense camera driver
- 

### **Squares misaligned**
- Open Rviz and add a image topic
- Inside the image topic select image/cropped
- Adjust the board on the table such that it is inside the frame

### **Gripper fails to pick pieces**
- Recalibrate open/close PWM values in `ArduinoCode.ino`. The value are set in by the task coordinator, verfiy 
- Ensure robot approach height is not too low/too high.

---

# 7. Results and Demonstration:

# 8. Discussion and Future Improvements

Throughout development, several engineering challenges emerged across perception, motion planning, end-effector performance, and overall system integration. These areas represent strong opportunities for refinement in a future release of the chess robot platform.

---

## **Perception**

The current perception pipeline uses HSV thresholding, contour extraction, and difference-based state comparison. While effective under controlled conditions, it was highly sensitive to environmental factors:

- Lighting fluctuations caused inconsistent segmentation.  
- Robot shadows occasionally triggered false detections.  
- A white boundary around the chessboard was required for stable detection.  

### **Future Improvements**

#### **1. Deep-learning-based detection (YOLOv8/YOLOv10)**  
A neural-network detector would be far more resilient to lighting variations and would eliminate the need for artificial borders around the board.

**How to implement:**
1. Collect labelled datasets of piece locations under varied lighting.  
2. Train a YOLO model to detect:
   - 64 square positions  
   - Piece classes (pawn, rook, knight, bishop, queen, king)  
   - Empty squares  
3. Integrate with ROS2 using a custom node or `ros_yolo` packages.  
4. Replace HSV segmentation with bounding-box centroid detection.

#### **2. Depth-sensing integration (Intel RealSense / ZED2i)**  
Depth data helps differentiate between squares, detect piece height, and resolve occlusions.

**How to implement:**
- Fuse RGB + depth into a unified RGB-D perception node.  
- Identify piece height using point cloud clustering.  
- Project depth centroids into the chessboard coordinate frame.

#### **3. Arm-mounted camera for mobile scanning**  
Mounting the camera on the UR5e wrist allows the robot to reposition for more complexed operations.

**Long-term capability:**
- Scan multiple chessboards on different tables using a single camera.  
- Automatically adjust vantage point to reduce occlusions.  

**How to implement:**
1. Add a `camera_link` in the robot URDF + TF tree.  
2. Perform hand–eye calibration.  
3. Create scanning trajectories (raster pattern or targeted waypoints).  
4. Capture images and stitch results into a board state model.

---

## **Motion Planning**

Although MoveIt handled most tasks well, several limitations were identified:

- Tall pieces increased collision risk during lateral motions.  
- Knight/queen trajectories required more sophisticated approach angles.  
- Small orientation drift could nudge adjacent pieces unintentionally.

### **Future Improvements**

#### **1. Pilz Industrial Motion Planner**  
Pilz provides deterministic LIN/PTP/CIRC motions ideal for tabletop interactions.

**How to implement:**
1. Enable Pilz by updating `planning_pipelines` in MoveIt config.  
2. Use LIN motions for approach, grasp, retreat:  
   - LIN (base → approach)  
   - LIN (approach → grasp)  
   - LIN (grasp → retreat)  
3. Retain PTP only for long-distance moves above the board.

#### **2. Dynamic collision objects from perception**  
Using live perception to update MoveIt’s planning scene reduces accidental bumps.

**How to implement:**
1. Publish each identified piece as a MoveIt collision object.  
2. Update at 5–10 Hz via the PlanningSceneInterface.  
3. Ensure planned paths avoid dynamically placed obstacles.

---

## **End-Effector Performance**

The current servo-driven finger gripper works reliably but is highly sensitive to alignment and tolerances:

- Minor calibration drift affects grasp consistency.  
- Servo backlash introduces small error in finger positioning, pushing the chess piece out in the release movement.  
- Some pieces are easier to pick than others depending on geometry.
- Current chess piece consists of a small groove that allows for easy picking
![Grooved chess piece](images/chess_piece.jpg)

### **Future Improvements**

#### **1. Suction-based gripper**
Ideal for flat-top pieces and independent of rotational alignment.

#### **2. Hybrid magnetic + mechanical design**
Useful for metal-core or retrofitted pieces.

#### **3. Improved servo calibration**
- Add startup homing via limit switches or stall sensing.  
- Smooth PWM transitions to prevent jerky motion.  
- Install a force sensor that measure the pick up exerted by the gripper for secure pick up.
- The gripper flanges doesn't contract and release at the same time due to friction, so the chess pieces will be moved slightly during the placing motion

---

## **System Integration**

The system relies heavily on accurate TF transforms between:

- `base_link`  
- `tool0`  
- `gripper_link`  
- `camera_frame`  
- `chessboard_frame`  

Small deviations in calibration significantly impacted manipulation accuracy.

### **Issues Observed**
- TF drift caused misaligned picks.  
- Manual calibration is required for each board offseting the white boarder to the corner position A1, A8, H1, H8 consumed time.  
- Camera mounting inconsistencies changed board position estimates.  

### **Future Improvements**
####  Diagnostics and health monitoring
- Add ROS2 Diagnostics messages for vision, gripper, TF, motion state.
- Add in Yolo to automatically adjust the 4 corner poses.
- Display health indicators on the UI.  
- Add a console panel in RViz for real-time alerts.

#### Multi-board and multi-table automation
Paired with an arm-mounted camera, the UR5e could act as a multi-station chess referee.

**How to implement:**
1. Define multiple table frames in the environment.  
2. Implement autonomous navigation between tables (via predefined joint targets).  
3. At each table, trigger a scanning routine.  
4. Create a scheduler to manage multiple concurrent games.

---

Overall, these improvements map a clear pathway toward a more robust, scalable, and fully autonomous chess-playing robotic system that can operate across variable environments and multiple concurrent games.

---

# 9. Contributors

| Member | Contribution |
|--------|--------------|
| **Ryan Li** | MoveIt integration, URDF/xacro modeling, TF integration, gripper implementation|
| **Johnnie Parris** | Vision pipeline, depth transforms, TF integration |
| **Justin Kwok** | Game engine integration, task coordination, GUI, gripper implementation|

Additional support was received in lab sessions from course staff.

---

# 10. Repository Structure

```
.
├── src/                         # ROS 2 packages (moveit config, drivers, vision, chess controller)
├── stockfish/                   # Stockfish chess engine binary & weights
├── ArduinoCode.ino              # Gripper firmware (servo control + motion presets)
├── board.png                    # Calibration board image
├── chess_square.py              # Coordinates of 64 physical board squares
├── environment_setup.sh         # Setup script (deps + build + env)
├── gui_test.py                  # Standalone GUI for board visualisation
├── kill_all.sh                  # Terminates all ROS + python nodes
├── launch.sh                    # One-command full system launcher
├── launch_tmux.sh               # Multi-window launcher for debugging
├── master.py                    # High-level game logic + motion sequencing
└── robot arm movement steps.txt # Internal motion notes for trajectory design
```

---

# 10. Repository Structure

The repository follows a modular ROS 2 workspace design. Each major subsystem
(arm control, perception, UI, game logic, custom interfaces, etc.) is isolated
into its own package for clarity, maintainability, and debugging.

Below is a detailed breakdown of each directory, its purpose, and any special notes
about its origin or usage.

```
src/
├── arm_controller/
│   ├── src/arm_controller_node.cpp        # Main robot TCP motion + MoveIt client
│   ├── launch/arm_controller.launch.py    # Launch file for arm control node
│   └── CMakeLists.txt / package.xml
│
├── brain/
│   # Placeholder for higher-level decision modules (not used heavily this term)
│
├── chess_master/
│   ├── chess_master/move_service.py       # Service node handling verified chess moves
│   ├── chess_master/__init__.py
│   └── CMakeLists.txt / package.xml
│
├── custom_interfaces/
│   ├── action/
│   │   ├── GripperCommand.action          # Custom action for opening/closing gripper
│   │   └── MoveTCP.action                 # Cartesian motion action for UR5e TCP
│   └── srv/
│       └── ChessMove.srv                  # Service for making a validated chess move
│
├── end_effector_description/
│   ├── urdf/                              # URDF/XACRO files for the custom gripper
│   ├── meshes/                            # STL/DAE meshes of the gripper
│   ├── config/                            # RViz + joint configuration
│   ├── rviz/
│   └── launch/
│       ├── display.launch.py              # Visualize end-effector only (testing)
│       └── display_ee.launch.py           # Joint state publisher + gripper visualization
│
├── gripper/
│   ├── gripper/gripper_bridge_node.py     # ROS <-> Arduino serial bridge
│   ├── gripper/gripper_server.py          # Action server for gripper open/close
│   ├── gripper/gripper_client.py          # Client used by arm_controller
│   └── launch/gripper_bringup.launch.py   # Brings up gripper control stack
│
├── perception/
│   ├── perception/aruco_detect.py         # ArUco board detection (optional)
│   ├── perception/chess_detector.py       # Main HSV + contour-based chessboard detector
│   ├── perception/image_publisher.py      # USB camera publisher
│   ├── perception/state_comparison.py     # Detects piece movement between frames
│   ├── resource/
│   ├── test-images/                       # Ground truth test images
│   └── test/                              # Automated testing utilities
│
├── ui/
│   ├── ui/board_state_sub.py              # Subscribes to board_state topic
│   ├── ui/user_interface.py               # Tkinter interface for game monitoring
│   ├── resource/
│   └── test/
│
├── ur5e_custom_description/               # NOT USED — kept for archival only
│   # (Old experiment — deprecated. Replaced completely by end_effector_description.)
│
├── ur5e_moveit_config_custom/
│   # This is the **actual MoveIt config used** by the robot.
│   #   Generated using MoveIt Setup Assistant and fully customised
│   #   to integrate the custom end-effector.
│   ├── config/
│   │   ├── end_effector_withDriverSupport.srdf  # SRDF defining planning groups
│   │   ├── initial_positions.yaml               # Used for RViz display startup
│   │   ├── joint_limits.yaml                    # URDF+MoveIt joint limits
│   │   ├── kinematics.yaml                      # IKFast/KDL solver config
│   │   ├── moveit_controllers.yaml              # MoveIt2 control mappings
│   │   ├── pilz_cartesian_limits.yaml           # Constraints for Pilz planner
│   │   └── moveit.rviz
│   ├── launch/
│   └── CMakeLists.txt / package.xml
│
├── ur_moveit_config_official/
│   #  Downloaded from **Universal Robots official MoveIt2 repository**.
│   #   Used as a clean, correct reference model for:
│   #     • MoveIt Setup Assistant input  
│   #     • URDF baseline (without our gripper)  
│   #     • Re-exporting custom configs
│   #   NOT used at runtime.
│   └── (Official UR-provided files)
│
└── ur5e_custom_description/                # Duplicate note: remains unused
```

---

##  Important Notes About UR Packages

### ** `ur_moveit_config_official/`**
- Pulled directly from the official Universal Robots MoveIt2 repository.
- Used **only for MoveIt Setup Assistant workflows**:
  - exporting correct SRDF groups  
  - inheriting correct joint limits  
  - ensuring compatibility with UR5e URDF  
- **Never launched during runtime** — serves as a clean reference.

### ** `ur5e_moveit_config_custom/`**
- **The MoveIt package actually used in the project.**
- Integrates:
  - Custom end-effector  
  - Custom joint limits & planning groups  
  - Corrected SRDF  
  - Collision meshes for the gripper  
- Generated using MoveIt Setup Assistant, starting from the official UR package above.

### ** `ur5e_custom_description/`**
- An early prototype.
- No longer used in MoveIt or any launch files.
- Kept only for documentation and archival reasons.

---

## Summary of Package Responsibilities

| Package | Purpose |
|--------|---------|
| `arm_controller` | Executes TCP motions, MoveIt control, action clients |
| `brain` | High-level logic (not majorly used this term) |
| `chess_master` | Validated chess move service + game coordination |
| `custom_interfaces` | Action & service definitions (`MoveTCP`, `GripperCommand`, `ChessMove`) |
| `end_effector_description` | URDF, meshes, and visualization for custom gripper |
| `gripper` | ROS ↔ Arduino interface, gripper action server |
| `perception` | HSV board detection, ArUco detection, move comparison |
| `ui` | Tkinter front-end for monitoring board & robot state |
| `ur_moveit_config_official` | Official UR reference package — used only for Setup Assistant |
| `ur5e_moveit_config_custom` | Actual MoveIt config used during operation |
| `ur5e_custom_description` | Old unused package retained for reference |



# 11. References & Acknowledgements

### **Frameworks and Libraries**
- ROS 2 Humble  
- MoveIt 2 Planning Framework  
- UR5e ROS 2 Driver  
- OpenCV for vision  
- Stockfish chess engine  

### **Academic Resources**
- MTRN4231 Robotics Course Notes  
- UR5e technical documentation  
- ROS 2 TF2 tutorials on camera calibration  

### **Special Thanks**
- MTRN4231 teaching team for ongoing support  
- Lab demonstrators David Nie and Alex Cronin for guidance and assistance  
- Fellow student teams for collaboration and shared testing time Nail Bot and Jenga Bot

---

    




cmake_minimum_required(VERSION 3.5)
project(move_to_marker)

# Use C++17
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
endif()

# Dependencies (headers + linking)
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(shape_msgs REQUIRED)
find_package(moveit_ros_planning_interface REQUIRED)   # MoveGroupInterface & PlanningSceneInterface
find_package(moveit_msgs REQUIRED)

add_executable(move_to_pose src/move_to_pose.cpp)
ament_target_dependencies(move_to_pose
  rclcpp
  geometry_msgs
  shape_msgs
  moveit_ros_planning_interface
  moveit_msgs
)

# Install binaries
install(TARGETS move_to_pose
  DESTINATION lib/${PROJECT_NAME}
)
install(DIRECTORY launch DESTINATION share/${PROJECT_NAME})


ament_package()

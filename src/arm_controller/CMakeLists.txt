cmake_minimum_required(VERSION 3.8)
project(arm_controller)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclcpp_action REQUIRED)
find_package(tf2_ros REQUIRED)
find_package(tf2_geometry_msgs REQUIRED)
find_package(moveit_ros_planning_interface REQUIRED)
find_package(custom_interfaces REQUIRED)
find_package(moveit_visual_tools REQUIRED)
find_package(geometry_msgs REQUIRED)


add_executable(arm_controller_node src/arm_controller_node.cpp)
ament_target_dependencies(arm_controller_node
  rclcpp rclcpp_action tf2_ros tf2_geometry_msgs moveit_visual_tools
  moveit_ros_planning_interface custom_interfaces)

add_executable(moveit_constrain_ur src/moveit_constrain_ur.cpp)
target_include_directories(moveit_constrain_ur PUBLIC  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include> $<INSTALL_INTERFACE:include>)
target_compile_features(moveit_constrain_ur PUBLIC c_std_99 cxx_std_17)  # Require C99 and C++17
ament_target_dependencies(
  moveit_constrain_ur
  "moveit_ros_planning_interface"
  "rclcpp"
  "moveit_visual_tools"
)

install(TARGETS arm_controller_node DESTINATION lib/${PROJECT_NAME})
install(DIRECTORY launch urdf srdf config rviz
  DESTINATION share/${PROJECT_NAME})



ament_package()

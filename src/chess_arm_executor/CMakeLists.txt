cmake_minimum_required(VERSION 3.8)
project(chess_arm_executor)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclcpp_action REQUIRED)
find_package(moveit_ros_planning_interface REQUIRED)
find_package(moveit_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(shape_msgs REQUIRED)
find_package(std_srvs REQUIRED)
find_package(tf2_ros REQUIRED)
find_package(tf2_geometry_msgs REQUIRED)
find_package(rosidl_default_generators REQUIRED)

# Generate the action
rosidl_generate_interfaces(${PROJECT_NAME}
  "action/ExecuteMove.action"
  DEPENDENCIES builtin_interfaces
)

# Node target
add_executable(arm_controller_node src/arm_controller_node.cpp)

# Make sure the compiler can find generated headers
target_include_directories(arm_controller_node PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}/rosidl_generator_cpp>
  $<INSTALL_INTERFACE:include>)

# Link deps
ament_target_dependencies(arm_controller_node
  rclcpp rclcpp_action moveit_ros_planning_interface moveit_msgs
  geometry_msgs shape_msgs std_srvs tf2_ros tf2_geometry_msgs rcl_interfaces)

# Ensure interfaces build before the node
add_dependencies(arm_controller_node ${PROJECT_NAME}__rosidl_typesupport_cpp)

# (Optional but robust) link typesupport target
rosidl_get_typesupport_target(cpp_typesupport_target ${PROJECT_NAME} "rosidl_typesupport_cpp")
target_link_libraries(arm_controller_node ${cpp_typesupport_target})

install(TARGETS arm_controller_node DESTINATION lib/${PROJECT_NAME})
install(DIRECTORY launch config action DESTINATION share/${PROJECT_NAME})
install(DIRECTORY launch DESTINATION share/${PROJECT_NAME})
install(DIRECTORY config DESTINATION share/${PROJECT_NAME})

ament_export_dependencies(rosidl_default_runtime)
ament_package()

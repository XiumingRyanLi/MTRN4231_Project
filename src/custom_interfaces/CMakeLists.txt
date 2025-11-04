cmake_minimum_required(VERSION 3.8)
project(custom_interfaces)

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(builtin_interfaces REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "action/MoveTCP.action"
  "action/GripperCommand.action"
  DEPENDENCIES geometry_msgs builtin_interfaces
)

# Ensure the actions are installed (so ament index sees the pkg)
install(DIRECTORY action
  DESTINATION share/${PROJECT_NAME}
)

ament_export_dependencies(rosidl_default_runtime)

ament_package()

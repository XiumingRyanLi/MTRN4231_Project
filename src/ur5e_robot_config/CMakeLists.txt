cmake_minimum_required(VERSION 3.8)
project(ur5e_robot_config)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)

# Install description, launch, config, rviz
install(DIRECTORY urdf config launch rviz
  DESTINATION share/${PROJECT_NAME}
)

ament_package()

cmake_minimum_required(VERSION 3.8)
project(detection_msgs)

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

# Dependencies
find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)

# Message files
set(msg_files
  "msg/BoundingBox2D.msg"
  "msg/Detection2D.msg"
  "msg/Detection2DArray.msg"
  "msg/TargetPosition.msg"
)

# Interface generation
rosidl_generate_interfaces(${PROJECT_NAME}
  ${msg_files}
  DEPENDENCIES std_msgs geometry_msgs
)

ament_export_dependencies(rosidl_default_runtime)
ament_package()

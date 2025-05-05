cmake_minimum_required(VERSION 3.8)
project(fusion_node)

# Default to C++14 (though Python node is used, this is required)
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

# Dependencies
find_package(ament_cmake REQUIRED)
find_package(rclpy REQUIRED)
find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(detection_msgs REQUIRED)

# Install Python node
install(
  PROGRAMS
    test_detection_publisher.py
    fusion_node.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()

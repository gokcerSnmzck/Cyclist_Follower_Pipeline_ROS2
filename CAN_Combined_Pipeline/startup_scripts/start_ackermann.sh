#!/bin/bash
source ~/my_nodes_project/install/setup.bash
ros2 launch cmdvel_to_ackermann cmdvel_to_ackermann.launch.py acceleration:=0.5 steering_velocity:=0.5

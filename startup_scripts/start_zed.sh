#!/bin/bash
source ~/my_nodes_project/install/setup.bash
ros2 launch zed_wrapper zed_camera.launch.py camera_model:=zed2i sim_mode:=true
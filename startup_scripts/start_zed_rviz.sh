#!/bin/bash
source ~/devel/my_nodes_project/install/setup.bash
ros2 launch zed_display_rviz2 display_zed_cam.launch.py camera_model:=zed2i sim_mode:=true

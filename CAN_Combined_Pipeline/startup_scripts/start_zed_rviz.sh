#!/bin/bash
source ~/CAN_Combined_Pipeline/install/setup.bash
ros2 launch zed_display_rviz2 display_zed_cam.launch.py camera_model:=zed2i sim_mode:=false

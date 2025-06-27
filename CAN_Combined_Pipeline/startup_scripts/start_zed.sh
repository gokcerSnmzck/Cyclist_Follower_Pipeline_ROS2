#!/bin/bash
source ~/CAN_Combined_Pipeline/install/setup.bash
ros2 launch zed_wrapper zed_camera.launch.py camera_model:=zed2i sim_mode:=false

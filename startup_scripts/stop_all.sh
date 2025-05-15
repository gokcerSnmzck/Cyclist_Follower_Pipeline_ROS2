#!/bin/bash
pkill -f zed_camera.launch.py
pkill -f hybrid_reid_ros_node
pkill -f deepstream_ros_node_json
pkill -f fusion_node.py
pkill -f person_follower
pkill -f cmdvel_to_ackermann.launch.py

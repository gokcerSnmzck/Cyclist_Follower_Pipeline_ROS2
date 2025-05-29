#!/bin/bash

# Start ZED
./start_zed.sh &

# Wait for ZED to initialize
sleep 3

# Choose detection strategy
USE_HYBRID=false

if [ "$USE_HYBRID" = true ]; then
    ./start_hybrid_reid.sh &
else
    ./start_deepstream.sh &
fi

sleep 1

USE_GESTURE_DETECTOR=false
if [ "$USE_GESTURE_DETECTOR" = true ]; then
    ./start_gesture_detector.sh &


# Wait before launching fusion
sleep 1
./start_fusion.sh &

sleep 1
./start_follower.sh &

sleep 1
./start_ackermann.sh &

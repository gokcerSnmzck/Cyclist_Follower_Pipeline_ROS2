#!/bin/bash

# Start ZED
./start_zed.sh > zed.log 2>&1 &

# Wait for ZED to initialize
sleep 3

# Choose detection strategy
USE_HYBRID=false

if [ "$USE_HYBRID" = true ]; then
    ./start_hybrid_reid.sh > hybrid_reid.log 2>&1 &
else
    ./start_deepstream.sh > deepstream.log 2>&1 &
fi

sleep 1

USE_GESTURE_DETECTOR=false
if [ "$USE_GESTURE_DETECTOR" = true ]; then
    ./start_gesture_detector.sh > gesture_detector.log 2>&1 &
fi

# Wait before launching fusion
sleep 1
./start_fusion.sh > fusion.log 2>&1 &

sleep 1
./start_follower.sh > follower.log 2>&1 &

sleep 1
./start_cmdvel_to_can.sh > cmdvel_to_can.log 2>&1 &
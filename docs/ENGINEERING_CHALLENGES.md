# Engineering challenges and solutions

[Project overview](../README.md) · [Technical contributions](TECHNICAL_CONTRIBUTIONS.md) · [Experimental results](EXPERIMENTAL_RESULTS.md)

These case studies connect engineering decisions to the implemented system and the August 2025 research experiments. Report page references use the printed page numbers.

## ROS 2 images inside an accelerated video pipeline

**Challenge →** ROS image callbacks and DeepStream operate with different data structures and processing lifecycles.

**Engineering approach →** Make the interface explicit in both directions: convert image data into GStreamer buffers, then convert tracker metadata into a ROS-facing detection representation.

**Implemented solution →** The [DeepStream node](../src/deepstream_ros_node_json/deepstream_ros_node_json/deepstream_ros_node_json.py) uses `cv_bridge`, BGRA conversion, a frame queue and `appsrc` buffer callbacks. Its metadata probe extracts object IDs, classes, confidence and bounding boxes and publishes JSON on `/deepstream/detections`.

**Observed result →** DeepStream became a perception component in the ROS following architecture, feeding fusion and control in the simulation and physical experiments. The integration preserves the detector/tracker identity across the ROS boundary. Report pp. 27–29 and 48–50.

## Keeping video buffering bounded

**Challenge →** Incoming camera frames could accumulate when downstream processing consumed them more slowly, increasing RAM use.

**Engineering approach →** Bound the pending work and prioritize recent observations for following.

**Implemented solution →** The input queue is limited to five frames. On overflow, the node discards the oldest waiting frame before inserting the new one; GStreamer requests frames through `need-data`.

**Observed result →** The report records that limiting buffering addressed the observed queue-related memory growth (p. 54). The current source retains the bounded queue. This supports the buffering improvement, rather than a claim of measured whole-process memory stability over an unspecified duration.

The separate Nsight Systems investigation into Jetson conversion behavior is documented in [technical contributions](TECHNICAL_CONTRIBUTIONS.md#6-buffer-management-profiling-and-integration-debugging).

## Deploying GPU-accelerated inference on Jetson

**Challenge →** Move a trained detector into the embedded video-processing stack while integrating tracker output with ROS.

**Engineering approach →** Use an ONNX model representation, DeepStream's inference plugin and a YOLO custom parser, with a TensorRT engine built/loaded for the target environment.

**Implemented solution →** The reported deployment exported YOLOv11 medium and compiled the custom YOLO inference implementation. The ROS node loads the external inference and NvDCF configurations and the NVIDIA tracker library. The physical platform used Jetson Orin NX with JetPack 6.1 and DeepStream 7.1.

**Observed result →** The robot ran the integrated perception-to-control pipeline during field trials. The report includes Jetson resource observations and control timing evidence, presented with their original scope in [experimental results](EXPERIMENTAL_RESULTS.md). Report pp. 14–16, 27–29 and 51–52.

## Connecting tracked identities to stereo localization

**Challenge →** DeepStream supplies tracked 2D boxes; following needs the selected target's 3D position from ZED, whose object observations have their own identities and image scale.

**Engineering approach →** Associate the two representations geometrically in image space, then use the corresponding stereo position.

**Implemented solution →** The [fusion node](../src/fusion_node/fusion_node.py) compares normalized box centers, compensates for the scale difference, gates candidate matches and publishes the chosen 3D position with the detector identity in `TargetPosition`.

**Observed result →** A consistent target interface connects visual identity to following commands. The [RViz view](../data/test_scene_1/scene1_rviz_pointcloud.png) shows the spatial-perception output, while reported simulation and physical following demonstrate the integrated use of localization. This is not a separate localization-accuracy benchmark.

## Selecting and recovering a following target through gestures

**Challenge →** Enable a person to establish or re-establish the following target without restarting the software pipeline.

**Engineering approach →** Convert a deliberate, sustained body gesture into a target-selection event.

**Implemented solution →** The [gesture node](../src/gesture_selector/gesture_selector/gesture_selector.py) checks wrist/shoulder displacement over two seconds and coordinates selection/reset state with fusion. Fusion enables this path using `USE_GESTURE_DETECTOR=true`.

**Observed result →** The report describes using gesture-based retargeting during practical tests to resume following after loss (p. 56). Recovery here is operator-initiated reselection; it is not evidence of automatic identity recovery under arbitrary occlusion.

## Connecting high-level following to physical actuation

**Challenge →** A ROS `Twist` command must become the chassis-specific velocity, steering, gear and brake fields transmitted over CAN.

**Engineering approach →** Separate target-following logic from protocol adaptation and keep CAN serialization in the supplied driver.

**Implemented solution →** The [Python adapter](../CAN_Combined_Pipeline/src/cmd_vel_to_can_node/cmd_vel_to_can_node/cmd_vel_to_can_node.py) subscribes to `/cmdvel`, scales the command fields and publishes YHS `ctrl_cmd`. The [vendor C++ driver](../CAN_Combined_Pipeline/src/mk-01/yhs_can_control/src/yhs_can_control_node.cpp) encodes frames, counters and checksums and receives feedback.

**Observed result →** The assembled ZED2i–Jetson–CAN–FR-max system followed a pedestrian indoors and demonstrated straight-line cyclist following indoors and outdoors at low speed. The physical tests also informed camera alignment: tilting the camera upward helped keep the cyclist in view at distance. Report pp. 48–50.

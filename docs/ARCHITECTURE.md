# System architecture

[Project overview](../README.md) · [Technical contributions](TECHNICAL_CONTRIBUTIONS.md) · [Setup](SETUP.md)

The system separates image processing, target identity, spatial localization and vehicle commands into ROS 2 components. This lets the same perception design serve a simulated Ackermann vehicle and the physical Yuhesen FR-max, with a dedicated control interface in each workspace.

## Execution paths

| Workspace | Input and perception | Motion output |
|---|---|---|
| [`src/`](../src) | ZED simulation acquisition, DeepStream, fusion and optional gesture selection | Follower → `/cmd_vel` → Ackermann adapter → `/ackermann_cmd` → Isaac Sim |
| [`CAN_Combined_Pipeline/src/`](../CAN_Combined_Pipeline/src) | Physical ZED2i acquisition, Jetson DeepStream, fusion and optional gesture selection | Follower → `/cmdvel` → command adapter → `ctrl_cmd` → YHS CAN driver → FR-max |

The custom packages have overlapping names. Each row is an independent build and runtime scope, rather than two overlays to source together. The [README diagram](../README.md#system-architecture) shows their common perception design and separate actuation paths.

## Components and message flow

| Component | Consumes | Produces / responsibility |
|---|---|---|
| ZED wrapper | Stereo camera or simulation input | Rectified image, spatial object detections and body skeletons |
| DeepStream ROS node | `/zed/zed_node/left/image_rect_color` (`sensor_msgs/Image`) | `/deepstream/detections` (`std_msgs/String` containing JSON): tracked boxes, IDs, classes and confidence |
| Gesture selector | `/zed/zed_node/body_trk/skeletons` | `/selected_person_bbox` and `/selected_person_id`; receives `/gesture_selector/reset` from fusion |
| Fusion node | DeepStream detections, `/zed/zed_node/obj_det/objects`, optional gesture selection | `/fused_target` (`detection_msgs/TargetPosition`); selected identity and 3D position |
| Person follower | `TargetPosition` | `geometry_msgs/Twist` on the workspace-specific velocity topic |
| Simulation adapter | `/cmd_vel` | `/ackermann_cmd` for the simulated vehicle |
| Physical command adapter | `/cmdvel` | YHS `ctrl_cmd` velocity, steering, gear and brake fields |
| Vendor CAN driver | YHS control messages | CAN serialization, counters/checksum and chassis feedback handling |

See the [target message definition](../src/detection_msgs/msg/TargetPosition.msg), [fusion implementation](../src/fusion_node/fusion_node.py) and [physical command adapter](../CAN_Combined_Pipeline/src/cmd_vel_to_can_node/cmd_vel_to_can_node/cmd_vel_to_can_node.py).

## ROS image to accelerated perception

The [DeepStream node](../src/deepstream_ros_node_json/deepstream_ros_node_json/deepstream_ros_node_json.py) converts supported ROS image encodings to BGRA. It holds at most five waiting frames, dropping the oldest queued frame when capacity is reached. GStreamer's `need-data` callback takes a frame, copies its bytes into a `Gst.Buffer` and pushes it into `appsrc`.

The linked processing path is:

```text
ROS image → cv_bridge / BGRA → bounded queue → appsrc
  → videoconvert → NV12 caps → nvvideoconvert → nvstreammux
  → nvinfer → nvtracker → nvvideoconvert → nvdsosd
  → display sink or fakesink
```

Input caps specify **960 × 540 at 30/1 FPS**. The stream multiplexer uses one stream. `nvinfer` and `nvtracker` load external model/tracker configurations; the historical deployment used YOLOv11 medium, TensorRT and NvDCF. A metadata probe publishes tracked detections back to ROS. This is an explicit image-copy bridge into accelerated processing.

## Associating identity with stereo position

Fusion maintains the latest detector metadata and ZED objects. It compares normalized bounding-box centers, accounting for the image-scale difference: detector centers are scaled by two before comparison with the ZED boxes. Candidates must pass the per-axis normalized distance threshold of `0.2`; the smallest summed center distance wins.

The node locks to a detector identity and publishes the associated ZED 3D position, class and confidence. This is asynchronous, latest-message association. The JSON detection message carries no acquisition header; the outgoing target header is stamped at publication and uses the ZED frame identifier. It should therefore be interpreted as a target output, not a synchronized multi-sensor timestamp record.

## Gesture-based selection

The [gesture selector](../src/gesture_selector/gesture_selector/gesture_selector.py) uses the configured skeleton joints: wrist index `4` and shoulder index `2`. A vertical difference above `0.1` held for two seconds triggers the selection workflow. The state machine coordinates selection, tracking and reselection using identity and bounding-box information.

Fusion enables this optional path through `USE_GESTURE_DETECTOR=true`. Starting the selector alone does not change fusion's mode. Selection provides an operator-facing way to establish or change the target, including retargeting during field experiments.

## Following and actuation

The [follower](../src/person_follower_pkg/person_follower_pkg/person_follower.py) uses target-relative position to generate forward and angular velocity requests. Current constants are a `1.5 m` desired separation, proportional forward control capped at `0.4`, and lateral control capped at `±0.8`. The resulting `Twist` is then adapted for the chosen platform.

In simulation, the [Ackermann adapter](../src/ackermann_control/cmdvel_to_ackermann/scripts/cmdvel_to_ackermann.py) converts the command using its vehicle-geometry parameters. On the robot, the [Python command adapter](../CAN_Combined_Pipeline/src/cmd_vel_to_can_node/cmd_vel_to_can_node/cmd_vel_to_can_node.py) applies the implemented velocity and steering scales (`×10` and `×40`) and sets gear/brake fields. The [YHS C++ driver](../CAN_Combined_Pipeline/src/mk-01/yhs_can_control/src/yhs_can_control_node.cpp) handles CAN encoding and feedback.

Those numeric fields belong to the configured software/protocol contract; they are not an independent measurement of physical chassis speed. Hardware operation uses supervised trials and an independent stop mechanism. See [physical workflow](SETUP.md#physical-robot-workflow) for the operating checks.

## Alternative perception integration

The [Hybrid ReID ROS package](../src/hybrid_reid_ros_node/README.md) exposes an alternative publisher on `/deepstream/detections`. It combines a YOLOv8 segmentation detector with DeepSORT and DINOv2-based appearance features. It is a separate experimental integration, and its results should not be substituted for the reported DeepStream deployment results. Run one detector publisher at a time.

## Design records

The repository retains the [original system diagram](../project_diagrams/v0.0.3_ROS_System_Diagram.png), [simulation ROS graph](../data/test_scene_1/ros_graph.png) and [physical pipeline graph](../data/can_integrated_pipeline/Screenshot%20from%202025-06-27%2002-11-34.png). These complement the current source-linked description above.

# Setup and usage

[Project overview](../README.md) · [Architecture](ARCHITECTURE.md) · [Experimental results](EXPERIMENTAL_RESULTS.md)

The project has separate **simulation**, **Jetson perception** and **physical-robot** workflows. The commands below follow the checked-in entry points. They require the corresponding vendor runtime, models and configuration; they are not a containerized, hardware-independent installation.

## Runtime environment

The August 2025 report identifies **Jetson Orin NX, JetPack 6.1, Ubuntu 22.04, DeepStream 7.1 and ROS 2 Humble** for the physical deployment. Retained logs identify ZED SDK 5.0.0, and a simulation capture identifies Isaac Sim 4.5.0. These records describe the research environments; use the matching vendor packages for the chosen machine.

| Layer | Dependencies / configuration |
|---|---|
| ROS 2 | Humble, colcon/ament, rclpy/rclcpp, standard messages, cv_bridge and custom interface generation |
| ZED | ZED2i, SDK, ROS wrapper and the `zed_msgs` message package consumed by the nodes; enable object detection and body tracking for the corresponding workflows |
| DeepStream | GStreamer plugins, DeepStream Python bindings (`pyds`), CUDA, TensorRT and the tracker library |
| YOLO deployment | Original ONNX/model export, labels, custom parser library, inference configuration and target-compatible TensorRT engine |
| Simulation | Isaac Sim with ROS bridge, required USD assets, ZED simulation configuration and Ackermann messages |
| Physical robot | YHS interfaces/driver, the chassis protocol configuration, CAN interface and an independent stop mechanism |
| Optional Hybrid experiment | Compatible PyTorch/torchvision, Ultralytics, deep-sort-realtime, NumPy, SciPy, OpenCV, Pillow, Numba and DINOv2 code/weights |

### ZED package revisions

The repository records the following vendor gitlinks. Restore the matching checkouts and their original source mapping, or supply the verified packages through a vendor underlay. This checkout does not include a `.gitmodules` URL mapping, so `git submodule update` alone will not restore them.

| Path | Recorded revision |
|---|---|
| `src/zed-ros2-wrapper` | `8e2ca63da1f4207977784cba15160688b4529739` |
| `src/zed-ros2-interfaces` | `de17255cba944fdb76347a85965338fcf22cbf3e` |
| `src/zed-ros2-examples` | `6527fb387b1cae1b491d0b8f03bcb9b8aa8c96f5` |

### Inference and tracker configuration

The DeepStream node currently consumes these literal paths. Restore the original files at these locations or adapt the paths for the deployment machine before running; they are not exposed as ROS path parameters.

| Purpose | Path consumed by the node |
|---|---|
| Inference configuration | `/home/gokcer/DeepStream-Yolo/config_infer_primary_yolo11.txt` |
| Tracker configuration | `/home/gokcer/DeepStream-Yolo/config_tracker_NvDCF_perf.yml` |
| Tracker library | `/opt/nvidia/deepstream/deepstream/lib/libnvds_nvmultiobjecttracker.so` |

The reported inference workflow used YOLOv11 medium → ONNX → DeepStream custom parser → TensorRT engine. Supply all model, label and parser files referenced by the configuration and build an engine for the intended target environment. Confirm the tracker configuration loads successfully in the startup output.

The optional Hybrid wrapper instead defaults to `yolov8n-seg.pt` relative to the working directory and loads `dinov2_vitb14_reg` through PyTorch Hub. Treat it as a separate experimental backend, with its own dependencies and model terms.

## Build one workspace

Set `REPO_DIR` to the clone's absolute path. Use a fresh terminal for each workflow and source only that workflow's overlay. The separate output directories below avoid relying on checked-in build artifacts from the original machine.

### Simulation workspace

After installing/restoring the dependencies:

```bash
REPO_DIR=/absolute/path/to/Cyclist_Follower_Pipeline_ROS2
source /opt/ros/humble/setup.bash
cd "$REPO_DIR"
colcon --log-base .portfolio-build/sim/log build \
  --base-paths src \
  --build-base .portfolio-build/sim/build \
  --install-base .portfolio-build/sim/install
source .portfolio-build/sim/install/setup.bash
```

### Physical workspace

Supply ZED/vendor packages in a separate underlay, then build the CAN tree:

```bash
REPO_DIR=/absolute/path/to/Cyclist_Follower_Pipeline_ROS2
source /opt/ros/humble/setup.bash
source /absolute/path/to/vendor-underlay/install/setup.bash
cd "$REPO_DIR"
colcon --log-base .portfolio-build/can/log build \
  --base-paths CAN_Combined_Pipeline/src \
  --packages-skip cyclist_follower_bringup \
  --build-base .portfolio-build/can/build \
  --install-base .portfolio-build/can/install
source .portfolio-build/can/install/setup.bash
```

The skipped bringup package references the simulation Ackermann adapter. Use the physical entry points below for the CAN workflow. Avoid a repository-wide default build: the two trees contain packages with the same names.

## Simulation workflow

Open a project stage such as [`scaled_robot_with_automated_scene_V3.usd`](../simulation/scaled_robot_with_automated_scene_V3.usd) in Isaac Sim. Resolve its asset references, enable the ROS bridge and inspect the scene's camera and `/ackermann_cmd` wiring. Use a ROS domain isolated from any physical robot.

With the simulation overlay sourced, start each process in its own terminal:

```bash
ros2 launch zed_wrapper zed_camera.launch.py camera_model:=zed2i sim_mode:=true
```

```bash
ros2 run deepstream_ros_node_json deepstream_ros_node_json --ros-args -p enable_visualization:=false
```

```bash
ros2 run fusion_node fusion_node.py
```

The camera launch arguments follow the retained startup scripts; confirm them against the restored ZED wrapper revision. Check image dimensions/encoding, detector metadata and `/fused_target` before starting simulation control:

```bash
ros2 run person_follower_pkg person_follower
```

```bash
ros2 launch cmdvel_to_ackermann cmdvel_to_ackermann.launch.py
```

The Ackermann launch exposes `track_width`, `publish_period_ms`, `acceleration` and `steering_velocity`. Match the geometry to the loaded vehicle. Use these individual commands instead of the root `startup_scripts/start_all.sh`, which contains an incomplete shell conditional.

### Optional gesture selection

Enable ZED body tracking and its skeleton topic. Start the selector:

```bash
ros2 run gesture_selector gesture_selector
```

Replace the plain fusion command with:

```bash
USE_GESTURE_DETECTOR=true ros2 run fusion_node fusion_node.py
```

The selector publishes `/selected_person_bbox` and `/selected_person_id`; fusion consumes the bounding-box message and sends `/gesture_selector/reset` when reselection is needed. Hold the configured raised-hand gesture for two seconds. Starting the selector alone does not enable selection in fusion.

## Jetson perception workflow

Use the physical-workspace overlay and the matching Jetson runtime. Start the physical camera:

```bash
ros2 launch zed_wrapper zed_camera.launch.py camera_model:=zed2i sim_mode:=false
```

Then run the DeepStream command from the simulation section. `enable_visualization:=false` selects `fakesink` while retaining the inference/tracking pipeline. Inspect the image stream, inference/tracker startup messages and `/deepstream/detections`; add fusion after both detection and ZED spatial-object topics are present.

For perception-only sessions, keep vehicle control subscribers disconnected. If experimenting with `ros2 run hybrid_reid_ros_node hybrid_reid_ros_node`, stop DeepStream first: both backends publish the same detection topic.

## Physical-robot workflow

The intended execution chain is:

```text
physical follower → /cmdvel → cmd_vel_to_can_node → ctrl_cmd
    → yhs_can_control_node → CAN → FR-max
```

Use the [vendor driver](../CAN_Combined_Pipeline/src/mk-01/yhs_can_control) and the chassis-specific CAN interface/bitrate configuration. Verify message decoding, velocity/steering units, gear/brake behavior and chassis feedback with actuation disabled before a supervised trial. The current Python adapter applies `×10` to forward velocity and `×40` to angular input; an all-zero command selects neutral with brake set. Validate those values against the actual chassis protocol.

The ROS entry points are `person_follower_pkg / person_follower` and `cmd_vel_to_can_node / cmd_vel_to_can_node`. Start them only as part of the prepared robot workflow, after perception/selection is established and the independent stop is available. The CAN workspace's `start_all.sh` does not start the vendor CAN driver and contains machine-specific workspace paths.

**Operating scope:** use low-speed, supervised trials with an independent stop. The follower's one-second message-receipt watchdog does not establish sensor freshness or guarantee a stop for every detector/node failure; validate target loss, process loss and emergency-stop behavior on the actual platform before motion.

## Offline checks

These commands require Python 3, not ROS, Jetson or a robot:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
python3 tools/summarize_log_rates.py
python3 tools/check_repository.py
```

The current unit suite contains 24 tests: 22 pass and two are marked expected failures. Those expected-failure regressions remain in place. The repository checker includes Python/XML/shell syntax checks and returns a nonzero status for the root startup script's incomplete conditional. Runtime build and hardware verification are separate from these offline checks.

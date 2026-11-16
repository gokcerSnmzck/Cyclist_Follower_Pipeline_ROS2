# Installation and reproduction

## What can be reproduced now

The offline checks require Python 3 and Bash, with no pip packages, ROS graph,
model downloads or hardware. Run from the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
python3 tools/check_repository.py
python3 tools/summarize_log_rates.py
```

The syntax checker deliberately reports the root startup error and exits 1.
The unit suite's expected failures represent open defects, not accepted safety
behavior. See [actual results](EVALUATION.md).

The commands below are source-checked recipes for a restored runtime, **not a
claim of a successful ROS build on the audit host**. ROS 2, colcon, OpenCV,
PyTorch, DeepStream Python bindings, the ZED SDK and Isaac Sim were unavailable
there. Do not source the checked-in `install/` tree: its generated paths belong
to another machine.

## Recover dependencies before a runtime build

Historical logs identify ROS 2 Humble / Python 3.10 and ZED SDK 5.0.0. A saved
simulation screenshot identifies Isaac Sim 4.5.0. These observations do not
establish a complete mutually compatible Jetson/runtime version matrix.

| Component | Required information / current gap |
|---|---|
| ROS 2 | Humble underlay, rclpy/rclcpp, ament, rosidl, geometry/sensor/std/builtin interfaces; Ackermann messages for simulation |
| ZED | ZED2i, SDK, wrapper, object/body tracking configuration, message package actually providing `zed_msgs`; current manifests also mention `zed_interfaces` |
| DeepStream | Compatible CUDA/TensorRT/GStreamer/DeepStream/pyds versions and plugin library paths for the target architecture |
| YOLO11 deployment | Original inference config, model export/labels, custom parser, engine build recipe, engine checksum, confidence/NMS settings |
| nvtracker | Original NvDCF config, matching low-level tracker library; historical warning means defaults were used for at least one run |
| Hybrid experiment | PyTorch/torchvision, OpenCV, NumPy, SciPy, Pillow, Ultralytics, deep-sort-realtime, Numba and verified model provenance/version pins |
| Physical robot | YHS protocol revision, CAN bitrate/interface, velocity/steering units, braking/gear definitions, independent stop mechanism |
| Isaac Sim | USD/asset availability, ROS bridge and scene topic wiring, compatible ZED simulator configuration and frame/clock policy |

No lockfile exists for the external AI stack. Installing arbitrary latest wheels
is not a reproduction strategy, especially for Jetson. Recover the original
environment first and verify against vendor documentation. The Hybrid CPU/mock
fallbacks have known defects; they are not a supported CPU-only alternative.

### Missing ZED checkout mapping

Three Git entries record revisions but their source directories are empty and
there is no `.gitmodules` mapping:

| Directory | Recorded commit |
|---|---|
| `src/zed-ros2-wrapper` | `8e2ca63da1f4207977784cba15160688b4529739` |
| `src/zed-ros2-interfaces` | `de17255cba944fdb76347a85965338fcf22cbf3e` |
| `src/zed-ros2-examples` | `6527fb387b1cae1b491d0b8f03bcb9b8aa8c96f5` |

Recover the original repository URLs and local modifications before repairing
these gitlinks. `git submodule update --init --recursive` alone is insufficient.
Do not replace them with guessed latest vendor branches. For the CAN workspace,
build/supply the verified vendor packages as a separate underlay rather than
overlaying both copies of this project's custom packages.

### External configuration values currently consumed

These are literal code paths, **not configurable ROS parameters** today:

| Consumer | Existing value | Operator must recover |
|---|---|---|
| nvinfer | `/home/gokcer/DeepStream-Yolo/config_infer_primary_yolo11.txt` | Original inference config and every referenced parser/model/label file |
| nvtracker config | `/home/gokcer/DeepStream-Yolo/config_tracker_NvDCF_perf.yml` | Actual tracker settings; filename alone is not evidence of use |
| nvtracker library | `/opt/nvidia/deepstream/deepstream/lib/libnvds_nvmultiobjecttracker.so` | SDK-provided library for the machine |
| Hybrid model | `yolov8n-seg.pt` relative to CWD | Checksum/provenance and path available in the run directory |
| DINOv2 | `torch.hub.load('facebookresearch/dinov2', 'dinov2_vitb14_reg')` | Versioned code/cache and weights; current call is not revision-pinned |

Recover the original values on a dedicated reproduction machine. Portable ROS
path parameters are proposed in the audit but not implemented, because changing
the resolved inference/tracker configuration can alter target behavior.
The existing `enable_visualization` parameter is supported; setting it false
selects fakesink but does not remove inference/OSD plugin requirements.

## Independent build scopes

After restoring the dependency underlay, set `REPO_DIR` to the clone's absolute
path. Use a fresh terminal for each workflow and source only its intended overlay.
The separate build/install/log directories avoid modifying historical artifacts.

Root simulation/perception workspace:

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

CAN integration workspace, after sourcing a verified ZED/vendor underlay in that
terminal (replace the placeholder path):

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

The skipped bringup package requires the simulation Ackermann package absent
from the CAN tree. This is not a workaround for the other dependency gaps.
Use `colcon list --base-paths src` or the CAN base path to inspect the scope
before building. Plain `colcon build` from the repository root can discover
duplicate packages. Run ROS tests only once the dependency environment builds;
the existing ament lint templates are not hardware integration tests.

## Simulation workflow

Inspect a stage such as
[`scaled_robot_with_automated_scene_V3.usd`](../simulation/scaled_robot_with_automated_scene_V3.usd)
in the compatible Isaac Sim environment. Resolve its asset references, inspect
its ROS bridge/subscriptions and confirm `/ackermann_cmd` before playback.
The binary stages were not opened during this audit; their names alone do not
establish which stage matches each recorded video.

In an isolated simulation ROS domain, with the root overlay sourced in every
terminal, the following entry points exist in source:

```bash
ros2 launch zed_wrapper zed_camera.launch.py camera_model:=zed2i sim_mode:=true
ros2 run deepstream_ros_node_json deepstream_ros_node_json --ros-args -p enable_visualization:=false
ros2 run fusion_node fusion_node.py
```

Run these in separate terminals, after the missing configs are restored. The
vendor launch file itself is missing from this checkout, so its arguments remain
supported by the historical scripts rather than locally revalidated vendor code.
`hybrid_reid_ros_node hybrid_reid_ros_node` is an alternative console executable,
not a second detector to run on the same topic; audit defects currently limit it.

Optional selection requires `ros2 run gesture_selector gesture_selector` and
`USE_GESTURE_DETECTOR=true ros2 run fusion_node fusion_node.py` in place of the
plain fusion command, plus valid skeleton publication/body format. Starting a
gesture node alone does not enable selection in fusion.

The simulation control entry points are `person_follower_pkg / person_follower`
and `cmdvel_to_ackermann / cmdvel_to_ackermann.launch.py`; the latter exposes
`acceleration`, `steering_velocity`, `track_width`, `publish_period_ms`. Start
them only after confirming domain isolation and the command-expiry limitations
in audit A02/A04. The broken root `start_all.sh` is intentionally not presented
as an executable quickstart.

## Jetson perception workflow

Use a verified Jetson-compatible vendor environment and a single chosen custom
workspace. For physical camera acquisition the historical launch command changes
to `sim_mode:=false`. Launch only camera and one detector for a perception-only
session; keep control subscribers disconnected from that ROS domain. Inspect
image encoding/dimensions, negotiated caps, empty detections, bus errors and
tracker-config load status before using fusion output.

No Jetson deployment or FPS/power claim has been revalidated here. The tracked
engine's filename is not sufficient to establish portable hardware compatibility.

## Physical-robot workflow and approval gate

The intended chain is CAN-tree follower → `/cmdvel` → `cmd_vel_to_can_node` →
`ctrl_cmd` → `yhs_can_control_node` → chassis. `start_all.sh` starts the first two
custom control components but not the CAN driver. Its workspace paths are
machine-specific, and `cyclist_follower.launch.py` is not physical bringup.

Before preparing a launchable deployment, resolve A01–A06 and agree the exact
watchdog/units/braking changes in the audit. Then validate decoding and frames
with the chassis disconnected, followed by supervised robot tests under an
independent stop mechanism. No CAN interface setup, driver launch, sample-command
publisher or hardware test was executed by this review. No new actuation
quickstart is offered while the physical command contract remains unresolved.

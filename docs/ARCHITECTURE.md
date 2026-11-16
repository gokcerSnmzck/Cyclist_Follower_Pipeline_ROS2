# Architecture and implementation map

This document describes the source entry points at baseline `4195d12` plus the
non-functional portfolio corrections. “Active” means selected by setup/CMake and
startup scripts, not certified or proven to match every historical experiment.

## Workspaces and authority

| Area | Entry-point evidence | Relationship |
|---|---|---|
| Root `src/` | `startup_scripts/start_zed.sh` sets `sim_mode:=true`; follower publishes `/cmd_vel`; Ackermann executable is installed by CMake | Simulation-oriented workspace with ZED vendor gitlinks |
| `CAN_Combined_Pipeline/src/` | CAN startup sets `sim_mode:=false`; follower publishes `/cmdvel`; adapter publishes `ctrl_cmd` | Physical-camera/CAN integration workspace; vendor ZED source is not included here |
| `simulation/` | Binary USD stages, scene screenshots/recordings | Isaac Sim research assets; simulator and external references are not packaged |
| CAN `cyclist_follower_bringup` | Launch explicitly sets simulation mode and resolves `cmdvel_to_ackermann` | Simulation-oriented launch copied into the CAN tree, not complete physical bringup |
| Historical variants | `_old`, `_OLD_LATEST`, `_Webcam`, `_buffer_leak`, `_Refactored`, `.txt` snapshots | Preserved experiments, not selected by normal console entry points |

Do not build both source trees in the same colcon package-discovery scope. Six
package names overlap. The active DeepStream files differ in visualization
default (root false, CAN true); the followers differ in command topic; fusion
differs in gesture reset logic. Hybrid modules also differ, including an
optional TensorRT branch in the CAN detector that its ROS wrapper does not enable.

The June 2025 logs support a physical ZED/CAN integration run, but the detector
log says visualization disabled while the current CAN source defaults true.
That could reflect a parameter override or another revision. Neither directory
can be asserted to be the exact source for reported experiments without the
report and a run manifest.

## Topics and contracts

| Producer → consumer | Topic | Message / key semantics |
|---|---|---|
| ZED → DeepStream or Hybrid | `/zed/zed_node/left/image_rect_color` | `sensor_msgs/Image` |
| DeepStream or Hybrid → fusion | `/deepstream/detections` | `std_msgs/String`: JSON `frame_number`, `objects`; top-left pixel `bbox` x/y/width/height, label/confidence/tracking_id; **no acquisition stamp or image dimensions** |
| ZED → fusion | `/zed/zed_node/obj_det/objects` | `zed_msgs/ObjectsStamped`, object bounding-box corners and 3D position |
| ZED → gesture | `/zed/zed_node/body_trk/skeletons` | `zed_msgs/ObjectsStamped`, skeleton keypoints |
| Gesture → fusion | `/selected_person_bbox` | `zed_msgs/Object`, optional startup environment gate |
| Gesture → observers | `/selected_person_id` | `std_msgs/Int32`; current fusion consumes bbox, not this ID topic |
| Fusion → gesture | `/gesture_selector/reset` | `std_msgs/Empty` |
| Fusion → follower | `/fused_target` | `detection_msgs/TargetPosition`: int32 ID, class, confidence, Point, Header stamped at fusion publication |
| Root follower → Ackermann | `/cmd_vel` | `geometry_msgs/Twist` |
| Ackermann → simulator bridge | `/ackermann_cmd` | `ackermann_msgs/AckermannDriveStamped`; scene wiring requires Isaac Sim inspection |
| CAN follower → adapter | `/cmdvel` | `geometry_msgs/Twist` |
| Adapter → YHS driver | `ctrl_cmd` | `yhs_can_interfaces/CtrlCmd`; relative name resolves to `/ctrl_cmd` in root namespace |
| YHS driver → observers | `chassis_info_fb`, `odom` | Chassis feedback and `nav_msgs/Odometry` |

The unused-on-this-path `Detection2D`, `BoundingBox2D`, `Detection2DArray`
interfaces coexist with the JSON transport. The historical test publisher uses
the array type on the JSON topic, so it is not a valid integration test.

Most Python endpoints specify depth 10 with no custom QoS profile. Their default
reliability must be checked against the actual vendor publishers; no live DDS
compatibility test was possible. Ackermann and CAN C++ endpoints use depth 1.
Python mains use `rclpy.spin(node)` without a custom executor. GStreamer demand
and pad-probe callbacks execute in streaming context; a thread-safe Python queue
bridges image input. There is no message_filters synchronization in fusion.

## DeepStream data and memory flow

1. CvBridge requests passthrough pixels. mono8/BGR8/RGB8 are converted to BGRA;
   BGRA8 is accepted; other encodings are rejected. OpenCV resizes to 960×540.
2. A Python queue holds at most five frames. When full, an oldest-frame removal
   precedes retrying insertion. This bounds this queue, not all DDS/GStreamer/GPU
   buffering; the get/put operations are not a single atomic transaction.
3. `need-data` takes a frame, creates Python bytes, allocates a Gst buffer and
   copies bytes into it. This is a CPU-copy bridge, not zero-copy GPU ingestion.
4. `appsrc (BGRA) → videoconvert → caps NV12 → nvvideoconvert → nvstreammux
   → nvinfer → nvtracker → nvvideoconvert → nvdsosd → sink`.
   A separate NVMM capsfilter is created but is not on the linked path.
   GPU surface negotiation/upload therefore requires inspection on the target SDK.
5. Streammux uses 960×540, batch 1, live-source and 40,000 µs push timeout.
   `nvinfer` reads an external YOLO11 config; its preprocessing/thresholds cannot
   be recovered from this checkout. The saved engine log describes a 3×640×640
   input; that is distinct from the 960×540 stream coordinate system.
6. The OSD sink probe reads SDK metadata and publishes JSON only when objects
   exist. It copies scalar metadata; it does not map image surfaces into NumPy.
   Python/GI manages buffer references here; no demonstrated need for manual
   unref was established. Changing ownership rules without SDK validation risks
   use-after-free or double release.
7. A 100 ms ROS timer polls ERROR/EOS and sets pipeline NULL. Main's finally
   also sets NULL on shutdown. A constructor exception precedes that finally;
   request pads are not explicitly released and link/flow results are not fully
   checked. See audit A14 for the distinction between code gaps and proven leaks.

Commit `e7f23a0` introduced bounded queuing, need-data feeding, explicit encoding
handling, live-source and ROS-timer bus polling in place of a GLib loop thread.
Those are demonstrable changes. They are not proof that every Jetson buffer or
memory issue was fixed. The screenshot titled “memory leak addressed” shows one
system-monitor view; the sanitizer text has no result beyond its banner.

## Association, gesture and control

The matcher compares `(zed_x/960, zed_y/540)` against `(2*ds_x/960, 2*ds_y/540)`.
Thus a ZED center `(960,540)` matches DeepStream center `(480,270)`. Under
1920×1080 ZED box coordinates this is a consistent half-resolution mapping.
The June camera log reports 1920×1080 grab and 960×540 publication, and fusion
logs contain ZED centers greater than 960. Confirm bounding-box convention from
the pinned ZED messages/bag before generalizing to another resolution.

Both axis differences must be strictly below 0.2; the smallest sum wins, with
first-in-list tie breaking. In full-resolution ZED pixels these gates correspond
to 192 horizontal and 108 vertical pixels. There is no one-to-one assignment,
confidence gate at fusion, age check or target-ID recovery policy after a tracker
ID switch when gesture mode is off. The first acceptable match locks the ID.
Position is copied from the ZED object, not triangulated in this repository.
Frame ID is preserved, but the follower does not transform or validate that frame.

Gesture selection uses keypoint indices 4/2 and `wrist_y > shoulder_y + 0.1` for
two seconds. This requires the corresponding body layout and axes. Enablement is
read from exported `USE_GESTURE_DETECTOR` at fusion construction; the historical
scripts' local Boolean variable alone does not propagate it. Root reset logic
can react to another object before reaching the selected one; CAN's membership
check improves that case, but empty object lists do not enter its reset loop.

Follower logic is `linear = clamp(x - 1.5, 0, 0.4)` and
`angular = clamp(y, -0.8, 0.8)` after `x > 0.1`. The values are source constants,
not measured safe vehicle limits. A 0.1 s watchdog sends one zero Twist after
more than 1 s without an accepted target. Receipt freshness cannot establish
sensor freshness. See audit A01–A04 before any physical deployment.

The CAN adapter's linear/steering scaling and neutral/brake branch are described
in the audit. The C++ driver packs extended CAN frames, counters and XOR checksums,
reads feedback on a separate thread, and integrates odometry. Its 15 ms receive
timeout diagnoses missing frames; it is not a command watchdog. Socket setup
failure paths, stop/thread ordering and lack of complete-frame-length checks
need bench validation; no CAN communication was run during this review.

## Alternative perception and experiments

The Hybrid wrapper defaults to YOLOv8 nano segmentation on CUDA, filters people
at 0.3 detection confidence, and configures a 0.5 tracker confidence threshold.
It estimates 30 FPS and derives max_age 198 frames for a nominal six-second
occlusion plus buffer; actual processed FPS and early no-detection returns make
this **not a measured six-second occlusion guarantee**.

The extractor loads DINOv2 ViT-B/14 with registers, 768 dimensions. Crops are
converted BGR→RGB, resized to 256, center-cropped to 224, ImageNet-normalized,
inferred under no_grad and L2-normalized. ResNet50 without its classifier is a
fallback (2048 channels); fallback tensor shape needs testing. Mask support is
implemented, but the active update calls do not pass masks to extraction.
The gallery helper assumes a different detection tuple shape and resizes an
entire mask into a crop; do not advertise validated background removal.

DeepSORT association, consistent-ID mapping, primary-object galleries, spatial
gates and “offline” ReID are derived from Hybrid ReID. Here “offline” is a
periodic method in the update path, not a separate processing service. The
DeepSORT API mismatch, ID allocation and inactive-track handling prevent a
claim of reliable long-term identity persistence. JSON confidence is hardcoded
to 0.9 by the wrapper. The CAN TensorRT option attempts to export `yolov8n.pt`
but then opens `yolov8n-seg.engine`; that optional path is not enabled by its ROS
wrapper and remains unvalidated.

`trajectory_follower` is installed separately but not selected by normal startup.
It transforms stored target points and uses a smoothed path/pure-pursuit-style
controller, publishes `/cmd_vel`, and has no target-loss watchdog. Its existence
does not establish a second validated robot controller. The `yhs_io_test` and
sample CtrlCmd publishers transmit robot commands and are not offline tests.

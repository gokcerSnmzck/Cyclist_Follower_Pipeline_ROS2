# Evaluation and validation record

## Historical evidence and measurement boundaries

The research report **“Bicyclist Detection and Tracking for a Follow-me Function
with a Mobile Robot”** is not present in this project tree. This prevents a
report/source discrepancy table and verification of its methodology or results.
The table below describes only retained source, logs and media; it does not
substitute for the report or establish a controlled benchmark.

| Quantity | Available evidence | What can be said |
|---|---|---|
| Camera acquisition configuration | [zed.log](../CAN_Combined_Pipeline/startup_scripts/zed.log#L181), lines 181/191–193 | HD1080@30, grab 1920×1080, published color/depth 960×540; configured mode, not measured delivered FPS |
| GStreamer input configuration | [node](../src/deepstream_ros_node_json/deepstream_ros_node_json/deepstream_ros_node_json.py#L30) | 960×540, 30/1 caps; negotiated/processed throughput unmeasured |
| Inference input | [deepstream.log](../CAN_Combined_Pipeline/startup_scripts/deepstream.log#L12) | Logged engine input 3×640×640; no isolated inference-throughput series |
| Follower logged updates | [follower.log](../CAN_Combined_Pipeline/startup_scripts/follower.log) | 278 events over 43.655894 s; **6.345 events/s**; median interval 71.557 ms |
| Fusion logged publications | [fusion.log](../CAN_Combined_Pipeline/startup_scripts/fusion.log) | 278 events over 43.656962 s; **6.345 events/s**; median interval 71.650 ms |
| CAN adapter logged callbacks | [cmdvel_to_can.log](../CAN_Combined_Pipeline/startup_scripts/cmdvel_to_can.log) | 280 events over 43.656672 s; **6.391 events/s**; median interval 71.840 ms; does not prove CAN delivery or motion |
| Fusion-to-control latency | No shared message sequence in these logs | Unavailable as a defensible paired measurement; log lines occur at different points relative to publication |
| Full end-to-end latency | Acquisition timestamp absent from JSON; fusion overwrites Header time | Unavailable; fusion timestamp subtraction would omit camera acquisition and inference |
| CPU/GPU/memory | [system-monitor screenshot](../data/memory_leak_of_deepstream_node_addressed.png) | A historical snapshot with simulator activity; not isolated node utilization, steady-state memory or a leak test |
| Power / Jetson thermals | No suitable measurement record found | No power-efficiency or thermal result claimed |
| Identity accuracy / occlusion | Algorithms and example media | No labeled evaluation set, ID-switch/MOTA/IDF1 record or repeatable occlusion success rate established |

Rates use `(N - 1) / (last timestamp - first timestamp)` for matching log events,
not `N / duration`. The median interval is not the reciprocal of the full-span
rate because event spacing varies. Shutdown/startup messages are excluded by
event text. Counts differ between files; there is no justified one-to-one
cross-file pairing. Generate the numbers without ROS:

```bash
python3 tools/summarize_log_rates.py
```

These logs are historical samples from one run, not general robot performance.
The camera log also reports skipped self-calibration and the detector log reports
a missing tracker config. The saved machine name and simulation GPU screenshot
do not establish execution on a Jetson. Filenames such as `fp32.engine` describe
an artifact name, not a full engine provenance or precision certification.

## Actual software-only validation, 2026-11-16

| Check | Observed result / boundary |
|---|---|
| Baseline Python syntax | All 99 tracked `.py` files under the two source trees parse |
| Baseline packaging regression | Six subtest failures reproduce missing ament resource-index declarations |
| Corrected packaging | All six declarations corrected; missing gesture/trajectory marker files added; console entry points resolve to source functions |
| Offline test suite | 24 tests: **22 pass, 2 expected failures** (A01 stale targets; A02 non-finite control input) |
| Final Python/XML/shell check | 104 Python files parse, 20 manifests parse as XML, 20/21 shell scripts pass `bash -n`; root `start_all.sh` fails at line 34; checker exits 1 |
| Log-rate analysis | Executed on the three retained logs; results above |
| Documentation/diff review | 67 local links resolve; source-line anchors are in bounds; `git diff --check` passes; 25 changed/new files, with application deltas confined to package metadata and model labels/comments |
| ROS/colcon | Not executed: ros2, colcon and rclpy unavailable; no `/opt/ros` installation |
| DeepStream/ZED/AI inference | Not executed: pyds, ZED Python SDK, OpenCV and PyTorch unavailable on this host |
| Isaac Sim / binary USD stages | Not executed / not semantically validated |
| CAN / vehicle | No interface opened, no messages transmitted, no robot actuated |

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
python3 tools/check_repository.py
```

Tests compile the actual class bodies from their source AST with in-memory
messages, clock, logger and publishers. They never execute module imports/main
or construct a GStreamer pipeline. They cover full/half-resolution centers,
axis gates, ties, filtering, empty/malformed detections, ID locking, repeated
stale matches, many-to-one association, differing gesture reset logic, gesture
hold/reset, follower saturation, timeout/reacquisition and CAN adapter arithmetic.
The DeepStream boundary test reproduces empty-frame suppression from the actual
probe method. They do not validate ROS message setters, DDS QoS, scheduling,
camera geometry, inference accuracy or the vehicle's physical response.

Expected failures explicitly assert desired behavior that is **not implemented**.
Characterization tests also preserve problematic current behavior so proposed
fixes can be reviewed against a known baseline. A green unittest exit therefore
does not mean every safety requirement is met. Existing ament lint templates
were inspected but not run; no external static analyzer was available.

## Discrepancies retained rather than reconciled

- The CAN detector defaults visualization on, while the saved run logs it off;
  an override/revision is unknown.
- Code names an NvDCF config, while the saved tracker reports that its file is
  missing. Effective historical algorithm/settings need recovery.
- Extractor previously described ViT-S/14 but called `dinov2_vitb14_reg`; only the
  log/comment was corrected, preserving model behavior.
- Metadata and package documentation disagree about licenses; ownership and
  redistribution remain open, not silently standardized.
- “30 FPS” input caps and estimated Hybrid FPS are configuration, while retained
  control logs show a different event rate. Neither is a measured inference FPS.

## Hardware-dependent acceptance work

1. Record Git revision/dirty state; exact model/config checksums; OS, ROS, SDK,
   driver, CUDA/TensorRT and device versions; camera mode, clocks and Jetson power
   mode. Pin third-party code and record how engines were built.
2. Capture acquisition and completion stamps plus a shared frame/target sequence
   across perception, fusion and control. Measure dropped/stale frames, queues,
   steady-state throughput, p50/p95/p99 latency and clock synchronization.
3. Replay labeled single/multiple-person, crossover, occlusion and reappearance
   sequences. Include detector/camera failure, malformed messages, non-finite
   3D positions, wrong frames, ID overflow and lost selections.
4. On the actual Jetson stack, record negotiated caps, Gst flow/bus failures,
   CPU copies, RSS/GPU memory trends and restart behavior over a declared soak
   duration with warm-up excluded. Keep simulator resource usage separate.
5. Bench-check protocol units, encoded CAN frames, brake/gear behavior, driver
   failure and independent command expiry before approved supervised robot work.

These are future test requirements, not successful results from this review.

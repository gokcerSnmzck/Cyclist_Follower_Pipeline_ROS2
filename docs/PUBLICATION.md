# Provenance, publication and portfolio presentation

## Attribution and release blockers

No repository-wide license is established by this cleanup. The source includes
conflicting package declarations and third-party notices, so no license text was
invented or replaced. The following is a provenance inventory, not legal clearance.

| Component | Evidence / attribution | Action before release |
|---|---|---|
| ROS integration, fusion, selection, follower and adapters | Project source and history; research context supplied by author | Confirm authorship boundaries and institutional publication permission; choose a license only for code you can license |
| Hybrid ReID | Wrapper header and prior package README identify [rvxfahim/Hybrid_reID](https://github.com/rvxfahim/Hybrid_reID); upstream displays Apache-2.0 | Recover copied revision and modifications, required license/notices, and reconcile local setup.py MIT vs package.xml TODO; do not present the tracker algorithm as original |
| DeepSORT | Imports `deep_sort_realtime`; [upstream](https://github.com/levan92/deep_sort_realtime) | Record exact version/license and API; no installed version was available to verify |
| DINOv2 | [Meta implementation](https://github.com/facebookresearch/dinov2) loaded through torch.hub | Record revision/weight provenance and terms; current loader is unpinned |
| YOLO / models | Ultralytics import and tracked `yolov8n-seg.pt`; external YOLO11 config path | Recover exact weight source and applicable software/model terms; no blanket license assertion for binaries |
| DeepStream-Yolo integration | Local absolute directory name; [candidate upstream](https://github.com/marcoslucianops/DeepStream-Yolo) supports YOLO integration | Confirm actual origin and revision; a directory name alone does not establish provenance |
| Ackermann adapter | Source header explicitly reserves NVIDIA rights and requires an express license agreement | Resolve distribution permission for this exact source before broad publication; do not erase or replace the notice |
| ZED wrapper/interfaces/examples | Three pinned gitlinks without URLs | Recover original URLs, commits, local changes and vendor terms |
| YHS driver, interfaces, chassis mesh | `mk-01`, `FR-max-description-ros2`, vendor-style author fields; TODO licensing | Establish upstream source, protocol/mesh rights and attribution |
| Isaac Sim scenes and recordings | Existing USDs, screenshots and videos | Confirm scene asset rights and recording/publication permission; provenance is not established merely by being tracked |

Upstream pages were consulted on 2026-11-16 for attribution/API identification;
they do not prove which versions were copied into this repository. The README
links existing demonstration media as historical evidence but does not create
new publicity images or assert redistribution clearance.

## Tracked artifacts and identifiers

Baseline `4195d12` has 6,045 tracked entries: 3,692 in `build/`, 1,387 in
`install/`, and 675 in `log/` (5,754 generated-tree entries in total). It also
tracks 72 `.pyc` files and three `.DS_Store` files. Largest reviewed artifacts:

| Artifact | Size (bytes) | Suggested treatment, subject to approval |
|---|---:|---|
| `CAN_Combined_Pipeline/startup_scripts/model_b1_gpu0_fp32.engine` | 94,853,244 | Preserve until provenance and engine regeneration/distribution strategy are established |
| `data/test_scene_1/test_video_rviz_point_cloud.webm` | 23,178,986 | Retain demonstration value; consider release hosting only after rights review |
| `simulation/my_scaled_leatherback_ROS.usd` | 13,349,994 | Preserve and document external asset references in Isaac Sim |
| `yolov8n-seg.pt` and CAN startup copy | 7,071,756 each | Verify matching checksums/source, then consider one licensed download manifest |

The expanded `.gitignore` prevents new build products, caches, engines, recordings
and local credential directories from being added accidentally. It does **not**
remove the tracked files listed above. A future cleanup can untrack approved
generated files in a normal commit without rewriting history. No files were
deleted or untracked in this task.

Logs contain personal/home paths, account/host names and ZED serial identifiers;
screenshots can expose desktop details. Review/redact release copies with owner
approval. A bounded pattern scan of tracked UTF-8 files up to 2 MB found no
private-key, AWS access-key, GitHub-token or quoted credential-assignment matches.
That scan is not a secret audit of Git history, binary files, larger files or
untracked private directories. No credential values were exported. Ignore rules
do not protect secrets already committed in history.

## What this improvement branch changes

| Files | Reason |
|---|---|
| Root README; architecture, installation, evaluation, audit and this document | Explain actual entry points/contracts, historical evidence, reproducibility gaps and approval boundaries |
| Six setup.py files and three resource markers | Make ament package registration explicit instead of relying on colcon fallback |
| Both feature_extractor.py files | Correct default-model label to match the existing call; no model/inference change |
| Both Hybrid package README files | Preserve upstream attribution while distinguishing source facts from unresolved licensing |
| `.gitignore` | Keep future generated/local artifacts out of ordinary adds |
| `tests/`, `tools/` | Reproduce packaging defects, characterize actual logic, expose open safety defects and calculate defensible historical log rates |

No source tree was deduplicated, no hardware dependency was upgraded, and no
motion/steering/brake/CAN or perception-to-control behavior was changed. The
unsafe startup/interface corrections are proposed in the audit for approval.

## Presenting the project in applications

Lead with the integration problem and evidence you can demonstrate:

> Integrated stereo perception, DeepStream tracking and ROS 2 target following
> across Isaac Sim and a CAN-based mobile-robot research workflow; implemented
> image/metadata bridging, resolution-aware 2D/3D association and gesture selection.

For Embedded AI roles, walk through the CPU-to-GStreamer copies, bounded queue,
SDK compatibility investigation and missing measurements you would add. For
Robotics roles, explain target identity, coordinate conventions, asynchronous
messages and why a controller receipt watchdog cannot prove sensor freshness.
For Embedded Software roles, distinguish the Python command mapping from CAN
serialization, units, timing and chassis feedback.

Show an existing simulation recording, the architecture, a short code path and
the offline test output. Attribute upstream algorithms explicitly. Describe
Jetson performance, robust re-identification, physical validation and memory
stability only to the extent supported by recovered report/run evidence. Avoid
“production-ready,” “zero-copy,” “30 FPS end-to-end,” and an invented accuracy or
latency result. Explaining an unresolved defect and its regression test is stronger
evidence of engineering judgment than claiming it has already been solved.

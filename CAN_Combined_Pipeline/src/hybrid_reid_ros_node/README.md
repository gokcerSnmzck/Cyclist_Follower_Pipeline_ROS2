# Hybrid ReID ROS 2 experiment — CAN workspace variant

This is a variant of the [root Hybrid integration](../../../src/hybrid_reid_ros_node/README.md),
derived from [Hybrid ReID](https://github.com/rvxfahim/Hybrid_reID).
Its upstream declares Apache-2.0; the copied revision, notices and conflicting
local license metadata still need reconciliation. See the
[publication review](../../../docs/PUBLICATION.md).

The wrapper defaults to YOLOv8 nano segmentation on CUDA, with DeepSORT and
DINOv2-based identity logic. The detector has an optional TensorRT path, but the
ROS wrapper does not enable it; that path's default export/load filenames also
disagree. This alternative is not validated as a drop-in production backend.
See the [architecture](../../../docs/ARCHITECTURE.md) and
[engineering audit](../../../docs/ENGINEERING_AUDIT.md).

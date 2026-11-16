# Hybrid ReID ROS 2 integration — CAN workspace

The physical-workspace variant of the [Hybrid ROS integration](../../../src/hybrid_reid_ros_node/README.md), publishing tracked detection JSON on `/deepstream/detections` for the fusion pipeline.

The ROS wrapper defaults to YOLOv8 nano segmentation on CUDA, with DeepSORT and DINOv2-based appearance features. The detector implementation includes an optional TensorRT path; the wrapper does not enable that path by default. Use one detection backend at a time.

This integration derives from [Hybrid ReID](https://github.com/rvxfahim/Hybrid_reID). The project contribution is the ROS integration and experimentation; existing upstream, source and model terms remain applicable. See [technical contributions and attribution](../../../docs/TECHNICAL_CONTRIBUTIONS.md), [architecture](../../../docs/ARCHITECTURE.md) and [setup](../../../docs/SETUP.md). The portfolio's main physical measurements belong to the DeepStream deployment.

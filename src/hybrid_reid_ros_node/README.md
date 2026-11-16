# Hybrid ReID ROS 2 integration

An experimental alternative perception backend for the cyclist-following system. The wrapper publishes tracked detection JSON on `/deepstream/detections`, allowing the downstream fusion and following components to consume the same topic used by DeepStream.

The default detector is Ultralytics `yolov8n-seg.pt`. Tracking combines DeepSORT with DINOv2 appearance features (`dinov2_vitb14_reg`, ViT-B/14 with registers); the feature extractor also contains a ResNet50 fallback. Run one detection publisher at a time.

The project contribution is the ROS wrapper and system integration. The underlying approach derives from [Hybrid ReID](https://github.com/rvxfahim/Hybrid_reID), with [deep-sort-realtime](https://github.com/levan92/deep_sort_realtime) and [DINOv2](https://github.com/facebookresearch/dinov2). Existing upstream, source and model terms apply; this README does not replace them or grant a new license.

This is a research alternative; the main portfolio's physical performance results refer to the DeepStream deployment. See [architecture](../../docs/ARCHITECTURE.md), [technical contributions](../../docs/TECHNICAL_CONTRIBUTIONS.md) and [setup](../../docs/SETUP.md).

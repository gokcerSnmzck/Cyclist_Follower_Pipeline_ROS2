# Hybrid ReID ROS 2 experiment

This package wraps components derived from
[Hybrid ReID](https://github.com/rvxfahim/Hybrid_reID), whose upstream repository
declares Apache-2.0. The exact copied revision and required notices still need
recovery; local setup.py and package.xml license declarations are inconsistent.
No relicensing is implied by this documentation.

The default detector is Ultralytics `yolov8n-seg.pt`. The feature extractor calls
`dinov2_vitb14_reg` (ViT-B/14 with registers), with ResNet50 fallback. The wrapper
publishes JSON on `/deepstream/detections` as an alternative to DeepStream.
Do not run both publishers concurrently.

This is an experimental integration: API, ID-allocation, fallback and occlusion
lifecycle defects remain. See the [architecture](../../docs/ARCHITECTURE.md),
[audit A07/A08/A15/A16](../../docs/ENGINEERING_AUDIT.md) and
[provenance review](../../docs/PUBLICATION.md) before runtime use.

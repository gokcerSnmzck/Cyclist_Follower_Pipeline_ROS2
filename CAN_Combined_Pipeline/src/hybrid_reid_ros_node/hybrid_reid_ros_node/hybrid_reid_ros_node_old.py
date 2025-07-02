#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

import json
import cv2
import time

# Tracking pipeline modules
from hybrid_reid_ros_node.feature_extractor import FeatureExtractor
from hybrid_reid_ros_node.hybrid_tracker import HybridTracker
from hybrid_reid_ros_node.yolo_detector import YOLODetector
from hybrid_reid_ros_node.utils import (
    calculate_max_age_from_fps,
    create_mock_detector
)


class HybridReIDNode(Node):
    def __init__(self):
        super().__init__('hybrid_reid_node')

        # Publisher (same format as DeepStream node)
        self.publisher_ = self.create_publisher(String, '/deepstream/detections', 10)

        # Subscriber to image topic
        self.subscription = self.create_subscription(
            Image,
            '/zed/zed_node/left/image_rect_color',
            self.image_callback,
            10
        )
        self.bridge = CvBridge()

        self.get_logger().info("HybridReID ROS2 node initialized, waiting for images...")

        # YOLO detector (fallback if CUDA not available)
        try:
            self.detector = YOLODetector(conf_threshold=0.3, device='cuda')
        except Exception as e:
            self.get_logger().warn(f"Falling back to mock detector: {e}")
            self.detector = create_mock_detector()

        # Tracker setup
        fps = 30  # estimate (could be refined dynamically)
        self.tracker = HybridTracker(
            max_cosine_distance=0.15,
            nn_budget=50,
            max_age=calculate_max_age_from_fps(fps, target_occlusion_seconds=6),
            min_confidence=0.5,
            re_id_interval=1,
            gallery_size=50,
            iou_threshold=0.05
        )

        self.frame_number = 0

    def image_callback(self, msg):
        try:
            frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        except Exception as e:
            self.get_logger().error(f"cv_bridge error: {e}")
            return

        detections = self.detector.detect(frame)
        tracks = self.tracker.update(frame, detections)

        objects = []
        for track in tracks:
            x1, y1, x2, y2, track_id, class_id = track
            # Fallback if class_id is missing or None
            try:
                if class_id is None:
                    raise ValueError("class_id is None")
                class_id_int = int(class_id.item()) if hasattr(class_id, "item") else int(class_id)
            except Exception as e:
                self.get_logger().warn(f"Failed to convert class_id {class_id}, defaulting to 0: {e}")
                class_id_int = 0
        
            bbox = {
                "x": float(x1),
                "y": float(y1),
                "width": float(x2 - x1),
                "height": float(y2 - y1)
            }
            objects.append({
                "class_id": class_id_int,
                "label": "person",
                "confidence": 0.9,  # adjust if detection confidence is available
                "tracking_id": int(track_id),
                "bbox": bbox
            })

        frame_data = {
            "frame_number": self.frame_number,
            "objects": objects
        }
        self.get_logger().info(f"Published JSON: {json.dumps(frame_data)}")
        self.publisher_.publish(String(data=json.dumps(frame_data)))
        self.get_logger().info(f"Published {len(objects)} objects on frame {self.frame_number}")
        self.frame_number += 1


def main(args=None):
    rclpy.init(args=args)
    node = HybridReIDNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down HybridReID node...")
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

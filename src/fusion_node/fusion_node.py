#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Header, String
from geometry_msgs.msg import Point
from zed_msgs.msg import ObjectsStamped
from detection_msgs.msg import TargetPosition
import math
import json


class FusionNode(Node):
    def __init__(self):
        super().__init__('fusion_node')
        self.get_logger().info("FusionNode started.")

        self.target_tracking_id = None  # Will be set dynamically
        self.last_ds_detections = []

        self.publisher_ = self.create_publisher(TargetPosition, '/fused_target', 10)

        self.create_subscription(String, '/deepstream/detections', self.ds_callback, 10)
        self.create_subscription(ObjectsStamped, '/zed/zed_node/obj_det/objects', self.zed_callback, 10)

    def ds_callback(self, msg):
        try:
            data = json.loads(msg.data)
            person_detections = [
                obj for obj in data["objects"]
                if obj["label"].lower() == "person" and obj["tracking_id"] is not None
            ]
            self.last_ds_detections = person_detections

            if self.target_tracking_id is None and person_detections:
                self.target_tracking_id = person_detections[0]["tracking_id"]
                self.get_logger().info(f"Auto-selected target_tracking_id: {self.target_tracking_id}")
        except Exception as e:
            self.get_logger().error(f"Failed to parse DeepStream message: {e}")

    def zed_callback(self, msg):
        self.get_logger().info(f"ZED object count: {len(msg.objects)}")
        
        for zed_obj in msg.objects:
            self.get_logger().info(f"ZED label: {zed_obj.label} (label_id: {zed_obj.label_id})")

            if zed_obj.label.lower() != "person":
                continue

            corners = zed_obj.bounding_box_2d.corners
            if len(corners) != 4:
                continue

            zed_cx = sum(pt.kp[0] for pt in corners) / 4.0
            zed_cy = sum(pt.kp[1] for pt in corners) / 4.0

            match = self.find_best_match(zed_cx, zed_cy)

            self.get_logger().info(f"ZED center: ({zed_cx:.1f}, {zed_cy:.1f})")

            if match is None:
                self.get_logger().warn("No matching DeepStream detection found for this ZED object.")
                continue

            self.get_logger().info(f"Match tracking ID: {match['tracking_id']}, Target: {self.target_tracking_id}")

            if match["tracking_id"] != self.target_tracking_id:
                continue

            self.get_logger().info(f"Best match tracking ID: {match['tracking_id']}")

            fused_msg = TargetPosition()
            fused_msg.header = Header()
            fused_msg.header.stamp = self.get_clock().now().to_msg()
            fused_msg.header.frame_id = msg.header.frame_id

            fused_msg.id = match["tracking_id"]
            fused_msg.class_id = 2  # person
            fused_msg.label = "person"
            fused_msg.confidence = match["confidence"]

            fused_msg.position = Point(
                x=float(zed_obj.position[0]),
                y=float(zed_obj.position[1]),
                z=float(zed_obj.position[2])
            )

            self.publisher_.publish(fused_msg)
            self.get_logger().info(
                f"Published target ID {fused_msg.id}: "
                f"({fused_msg.position.x:.2f}, {fused_msg.position.y:.2f}, {fused_msg.position.z:.2f})"
            )


    def find_best_match(self, zed_cx, zed_cy):
        best_match = None
        min_diff = float('inf')

        # Example camera resolution (adjust to your camera setup)
        image_width = 960
        image_height = 540

        zed_cx_norm = zed_cx / image_width
        zed_cy_norm = zed_cy / image_height

        for det in self.last_ds_detections:
            cx = det["bbox"]["x"] + det["bbox"]["width"] / 2
            cy = det["bbox"]["y"] + det["bbox"]["height"] / 2

            cx_norm = 2 * cx / image_width
            cy_norm = 2 * cy / image_height

            dx = abs(zed_cx_norm - cx_norm)
            dy = abs(zed_cy_norm - cy_norm)

            self.get_logger().info(f"ZED center: ({zed_cx:.1f}, {zed_cy:.1f}), DS center: ({cx:.1f}, {cy:.1f}), dx: {dx:.1f}, dy: {dy:.1f}")

            if dx < 0.1 and dy < 0.1:  # 10% image width/height tolerance
                total_diff = dx + dy
                if total_diff < min_diff:
                    best_match = det
                    min_diff = total_diff

        return best_match



def main(args=None):
    rclpy.init(args=args)
    node = FusionNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down FusionNode")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

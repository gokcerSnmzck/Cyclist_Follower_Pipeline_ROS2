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

        self.last_ds_detections = []

        self.publisher_ = self.create_publisher(TargetPosition, '/fused_target', 10)

        self.create_subscription(
            String, '/detection', self.ds_callback, 10)
        self.create_subscription(
            ObjectsStamped, '/zed2i/obj_det/objects', self.zed_callback, 10)

    def ds_callback(self, msg):
        try:
            data = json.loads(msg.data)
            self.last_ds_detections = data["objects"]
            self.get_logger().info(f"Received {len(self.last_ds_detections)} detections")
        except Exception as e:
            self.get_logger().error(f"Failed to parse detection message: {e}")

    def zed_callback(self, msg):
        self.get_logger().info(f"Received {len(msg.objects)} ZED 3D objects.")
        for zed_obj in msg.objects:
            label_id = zed_obj.label_id
            self.get_logger().info(f"ZED object label_id: {label_id}")

            if label_id != 51:  # Person class
                continue

            corners = zed_obj.bounding_box_2d.corners
            if len(corners) != 4:
                self.get_logger().warn("ZED 2D bounding box does not have 4 corners.")
                continue

            zed_center_x = sum([pt.kp[0] for pt in corners]) / 4.0
            zed_center_y = sum([pt.kp[1] for pt in corners]) / 4.0
            self.get_logger().info(f"ZED center: ({zed_center_x:.2f}, {zed_center_y:.2f})")

            best_match = self.find_best_match(zed_center_x, zed_center_y, label_id)
            if best_match is None:
                self.get_logger().info("No matching DeepStream detection found for ZED object.")
                continue

            fused_msg = TargetPosition()
            fused_msg.header = Header()
            fused_msg.header.stamp = self.get_clock().now().to_msg()
            fused_msg.header.frame_id = msg.header.frame_id

            fused_msg.id = best_match["tracking_id"]
            fused_msg.class_id = best_match["class_id"]
            fused_msg.label = best_match["label"]
            fused_msg.confidence = best_match["confidence"]

            fused_msg.position = Point(
                x=float(zed_obj.position[0]),
                y=float(zed_obj.position[1]),
                z=float(zed_obj.position[2])
            )

            self.publisher_.publish(fused_msg)
            self.get_logger().info(f"Published fused target: ID {fused_msg.id} at ({fused_msg.position.x:.2f}, {fused_msg.position.y:.2f}, {fused_msg.position.z:.2f})")

    def find_best_match(self, zed_cx, zed_cy, zed_label_id):
        best_match = None
        min_dist = float('inf')

        for det in self.last_ds_detections:
            if det["label"].lower() != "person":
                continue

            cx = det["bbox"]["x"] + det["bbox"]["width"] / 2
            cy = det["bbox"]["y"] + det["bbox"]["height"] / 2
            dist = math.hypot(zed_cx - cx, zed_cy - cy)
            self.get_logger().info(f"Checking DS detection center: ({cx:.2f}, {cy:.2f}) for label: {det['label']}")

            if dist < 80.0 and dist < min_dist:
                best_match = det
                min_dist = dist

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
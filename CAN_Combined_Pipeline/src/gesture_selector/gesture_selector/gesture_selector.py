#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from zed_msgs.msg import ObjectsStamped, Object
from std_msgs.msg import Int32, Empty
from geometry_msgs.msg import Point
import math
import time

WRIST_INDEX = 4        # RIGHT_WRIST
SHOULDER_INDEX = 2     # RIGHT_SHOULDER
RAISE_DURATION = 2.0   # seconds

class GestureSelector(Node):
    def __init__(self):
        super().__init__('gesture_selector_node')

        self.subscription = self.create_subscription(
            ObjectsStamped,
            '/zed/zed_node/body_trk/skeletons',
            self.callback,
            10
        )

        self.publisher = self.create_publisher(Int32, '/selected_person_id', 10)
        self.bbox_pub = self.create_publisher(Object, '/selected_person_bbox', 10)

        # New: Reset gesture selector state externally
        self.create_subscription(Empty, '/gesture_selector/reset', self.reset_callback, 10)

        self.state = 'IDLE'
        self.raised_start_time = None
        self.tracked_person_id = None

        self.get_logger().info("Gesture selector node started.")

    def change_state(self, new_state):
        self.get_logger().info(f"State change: {self.state} -> {new_state}")
        self.state = new_state
        self.raised_start_time = None

    def callback(self, msg):
        current_time = self.get_clock().now().nanoseconds / 1e9

        for obj in msg.objects:
            if not obj.skeleton_available:
                continue

            keypoints = obj.skeleton_3d.keypoints
            if len(keypoints) <= max(WRIST_INDEX, SHOULDER_INDEX):
                continue

            wrist = keypoints[WRIST_INDEX].kp
            shoulder = keypoints[SHOULDER_INDEX].kp

            if any(math.isnan(val) for val in wrist + shoulder):
                continue

            person_id = obj.label_id
            wrist_y = wrist[1]
            shoulder_y = shoulder[1]

            if self.state == 'IDLE':
                if wrist_y > shoulder_y + 0.1:
                    self.get_logger().info(f"🙋 Person {person_id} raised hand.")
                    self.tracked_person_id = person_id
                    self.change_state('HAND_RAISED')
                    self.raised_start_time = current_time

            elif self.state == 'HAND_RAISED' and person_id == self.tracked_person_id:
                if wrist_y > shoulder_y + 0.1:
                    if current_time - self.raised_start_time >= RAISE_DURATION:
                        self.get_logger().info(f"✅ Person {person_id} held hand up for {RAISE_DURATION} seconds.")
                        self.publisher.publish(Int32(data=person_id))
                        self.bbox_pub.publish(obj)
                        self.change_state('SELECTED')
                else:
                    self.get_logger().info("❌ Hand lowered too soon. Returning to IDLE.")
                    self.change_state('IDLE')
                    self.tracked_person_id = None

            elif self.state == 'SELECTED':
                # Do nothing — wait for reset
                pass

    def reset_callback(self, _):
        self.get_logger().info("🔄 Gesture selector reset triggered.")
        self.state = 'IDLE'
        self.raised_start_time = None
        self.tracked_person_id = None

def main(args=None):
    rclpy.init(args=args)
    node = GestureSelector()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

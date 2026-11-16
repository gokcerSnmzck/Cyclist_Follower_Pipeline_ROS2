"""Characterization and defect reproductions for both research workflows."""

import json
import unittest
from unittest.mock import patch

from offline_support import (
    TREES, Message, Publisher, Twist, detection, load_class, zed_message, zed_object,
)


def fusion(tree, gesture=False):
    cls = load_class(f"{tree}/fusion_node/fusion_node.py", "FusionNode")
    with patch.dict("os.environ", {"USE_GESTURE_DETECTOR": str(gesture).lower()}):
        return cls()


def follower(tree):
    return load_class(
        f"{tree}/person_follower_pkg/person_follower_pkg/person_follower.py",
        "PersonFollower")()


class FusionTests(unittest.TestCase):
    def test_resolution_transform_matches_full_resolution_zed_to_half_size_ds(self):
        for tree in TREES:
            with self.subTest(tree=tree):
                node = fusion(tree)
                candidate = detection()
                node.last_ds_detections = [candidate]
                self.assertIs(candidate, node.find_best_match(960, 540))
                self.assertIsNone(node.find_best_match(480, 270))

    def test_no_candidates(self):
        for tree in TREES:
            self.assertIsNone(fusion(tree).find_best_match(960, 540))

    def test_gate_is_strict_and_applies_to_both_axes(self):
        for tree in TREES:
            with self.subTest(tree=tree):
                node = fusion(tree)
                node.last_ds_detections = [detection(0, 0)]
                self.assertIsNotNone(node.find_best_match(191.9, 107.9))
                self.assertIsNone(node.find_best_match(192, 0))
                self.assertIsNone(node.find_best_match(0, 108))

    def test_nearest_center_and_first_in_tie(self):
        for tree in TREES:
            node = fusion(tree)
            first, second = detection(450, 270, 1), detection(480, 270, 2)
            node.last_ds_detections = [first, second]
            self.assertIs(second, node.find_best_match(960, 540))
            node.last_ds_detections = [second, detection(track_id=3)]
            self.assertIs(second, node.find_best_match(960, 540))

    def test_person_filter_accepts_id_zero_and_rejects_missing_id(self):
        for tree in TREES:
            node = fusion(tree)
            node.ds_callback(Message(data=json.dumps({"objects": [
                detection(track_id=0, label="PERSON"),
                detection(track_id=None), detection(label="bicycle")]})))
            self.assertEqual([0], [d["tracking_id"] for d in node.last_ds_detections])

    def test_explicit_empty_detection_message_clears_cache(self):
        for tree in TREES:
            node = fusion(tree)
            node.last_ds_detections = [detection()]
            node.ds_callback(Message(data='{"objects":[]}'))
            self.assertEqual([], node.last_ds_detections)

    def test_malformed_json_currently_preserves_cache(self):
        for tree in TREES:
            node = fusion(tree)
            node.last_ds_detections = [detection()]
            node.ds_callback(Message(data="{"))
            self.assertEqual(1, len(node.last_ds_detections))

    def test_target_id_lock_skips_other_id(self):
        for tree in TREES:
            node = fusion(tree)
            node.last_ds_detections = [detection(track_id=7)]
            node.zed_callback(zed_message(zed_object()))
            node.last_ds_detections = [detection(track_id=8)]
            node.zed_callback(zed_message(zed_object()))
            self.assertEqual([7], [m.id for m in node.publisher_.messages])

    def test_reproduces_stale_cache_republished_with_fresh_stamp(self):
        for tree in TREES:
            node = fusion(tree)
            node.last_ds_detections = [detection()]
            node.zed_callback(zed_message(zed_object()))
            node.now_ns = 60 * 10**9
            node.zed_callback(zed_message(zed_object()))
            self.assertEqual(2, len(node.publisher_.messages))
            self.assertEqual(60, node.publisher_.messages[-1].header.stamp.sec)

    def test_reproduces_two_zed_people_reusing_one_detection(self):
        for tree in TREES:
            node = fusion(tree)
            node.last_ds_detections = [detection()]
            node.zed_callback(zed_message(zed_object(), zed_object(970, 540, 2)))
            self.assertEqual([7, 7], [m.id for m in node.publisher_.messages])

    def test_root_and_can_gesture_reset_differ_when_target_still_present(self):
        for tree in TREES:
            node = fusion(tree, gesture=True)
            node.last_ds_detections = [detection()]
            selected = zed_object()
            node.selected_callback(selected)
            node.zed_callback(zed_message(selected))
            node.zed_callback(zed_message(zed_object(label_id=2), selected))
            self.assertEqual(tree == "src", bool(node.reset_pub.messages))

    @unittest.expectedFailure
    def test_A01_expired_detections_should_not_publish_target(self):
        node = fusion("src")
        node.ds_callback(Message(data=json.dumps({"objects": [detection()]})))
        node.now_ns = 60 * 10**9
        node.zed_callback(zed_message(zed_object()))
        self.assertEqual([], node.publisher_.messages)


class FollowerTests(unittest.TestCase):
    def test_speed_limits_and_minimum_distance(self):
        for tree in TREES:
            for x, y, linear, angular in [(1.5, 0, 0, 0), (1.7, 0.2, 0.2, 0.2),
                                           (20, 10, 0.4, 0.8), (2, -10, 0.4, -0.8)]:
                with self.subTest(tree=tree, x=x, y=y):
                    node = follower(tree)
                    node.target_callback(Message(id=7, position=Message(x=x, y=y)))
                    cmd = node.cmd_pub.messages[-1]
                    self.assertAlmostEqual(linear, cmd.linear.x)
                    self.assertAlmostEqual(angular, cmd.angular.z)

    def test_watchdog_stops_once_strictly_after_timeout(self):
        for tree in TREES:
            node = follower(tree)
            node.target_callback(Message(id=7, position=Message(x=2, y=0)))
            node.now_ns = 10**9
            node.watchdog_callback()
            self.assertEqual(1, len(node.cmd_pub.messages))
            node.now_ns += 1
            node.watchdog_callback()
            node.watchdog_callback()
            self.assertEqual(2, len(node.cmd_pub.messages))
            self.assertEqual(0, node.cmd_pub.messages[-1].linear.x)

    def test_startup_and_invalid_position_do_not_publish_stop(self):
        for tree in TREES:
            node = follower(tree)
            node.now_ns = 2 * 10**9
            node.watchdog_callback()
            node.target_callback(Message(id=7, position=Message(x=0.1, y=0)))
            self.assertEqual([], node.cmd_pub.messages)

    def test_reacquisition_after_timeout(self):
        for tree in TREES:
            node = follower(tree)
            msg = Message(id=7, position=Message(x=2, y=0))
            node.target_callback(msg)
            node.now_ns = 2 * 10**9
            node.watchdog_callback()
            node.target_callback(msg)
            self.assertFalse(node.target_lost)
            self.assertEqual(0.4, node.cmd_pub.messages[-1].linear.x)

    def test_workflow_topics_are_distinct(self):
        self.assertIn('/cmd_vel', follower('src').publishers)
        self.assertIn('/cmdvel', follower('CAN_Combined_Pipeline/src').publishers)

    @unittest.expectedFailure
    def test_A02_nonfinite_target_should_not_produce_motion(self):
        node = follower("src")
        node.target_callback(Message(id=7, position=Message(x=2, y=float("nan"))))
        self.assertTrue(all(m.linear.x == 0 and m.angular.z == 0
                            for m in node.cmd_pub.messages))


class CANAdapterTests(unittest.TestCase):
    def test_existing_scaling_gear_and_brake_without_can_transport(self):
        cls = load_class(
            "CAN_Combined_Pipeline/src/cmd_vel_to_can_node/"
            "cmd_vel_to_can_node/cmd_vel_to_can_node.py", "CmdVelToCAN")
        for v, w, speed, steering, gear, brake in [
                (0.4, 0.8, 4.0, 32.0, 4, 0), (0, 0, 0, 0, 3, 1),
                (0, 0.2, 0, 8, 4, 0)]:
            node = cls()
            msg = Twist()
            msg.linear.x, msg.angular.z = v, w
            node.cmdvel_callback(msg)
            out = node.publisher_.messages[-1]
            self.assertEqual((speed, steering, gear, brake), (
                out.ctrl_cmd_velocity, out.ctrl_cmd_steering,
                out.ctrl_cmd_gear, out.ctrl_cmd_brake))


class PerceptionBoundaryTests(unittest.TestCase):
    def test_deepstream_empty_frame_does_not_publish_clear_message(self):
        frame = Message(frame_num=1, obj_meta_list=None)
        batch = Message(frame_meta_list=Message(data=frame, next=None))
        gst = Message(PadProbeReturn=Message(OK="ok"))
        pyds = Message(gst_buffer_get_nvds_batch_meta=lambda _: batch,
                       NvDsFrameMeta=Message(cast=lambda value: value))
        for tree in TREES:
            cls = load_class(
                f"{tree}/deepstream_ros_node_json/deepstream_ros_node_json/"
                "deepstream_ros_node_json.py", "DeepStreamROSNode", Gst=gst,
                pyds=pyds, rclpy=Message(ok=lambda: True))
            node = cls.__new__(cls)  # Never construct a GStreamer pipeline.
            node.publisher_ = Publisher()
            self.assertEqual("ok", node.osd_sink_pad_buffer_probe(
                None, Message(get_buffer=lambda: 1), None))
            self.assertEqual([], node.publisher_.messages)

    def test_gesture_hold_selection_and_reset(self):
        for tree in TREES:
            cls = load_class(
                f"{tree}/gesture_selector/gesture_selector/gesture_selector.py",
                "GestureSelector", WRIST_INDEX=4, SHOULDER_INDEX=2, RAISE_DURATION=2.0)
            node = cls()
            obj = zed_object()
            obj.skeleton_available = True
            points = [Message(kp=[0.0, 0.0, 0.0]) for _ in range(5)]
            points[4].kp[1] = 0.3
            obj.skeleton_3d = Message(keypoints=points)
            node.callback(zed_message(obj))
            self.assertEqual("HAND_RAISED", node.state)
            node.now_ns = 2 * 10**9
            node.callback(zed_message(obj))
            self.assertEqual("SELECTED", node.state)
            self.assertEqual(1, node.publisher.messages[0].data)
            node.reset_callback(None)
            self.assertEqual("IDLE", node.state)


if __name__ == "__main__":
    unittest.main()

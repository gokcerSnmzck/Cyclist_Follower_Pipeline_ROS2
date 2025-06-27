#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, PoseStamped
from nav_msgs.msg import Odometry, Path
from detection_msgs.msg import TargetPosition
from collections import deque
import math
from scipy.spatial.transform import Rotation as R
import tf2_ros
from tf2_geometry_msgs import do_transform_pose

class TrajectoryFollower(Node):
    def __init__(self):
        super().__init__('trajectory_follower')

        # Subscriptions and publishers
        self.target_sub = self.create_subscription(TargetPosition, '/fused_target', self.target_callback, 10)
        self.odom_sub = self.create_subscription(Odometry, '/zed/zed_node/odom', self.odom_callback, 10)
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.path_pub = self.create_publisher(Path, '/tracked_path', 10)

        # TF buffer and listener
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)

        # Parameters
        self.min_distance = 1.0
        self.max_linear_speed = 0.4
        self.max_angular_speed = 0.8
        self.lookahead_distance = 0.5

        self.path_buffer = deque(maxlen=50)  # Store last 50 positions
        self.current_pose = (0.0, 0.0, 0.0)  # (x, y, yaw)

        self.get_logger().info("TrajectoryFollower node initialized.")

        # Wait for initial TFs to be available
        self.create_timer(1.0, self.check_tf_ready)

    def odom_callback(self, msg: Odometry):
        pos = msg.pose.pose.position
        ori = msg.pose.pose.orientation
        rot = R.from_quat([ori.x, ori.y, ori.z, ori.w])
        _, _, yaw = rot.as_euler('xyz')
        self.current_pose = (pos.x, pos.y, yaw)

    def target_callback(self, msg: TargetPosition):
        if msg.position.x <= 0.1:
            self.get_logger().warn("Invalid or too close target position. Skipping.")
            return

        # Transform target position to odom frame
        target_pose = PoseStamped()
        target_pose.header.stamp = self.get_clock().now().to_msg()
        target_pose.header.frame_id = 'base_link'
        target_pose.pose.position.x = msg.position.x
        target_pose.pose.position.y = msg.position.y
        target_pose.pose.position.z = msg.position.z
        target_pose.pose.orientation.w = 1.0  # Neutral orientation

        try:
            transform = self.tf_buffer.lookup_transform('odom', 'base_link', rclpy.time.Time(), timeout=rclpy.duration.Duration(seconds=0.5))
            transformed_pose = do_transform_pose(target_pose, transform)
            tx = transformed_pose.pose.position.x
            ty = transformed_pose.pose.position.y
            self.path_buffer.append((tx, ty))
        except Exception as e:
            self.get_logger().error(f"TF transform failed: {e}")
            return

        # Smooth the path (optional)
        smoothed_path = self.smooth_path(list(self.path_buffer))

        # Visualize path
        self.publish_path(smoothed_path)

        # Compute control
        linear, angular = self.pure_pursuit_control(self.current_pose, smoothed_path)

        twist = Twist()
        twist.linear.x = linear
        twist.angular.z = angular

        self.cmd_pub.publish(twist)
        self.get_logger().info(f"Tracking path: linear={linear:.2f}, angular={angular:.2f}")

    def pure_pursuit_control(self, current_pose, path):
        cx, cy, cyaw = current_pose
        for px, py in path:
            dx = px - cx
            dy = py - cy
            distance = math.hypot(dx, dy)
            if distance >= self.lookahead_distance:
                angle_to_goal = math.atan2(dy, dx)
                alpha = angle_to_goal - cyaw
                linear = min(self.max_linear_speed, distance)
                angular = 2.0 * math.sin(alpha) / self.lookahead_distance
                angular = max(-self.max_angular_speed, min(self.max_angular_speed, angular))
                return linear, angular
        return 0.0, 0.0

    def smooth_path(self, path):
        if len(path) < 3:
            return path
        smoothed = []
        for i in range(1, len(path)-1):
            x_avg = (path[i-1][0] + path[i][0] + path[i+1][0]) / 3.0
            y_avg = (path[i-1][1] + path[i][1] + path[i+1][1]) / 3.0
            smoothed.append((x_avg, y_avg))
        return smoothed

    def publish_path(self, path):
        ros_path = Path()
        ros_path.header.stamp = self.get_clock().now().to_msg()
        ros_path.header.frame_id = 'odom'

        for x, y in path:
            pose = PoseStamped()
            pose.header.stamp = self.get_clock().now().to_msg()
            pose.header.frame_id = 'odom'
            pose.pose.position.x = x
            pose.pose.position.y = y
            pose.pose.orientation.w = 1.0
            ros_path.poses.append(pose)

        self.path_pub.publish(ros_path)

    def check_tf_ready(self):
        try:
            if self.tf_buffer.can_transform('odom', 'base_link', rclpy.time.Time()):
                self.get_logger().info("TF transform between 'odom' and 'base_link' is now available.")
            else:
                self.get_logger().warn("TF transform between 'odom' and 'base_link' is NOT available yet.")
        except Exception as e:
            self.get_logger().warn(f"Initial TF check failed: {e}")


def main(args=None):
    rclpy.init(args=args)
    node = TrajectoryFollower()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

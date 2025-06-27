#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from detection_msgs.msg import TargetPosition
from geometry_msgs.msg import Twist


class PersonFollower(Node):
    def __init__(self):
        super().__init__('person_follower')
        self.target_sub = self.create_subscription(TargetPosition, '/fused_target', self.target_callback, 10)
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        # Parameters
        self.target_id = None     # If you only want to follow a specific person
        self.min_distance = 1.5   # meters
        self.max_linear_speed = 0.4
        self.max_angular_speed = 0.8

        self.get_logger().info("PersonFollower node initialized.")

    def target_callback(self, msg: TargetPosition):
        # Optional: only follow specific ID
        if self.target_id is not None and msg.id != self.target_id:
            return

        x = msg.position.x  # forward/back
        y = msg.position.y  # left/right

        if x <= 0.1:
            self.get_logger().warn("Invalid or too close target position. Skipping.")
            return

        # Control logic
        linear = min(self.max_linear_speed, max(0.0, x - self.min_distance))
        angular = max(-self.max_angular_speed, min(self.max_angular_speed, y))

        twist = Twist()
        twist.linear.x = linear
        twist.angular.z = angular

        self.cmd_pub.publish(twist)

        self.get_logger().info(f"Following person ID {msg.id}: linear={linear:.2f} m/s, angular={angular:.2f} rad/s")
        self.get_logger().info(f"Target x={x:.2f}, y={y:.2f}")


def main(args=None):
    rclpy.init(args=args)
    node = PersonFollower()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

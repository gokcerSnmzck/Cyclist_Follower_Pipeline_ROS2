#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import socket
import struct
import os
import fcntl

CAN_INTERFACE = 'can0'
LEFT_MOTOR_ID = 0x141
RIGHT_MOTOR_ID = 0x142

class CmdVelToCAN(Node):
    def __init__(self):
        super().__init__('cmd_vel_to_can')

        # CAN setup
        self.socket = socket.socket(socket.PF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
        ifr = struct.pack('256s', bytes(CAN_INTERFACE[:15], 'utf-8'))
        try:
            if_index = struct.unpack('i', fcntl.ioctl(self.socket, 0x8933, ifr)[16:20])[0]
            self.socket.bind((CAN_INTERFACE,))
        except Exception as e:
            self.get_logger().error(f"Failed to bind CAN interface: {e}")
            raise

        # Subscribe to /cmd_vel
        self.subscription = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_vel_callback,
            10
        )

        # Robot geometry parameters
        self.wheel_base = 0.5     # meters
        self.wheel_radius = 0.1   # meters

        self.get_logger().info("cmd_vel_to_can node initialized.")

    def cmd_vel_callback(self, msg: Twist):
        linear = msg.linear.x
        angular = msg.angular.z

        v_left = linear - angular * self.wheel_base / 2.0
        v_right = linear + angular * self.wheel_base / 2.0

        rpm_left = int(v_left * 60.0 / (2 * 3.1416 * self.wheel_radius))
        rpm_right = int(v_right * 60.0 / (2 * 3.1416 * self.wheel_radius))

        self.send_can_command(LEFT_MOTOR_ID, rpm_left)
        self.send_can_command(RIGHT_MOTOR_ID, rpm_right)

        self.get_logger().info(
            f"cmd_vel: linear={linear:.2f}, angular={angular:.2f} -> rpm L={rpm_left}, R={rpm_right}"
        )

    # def send_can_command(self, can_id: int, rpm: int):
    #     frame = struct.pack(
    #         "<IB3xB4s",
    #         can_id,  # CAN ID
    #         8,       # DLC
    #         0xA2,    # Control command: set velocity
    #         rpm.to_bytes(4, byteorder='little', signed=True)
    #     )
    #     try:
    #         self.socket.send(frame)
    #     except OSError as e:
    #         self.get_logger().error(f"Failed to send CAN frame: {e}")

    def send_can_command(self, can_id: int, rpm: int):
        # CAN frame: 4-byte ID + 1-byte DLC + 3 bytes padding + 8-byte data
        can_dlc = 8
        command = 0xA2
        data = bytearray(8)
        data[0] = command
        data[1:5] = rpm.to_bytes(4, byteorder='little', signed=True)

        can_frame_fmt = "=IB3x8s"  # standard struct for CAN frame
        frame = struct.pack(can_frame_fmt, can_id, can_dlc, bytes(data))

        try:
            self.socket.send(frame)
        except OSError as e:
            self.get_logger().error(f"Failed to send CAN frame: {e}")


def main(args=None):
    rclpy.init(args=args)
    node = CmdVelToCAN()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.socket.close()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
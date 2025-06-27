#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import socket
import struct
import os
import fcntl

CAN_INTERFACE = 'can0'
CAN_ID_CTRL_CMD = 0x98C4D2D0  # 29-bit extended CAN ID

class CmdVelToCAN(Node):
    def __init__(self):
        super().__init__('cmd_vel_to_can')

        # Set up CAN socket
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

        # Robot parameters
        self.frame_counter = 0

        self.get_logger().info("cmd_vel_to_can node initialized.")

    def cmd_vel_callback(self, msg: Twist):
        linear = msg.linear.x      # m/s
        angular = msg.angular.z    # rad/s

        # Example conversion (scale based on your hardware spec)
        velocity = int(linear * 1000) & 0xFFFF     # 16-bit velocity
        angular_val = int(angular * 1000) & 0xFFFF # 16-bit angular steering
        gear = 1 if linear >= 0 else 2             # 1 = forward, 2 = reverse
        brake = 0                                   # No brake applied

        self.send_ctrl_cmd(gear, velocity, angular_val, brake)

    def send_ctrl_cmd(self, gear, velocity, angular, brake):
        frame = bytearray(8)

        # Byte 0: Gear (4 bits) + low 4 bits of velocity
        frame[0] = ((gear & 0x0F) << 4) | ((velocity >> 0) & 0x0F)

        # Byte 1: Velocity bits [4–11]
        frame[1] = (velocity >> 4) & 0xFF

        # Byte 2: Velocity bits [12–15] + low 4 bits of angular
        frame[2] = ((velocity >> 12) & 0x0F) | ((angular & 0x0F) << 4)

        # Byte 3: Angular bits [4–11]
        frame[3] = (angular >> 4) & 0xFF

        # Byte 4: Brake (4 bits) + angular bits [12–15]
        frame[4] = ((brake & 0x0F) << 4) | ((angular >> 12) & 0x0F)

        # Byte 5: Brake bits [4–7]
        frame[5] = (brake >> 4) & 0x0F

        # Byte 6: Frame count (0–15) << 4
        frame[6] = (self.frame_counter & 0x0F) << 4
        self.frame_counter = (self.frame_counter + 1) % 16

        # Byte 7: XOR checksum of bytes 0–6
        checksum = 0
        for b in frame[:7]:
            checksum ^= b
        frame[7] = checksum

        # Build CAN frame: 29-bit CAN ID with 8 data bytes
        can_id_with_flags = CAN_ID_CTRL_CMD | socket.CAN_EFF_FLAG  # EFF flag for 29-bit ID

        try:
            self.socket.send(struct.pack("<IB3x8s", can_id_with_flags, 8, frame))
            self.get_logger().info(f"Sent CAN frame: {frame.hex()}")
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

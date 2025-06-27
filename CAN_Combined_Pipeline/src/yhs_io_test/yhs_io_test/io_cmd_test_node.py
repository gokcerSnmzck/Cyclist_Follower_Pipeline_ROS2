#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from yhs_can_interfaces.msg import IoCmd
import time


class IoCmdTestNode(Node):
    """
    A test node for yhs_can_interfaces/msg/IoCmd
    
    This node publishes various IoCmd messages to test all the features:
    - io_cmd_enable: bool - Enable/disable IO commands
    - io_cmd_upper_beam_headlamp: bool - Control upper beam headlamp
    - io_cmd_turn_lamp: uint8 - Control turn signals (0=off, 1=left, 2=right)
    - io_cmd_speaker: bool - Control speaker
    """
    
    def __init__(self):
        super().__init__('io_cmd_test_node')
        
        # Create publisher for IoCmd messages
        self.io_cmd_publisher = self.create_publisher(
            IoCmd,
            'io_cmd',
            10
        )
        
        # Create timer for periodic testing
        self.timer = self.create_timer(2.0, self.publish_test_commands)
        
        # Test sequence counter
        self.test_sequence = 0
        
        self.get_logger().info('IoCmd Test Node started!')
        self.get_logger().info('Publishing IoCmd messages on topic: io_cmd')
        self.get_logger().info('Turn lamp values: 0=off, 1=left, 2=right')
        
    def publish_test_commands(self):
        """Publish different test commands in sequence"""
        msg = IoCmd()
        
        # Cycle through different test scenarios
        if self.test_sequence == 0:
            # Test 1: Enable with left turn signal
            msg.io_cmd_enable = True
            msg.io_cmd_upper_beam_headlamp = False
            msg.io_cmd_turn_lamp = 1  # Left turn
            msg.io_cmd_speaker = False
            self.get_logger().info('Test 1: Enable=True, Headlamp=False, Turn=Left(1), Speaker=False')
            
        elif self.test_sequence == 1:
            # Test 2: Enable with right turn signal and headlamp
            msg.io_cmd_enable = True
            msg.io_cmd_upper_beam_headlamp = True
            msg.io_cmd_turn_lamp = 2  # Right turn
            msg.io_cmd_speaker = False
            self.get_logger().info('Test 2: Enable=True, Headlamp=True, Turn=Right(2), Speaker=False')
            
        elif self.test_sequence == 2:
            # Test 3: Enable with speaker and no turn signals
            msg.io_cmd_enable = True
            msg.io_cmd_upper_beam_headlamp = False
            msg.io_cmd_turn_lamp = 0  # No turn signal
            msg.io_cmd_speaker = True
            self.get_logger().info('Test 3: Enable=True, Headlamp=False, Turn=Off(0), Speaker=True')
            
        elif self.test_sequence == 3:
            # Test 4: All features enabled
            msg.io_cmd_enable = True
            msg.io_cmd_upper_beam_headlamp = True
            msg.io_cmd_turn_lamp = 1  # Left turn
            msg.io_cmd_speaker = True
            self.get_logger().info('Test 4: Enable=True, Headlamp=True, Turn=Left(1), Speaker=True')
            
        elif self.test_sequence == 4:
            # Test 5: All disabled
            msg.io_cmd_enable = False
            msg.io_cmd_upper_beam_headlamp = False
            msg.io_cmd_turn_lamp = 0  # No turn signal
            msg.io_cmd_speaker = False
            self.get_logger().info('Test 5: Enable=False, Headlamp=False, Turn=Off(0), Speaker=False')
            
        # Publish the message
        self.io_cmd_publisher.publish(msg)
        
        # Advance to next test (cycle through 0-4)
        self.test_sequence = (self.test_sequence + 1) % 5


def main(args=None):
    rclpy.init(args=args)
    
    node = IoCmdTestNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Shutting down IoCmd Test Node...')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

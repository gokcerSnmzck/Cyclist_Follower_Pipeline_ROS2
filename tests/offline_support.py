"""Load actual class bodies with in-memory ROS substitutes; never start DDS."""

import ast
import json
import math
import os
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
TREES = ("src", "CAN_Combined_Pipeline/src")


class Message(SimpleNamespace):
    pass


class Twist:
    def __init__(self):
        self.linear = Message(x=0.0, y=0.0, z=0.0)
        self.angular = Message(x=0.0, y=0.0, z=0.0)


class Publisher:
    def __init__(self):
        self.messages = []

    def publish(self, message):
        self.messages.append(message)


class Time:
    def __init__(self, nanoseconds=0):
        self.nanoseconds = nanoseconds

    def __sub__(self, other):
        return Time(self.nanoseconds - other.nanoseconds)

    def to_msg(self):
        return Message(sec=self.nanoseconds // 10**9)


class Node:
    def __init__(self, name):
        self.now_ns = 0
        self.publishers = {}

    def create_publisher(self, kind, topic, depth):
        publisher = Publisher()
        self.publishers[topic] = publisher
        return publisher

    def create_subscription(self, *args):
        return None

    def create_timer(self, *args):
        return None

    def get_clock(self):
        return Message(now=lambda: Time(self.now_ns))

    def get_logger(self):
        return Message(**{name: lambda *args: None for name in
                          ("info", "warn", "error", "debug")})


def load_class(relative_path, name, **extra_globals):
    """Compile the unchanged class AST, excluding module imports/main side effects.

    Tests exercise Python logic only. Stub messages do not validate ROS field
    types/ranges, serialization, executor scheduling or QoS compatibility.
    """
    path = ROOT / relative_path
    tree = ast.parse(path.read_text(), filename=str(path))
    definition = next(n for n in tree.body
                      if isinstance(n, ast.ClassDef) and n.name == name)
    future = ast.ImportFrom(module="__future__",
                            names=[ast.alias(name="annotations")], level=0)
    module = ast.fix_missing_locations(ast.Module(
        body=[future, definition], type_ignores=[]))
    namespace = dict(Node=Node, json=json, math=math, os=os, Twist=Twist)
    namespace.update({key: Message for key in (
        "TargetPosition", "Point", "Header", "Empty", "String", "Object",
        "ObjectsStamped", "Int32", "CtrlCmd")})
    namespace.update(extra_globals)
    exec(compile(module, str(path), "exec"), namespace)
    return namespace[name]


def detection(cx=480.0, cy=270.0, track_id=7, label="person"):
    return dict(label=label, tracking_id=track_id, confidence=0.9,
                bbox=dict(x=cx - 10, y=cy - 20, width=20, height=40))


def zed_object(cx=960.0, cy=540.0, label_id=1):
    corners = [Message(kp=[cx + dx, cy + dy])
               for dx, dy in ((-20, -40), (20, -40), (20, 40), (-20, 40))]
    return Message(label="person", label_id=label_id,
                   bounding_box_2d=Message(corners=corners),
                   position=[2.0, 0.1, 0.0])


def zed_message(*objects):
    return Message(objects=list(objects), header=Message(frame_id="camera"))

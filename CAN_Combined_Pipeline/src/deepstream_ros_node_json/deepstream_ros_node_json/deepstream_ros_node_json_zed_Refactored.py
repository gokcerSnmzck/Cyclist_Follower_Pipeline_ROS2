from rclpy.node import Node
import rclpy
import gi
import json
import pyds
from queue import Queue, Full, Empty
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import numpy as np
import cv2

gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib


class DeepStreamROSNode(Node):
    def __init__(self):
        super().__init__('deepstream_json_node')
        self.declare_parameter('enable_visualization', False)
        self.enable_visualization = self.get_parameter('enable_visualization').get_parameter_value().bool_value
        Gst.init(None)

        self.publisher_ = self.create_publisher(String, '/deepstream/detections', 10)
        self.bridge = CvBridge()
        self.frame_queue = Queue(maxsize=5)

        self.pipeline = Gst.Pipeline.new("deepstream-pipeline")

        # Create GStreamer elements
        self.source = Gst.ElementFactory.make("appsrc", "ros_appsrc")
        self.vidconvsrc = Gst.ElementFactory.make("videoconvert", "convertor_src1")
        self.caps_nv12 = Gst.ElementFactory.make("capsfilter", "caps_nv12")
        self.nvvidconvsrc = Gst.ElementFactory.make("nvvideoconvert", "convertor_src2")
        self.streammux = Gst.ElementFactory.make("nvstreammux", "streammux")
        self.pgie = Gst.ElementFactory.make("nvinfer", "primary-inference")
        self.tracker = Gst.ElementFactory.make("nvtracker", "tracker")
        self.nvvidconv = Gst.ElementFactory.make("nvvideoconvert", "convertor")
        self.nvosd = Gst.ElementFactory.make("nvdsosd", "onscreendisplay")
        self.sink = Gst.ElementFactory.make("nveglglessink" if self.enable_visualization else "fakesink", "nvvideo-renderer")

        # Set properties
        self.source.set_property("caps", Gst.Caps.from_string("video/x-raw,format=BGRA,width=960,height=540,framerate=30/1"))
        self.source.set_property("is-live", True)
        self.source.set_property("do-timestamp", True)
        self.source.set_property("block", False)
        self.source.connect("need-data", self.on_need_data)

        self.caps_nv12.set_property("caps", Gst.Caps.from_string("video/x-raw,format=NV12"))
        self.streammux.set_property("width", 960)
        self.streammux.set_property("height", 540)
        self.streammux.set_property("batch-size", 1)
        self.streammux.set_property("batched-push-timeout", 40000)
        self.streammux.set_property("live-source", 1)

        self.pgie.set_property("config-file-path", "/home/gokcer/DeepStream-Yolo/config_infer_primary_yolo11.txt")
        self.tracker.set_property("ll-lib-file", "/opt/nvidia/deepstream/deepstream/lib/libnvds_nvmultiobjecttracker.so")
        self.tracker.set_property("ll-config-file", "/home/gokcer/DeepStream-Yolo/config_tracker_NvDCF_perf.yml")
        self.sink.set_property("sync", False)

        # Add elements to pipeline
        for elem in [self.source, self.vidconvsrc, self.caps_nv12, self.nvvidconvsrc, self.streammux, self.pgie,
                     self.tracker, self.nvvidconv, self.nvosd, self.sink]:
            if not elem:
                raise RuntimeError("Failed to create one of the GStreamer elements.")
            self.pipeline.add(elem)

        # Link elements
        if not self.source.link(self.vidconvsrc):
            raise RuntimeError("Failed to link source -> vidconvsrc")
        if not self.vidconvsrc.link(self.caps_nv12):
            raise RuntimeError("Failed to link vidconvsrc -> caps_nv12")
        if not self.caps_nv12.link(self.nvvidconvsrc):
            raise RuntimeError("Failed to link caps_nv12 -> nvvidconvsrc")

        srcpad = self.nvvidconvsrc.get_static_pad("src")
        sinkpad = self.streammux.get_request_pad("sink_0")
        if not srcpad or not sinkpad or srcpad.link(sinkpad) != Gst.PadLinkReturn.OK:
            raise RuntimeError("Failed to link nvvidconvsrc -> streammux")

        if not self.streammux.link(self.pgie):
            raise RuntimeError("Failed to link streammux -> pgie")
        if not self.pgie.link(self.tracker):
            raise RuntimeError("Failed to link pgie -> tracker")
        if not self.tracker.link(self.nvvidconv):
            raise RuntimeError("Failed to link tracker -> nvvidconv")
        if not self.nvvidconv.link(self.nvosd):
            raise RuntimeError("Failed to link nvvidconv -> nvosd")
        if not self.nvosd.link(self.sink):
            raise RuntimeError("Failed to link nvosd -> sink")

        osd_sink_pad = self.nvosd.get_static_pad("sink")
        if osd_sink_pad:
            osd_sink_pad.add_probe(Gst.PadProbeType.BUFFER, self.osd_sink_pad_buffer_probe, 0)

        self.subscription = self.create_subscription(Image, '/zed/zed_node/left/image_rect_color', self.ros_image_callback, 10)
        self.pipeline.set_state(Gst.State.PLAYING)
        self.bus_timer = self.create_timer(0.1, self.poll_gst_bus)

    def ros_image_callback(self, msg):
        if not rclpy.ok():
            return
        try:
            frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')
            if msg.encoding == "mono8":
                frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGRA)
            elif msg.encoding == "bgr8":
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
            elif msg.encoding == "rgb8":
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGRA)
            elif msg.encoding != "bgra8":
                self.get_logger().error(f"Unsupported image encoding: {msg.encoding}")
                return
            frame = cv2.resize(frame, (960, 540))
            frame = np.ascontiguousarray(frame)
            try:
                self.frame_queue.put_nowait(frame)
            except Full:
                self.frame_queue.get_nowait()
                self.frame_queue.put_nowait(frame)
        except Exception as e:
            self.get_logger().error(f"Image callback error: {e}")

    def on_need_data(self, src, length):
        import time
        try:
            frame = self.frame_queue.get(timeout=0.05)
            data = frame.tobytes()
            buf = Gst.Buffer.new_allocate(None, len(data), None)
            buf.fill(0, data)
            buf.pts = buf.dts = Gst.util_get_timestamp()
            buf.duration = Gst.util_uint64_scale_int(1, Gst.SECOND, 30)
            src.emit("push-buffer", buf)
        except Empty:
            self.get_logger().debug("No frame available for appsrc.")
        except Exception as e:
            self.get_logger().error(f"on_need_data error: {e}")

    def osd_sink_pad_buffer_probe(self, pad, info, u_data):
        buffer = info.get_buffer()
        if not buffer:
            return Gst.PadProbeReturn.OK
        batch_meta = pyds.gst_buffer_get_nvds_batch_meta(hash(buffer))
        if not batch_meta:
            return Gst.PadProbeReturn.OK

        l_frame = batch_meta.frame_meta_list
        while l_frame:
            frame_meta = pyds.NvDsFrameMeta.cast(l_frame.data)
            objects = []
            l_obj = frame_meta.obj_meta_list
            while l_obj:
                obj_meta = pyds.NvDsObjectMeta.cast(l_obj.data)
                objects.append({
                    "class_id": 0,
                    "label": obj_meta.obj_label,
                    "confidence": obj_meta.confidence,
                    "tracking_id": obj_meta.object_id,
                    "bbox": {
                        "x": obj_meta.rect_params.left,
                        "y": obj_meta.rect_params.top,
                        "width": obj_meta.rect_params.width,
                        "height": obj_meta.rect_params.height
                    }
                })
                try:
                    l_obj = l_obj.next
                except StopIteration:
                    break
            if objects and rclpy.ok():
                frame_data = {
                    "frame_number": frame_meta.frame_num,
                    "objects": objects
                }
                json_msg = json.dumps(frame_data, separators=(',', ':'))
                self.publisher_.publish(String(data=json_msg))
            try:
                l_frame = l_frame.next
            except StopIteration:
                break
        return Gst.PadProbeReturn.OK

    def poll_gst_bus(self):
        msg = self.pipeline.get_bus().pop_filtered(Gst.MessageType.ERROR | Gst.MessageType.EOS)
        if not msg:
            return
        t = msg.type
        if t == Gst.MessageType.EOS:
            self.get_logger().warn("GStreamer: End of stream.")
            self.pipeline.set_state(Gst.State.NULL)
        elif t == Gst.MessageType.ERROR:
            err, dbg = msg.parse_error()
            self.get_logger().error(f"GStreamer Error: {err.message}, Debug: {dbg}")
            self.pipeline.set_state(Gst.State.NULL)

def main(args=None):
    rclpy.init(args=args)
    node = DeepStreamROSNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutdown requested by user.")
    finally:
        node.pipeline.set_state(Gst.State.NULL)
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
# This code is a refactored version of the original DeepStream ROS node for ZED cameras.
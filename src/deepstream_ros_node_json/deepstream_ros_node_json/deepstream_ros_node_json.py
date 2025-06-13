from rclpy.node import Node
import rclpy
import gi
import json
import pyds
import threading
from queue import Queue, Full, Empty
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

gi.require_version('Gst', '1.0')
from gi.repository import Gst


class DeepStreamROSNode(Node):
    def __init__(self):
        super().__init__('deepstream_json_node')
        self.declare_parameter('enable_visualization', False)
        self.enable_visualization = self.get_parameter('enable_visualization').get_parameter_value().bool_value
        Gst.init(None)

        self.publisher_ = self.create_publisher(String, '/deepstream/detections', 10)
        self.bridge = CvBridge()
        self.frame_queue = Queue(maxsize=5)
        self.pipeline = Gst.Pipeline()

        source = Gst.ElementFactory.make("appsrc", "ros_appsrc")
        source.set_property("caps", Gst.Caps.from_string("video/x-raw,format=BGRA,width=960,height=540,framerate=30/1"))
        source.set_property("is-live", True)
        source.set_property("do-timestamp", True)
        source.set_property("block", False)
        source.connect("need-data", self.on_need_data)

        vidconvsrc = Gst.ElementFactory.make("videoconvert", "convertor_src1")
        caps_nv12 = Gst.ElementFactory.make("capsfilter", "caps_nv12")
        nvvidconvsrc = Gst.ElementFactory.make("nvvideoconvert", "convertor_src2")
        caps_nvmm = Gst.ElementFactory.make("capsfilter", "nvmm_caps")
        pgie = Gst.ElementFactory.make("nvinfer", "primary-inference")
        tracker = Gst.ElementFactory.make("nvtracker", "tracker")
        nvvidconv = Gst.ElementFactory.make("nvvideoconvert", "convertor")
        nvosd = Gst.ElementFactory.make("nvdsosd", "onscreendisplay")
        sink = Gst.ElementFactory.make("nveglglessink" if self.enable_visualization else "fakesink", "nvvideo-renderer")
        sink.set_property("sync", False)

        self.get_logger().info("Visualization ENABLED." if self.enable_visualization else "Visualization DISABLED.")

        elements = [
            ("streammux", Gst.ElementFactory.make("nvstreammux", "streammux")),
            ("source", source), ("vidconvsrc", vidconvsrc), ("caps_nv12", caps_nv12),
            ("nvvidconvsrc", nvvidconvsrc), ("caps_nvmm", caps_nvmm), ("pgie", pgie),
            ("tracker", tracker), ("nvvidconv", nvvidconv), ("nvosd", nvosd), ("sink", sink)
        ]

        for name, elem in elements:
            if not elem:
                self.get_logger().error(f"Failed to create element: {name}")
                raise RuntimeError(f"GStreamer element creation failed: {name}")
            self.pipeline.add(elem)

        caps_nv12.set_property("caps", Gst.Caps.from_string("video/x-raw,format=NV12"))
        caps_nvmm.set_property("caps", Gst.Caps.from_string("video/x-raw(memory:NVMM)"))
        pgie.set_property("config-file-path", "/home/gokcer/DeepStream-Yolo/config_infer_primary_yolo11.txt")
        tracker.set_property("ll-lib-file", "/opt/nvidia/deepstream/deepstream/lib/libnvds_nvmultiobjecttracker.so")
        tracker.set_property("ll-config-file", "/home/gokcer/DeepStream-Yolo/config_tracker_NvDCF_perf.yml")

        source.link(vidconvsrc)
        vidconvsrc.link(caps_nv12)
        caps_nv12.link(nvvidconvsrc)

        streammux = dict(elements)["streammux"]
        streammux.set_property("width", 960)
        streammux.set_property("height", 540)
        streammux.set_property("batch-size", 1)
        streammux.set_property("batched-push-timeout", 40000)
        streammux.set_property("live-source", 1)

        self.pipeline.add(streammux)
        sinkpad = streammux.get_request_pad("sink_0")
        srcpad = nvvidconvsrc.get_static_pad("src")
        if not sinkpad or not srcpad:
            raise RuntimeError("Failed to get pads for linking to streammux")
        srcpad.link(sinkpad)

        streammux.link(pgie)
        pgie.link(tracker)
        tracker.link(nvvidconv)
        nvvidconv.link(nvosd)
        nvosd.link(sink)

        osd = self.pipeline.get_by_name("onscreendisplay")
        if osd:
            osd_sink_pad = osd.get_static_pad("sink")
            if osd_sink_pad:
                osd_sink_pad.add_probe(Gst.PadProbeType.BUFFER, self.osd_sink_pad_buffer_probe, 0)

        self.appsrc = self.pipeline.get_by_name("ros_appsrc")

        self.subscription = self.create_subscription(
            Image,
            '/zed/zed_node/left/image_rect_color',
            self.ros_image_callback,
            10
        )

        ret = self.pipeline.set_state(Gst.State.PLAYING)
        if ret != Gst.StateChangeReturn.ASYNC:
            self.get_logger().warn(f"Pipeline state change returned: {ret}")

        self.bus_timer = self.create_timer(0.1, self.poll_gst_bus)
        self.get_logger().info("DeepStream ROS node pipeline started.")

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
            try:
                self.frame_queue.put_nowait(frame)
            except Full:
                self.frame_queue.get_nowait()
                self.frame_queue.put_nowait(frame)

        except Exception as e:
            self.get_logger().error(f"Image callback error: {e}")

    def on_need_data(self, src, length):
        import time
        frame = None
        for _ in range(5):
            try:
                frame = self.frame_queue.get(timeout=0.05)
                break
            except Empty:
                time.sleep(0.01)

        if frame is None:
            self.get_logger().debug("No frame available for appsrc.")
            return

        try:
            data = frame.tobytes()
            buf = Gst.Buffer.new_allocate(None, len(data), None)
            buf.fill(0, data)
            buf.pts = buf.dts = Gst.util_get_timestamp()
            buf.duration = Gst.util_uint64_scale_int(1, Gst.SECOND, 30)
            retval = src.emit("push-buffer", buf)
            self.get_logger().debug(f"Pushed frame to appsrc, result: {retval}")
        except Exception as e:
            self.get_logger().error(f"on_need_data error: {e}")

    def osd_sink_pad_buffer_probe(self, pad, info, u_data):
        buffer = info.get_buffer()
        if not buffer:
            return Gst.PadProbeReturn.OK

        batch_meta = pyds.gst_buffer_get_nvds_batch_meta(hash(buffer))
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

            frame_data = {
                "frame_number": frame_meta.frame_num,
                "objects": objects
            }
            if objects and rclpy.ok():
                json_msg = json.dumps(frame_data, separators=(',', ':'))
                self.publisher_.publish(String(data=json_msg))

            try:
                l_frame = l_frame.next
            except StopIteration:
                break

        return Gst.PadProbeReturn.OK

    def poll_gst_bus(self):
        msg = self.pipeline.get_bus().pop_filtered(
            Gst.MessageType.ERROR | Gst.MessageType.EOS
        )
        if not msg:
            return

        msg_type = msg.type
        if msg_type == Gst.MessageType.EOS:
            self.get_logger().warn("GStreamer: End of stream.")
            self.pipeline.set_state(Gst.State.NULL)
        elif msg_type == Gst.MessageType.ERROR:
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

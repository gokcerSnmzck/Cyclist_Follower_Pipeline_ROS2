from rclpy.node import Node
import rclpy
import gi
import json
import pyds
import threading
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import json


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
        self.pipeline = Gst.Pipeline()

        source = Gst.ElementFactory.make("appsrc", "ros_appsrc")
        source.set_property("caps", Gst.Caps.from_string("video/x-raw,format=BGRA,width=960,height=540,framerate=30/1"))
        vidconvsrc = Gst.ElementFactory.make("videoconvert", "convertor_src1")
        caps_nv12 = Gst.ElementFactory.make("capsfilter", "caps_nv12")
        nvvidconvsrc = Gst.ElementFactory.make("nvvideoconvert", "convertor_src2")
        caps_nvmm = Gst.ElementFactory.make("capsfilter", "nvmm_caps")
        pgie = Gst.ElementFactory.make("nvinfer", "primary-inference")
        tracker = Gst.ElementFactory.make("nvtracker", "tracker")
        nvvidconv = Gst.ElementFactory.make("nvvideoconvert", "convertor")
        nvosd = Gst.ElementFactory.make("nvdsosd", "onscreendisplay")
        if self.enable_visualization:
            sink = Gst.ElementFactory.make("nveglglessink", "nvvideo-renderer")
            sink.set_property("sync", False)
            self.get_logger().info("Visualization ENABLED.")
        else:
            sink = Gst.ElementFactory.make("fakesink", "fakesink")
            sink.set_property("sync", False)
            self.get_logger().info("Visualization DISABLED.")


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
        pgie.set_property("config-file-path", "/home/student/devel/DeepStream-Yolo/config_infer_primary_yolo11.txt")
        tracker.set_property("ll-lib-file", "/opt/nvidia/deepstream/deepstream/lib/libnvds_nvmultiobjecttracker.so")
        tracker.set_property("ll-config-file", "/home/student/devel/DeepStream-Yolo/config_tracker_NvDCF_perf.yml")
        sink.set_property("sync", False)

        source.link(vidconvsrc)
        vidconvsrc.link(caps_nv12)
        caps_nv12.link(nvvidconvsrc)

        streammux = dict(elements)["streammux"]
        self.pipeline.add(streammux)
        streammux.set_property("width", 960)
        streammux.set_property("height", 540)
        streammux.set_property("batch-size", 1)
        streammux.set_property("batched-push-timeout", 40000)

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
        bus = self.pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.bus_call)

        self.subscription = self.create_subscription(
            Image,
            '/zed/zed_node/left/image_rect_color',
            self.ros_image_callback,
            10)

        self.pipeline.set_state(Gst.State.PLAYING)

        self.loop = GLib.MainLoop()
        self.loop_thread = threading.Thread(target=self.loop.run)
        self.loop_thread.start()
        self.get_logger().info("DeepStream ROS node pipeline started.")

    def ros_image_callback(self, msg):
        if not rclpy.ok():
            return
        try:
            frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgra8')
            gst_buffer = Gst.Buffer.new_allocate(None, frame.nbytes, None)
            gst_buffer.fill(0, frame.tobytes())
            duration = Gst.util_uint64_scale_int(1, Gst.SECOND, 30)
            gst_buffer.duration = duration
            timestamp = Gst.util_get_timestamp()
            gst_buffer.pts = gst_buffer.dts = timestamp
            self.appsrc.emit("push-buffer", gst_buffer)
        except Exception as e:
            self.get_logger().error(f"Error converting and pushing frame: {e}")

    def osd_sink_pad_buffer_probe(self, pad, info, u_data):
        print(">>> Pad probe activated")
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
                print(f"Detected object: {obj_meta.obj_label}, confidence: {obj_meta.confidence}")
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

            json_msg = json.dumps(frame_data)

            print(f">>> Publishing: {json_msg}")
            if rclpy.ok():
                self.publisher_.publish(String(data=json_msg))

            # if rclpy.ok():
            #     payload = json.dumps(frame_data)
            #     print(">>> Publishing:", payload)
            #     self.publisher_.publish(String(data=payload))
            # else:
            #     print("rclpy not OK")

            try:
                l_frame = l_frame.next
            except StopIteration:
                break

        return Gst.PadProbeReturn.OK

    def bus_call(self, bus, message):
        msg_type = message.type
        if msg_type == Gst.MessageType.EOS:
            self.get_logger().info("End of stream")
            self.pipeline.set_state(Gst.State.NULL)
            self.loop.quit()
        elif msg_type == Gst.MessageType.ERROR:
            err, debug = message.parse_error()
            self.get_logger().error(f"Error: {err}, Debug info: {debug}")
            self.pipeline.set_state(Gst.State.NULL)
            self.loop.quit()
        return True


def main(args=None):
    rclpy.init(args=args)
    node = DeepStreamROSNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("KeyboardInterrupt received. Shutting down...")
    finally:
        node.loop.quit()
        node.loop_thread.join()
        node.pipeline.set_state(Gst.State.NULL)
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

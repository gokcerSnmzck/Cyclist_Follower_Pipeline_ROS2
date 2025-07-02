import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import gi
import json
import pyds
import os

gi.require_version('Gst', '1.0')
from gi.repository import Gst


class DeepStreamWebcamNode(Node):
    def __init__(self):
        os.environ["GST_DEBUG_DUMP_DOT_DIR"] = "."
        super().__init__('deepstream_webcam_node')
        self.declare_parameter('enable_visualization', True)
        self.enable_visualization = self.get_parameter('enable_visualization').get_parameter_value().bool_value

        Gst.init(None)
        self.publisher_ = self.create_publisher(String, '/deepstream/detections', 10)
        self.pipeline = Gst.Pipeline()

        # Webcam input
        source = Gst.ElementFactory.make("v4l2src", "webcam_source")
        source.set_property("device", "/dev/video0")

        # Caps for MJPEG input
        caps_v4l2 = Gst.ElementFactory.make("capsfilter", "caps_v4l2")
        caps_v4l2.set_property("caps", Gst.Caps.from_string("image/jpeg,width=1280,height=720,framerate=30/1"))

        # Decode MJPEG to raw
        jpegdec = Gst.ElementFactory.make("jpegdec", "jpeg_decoder")

        # Convert to NVMM memory
        vidconvsrc = Gst.ElementFactory.make("videoconvert", "convertor_src1")
        nvvidconvsrc = Gst.ElementFactory.make("nvvideoconvert", "convertor_src2")
        caps_nvmm = Gst.ElementFactory.make("capsfilter", "caps_nvmm")
        caps_nvmm.set_property("caps", Gst.Caps.from_string("video/x-raw(memory:NVMM),format=NV12"))

        # Stream muxer
        streammux = Gst.ElementFactory.make("nvstreammux", "streammux")
        streammux.set_property("width", 1280)
        streammux.set_property("height", 720)
        streammux.set_property("batch-size", 1)
        streammux.set_property("batched-push-timeout", 40000)
        streammux.set_property("live-source", 1)

        # Inference + Tracker
        pgie = Gst.ElementFactory.make("nvinfer", "primary-inference")
        pgie.set_property("config-file-path", "/home/gokcer/DeepStream-Yolo/config_infer_primary_yolo11.txt")

        tracker = Gst.ElementFactory.make("nvtracker", "tracker")
        tracker.set_property("ll-lib-file", "/opt/nvidia/deepstream/deepstream/lib/libnvds_nvmultiobjecttracker.so")
        tracker.set_property("ll-config-file", "/home/gokcer/DeepStream-Yolo/config_tracker_NvDCF_perf.yml")

        # Display / Sink
        nvvidconv = Gst.ElementFactory.make("nvvideoconvert", "convertor")
        nvosd = Gst.ElementFactory.make("nvdsosd", "onscreendisplay")
        sink = Gst.ElementFactory.make("nveglglessink" if self.enable_visualization else "fakesink", "nvvideo-renderer")
        sink.set_property("sync", False)

        self.get_logger().info("Visualization ENABLED." if self.enable_visualization else "Visualization DISABLED.")

        elements = [
            source, caps_v4l2, jpegdec, vidconvsrc, nvvidconvsrc, caps_nvmm,
            streammux, pgie, tracker, nvvidconv, nvosd, sink
        ]
        for elem in elements:
            if not elem:
                raise RuntimeError("Failed to create GStreamer element.")
            self.pipeline.add(elem)

        # Link all elements in order
        source.link(caps_v4l2)
        caps_v4l2.link(jpegdec)
        jpegdec.link(vidconvsrc)
        vidconvsrc.link(nvvidconvsrc)
        nvvidconvsrc.link(caps_nvmm)

        # Link to streammux manually
        sinkpad = streammux.get_request_pad("sink_0")
        srcpad = caps_nvmm.get_static_pad("src")
        if not sinkpad or not srcpad or srcpad.link(sinkpad) != Gst.PadLinkReturn.OK:
            raise RuntimeError("Failed to link to nvstreammux")

        streammux.link(pgie)
        pgie.link(tracker)
        tracker.link(nvvidconv)
        nvvidconv.link(nvosd)
        nvosd.link(sink)

        # Add metadata probe
        osd_sink_pad = nvosd.get_static_pad("sink")
        if osd_sink_pad:
            osd_sink_pad.add_probe(Gst.PadProbeType.BUFFER, self.osd_sink_pad_buffer_probe, 0)

        # Save pipeline to dot file for debugging
        Gst.debug_bin_to_dot_file(self.pipeline, Gst.DebugGraphDetails.ALL, "pipeline")
        # Start pipeline
        ret = self.pipeline.set_state(Gst.State.PLAYING)
        if ret != Gst.StateChangeReturn.ASYNC:
            self.get_logger().warn(f"Pipeline state change returned: {ret}")

        self.bus_timer = self.create_timer(0.1, self.poll_gst_bus)
        self.get_logger().info("DeepStream webcam node pipeline started.")

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
        msg = self.pipeline.get_bus().pop_filtered(Gst.MessageType.ERROR | Gst.MessageType.EOS)
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
    node = DeepStreamWebcamNode()
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

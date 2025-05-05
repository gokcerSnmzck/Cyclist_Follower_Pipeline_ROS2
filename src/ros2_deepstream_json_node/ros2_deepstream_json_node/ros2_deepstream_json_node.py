import rclpy
from rclpy.node import Node
import gi
import json

# GStreamer and DeepStream Setup
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib
import pyds
from std_msgs.msg import String


class DeepStreamROSNode(Node):
    def __init__(self):
        super().__init__('deepstream_json_node')
        Gst.init(None)

        # Path to your DeepStream config
        self.config_path = "/home/gokcer/DeepStream-Yolo/deepstream_app_config_save.txt"  # CHANGE THIS

        # Create DeepStream pipeline
        self.pipeline = Gst.parse_launch(f"uridecodebin uri=file://{self.config_path}")

        # Publisher for detection data
        self.publisher_ = self.create_publisher(String, 'detections', 10)

        # Add probe to OSD sink pad
        osd_sink_pad = self.pipeline.get_by_name("nvosd").get_static_pad("sink")
        if osd_sink_pad:
            osd_sink_pad.add_probe(Gst.PadProbeType.BUFFER, self.osd_sink_pad_buffer_probe, None)

        # Bus and MainLoop
        bus = self.pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.bus_call)
        self.loop = GLib.MainLoop()

        # Start pipeline
        self.pipeline.set_state(Gst.State.PLAYING)
        self.get_logger().info("DeepStream pipeline started.")
        self.run_loop()

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
                    "id": obj_meta.object_id,
                    "class": obj_meta.obj_label,
                    "bbox": [
                        obj_meta.rect_params.left,
                        obj_meta.rect_params.top,
                        obj_meta.rect_params.width,
                        obj_meta.rect_params.height
                    ],
                    "confidence": obj_meta.confidence
                })
                try:
                    l_obj = l_obj.next
                except StopIteration:
                    break

            frame_data = {
                "frame_number": frame_meta.frame_num,
                "objects": objects
            }
            self.publisher_.publish(String(data=json.dumps(frame_data)))

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

    def run_loop(self):
        try:
            self.loop.run()
        except KeyboardInterrupt:
            self.pipeline.set_state(Gst.State.NULL)
            self.loop.quit()


def main(args=None):
    rclpy.init(args=args)
    node = DeepStreamROSNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

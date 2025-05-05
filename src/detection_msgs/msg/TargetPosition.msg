# TargetPosition.msg

# Standard header for timestamp and frame
std_msgs/Header header

# Unique tracking ID from DeepStream
int32 id

# Class label ID (e.g., person, cyclist, etc.)
int32 class_id

# Detection confidence score (0.0 to 1.0)
float32 confidence

# 3D position of the target in the camera frame
geometry_msgs/Point position

# Optional: Label name for readability
string label

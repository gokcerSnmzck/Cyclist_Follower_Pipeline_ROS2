// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from detection_msgs:msg/Detection2D.idl
// generated code does not contain a copyright notice

#ifndef DETECTION_MSGS__MSG__DETAIL__DETECTION2_D__STRUCT_H_
#define DETECTION_MSGS__MSG__DETAIL__DETECTION2_D__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'label'
#include "rosidl_runtime_c/string.h"
// Member 'bbox'
#include "detection_msgs/msg/detail/bounding_box2_d__struct.h"

/// Struct defined in msg/Detection2D in the package detection_msgs.
/**
  * Detection2D.msg
 */
typedef struct detection_msgs__msg__Detection2D
{
  /// Unique tracking ID (from DeepStream tracker)
  int32_t tracking_id;
  /// Detected object class (e.g., person = 0)
  int32_t class_id;
  /// Human-readable label, e.g., "person"
  rosidl_runtime_c__String label;
  /// Confidence score (0.0 to 1.0)
  float confidence;
  /// 2D bounding box in image coordinates
  detection_msgs__msg__BoundingBox2D bbox;
} detection_msgs__msg__Detection2D;

// Struct for a sequence of detection_msgs__msg__Detection2D.
typedef struct detection_msgs__msg__Detection2D__Sequence
{
  detection_msgs__msg__Detection2D * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} detection_msgs__msg__Detection2D__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // DETECTION_MSGS__MSG__DETAIL__DETECTION2_D__STRUCT_H_

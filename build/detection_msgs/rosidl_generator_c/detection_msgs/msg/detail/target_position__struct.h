// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from detection_msgs:msg/TargetPosition.idl
// generated code does not contain a copyright notice

#ifndef DETECTION_MSGS__MSG__DETAIL__TARGET_POSITION__STRUCT_H_
#define DETECTION_MSGS__MSG__DETAIL__TARGET_POSITION__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.h"
// Member 'position'
#include "geometry_msgs/msg/detail/point__struct.h"
// Member 'label'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/TargetPosition in the package detection_msgs.
/**
  * TargetPosition.msg
 */
typedef struct detection_msgs__msg__TargetPosition
{
  /// Standard header for timestamp and frame
  std_msgs__msg__Header header;
  /// Unique tracking ID from DeepStream
  int32_t id;
  /// Class label ID (e.g., person, cyclist, etc.)
  int32_t class_id;
  /// Detection confidence score (0.0 to 1.0)
  float confidence;
  /// 3D position of the target in the camera frame
  geometry_msgs__msg__Point position;
  /// Optional: Label name for readability
  rosidl_runtime_c__String label;
} detection_msgs__msg__TargetPosition;

// Struct for a sequence of detection_msgs__msg__TargetPosition.
typedef struct detection_msgs__msg__TargetPosition__Sequence
{
  detection_msgs__msg__TargetPosition * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} detection_msgs__msg__TargetPosition__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // DETECTION_MSGS__MSG__DETAIL__TARGET_POSITION__STRUCT_H_

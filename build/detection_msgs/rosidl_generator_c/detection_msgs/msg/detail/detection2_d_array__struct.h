// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from detection_msgs:msg/Detection2DArray.idl
// generated code does not contain a copyright notice

#ifndef DETECTION_MSGS__MSG__DETAIL__DETECTION2_D_ARRAY__STRUCT_H_
#define DETECTION_MSGS__MSG__DETAIL__DETECTION2_D_ARRAY__STRUCT_H_

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
// Member 'detections'
#include "detection_msgs/msg/detail/detection2_d__struct.h"

/// Struct defined in msg/Detection2DArray in the package detection_msgs.
/**
  * Detection2DArray.msg
 */
typedef struct detection_msgs__msg__Detection2DArray
{
  /// Standard ROS header (includes timestamp and frame_id)
  std_msgs__msg__Header header;
  /// Array of 2D detections
  detection_msgs__msg__Detection2D__Sequence detections;
} detection_msgs__msg__Detection2DArray;

// Struct for a sequence of detection_msgs__msg__Detection2DArray.
typedef struct detection_msgs__msg__Detection2DArray__Sequence
{
  detection_msgs__msg__Detection2DArray * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} detection_msgs__msg__Detection2DArray__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // DETECTION_MSGS__MSG__DETAIL__DETECTION2_D_ARRAY__STRUCT_H_

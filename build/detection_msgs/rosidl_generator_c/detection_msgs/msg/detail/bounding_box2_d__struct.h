// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from detection_msgs:msg/BoundingBox2D.idl
// generated code does not contain a copyright notice

#ifndef DETECTION_MSGS__MSG__DETAIL__BOUNDING_BOX2_D__STRUCT_H_
#define DETECTION_MSGS__MSG__DETAIL__BOUNDING_BOX2_D__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/BoundingBox2D in the package detection_msgs.
/**
  * BoundingBox2D.msg
 */
typedef struct detection_msgs__msg__BoundingBox2D
{
  /// Top-left x, y and width, height of bounding box
  float x;
  float y;
  float width;
  float height;
} detection_msgs__msg__BoundingBox2D;

// Struct for a sequence of detection_msgs__msg__BoundingBox2D.
typedef struct detection_msgs__msg__BoundingBox2D__Sequence
{
  detection_msgs__msg__BoundingBox2D * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} detection_msgs__msg__BoundingBox2D__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // DETECTION_MSGS__MSG__DETAIL__BOUNDING_BOX2_D__STRUCT_H_

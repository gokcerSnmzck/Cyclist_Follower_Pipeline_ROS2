// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from detection_msgs:msg/Detection2D.idl
// generated code does not contain a copyright notice
#include "detection_msgs/msg/detail/detection2_d__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "detection_msgs/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "detection_msgs/msg/detail/detection2_d__struct.h"
#include "detection_msgs/msg/detail/detection2_d__functions.h"
#include "fastcdr/Cdr.h"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

// includes and forward declarations of message dependencies and their conversion functions

#if defined(__cplusplus)
extern "C"
{
#endif

#include "detection_msgs/msg/detail/bounding_box2_d__functions.h"  // bbox
#include "rosidl_runtime_c/string.h"  // label
#include "rosidl_runtime_c/string_functions.h"  // label

// forward declare type support functions
size_t get_serialized_size_detection_msgs__msg__BoundingBox2D(
  const void * untyped_ros_message,
  size_t current_alignment);

size_t max_serialized_size_detection_msgs__msg__BoundingBox2D(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, detection_msgs, msg, BoundingBox2D)();


using _Detection2D__ros_msg_type = detection_msgs__msg__Detection2D;

static bool _Detection2D__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _Detection2D__ros_msg_type * ros_message = static_cast<const _Detection2D__ros_msg_type *>(untyped_ros_message);
  // Field name: tracking_id
  {
    cdr << ros_message->tracking_id;
  }

  // Field name: class_id
  {
    cdr << ros_message->class_id;
  }

  // Field name: label
  {
    const rosidl_runtime_c__String * str = &ros_message->label;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: confidence
  {
    cdr << ros_message->confidence;
  }

  // Field name: bbox
  {
    const message_type_support_callbacks_t * callbacks =
      static_cast<const message_type_support_callbacks_t *>(
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
        rosidl_typesupport_fastrtps_c, detection_msgs, msg, BoundingBox2D
      )()->data);
    if (!callbacks->cdr_serialize(
        &ros_message->bbox, cdr))
    {
      return false;
    }
  }

  return true;
}

static bool _Detection2D__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _Detection2D__ros_msg_type * ros_message = static_cast<_Detection2D__ros_msg_type *>(untyped_ros_message);
  // Field name: tracking_id
  {
    cdr >> ros_message->tracking_id;
  }

  // Field name: class_id
  {
    cdr >> ros_message->class_id;
  }

  // Field name: label
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->label.data) {
      rosidl_runtime_c__String__init(&ros_message->label);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->label,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'label'\n");
      return false;
    }
  }

  // Field name: confidence
  {
    cdr >> ros_message->confidence;
  }

  // Field name: bbox
  {
    const message_type_support_callbacks_t * callbacks =
      static_cast<const message_type_support_callbacks_t *>(
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
        rosidl_typesupport_fastrtps_c, detection_msgs, msg, BoundingBox2D
      )()->data);
    if (!callbacks->cdr_deserialize(
        cdr, &ros_message->bbox))
    {
      return false;
    }
  }

  return true;
}  // NOLINT(readability/fn_size)

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_detection_msgs
size_t get_serialized_size_detection_msgs__msg__Detection2D(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _Detection2D__ros_msg_type * ros_message = static_cast<const _Detection2D__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name tracking_id
  {
    size_t item_size = sizeof(ros_message->tracking_id);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name class_id
  {
    size_t item_size = sizeof(ros_message->class_id);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name label
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->label.size + 1);
  // field.name confidence
  {
    size_t item_size = sizeof(ros_message->confidence);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name bbox

  current_alignment += get_serialized_size_detection_msgs__msg__BoundingBox2D(
    &(ros_message->bbox), current_alignment);

  return current_alignment - initial_alignment;
}

static uint32_t _Detection2D__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_detection_msgs__msg__Detection2D(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_detection_msgs
size_t max_serialized_size_detection_msgs__msg__Detection2D(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;

  // member: tracking_id
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }
  // member: class_id
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }
  // member: label
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }
  // member: confidence
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }
  // member: bbox
  {
    size_t array_size = 1;


    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_detection_msgs__msg__BoundingBox2D(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = detection_msgs__msg__Detection2D;
    is_plain =
      (
      offsetof(DataType, bbox) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static size_t _Detection2D__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_detection_msgs__msg__Detection2D(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_Detection2D = {
  "detection_msgs::msg",
  "Detection2D",
  _Detection2D__cdr_serialize,
  _Detection2D__cdr_deserialize,
  _Detection2D__get_serialized_size,
  _Detection2D__max_serialized_size
};

static rosidl_message_type_support_t _Detection2D__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_Detection2D,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, detection_msgs, msg, Detection2D)() {
  return &_Detection2D__type_support;
}

#if defined(__cplusplus)
}
#endif

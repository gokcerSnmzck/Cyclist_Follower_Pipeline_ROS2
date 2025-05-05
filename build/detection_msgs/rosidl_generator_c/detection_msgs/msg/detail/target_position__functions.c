// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from detection_msgs:msg/TargetPosition.idl
// generated code does not contain a copyright notice
#include "detection_msgs/msg/detail/target_position__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"
// Member `position`
#include "geometry_msgs/msg/detail/point__functions.h"
// Member `label`
#include "rosidl_runtime_c/string_functions.h"

bool
detection_msgs__msg__TargetPosition__init(detection_msgs__msg__TargetPosition * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    detection_msgs__msg__TargetPosition__fini(msg);
    return false;
  }
  // id
  // class_id
  // confidence
  // position
  if (!geometry_msgs__msg__Point__init(&msg->position)) {
    detection_msgs__msg__TargetPosition__fini(msg);
    return false;
  }
  // label
  if (!rosidl_runtime_c__String__init(&msg->label)) {
    detection_msgs__msg__TargetPosition__fini(msg);
    return false;
  }
  return true;
}

void
detection_msgs__msg__TargetPosition__fini(detection_msgs__msg__TargetPosition * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // id
  // class_id
  // confidence
  // position
  geometry_msgs__msg__Point__fini(&msg->position);
  // label
  rosidl_runtime_c__String__fini(&msg->label);
}

bool
detection_msgs__msg__TargetPosition__are_equal(const detection_msgs__msg__TargetPosition * lhs, const detection_msgs__msg__TargetPosition * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__are_equal(
      &(lhs->header), &(rhs->header)))
  {
    return false;
  }
  // id
  if (lhs->id != rhs->id) {
    return false;
  }
  // class_id
  if (lhs->class_id != rhs->class_id) {
    return false;
  }
  // confidence
  if (lhs->confidence != rhs->confidence) {
    return false;
  }
  // position
  if (!geometry_msgs__msg__Point__are_equal(
      &(lhs->position), &(rhs->position)))
  {
    return false;
  }
  // label
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->label), &(rhs->label)))
  {
    return false;
  }
  return true;
}

bool
detection_msgs__msg__TargetPosition__copy(
  const detection_msgs__msg__TargetPosition * input,
  detection_msgs__msg__TargetPosition * output)
{
  if (!input || !output) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__copy(
      &(input->header), &(output->header)))
  {
    return false;
  }
  // id
  output->id = input->id;
  // class_id
  output->class_id = input->class_id;
  // confidence
  output->confidence = input->confidence;
  // position
  if (!geometry_msgs__msg__Point__copy(
      &(input->position), &(output->position)))
  {
    return false;
  }
  // label
  if (!rosidl_runtime_c__String__copy(
      &(input->label), &(output->label)))
  {
    return false;
  }
  return true;
}

detection_msgs__msg__TargetPosition *
detection_msgs__msg__TargetPosition__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  detection_msgs__msg__TargetPosition * msg = (detection_msgs__msg__TargetPosition *)allocator.allocate(sizeof(detection_msgs__msg__TargetPosition), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(detection_msgs__msg__TargetPosition));
  bool success = detection_msgs__msg__TargetPosition__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
detection_msgs__msg__TargetPosition__destroy(detection_msgs__msg__TargetPosition * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    detection_msgs__msg__TargetPosition__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
detection_msgs__msg__TargetPosition__Sequence__init(detection_msgs__msg__TargetPosition__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  detection_msgs__msg__TargetPosition * data = NULL;

  if (size) {
    data = (detection_msgs__msg__TargetPosition *)allocator.zero_allocate(size, sizeof(detection_msgs__msg__TargetPosition), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = detection_msgs__msg__TargetPosition__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        detection_msgs__msg__TargetPosition__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
detection_msgs__msg__TargetPosition__Sequence__fini(detection_msgs__msg__TargetPosition__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      detection_msgs__msg__TargetPosition__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

detection_msgs__msg__TargetPosition__Sequence *
detection_msgs__msg__TargetPosition__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  detection_msgs__msg__TargetPosition__Sequence * array = (detection_msgs__msg__TargetPosition__Sequence *)allocator.allocate(sizeof(detection_msgs__msg__TargetPosition__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = detection_msgs__msg__TargetPosition__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
detection_msgs__msg__TargetPosition__Sequence__destroy(detection_msgs__msg__TargetPosition__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    detection_msgs__msg__TargetPosition__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
detection_msgs__msg__TargetPosition__Sequence__are_equal(const detection_msgs__msg__TargetPosition__Sequence * lhs, const detection_msgs__msg__TargetPosition__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!detection_msgs__msg__TargetPosition__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
detection_msgs__msg__TargetPosition__Sequence__copy(
  const detection_msgs__msg__TargetPosition__Sequence * input,
  detection_msgs__msg__TargetPosition__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(detection_msgs__msg__TargetPosition);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    detection_msgs__msg__TargetPosition * data =
      (detection_msgs__msg__TargetPosition *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!detection_msgs__msg__TargetPosition__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          detection_msgs__msg__TargetPosition__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!detection_msgs__msg__TargetPosition__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}

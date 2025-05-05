// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from detection_msgs:msg/BoundingBox2D.idl
// generated code does not contain a copyright notice
#include "detection_msgs/msg/detail/bounding_box2_d__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


bool
detection_msgs__msg__BoundingBox2D__init(detection_msgs__msg__BoundingBox2D * msg)
{
  if (!msg) {
    return false;
  }
  // x
  // y
  // width
  // height
  return true;
}

void
detection_msgs__msg__BoundingBox2D__fini(detection_msgs__msg__BoundingBox2D * msg)
{
  if (!msg) {
    return;
  }
  // x
  // y
  // width
  // height
}

bool
detection_msgs__msg__BoundingBox2D__are_equal(const detection_msgs__msg__BoundingBox2D * lhs, const detection_msgs__msg__BoundingBox2D * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // x
  if (lhs->x != rhs->x) {
    return false;
  }
  // y
  if (lhs->y != rhs->y) {
    return false;
  }
  // width
  if (lhs->width != rhs->width) {
    return false;
  }
  // height
  if (lhs->height != rhs->height) {
    return false;
  }
  return true;
}

bool
detection_msgs__msg__BoundingBox2D__copy(
  const detection_msgs__msg__BoundingBox2D * input,
  detection_msgs__msg__BoundingBox2D * output)
{
  if (!input || !output) {
    return false;
  }
  // x
  output->x = input->x;
  // y
  output->y = input->y;
  // width
  output->width = input->width;
  // height
  output->height = input->height;
  return true;
}

detection_msgs__msg__BoundingBox2D *
detection_msgs__msg__BoundingBox2D__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  detection_msgs__msg__BoundingBox2D * msg = (detection_msgs__msg__BoundingBox2D *)allocator.allocate(sizeof(detection_msgs__msg__BoundingBox2D), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(detection_msgs__msg__BoundingBox2D));
  bool success = detection_msgs__msg__BoundingBox2D__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
detection_msgs__msg__BoundingBox2D__destroy(detection_msgs__msg__BoundingBox2D * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    detection_msgs__msg__BoundingBox2D__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
detection_msgs__msg__BoundingBox2D__Sequence__init(detection_msgs__msg__BoundingBox2D__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  detection_msgs__msg__BoundingBox2D * data = NULL;

  if (size) {
    data = (detection_msgs__msg__BoundingBox2D *)allocator.zero_allocate(size, sizeof(detection_msgs__msg__BoundingBox2D), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = detection_msgs__msg__BoundingBox2D__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        detection_msgs__msg__BoundingBox2D__fini(&data[i - 1]);
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
detection_msgs__msg__BoundingBox2D__Sequence__fini(detection_msgs__msg__BoundingBox2D__Sequence * array)
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
      detection_msgs__msg__BoundingBox2D__fini(&array->data[i]);
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

detection_msgs__msg__BoundingBox2D__Sequence *
detection_msgs__msg__BoundingBox2D__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  detection_msgs__msg__BoundingBox2D__Sequence * array = (detection_msgs__msg__BoundingBox2D__Sequence *)allocator.allocate(sizeof(detection_msgs__msg__BoundingBox2D__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = detection_msgs__msg__BoundingBox2D__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
detection_msgs__msg__BoundingBox2D__Sequence__destroy(detection_msgs__msg__BoundingBox2D__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    detection_msgs__msg__BoundingBox2D__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
detection_msgs__msg__BoundingBox2D__Sequence__are_equal(const detection_msgs__msg__BoundingBox2D__Sequence * lhs, const detection_msgs__msg__BoundingBox2D__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!detection_msgs__msg__BoundingBox2D__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
detection_msgs__msg__BoundingBox2D__Sequence__copy(
  const detection_msgs__msg__BoundingBox2D__Sequence * input,
  detection_msgs__msg__BoundingBox2D__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(detection_msgs__msg__BoundingBox2D);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    detection_msgs__msg__BoundingBox2D * data =
      (detection_msgs__msg__BoundingBox2D *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!detection_msgs__msg__BoundingBox2D__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          detection_msgs__msg__BoundingBox2D__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!detection_msgs__msg__BoundingBox2D__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}

// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from detection_msgs:msg/BoundingBox2D.idl
// generated code does not contain a copyright notice

#ifndef DETECTION_MSGS__MSG__DETAIL__BOUNDING_BOX2_D__STRUCT_HPP_
#define DETECTION_MSGS__MSG__DETAIL__BOUNDING_BOX2_D__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__detection_msgs__msg__BoundingBox2D __attribute__((deprecated))
#else
# define DEPRECATED__detection_msgs__msg__BoundingBox2D __declspec(deprecated)
#endif

namespace detection_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct BoundingBox2D_
{
  using Type = BoundingBox2D_<ContainerAllocator>;

  explicit BoundingBox2D_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->x = 0.0f;
      this->y = 0.0f;
      this->width = 0.0f;
      this->height = 0.0f;
    }
  }

  explicit BoundingBox2D_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->x = 0.0f;
      this->y = 0.0f;
      this->width = 0.0f;
      this->height = 0.0f;
    }
  }

  // field types and members
  using _x_type =
    float;
  _x_type x;
  using _y_type =
    float;
  _y_type y;
  using _width_type =
    float;
  _width_type width;
  using _height_type =
    float;
  _height_type height;

  // setters for named parameter idiom
  Type & set__x(
    const float & _arg)
  {
    this->x = _arg;
    return *this;
  }
  Type & set__y(
    const float & _arg)
  {
    this->y = _arg;
    return *this;
  }
  Type & set__width(
    const float & _arg)
  {
    this->width = _arg;
    return *this;
  }
  Type & set__height(
    const float & _arg)
  {
    this->height = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    detection_msgs::msg::BoundingBox2D_<ContainerAllocator> *;
  using ConstRawPtr =
    const detection_msgs::msg::BoundingBox2D_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<detection_msgs::msg::BoundingBox2D_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<detection_msgs::msg::BoundingBox2D_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      detection_msgs::msg::BoundingBox2D_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<detection_msgs::msg::BoundingBox2D_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      detection_msgs::msg::BoundingBox2D_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<detection_msgs::msg::BoundingBox2D_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<detection_msgs::msg::BoundingBox2D_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<detection_msgs::msg::BoundingBox2D_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__detection_msgs__msg__BoundingBox2D
    std::shared_ptr<detection_msgs::msg::BoundingBox2D_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__detection_msgs__msg__BoundingBox2D
    std::shared_ptr<detection_msgs::msg::BoundingBox2D_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const BoundingBox2D_ & other) const
  {
    if (this->x != other.x) {
      return false;
    }
    if (this->y != other.y) {
      return false;
    }
    if (this->width != other.width) {
      return false;
    }
    if (this->height != other.height) {
      return false;
    }
    return true;
  }
  bool operator!=(const BoundingBox2D_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct BoundingBox2D_

// alias to use template instance with default allocator
using BoundingBox2D =
  detection_msgs::msg::BoundingBox2D_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace detection_msgs

#endif  // DETECTION_MSGS__MSG__DETAIL__BOUNDING_BOX2_D__STRUCT_HPP_

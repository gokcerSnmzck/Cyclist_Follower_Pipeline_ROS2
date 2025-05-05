// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from detection_msgs:msg/TargetPosition.idl
// generated code does not contain a copyright notice

#ifndef DETECTION_MSGS__MSG__DETAIL__TARGET_POSITION__STRUCT_HPP_
#define DETECTION_MSGS__MSG__DETAIL__TARGET_POSITION__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.hpp"
// Member 'position'
#include "geometry_msgs/msg/detail/point__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__detection_msgs__msg__TargetPosition __attribute__((deprecated))
#else
# define DEPRECATED__detection_msgs__msg__TargetPosition __declspec(deprecated)
#endif

namespace detection_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct TargetPosition_
{
  using Type = TargetPosition_<ContainerAllocator>;

  explicit TargetPosition_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init),
    position(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->id = 0l;
      this->class_id = 0l;
      this->confidence = 0.0f;
      this->label = "";
    }
  }

  explicit TargetPosition_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init),
    position(_alloc, _init),
    label(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->id = 0l;
      this->class_id = 0l;
      this->confidence = 0.0f;
      this->label = "";
    }
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _id_type =
    int32_t;
  _id_type id;
  using _class_id_type =
    int32_t;
  _class_id_type class_id;
  using _confidence_type =
    float;
  _confidence_type confidence;
  using _position_type =
    geometry_msgs::msg::Point_<ContainerAllocator>;
  _position_type position;
  using _label_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _label_type label;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__id(
    const int32_t & _arg)
  {
    this->id = _arg;
    return *this;
  }
  Type & set__class_id(
    const int32_t & _arg)
  {
    this->class_id = _arg;
    return *this;
  }
  Type & set__confidence(
    const float & _arg)
  {
    this->confidence = _arg;
    return *this;
  }
  Type & set__position(
    const geometry_msgs::msg::Point_<ContainerAllocator> & _arg)
  {
    this->position = _arg;
    return *this;
  }
  Type & set__label(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->label = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    detection_msgs::msg::TargetPosition_<ContainerAllocator> *;
  using ConstRawPtr =
    const detection_msgs::msg::TargetPosition_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<detection_msgs::msg::TargetPosition_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<detection_msgs::msg::TargetPosition_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      detection_msgs::msg::TargetPosition_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<detection_msgs::msg::TargetPosition_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      detection_msgs::msg::TargetPosition_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<detection_msgs::msg::TargetPosition_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<detection_msgs::msg::TargetPosition_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<detection_msgs::msg::TargetPosition_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__detection_msgs__msg__TargetPosition
    std::shared_ptr<detection_msgs::msg::TargetPosition_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__detection_msgs__msg__TargetPosition
    std::shared_ptr<detection_msgs::msg::TargetPosition_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const TargetPosition_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->id != other.id) {
      return false;
    }
    if (this->class_id != other.class_id) {
      return false;
    }
    if (this->confidence != other.confidence) {
      return false;
    }
    if (this->position != other.position) {
      return false;
    }
    if (this->label != other.label) {
      return false;
    }
    return true;
  }
  bool operator!=(const TargetPosition_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct TargetPosition_

// alias to use template instance with default allocator
using TargetPosition =
  detection_msgs::msg::TargetPosition_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace detection_msgs

#endif  // DETECTION_MSGS__MSG__DETAIL__TARGET_POSITION__STRUCT_HPP_

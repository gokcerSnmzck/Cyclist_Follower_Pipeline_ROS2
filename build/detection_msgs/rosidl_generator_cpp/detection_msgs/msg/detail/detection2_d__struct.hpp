// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from detection_msgs:msg/Detection2D.idl
// generated code does not contain a copyright notice

#ifndef DETECTION_MSGS__MSG__DETAIL__DETECTION2_D__STRUCT_HPP_
#define DETECTION_MSGS__MSG__DETAIL__DETECTION2_D__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'bbox'
#include "detection_msgs/msg/detail/bounding_box2_d__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__detection_msgs__msg__Detection2D __attribute__((deprecated))
#else
# define DEPRECATED__detection_msgs__msg__Detection2D __declspec(deprecated)
#endif

namespace detection_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct Detection2D_
{
  using Type = Detection2D_<ContainerAllocator>;

  explicit Detection2D_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : bbox(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->tracking_id = 0l;
      this->class_id = 0l;
      this->label = "";
      this->confidence = 0.0f;
    }
  }

  explicit Detection2D_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : label(_alloc),
    bbox(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->tracking_id = 0l;
      this->class_id = 0l;
      this->label = "";
      this->confidence = 0.0f;
    }
  }

  // field types and members
  using _tracking_id_type =
    int32_t;
  _tracking_id_type tracking_id;
  using _class_id_type =
    int32_t;
  _class_id_type class_id;
  using _label_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _label_type label;
  using _confidence_type =
    float;
  _confidence_type confidence;
  using _bbox_type =
    detection_msgs::msg::BoundingBox2D_<ContainerAllocator>;
  _bbox_type bbox;

  // setters for named parameter idiom
  Type & set__tracking_id(
    const int32_t & _arg)
  {
    this->tracking_id = _arg;
    return *this;
  }
  Type & set__class_id(
    const int32_t & _arg)
  {
    this->class_id = _arg;
    return *this;
  }
  Type & set__label(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->label = _arg;
    return *this;
  }
  Type & set__confidence(
    const float & _arg)
  {
    this->confidence = _arg;
    return *this;
  }
  Type & set__bbox(
    const detection_msgs::msg::BoundingBox2D_<ContainerAllocator> & _arg)
  {
    this->bbox = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    detection_msgs::msg::Detection2D_<ContainerAllocator> *;
  using ConstRawPtr =
    const detection_msgs::msg::Detection2D_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<detection_msgs::msg::Detection2D_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<detection_msgs::msg::Detection2D_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      detection_msgs::msg::Detection2D_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<detection_msgs::msg::Detection2D_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      detection_msgs::msg::Detection2D_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<detection_msgs::msg::Detection2D_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<detection_msgs::msg::Detection2D_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<detection_msgs::msg::Detection2D_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__detection_msgs__msg__Detection2D
    std::shared_ptr<detection_msgs::msg::Detection2D_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__detection_msgs__msg__Detection2D
    std::shared_ptr<detection_msgs::msg::Detection2D_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Detection2D_ & other) const
  {
    if (this->tracking_id != other.tracking_id) {
      return false;
    }
    if (this->class_id != other.class_id) {
      return false;
    }
    if (this->label != other.label) {
      return false;
    }
    if (this->confidence != other.confidence) {
      return false;
    }
    if (this->bbox != other.bbox) {
      return false;
    }
    return true;
  }
  bool operator!=(const Detection2D_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Detection2D_

// alias to use template instance with default allocator
using Detection2D =
  detection_msgs::msg::Detection2D_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace detection_msgs

#endif  // DETECTION_MSGS__MSG__DETAIL__DETECTION2_D__STRUCT_HPP_

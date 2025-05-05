// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from detection_msgs:msg/TargetPosition.idl
// generated code does not contain a copyright notice

#ifndef DETECTION_MSGS__MSG__DETAIL__TARGET_POSITION__TRAITS_HPP_
#define DETECTION_MSGS__MSG__DETAIL__TARGET_POSITION__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "detection_msgs/msg/detail/target_position__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"
// Member 'position'
#include "geometry_msgs/msg/detail/point__traits.hpp"

namespace detection_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const TargetPosition & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: id
  {
    out << "id: ";
    rosidl_generator_traits::value_to_yaml(msg.id, out);
    out << ", ";
  }

  // member: class_id
  {
    out << "class_id: ";
    rosidl_generator_traits::value_to_yaml(msg.class_id, out);
    out << ", ";
  }

  // member: confidence
  {
    out << "confidence: ";
    rosidl_generator_traits::value_to_yaml(msg.confidence, out);
    out << ", ";
  }

  // member: position
  {
    out << "position: ";
    to_flow_style_yaml(msg.position, out);
    out << ", ";
  }

  // member: label
  {
    out << "label: ";
    rosidl_generator_traits::value_to_yaml(msg.label, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const TargetPosition & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: header
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "header:\n";
    to_block_style_yaml(msg.header, out, indentation + 2);
  }

  // member: id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "id: ";
    rosidl_generator_traits::value_to_yaml(msg.id, out);
    out << "\n";
  }

  // member: class_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "class_id: ";
    rosidl_generator_traits::value_to_yaml(msg.class_id, out);
    out << "\n";
  }

  // member: confidence
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "confidence: ";
    rosidl_generator_traits::value_to_yaml(msg.confidence, out);
    out << "\n";
  }

  // member: position
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "position:\n";
    to_block_style_yaml(msg.position, out, indentation + 2);
  }

  // member: label
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "label: ";
    rosidl_generator_traits::value_to_yaml(msg.label, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const TargetPosition & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace detection_msgs

namespace rosidl_generator_traits
{

[[deprecated("use detection_msgs::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const detection_msgs::msg::TargetPosition & msg,
  std::ostream & out, size_t indentation = 0)
{
  detection_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use detection_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const detection_msgs::msg::TargetPosition & msg)
{
  return detection_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<detection_msgs::msg::TargetPosition>()
{
  return "detection_msgs::msg::TargetPosition";
}

template<>
inline const char * name<detection_msgs::msg::TargetPosition>()
{
  return "detection_msgs/msg/TargetPosition";
}

template<>
struct has_fixed_size<detection_msgs::msg::TargetPosition>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<detection_msgs::msg::TargetPosition>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<detection_msgs::msg::TargetPosition>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // DETECTION_MSGS__MSG__DETAIL__TARGET_POSITION__TRAITS_HPP_

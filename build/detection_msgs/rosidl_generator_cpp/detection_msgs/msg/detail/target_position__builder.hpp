// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from detection_msgs:msg/TargetPosition.idl
// generated code does not contain a copyright notice

#ifndef DETECTION_MSGS__MSG__DETAIL__TARGET_POSITION__BUILDER_HPP_
#define DETECTION_MSGS__MSG__DETAIL__TARGET_POSITION__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "detection_msgs/msg/detail/target_position__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace detection_msgs
{

namespace msg
{

namespace builder
{

class Init_TargetPosition_label
{
public:
  explicit Init_TargetPosition_label(::detection_msgs::msg::TargetPosition & msg)
  : msg_(msg)
  {}
  ::detection_msgs::msg::TargetPosition label(::detection_msgs::msg::TargetPosition::_label_type arg)
  {
    msg_.label = std::move(arg);
    return std::move(msg_);
  }

private:
  ::detection_msgs::msg::TargetPosition msg_;
};

class Init_TargetPosition_position
{
public:
  explicit Init_TargetPosition_position(::detection_msgs::msg::TargetPosition & msg)
  : msg_(msg)
  {}
  Init_TargetPosition_label position(::detection_msgs::msg::TargetPosition::_position_type arg)
  {
    msg_.position = std::move(arg);
    return Init_TargetPosition_label(msg_);
  }

private:
  ::detection_msgs::msg::TargetPosition msg_;
};

class Init_TargetPosition_confidence
{
public:
  explicit Init_TargetPosition_confidence(::detection_msgs::msg::TargetPosition & msg)
  : msg_(msg)
  {}
  Init_TargetPosition_position confidence(::detection_msgs::msg::TargetPosition::_confidence_type arg)
  {
    msg_.confidence = std::move(arg);
    return Init_TargetPosition_position(msg_);
  }

private:
  ::detection_msgs::msg::TargetPosition msg_;
};

class Init_TargetPosition_class_id
{
public:
  explicit Init_TargetPosition_class_id(::detection_msgs::msg::TargetPosition & msg)
  : msg_(msg)
  {}
  Init_TargetPosition_confidence class_id(::detection_msgs::msg::TargetPosition::_class_id_type arg)
  {
    msg_.class_id = std::move(arg);
    return Init_TargetPosition_confidence(msg_);
  }

private:
  ::detection_msgs::msg::TargetPosition msg_;
};

class Init_TargetPosition_id
{
public:
  explicit Init_TargetPosition_id(::detection_msgs::msg::TargetPosition & msg)
  : msg_(msg)
  {}
  Init_TargetPosition_class_id id(::detection_msgs::msg::TargetPosition::_id_type arg)
  {
    msg_.id = std::move(arg);
    return Init_TargetPosition_class_id(msg_);
  }

private:
  ::detection_msgs::msg::TargetPosition msg_;
};

class Init_TargetPosition_header
{
public:
  Init_TargetPosition_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_TargetPosition_id header(::detection_msgs::msg::TargetPosition::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_TargetPosition_id(msg_);
  }

private:
  ::detection_msgs::msg::TargetPosition msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::detection_msgs::msg::TargetPosition>()
{
  return detection_msgs::msg::builder::Init_TargetPosition_header();
}

}  // namespace detection_msgs

#endif  // DETECTION_MSGS__MSG__DETAIL__TARGET_POSITION__BUILDER_HPP_

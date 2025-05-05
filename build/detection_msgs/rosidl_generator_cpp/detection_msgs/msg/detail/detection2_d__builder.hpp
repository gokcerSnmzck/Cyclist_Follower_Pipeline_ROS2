// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from detection_msgs:msg/Detection2D.idl
// generated code does not contain a copyright notice

#ifndef DETECTION_MSGS__MSG__DETAIL__DETECTION2_D__BUILDER_HPP_
#define DETECTION_MSGS__MSG__DETAIL__DETECTION2_D__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "detection_msgs/msg/detail/detection2_d__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace detection_msgs
{

namespace msg
{

namespace builder
{

class Init_Detection2D_bbox
{
public:
  explicit Init_Detection2D_bbox(::detection_msgs::msg::Detection2D & msg)
  : msg_(msg)
  {}
  ::detection_msgs::msg::Detection2D bbox(::detection_msgs::msg::Detection2D::_bbox_type arg)
  {
    msg_.bbox = std::move(arg);
    return std::move(msg_);
  }

private:
  ::detection_msgs::msg::Detection2D msg_;
};

class Init_Detection2D_confidence
{
public:
  explicit Init_Detection2D_confidence(::detection_msgs::msg::Detection2D & msg)
  : msg_(msg)
  {}
  Init_Detection2D_bbox confidence(::detection_msgs::msg::Detection2D::_confidence_type arg)
  {
    msg_.confidence = std::move(arg);
    return Init_Detection2D_bbox(msg_);
  }

private:
  ::detection_msgs::msg::Detection2D msg_;
};

class Init_Detection2D_label
{
public:
  explicit Init_Detection2D_label(::detection_msgs::msg::Detection2D & msg)
  : msg_(msg)
  {}
  Init_Detection2D_confidence label(::detection_msgs::msg::Detection2D::_label_type arg)
  {
    msg_.label = std::move(arg);
    return Init_Detection2D_confidence(msg_);
  }

private:
  ::detection_msgs::msg::Detection2D msg_;
};

class Init_Detection2D_class_id
{
public:
  explicit Init_Detection2D_class_id(::detection_msgs::msg::Detection2D & msg)
  : msg_(msg)
  {}
  Init_Detection2D_label class_id(::detection_msgs::msg::Detection2D::_class_id_type arg)
  {
    msg_.class_id = std::move(arg);
    return Init_Detection2D_label(msg_);
  }

private:
  ::detection_msgs::msg::Detection2D msg_;
};

class Init_Detection2D_tracking_id
{
public:
  Init_Detection2D_tracking_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Detection2D_class_id tracking_id(::detection_msgs::msg::Detection2D::_tracking_id_type arg)
  {
    msg_.tracking_id = std::move(arg);
    return Init_Detection2D_class_id(msg_);
  }

private:
  ::detection_msgs::msg::Detection2D msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::detection_msgs::msg::Detection2D>()
{
  return detection_msgs::msg::builder::Init_Detection2D_tracking_id();
}

}  // namespace detection_msgs

#endif  // DETECTION_MSGS__MSG__DETAIL__DETECTION2_D__BUILDER_HPP_

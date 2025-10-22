// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from arm_interfaces:action/PickPlace.idl
// generated code does not contain a copyright notice

#ifndef ARM_INTERFACES__ACTION__DETAIL__PICK_PLACE__BUILDER_HPP_
#define ARM_INTERFACES__ACTION__DETAIL__PICK_PLACE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "arm_interfaces/action/detail/pick_place__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace arm_interfaces
{

namespace action
{

namespace builder
{

class Init_PickPlace_Goal_lift_distance
{
public:
  explicit Init_PickPlace_Goal_lift_distance(::arm_interfaces::action::PickPlace_Goal & msg)
  : msg_(msg)
  {}
  ::arm_interfaces::action::PickPlace_Goal lift_distance(::arm_interfaces::action::PickPlace_Goal::_lift_distance_type arg)
  {
    msg_.lift_distance = std::move(arg);
    return std::move(msg_);
  }

private:
  ::arm_interfaces::action::PickPlace_Goal msg_;
};

class Init_PickPlace_Goal_place_pose
{
public:
  explicit Init_PickPlace_Goal_place_pose(::arm_interfaces::action::PickPlace_Goal & msg)
  : msg_(msg)
  {}
  Init_PickPlace_Goal_lift_distance place_pose(::arm_interfaces::action::PickPlace_Goal::_place_pose_type arg)
  {
    msg_.place_pose = std::move(arg);
    return Init_PickPlace_Goal_lift_distance(msg_);
  }

private:
  ::arm_interfaces::action::PickPlace_Goal msg_;
};

class Init_PickPlace_Goal_pick_pose
{
public:
  Init_PickPlace_Goal_pick_pose()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PickPlace_Goal_place_pose pick_pose(::arm_interfaces::action::PickPlace_Goal::_pick_pose_type arg)
  {
    msg_.pick_pose = std::move(arg);
    return Init_PickPlace_Goal_place_pose(msg_);
  }

private:
  ::arm_interfaces::action::PickPlace_Goal msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::arm_interfaces::action::PickPlace_Goal>()
{
  return arm_interfaces::action::builder::Init_PickPlace_Goal_pick_pose();
}

}  // namespace arm_interfaces


namespace arm_interfaces
{

namespace action
{

namespace builder
{

class Init_PickPlace_Result_message
{
public:
  explicit Init_PickPlace_Result_message(::arm_interfaces::action::PickPlace_Result & msg)
  : msg_(msg)
  {}
  ::arm_interfaces::action::PickPlace_Result message(::arm_interfaces::action::PickPlace_Result::_message_type arg)
  {
    msg_.message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::arm_interfaces::action::PickPlace_Result msg_;
};

class Init_PickPlace_Result_success
{
public:
  Init_PickPlace_Result_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PickPlace_Result_message success(::arm_interfaces::action::PickPlace_Result::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_PickPlace_Result_message(msg_);
  }

private:
  ::arm_interfaces::action::PickPlace_Result msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::arm_interfaces::action::PickPlace_Result>()
{
  return arm_interfaces::action::builder::Init_PickPlace_Result_success();
}

}  // namespace arm_interfaces


namespace arm_interfaces
{

namespace action
{

namespace builder
{

class Init_PickPlace_Feedback_stage
{
public:
  explicit Init_PickPlace_Feedback_stage(::arm_interfaces::action::PickPlace_Feedback & msg)
  : msg_(msg)
  {}
  ::arm_interfaces::action::PickPlace_Feedback stage(::arm_interfaces::action::PickPlace_Feedback::_stage_type arg)
  {
    msg_.stage = std::move(arg);
    return std::move(msg_);
  }

private:
  ::arm_interfaces::action::PickPlace_Feedback msg_;
};

class Init_PickPlace_Feedback_progress_percent
{
public:
  Init_PickPlace_Feedback_progress_percent()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PickPlace_Feedback_stage progress_percent(::arm_interfaces::action::PickPlace_Feedback::_progress_percent_type arg)
  {
    msg_.progress_percent = std::move(arg);
    return Init_PickPlace_Feedback_stage(msg_);
  }

private:
  ::arm_interfaces::action::PickPlace_Feedback msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::arm_interfaces::action::PickPlace_Feedback>()
{
  return arm_interfaces::action::builder::Init_PickPlace_Feedback_progress_percent();
}

}  // namespace arm_interfaces


namespace arm_interfaces
{

namespace action
{

namespace builder
{

class Init_PickPlace_SendGoal_Request_goal
{
public:
  explicit Init_PickPlace_SendGoal_Request_goal(::arm_interfaces::action::PickPlace_SendGoal_Request & msg)
  : msg_(msg)
  {}
  ::arm_interfaces::action::PickPlace_SendGoal_Request goal(::arm_interfaces::action::PickPlace_SendGoal_Request::_goal_type arg)
  {
    msg_.goal = std::move(arg);
    return std::move(msg_);
  }

private:
  ::arm_interfaces::action::PickPlace_SendGoal_Request msg_;
};

class Init_PickPlace_SendGoal_Request_goal_id
{
public:
  Init_PickPlace_SendGoal_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PickPlace_SendGoal_Request_goal goal_id(::arm_interfaces::action::PickPlace_SendGoal_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_PickPlace_SendGoal_Request_goal(msg_);
  }

private:
  ::arm_interfaces::action::PickPlace_SendGoal_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::arm_interfaces::action::PickPlace_SendGoal_Request>()
{
  return arm_interfaces::action::builder::Init_PickPlace_SendGoal_Request_goal_id();
}

}  // namespace arm_interfaces


namespace arm_interfaces
{

namespace action
{

namespace builder
{

class Init_PickPlace_SendGoal_Response_stamp
{
public:
  explicit Init_PickPlace_SendGoal_Response_stamp(::arm_interfaces::action::PickPlace_SendGoal_Response & msg)
  : msg_(msg)
  {}
  ::arm_interfaces::action::PickPlace_SendGoal_Response stamp(::arm_interfaces::action::PickPlace_SendGoal_Response::_stamp_type arg)
  {
    msg_.stamp = std::move(arg);
    return std::move(msg_);
  }

private:
  ::arm_interfaces::action::PickPlace_SendGoal_Response msg_;
};

class Init_PickPlace_SendGoal_Response_accepted
{
public:
  Init_PickPlace_SendGoal_Response_accepted()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PickPlace_SendGoal_Response_stamp accepted(::arm_interfaces::action::PickPlace_SendGoal_Response::_accepted_type arg)
  {
    msg_.accepted = std::move(arg);
    return Init_PickPlace_SendGoal_Response_stamp(msg_);
  }

private:
  ::arm_interfaces::action::PickPlace_SendGoal_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::arm_interfaces::action::PickPlace_SendGoal_Response>()
{
  return arm_interfaces::action::builder::Init_PickPlace_SendGoal_Response_accepted();
}

}  // namespace arm_interfaces


namespace arm_interfaces
{

namespace action
{

namespace builder
{

class Init_PickPlace_GetResult_Request_goal_id
{
public:
  Init_PickPlace_GetResult_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::arm_interfaces::action::PickPlace_GetResult_Request goal_id(::arm_interfaces::action::PickPlace_GetResult_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return std::move(msg_);
  }

private:
  ::arm_interfaces::action::PickPlace_GetResult_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::arm_interfaces::action::PickPlace_GetResult_Request>()
{
  return arm_interfaces::action::builder::Init_PickPlace_GetResult_Request_goal_id();
}

}  // namespace arm_interfaces


namespace arm_interfaces
{

namespace action
{

namespace builder
{

class Init_PickPlace_GetResult_Response_result
{
public:
  explicit Init_PickPlace_GetResult_Response_result(::arm_interfaces::action::PickPlace_GetResult_Response & msg)
  : msg_(msg)
  {}
  ::arm_interfaces::action::PickPlace_GetResult_Response result(::arm_interfaces::action::PickPlace_GetResult_Response::_result_type arg)
  {
    msg_.result = std::move(arg);
    return std::move(msg_);
  }

private:
  ::arm_interfaces::action::PickPlace_GetResult_Response msg_;
};

class Init_PickPlace_GetResult_Response_status
{
public:
  Init_PickPlace_GetResult_Response_status()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PickPlace_GetResult_Response_result status(::arm_interfaces::action::PickPlace_GetResult_Response::_status_type arg)
  {
    msg_.status = std::move(arg);
    return Init_PickPlace_GetResult_Response_result(msg_);
  }

private:
  ::arm_interfaces::action::PickPlace_GetResult_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::arm_interfaces::action::PickPlace_GetResult_Response>()
{
  return arm_interfaces::action::builder::Init_PickPlace_GetResult_Response_status();
}

}  // namespace arm_interfaces


namespace arm_interfaces
{

namespace action
{

namespace builder
{

class Init_PickPlace_FeedbackMessage_feedback
{
public:
  explicit Init_PickPlace_FeedbackMessage_feedback(::arm_interfaces::action::PickPlace_FeedbackMessage & msg)
  : msg_(msg)
  {}
  ::arm_interfaces::action::PickPlace_FeedbackMessage feedback(::arm_interfaces::action::PickPlace_FeedbackMessage::_feedback_type arg)
  {
    msg_.feedback = std::move(arg);
    return std::move(msg_);
  }

private:
  ::arm_interfaces::action::PickPlace_FeedbackMessage msg_;
};

class Init_PickPlace_FeedbackMessage_goal_id
{
public:
  Init_PickPlace_FeedbackMessage_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PickPlace_FeedbackMessage_feedback goal_id(::arm_interfaces::action::PickPlace_FeedbackMessage::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_PickPlace_FeedbackMessage_feedback(msg_);
  }

private:
  ::arm_interfaces::action::PickPlace_FeedbackMessage msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::arm_interfaces::action::PickPlace_FeedbackMessage>()
{
  return arm_interfaces::action::builder::Init_PickPlace_FeedbackMessage_goal_id();
}

}  // namespace arm_interfaces

#endif  // ARM_INTERFACES__ACTION__DETAIL__PICK_PLACE__BUILDER_HPP_

// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from chess_arm_executor:action/ExecuteMove.idl
// generated code does not contain a copyright notice

#ifndef CHESS_ARM_EXECUTOR__ACTION__DETAIL__EXECUTE_MOVE__BUILDER_HPP_
#define CHESS_ARM_EXECUTOR__ACTION__DETAIL__EXECUTE_MOVE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "chess_arm_executor/action/detail/execute_move__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace chess_arm_executor
{

namespace action
{

namespace builder
{

class Init_ExecuteMove_Goal_piece_type
{
public:
  explicit Init_ExecuteMove_Goal_piece_type(::chess_arm_executor::action::ExecuteMove_Goal & msg)
  : msg_(msg)
  {}
  ::chess_arm_executor::action::ExecuteMove_Goal piece_type(::chess_arm_executor::action::ExecuteMove_Goal::_piece_type_type arg)
  {
    msg_.piece_type = std::move(arg);
    return std::move(msg_);
  }

private:
  ::chess_arm_executor::action::ExecuteMove_Goal msg_;
};

class Init_ExecuteMove_Goal_dst_square
{
public:
  explicit Init_ExecuteMove_Goal_dst_square(::chess_arm_executor::action::ExecuteMove_Goal & msg)
  : msg_(msg)
  {}
  Init_ExecuteMove_Goal_piece_type dst_square(::chess_arm_executor::action::ExecuteMove_Goal::_dst_square_type arg)
  {
    msg_.dst_square = std::move(arg);
    return Init_ExecuteMove_Goal_piece_type(msg_);
  }

private:
  ::chess_arm_executor::action::ExecuteMove_Goal msg_;
};

class Init_ExecuteMove_Goal_src_square
{
public:
  Init_ExecuteMove_Goal_src_square()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ExecuteMove_Goal_dst_square src_square(::chess_arm_executor::action::ExecuteMove_Goal::_src_square_type arg)
  {
    msg_.src_square = std::move(arg);
    return Init_ExecuteMove_Goal_dst_square(msg_);
  }

private:
  ::chess_arm_executor::action::ExecuteMove_Goal msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::chess_arm_executor::action::ExecuteMove_Goal>()
{
  return chess_arm_executor::action::builder::Init_ExecuteMove_Goal_src_square();
}

}  // namespace chess_arm_executor


namespace chess_arm_executor
{

namespace action
{

namespace builder
{

class Init_ExecuteMove_Result_z_pick_used
{
public:
  explicit Init_ExecuteMove_Result_z_pick_used(::chess_arm_executor::action::ExecuteMove_Result & msg)
  : msg_(msg)
  {}
  ::chess_arm_executor::action::ExecuteMove_Result z_pick_used(::chess_arm_executor::action::ExecuteMove_Result::_z_pick_used_type arg)
  {
    msg_.z_pick_used = std::move(arg);
    return std::move(msg_);
  }

private:
  ::chess_arm_executor::action::ExecuteMove_Result msg_;
};

class Init_ExecuteMove_Result_message
{
public:
  explicit Init_ExecuteMove_Result_message(::chess_arm_executor::action::ExecuteMove_Result & msg)
  : msg_(msg)
  {}
  Init_ExecuteMove_Result_z_pick_used message(::chess_arm_executor::action::ExecuteMove_Result::_message_type arg)
  {
    msg_.message = std::move(arg);
    return Init_ExecuteMove_Result_z_pick_used(msg_);
  }

private:
  ::chess_arm_executor::action::ExecuteMove_Result msg_;
};

class Init_ExecuteMove_Result_ok
{
public:
  Init_ExecuteMove_Result_ok()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ExecuteMove_Result_message ok(::chess_arm_executor::action::ExecuteMove_Result::_ok_type arg)
  {
    msg_.ok = std::move(arg);
    return Init_ExecuteMove_Result_message(msg_);
  }

private:
  ::chess_arm_executor::action::ExecuteMove_Result msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::chess_arm_executor::action::ExecuteMove_Result>()
{
  return chess_arm_executor::action::builder::Init_ExecuteMove_Result_ok();
}

}  // namespace chess_arm_executor


namespace chess_arm_executor
{

namespace action
{

namespace builder
{

class Init_ExecuteMove_Feedback_z_pick_used
{
public:
  explicit Init_ExecuteMove_Feedback_z_pick_used(::chess_arm_executor::action::ExecuteMove_Feedback & msg)
  : msg_(msg)
  {}
  ::chess_arm_executor::action::ExecuteMove_Feedback z_pick_used(::chess_arm_executor::action::ExecuteMove_Feedback::_z_pick_used_type arg)
  {
    msg_.z_pick_used = std::move(arg);
    return std::move(msg_);
  }

private:
  ::chess_arm_executor::action::ExecuteMove_Feedback msg_;
};

class Init_ExecuteMove_Feedback_stage
{
public:
  Init_ExecuteMove_Feedback_stage()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ExecuteMove_Feedback_z_pick_used stage(::chess_arm_executor::action::ExecuteMove_Feedback::_stage_type arg)
  {
    msg_.stage = std::move(arg);
    return Init_ExecuteMove_Feedback_z_pick_used(msg_);
  }

private:
  ::chess_arm_executor::action::ExecuteMove_Feedback msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::chess_arm_executor::action::ExecuteMove_Feedback>()
{
  return chess_arm_executor::action::builder::Init_ExecuteMove_Feedback_stage();
}

}  // namespace chess_arm_executor


namespace chess_arm_executor
{

namespace action
{

namespace builder
{

class Init_ExecuteMove_SendGoal_Request_goal
{
public:
  explicit Init_ExecuteMove_SendGoal_Request_goal(::chess_arm_executor::action::ExecuteMove_SendGoal_Request & msg)
  : msg_(msg)
  {}
  ::chess_arm_executor::action::ExecuteMove_SendGoal_Request goal(::chess_arm_executor::action::ExecuteMove_SendGoal_Request::_goal_type arg)
  {
    msg_.goal = std::move(arg);
    return std::move(msg_);
  }

private:
  ::chess_arm_executor::action::ExecuteMove_SendGoal_Request msg_;
};

class Init_ExecuteMove_SendGoal_Request_goal_id
{
public:
  Init_ExecuteMove_SendGoal_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ExecuteMove_SendGoal_Request_goal goal_id(::chess_arm_executor::action::ExecuteMove_SendGoal_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_ExecuteMove_SendGoal_Request_goal(msg_);
  }

private:
  ::chess_arm_executor::action::ExecuteMove_SendGoal_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::chess_arm_executor::action::ExecuteMove_SendGoal_Request>()
{
  return chess_arm_executor::action::builder::Init_ExecuteMove_SendGoal_Request_goal_id();
}

}  // namespace chess_arm_executor


namespace chess_arm_executor
{

namespace action
{

namespace builder
{

class Init_ExecuteMove_SendGoal_Response_stamp
{
public:
  explicit Init_ExecuteMove_SendGoal_Response_stamp(::chess_arm_executor::action::ExecuteMove_SendGoal_Response & msg)
  : msg_(msg)
  {}
  ::chess_arm_executor::action::ExecuteMove_SendGoal_Response stamp(::chess_arm_executor::action::ExecuteMove_SendGoal_Response::_stamp_type arg)
  {
    msg_.stamp = std::move(arg);
    return std::move(msg_);
  }

private:
  ::chess_arm_executor::action::ExecuteMove_SendGoal_Response msg_;
};

class Init_ExecuteMove_SendGoal_Response_accepted
{
public:
  Init_ExecuteMove_SendGoal_Response_accepted()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ExecuteMove_SendGoal_Response_stamp accepted(::chess_arm_executor::action::ExecuteMove_SendGoal_Response::_accepted_type arg)
  {
    msg_.accepted = std::move(arg);
    return Init_ExecuteMove_SendGoal_Response_stamp(msg_);
  }

private:
  ::chess_arm_executor::action::ExecuteMove_SendGoal_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::chess_arm_executor::action::ExecuteMove_SendGoal_Response>()
{
  return chess_arm_executor::action::builder::Init_ExecuteMove_SendGoal_Response_accepted();
}

}  // namespace chess_arm_executor


namespace chess_arm_executor
{

namespace action
{

namespace builder
{

class Init_ExecuteMove_GetResult_Request_goal_id
{
public:
  Init_ExecuteMove_GetResult_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::chess_arm_executor::action::ExecuteMove_GetResult_Request goal_id(::chess_arm_executor::action::ExecuteMove_GetResult_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return std::move(msg_);
  }

private:
  ::chess_arm_executor::action::ExecuteMove_GetResult_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::chess_arm_executor::action::ExecuteMove_GetResult_Request>()
{
  return chess_arm_executor::action::builder::Init_ExecuteMove_GetResult_Request_goal_id();
}

}  // namespace chess_arm_executor


namespace chess_arm_executor
{

namespace action
{

namespace builder
{

class Init_ExecuteMove_GetResult_Response_result
{
public:
  explicit Init_ExecuteMove_GetResult_Response_result(::chess_arm_executor::action::ExecuteMove_GetResult_Response & msg)
  : msg_(msg)
  {}
  ::chess_arm_executor::action::ExecuteMove_GetResult_Response result(::chess_arm_executor::action::ExecuteMove_GetResult_Response::_result_type arg)
  {
    msg_.result = std::move(arg);
    return std::move(msg_);
  }

private:
  ::chess_arm_executor::action::ExecuteMove_GetResult_Response msg_;
};

class Init_ExecuteMove_GetResult_Response_status
{
public:
  Init_ExecuteMove_GetResult_Response_status()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ExecuteMove_GetResult_Response_result status(::chess_arm_executor::action::ExecuteMove_GetResult_Response::_status_type arg)
  {
    msg_.status = std::move(arg);
    return Init_ExecuteMove_GetResult_Response_result(msg_);
  }

private:
  ::chess_arm_executor::action::ExecuteMove_GetResult_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::chess_arm_executor::action::ExecuteMove_GetResult_Response>()
{
  return chess_arm_executor::action::builder::Init_ExecuteMove_GetResult_Response_status();
}

}  // namespace chess_arm_executor


namespace chess_arm_executor
{

namespace action
{

namespace builder
{

class Init_ExecuteMove_FeedbackMessage_feedback
{
public:
  explicit Init_ExecuteMove_FeedbackMessage_feedback(::chess_arm_executor::action::ExecuteMove_FeedbackMessage & msg)
  : msg_(msg)
  {}
  ::chess_arm_executor::action::ExecuteMove_FeedbackMessage feedback(::chess_arm_executor::action::ExecuteMove_FeedbackMessage::_feedback_type arg)
  {
    msg_.feedback = std::move(arg);
    return std::move(msg_);
  }

private:
  ::chess_arm_executor::action::ExecuteMove_FeedbackMessage msg_;
};

class Init_ExecuteMove_FeedbackMessage_goal_id
{
public:
  Init_ExecuteMove_FeedbackMessage_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ExecuteMove_FeedbackMessage_feedback goal_id(::chess_arm_executor::action::ExecuteMove_FeedbackMessage::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_ExecuteMove_FeedbackMessage_feedback(msg_);
  }

private:
  ::chess_arm_executor::action::ExecuteMove_FeedbackMessage msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::chess_arm_executor::action::ExecuteMove_FeedbackMessage>()
{
  return chess_arm_executor::action::builder::Init_ExecuteMove_FeedbackMessage_goal_id();
}

}  // namespace chess_arm_executor

#endif  // CHESS_ARM_EXECUTOR__ACTION__DETAIL__EXECUTE_MOVE__BUILDER_HPP_

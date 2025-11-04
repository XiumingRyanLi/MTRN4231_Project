// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from interfaces:srv/ChessMove.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES__SRV__DETAIL__CHESS_MOVE__BUILDER_HPP_
#define INTERFACES__SRV__DETAIL__CHESS_MOVE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "interfaces/srv/detail/chess_move__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace interfaces
{

namespace srv
{

namespace builder
{

class Init_ChessMove_Request_user_move
{
public:
  Init_ChessMove_Request_user_move()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::interfaces::srv::ChessMove_Request user_move(::interfaces::srv::ChessMove_Request::_user_move_type arg)
  {
    msg_.user_move = std::move(arg);
    return std::move(msg_);
  }

private:
  ::interfaces::srv::ChessMove_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::interfaces::srv::ChessMove_Request>()
{
  return interfaces::srv::builder::Init_ChessMove_Request_user_move();
}

}  // namespace interfaces


namespace interfaces
{

namespace srv
{

namespace builder
{

class Init_ChessMove_Response_is_promotion
{
public:
  explicit Init_ChessMove_Response_is_promotion(::interfaces::srv::ChessMove_Response & msg)
  : msg_(msg)
  {}
  ::interfaces::srv::ChessMove_Response is_promotion(::interfaces::srv::ChessMove_Response::_is_promotion_type arg)
  {
    msg_.is_promotion = std::move(arg);
    return std::move(msg_);
  }

private:
  ::interfaces::srv::ChessMove_Response msg_;
};

class Init_ChessMove_Response_is_castling
{
public:
  explicit Init_ChessMove_Response_is_castling(::interfaces::srv::ChessMove_Response & msg)
  : msg_(msg)
  {}
  Init_ChessMove_Response_is_promotion is_castling(::interfaces::srv::ChessMove_Response::_is_castling_type arg)
  {
    msg_.is_castling = std::move(arg);
    return Init_ChessMove_Response_is_promotion(msg_);
  }

private:
  ::interfaces::srv::ChessMove_Response msg_;
};

class Init_ChessMove_Response_is_capture
{
public:
  explicit Init_ChessMove_Response_is_capture(::interfaces::srv::ChessMove_Response & msg)
  : msg_(msg)
  {}
  Init_ChessMove_Response_is_castling is_capture(::interfaces::srv::ChessMove_Response::_is_capture_type arg)
  {
    msg_.is_capture = std::move(arg);
    return Init_ChessMove_Response_is_castling(msg_);
  }

private:
  ::interfaces::srv::ChessMove_Response msg_;
};

class Init_ChessMove_Response_is_en_passant
{
public:
  explicit Init_ChessMove_Response_is_en_passant(::interfaces::srv::ChessMove_Response & msg)
  : msg_(msg)
  {}
  Init_ChessMove_Response_is_capture is_en_passant(::interfaces::srv::ChessMove_Response::_is_en_passant_type arg)
  {
    msg_.is_en_passant = std::move(arg);
    return Init_ChessMove_Response_is_capture(msg_);
  }

private:
  ::interfaces::srv::ChessMove_Response msg_;
};

class Init_ChessMove_Response_robot_move
{
public:
  Init_ChessMove_Response_robot_move()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ChessMove_Response_is_en_passant robot_move(::interfaces::srv::ChessMove_Response::_robot_move_type arg)
  {
    msg_.robot_move = std::move(arg);
    return Init_ChessMove_Response_is_en_passant(msg_);
  }

private:
  ::interfaces::srv::ChessMove_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::interfaces::srv::ChessMove_Response>()
{
  return interfaces::srv::builder::Init_ChessMove_Response_robot_move();
}

}  // namespace interfaces

#endif  // INTERFACES__SRV__DETAIL__CHESS_MOVE__BUILDER_HPP_

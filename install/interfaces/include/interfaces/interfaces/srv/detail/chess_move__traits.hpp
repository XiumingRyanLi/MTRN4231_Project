// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from interfaces:srv/ChessMove.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES__SRV__DETAIL__CHESS_MOVE__TRAITS_HPP_
#define INTERFACES__SRV__DETAIL__CHESS_MOVE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "interfaces/srv/detail/chess_move__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const ChessMove_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: user_move
  {
    out << "user_move: ";
    rosidl_generator_traits::value_to_yaml(msg.user_move, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ChessMove_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: user_move
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "user_move: ";
    rosidl_generator_traits::value_to_yaml(msg.user_move, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ChessMove_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace interfaces

namespace rosidl_generator_traits
{

[[deprecated("use interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const interfaces::srv::ChessMove_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const interfaces::srv::ChessMove_Request & msg)
{
  return interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<interfaces::srv::ChessMove_Request>()
{
  return "interfaces::srv::ChessMove_Request";
}

template<>
inline const char * name<interfaces::srv::ChessMove_Request>()
{
  return "interfaces/srv/ChessMove_Request";
}

template<>
struct has_fixed_size<interfaces::srv::ChessMove_Request>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<interfaces::srv::ChessMove_Request>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<interfaces::srv::ChessMove_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const ChessMove_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: robot_move
  {
    out << "robot_move: ";
    rosidl_generator_traits::value_to_yaml(msg.robot_move, out);
    out << ", ";
  }

  // member: is_en_passant
  {
    out << "is_en_passant: ";
    rosidl_generator_traits::value_to_yaml(msg.is_en_passant, out);
    out << ", ";
  }

  // member: is_capture
  {
    out << "is_capture: ";
    rosidl_generator_traits::value_to_yaml(msg.is_capture, out);
    out << ", ";
  }

  // member: is_castling
  {
    out << "is_castling: ";
    rosidl_generator_traits::value_to_yaml(msg.is_castling, out);
    out << ", ";
  }

  // member: is_promotion
  {
    out << "is_promotion: ";
    rosidl_generator_traits::value_to_yaml(msg.is_promotion, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ChessMove_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: robot_move
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "robot_move: ";
    rosidl_generator_traits::value_to_yaml(msg.robot_move, out);
    out << "\n";
  }

  // member: is_en_passant
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "is_en_passant: ";
    rosidl_generator_traits::value_to_yaml(msg.is_en_passant, out);
    out << "\n";
  }

  // member: is_capture
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "is_capture: ";
    rosidl_generator_traits::value_to_yaml(msg.is_capture, out);
    out << "\n";
  }

  // member: is_castling
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "is_castling: ";
    rosidl_generator_traits::value_to_yaml(msg.is_castling, out);
    out << "\n";
  }

  // member: is_promotion
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "is_promotion: ";
    rosidl_generator_traits::value_to_yaml(msg.is_promotion, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ChessMove_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace interfaces

namespace rosidl_generator_traits
{

[[deprecated("use interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const interfaces::srv::ChessMove_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const interfaces::srv::ChessMove_Response & msg)
{
  return interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<interfaces::srv::ChessMove_Response>()
{
  return "interfaces::srv::ChessMove_Response";
}

template<>
inline const char * name<interfaces::srv::ChessMove_Response>()
{
  return "interfaces/srv/ChessMove_Response";
}

template<>
struct has_fixed_size<interfaces::srv::ChessMove_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<interfaces::srv::ChessMove_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<interfaces::srv::ChessMove_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<interfaces::srv::ChessMove>()
{
  return "interfaces::srv::ChessMove";
}

template<>
inline const char * name<interfaces::srv::ChessMove>()
{
  return "interfaces/srv/ChessMove";
}

template<>
struct has_fixed_size<interfaces::srv::ChessMove>
  : std::integral_constant<
    bool,
    has_fixed_size<interfaces::srv::ChessMove_Request>::value &&
    has_fixed_size<interfaces::srv::ChessMove_Response>::value
  >
{
};

template<>
struct has_bounded_size<interfaces::srv::ChessMove>
  : std::integral_constant<
    bool,
    has_bounded_size<interfaces::srv::ChessMove_Request>::value &&
    has_bounded_size<interfaces::srv::ChessMove_Response>::value
  >
{
};

template<>
struct is_service<interfaces::srv::ChessMove>
  : std::true_type
{
};

template<>
struct is_service_request<interfaces::srv::ChessMove_Request>
  : std::true_type
{
};

template<>
struct is_service_response<interfaces::srv::ChessMove_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // INTERFACES__SRV__DETAIL__CHESS_MOVE__TRAITS_HPP_

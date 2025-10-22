// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from arm_interfaces:action/PickPlace.idl
// generated code does not contain a copyright notice

#ifndef ARM_INTERFACES__ACTION__DETAIL__PICK_PLACE__TRAITS_HPP_
#define ARM_INTERFACES__ACTION__DETAIL__PICK_PLACE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "arm_interfaces/action/detail/pick_place__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'pick_pose'
// Member 'place_pose'
#include "geometry_msgs/msg/detail/pose_stamped__traits.hpp"

namespace arm_interfaces
{

namespace action
{

inline void to_flow_style_yaml(
  const PickPlace_Goal & msg,
  std::ostream & out)
{
  out << "{";
  // member: pick_pose
  {
    out << "pick_pose: ";
    to_flow_style_yaml(msg.pick_pose, out);
    out << ", ";
  }

  // member: place_pose
  {
    out << "place_pose: ";
    to_flow_style_yaml(msg.place_pose, out);
    out << ", ";
  }

  // member: lift_distance
  {
    out << "lift_distance: ";
    rosidl_generator_traits::value_to_yaml(msg.lift_distance, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const PickPlace_Goal & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: pick_pose
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "pick_pose:\n";
    to_block_style_yaml(msg.pick_pose, out, indentation + 2);
  }

  // member: place_pose
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "place_pose:\n";
    to_block_style_yaml(msg.place_pose, out, indentation + 2);
  }

  // member: lift_distance
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "lift_distance: ";
    rosidl_generator_traits::value_to_yaml(msg.lift_distance, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const PickPlace_Goal & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace arm_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use arm_interfaces::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const arm_interfaces::action::PickPlace_Goal & msg,
  std::ostream & out, size_t indentation = 0)
{
  arm_interfaces::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use arm_interfaces::action::to_yaml() instead")]]
inline std::string to_yaml(const arm_interfaces::action::PickPlace_Goal & msg)
{
  return arm_interfaces::action::to_yaml(msg);
}

template<>
inline const char * data_type<arm_interfaces::action::PickPlace_Goal>()
{
  return "arm_interfaces::action::PickPlace_Goal";
}

template<>
inline const char * name<arm_interfaces::action::PickPlace_Goal>()
{
  return "arm_interfaces/action/PickPlace_Goal";
}

template<>
struct has_fixed_size<arm_interfaces::action::PickPlace_Goal>
  : std::integral_constant<bool, has_fixed_size<geometry_msgs::msg::PoseStamped>::value> {};

template<>
struct has_bounded_size<arm_interfaces::action::PickPlace_Goal>
  : std::integral_constant<bool, has_bounded_size<geometry_msgs::msg::PoseStamped>::value> {};

template<>
struct is_message<arm_interfaces::action::PickPlace_Goal>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace arm_interfaces
{

namespace action
{

inline void to_flow_style_yaml(
  const PickPlace_Result & msg,
  std::ostream & out)
{
  out << "{";
  // member: success
  {
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << ", ";
  }

  // member: message
  {
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const PickPlace_Result & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: success
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << "\n";
  }

  // member: message
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const PickPlace_Result & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace arm_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use arm_interfaces::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const arm_interfaces::action::PickPlace_Result & msg,
  std::ostream & out, size_t indentation = 0)
{
  arm_interfaces::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use arm_interfaces::action::to_yaml() instead")]]
inline std::string to_yaml(const arm_interfaces::action::PickPlace_Result & msg)
{
  return arm_interfaces::action::to_yaml(msg);
}

template<>
inline const char * data_type<arm_interfaces::action::PickPlace_Result>()
{
  return "arm_interfaces::action::PickPlace_Result";
}

template<>
inline const char * name<arm_interfaces::action::PickPlace_Result>()
{
  return "arm_interfaces/action/PickPlace_Result";
}

template<>
struct has_fixed_size<arm_interfaces::action::PickPlace_Result>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<arm_interfaces::action::PickPlace_Result>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<arm_interfaces::action::PickPlace_Result>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace arm_interfaces
{

namespace action
{

inline void to_flow_style_yaml(
  const PickPlace_Feedback & msg,
  std::ostream & out)
{
  out << "{";
  // member: progress_percent
  {
    out << "progress_percent: ";
    rosidl_generator_traits::value_to_yaml(msg.progress_percent, out);
    out << ", ";
  }

  // member: stage
  {
    out << "stage: ";
    rosidl_generator_traits::value_to_yaml(msg.stage, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const PickPlace_Feedback & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: progress_percent
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "progress_percent: ";
    rosidl_generator_traits::value_to_yaml(msg.progress_percent, out);
    out << "\n";
  }

  // member: stage
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "stage: ";
    rosidl_generator_traits::value_to_yaml(msg.stage, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const PickPlace_Feedback & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace arm_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use arm_interfaces::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const arm_interfaces::action::PickPlace_Feedback & msg,
  std::ostream & out, size_t indentation = 0)
{
  arm_interfaces::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use arm_interfaces::action::to_yaml() instead")]]
inline std::string to_yaml(const arm_interfaces::action::PickPlace_Feedback & msg)
{
  return arm_interfaces::action::to_yaml(msg);
}

template<>
inline const char * data_type<arm_interfaces::action::PickPlace_Feedback>()
{
  return "arm_interfaces::action::PickPlace_Feedback";
}

template<>
inline const char * name<arm_interfaces::action::PickPlace_Feedback>()
{
  return "arm_interfaces/action/PickPlace_Feedback";
}

template<>
struct has_fixed_size<arm_interfaces::action::PickPlace_Feedback>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<arm_interfaces::action::PickPlace_Feedback>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<arm_interfaces::action::PickPlace_Feedback>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'goal_id'
#include "unique_identifier_msgs/msg/detail/uuid__traits.hpp"
// Member 'goal'
#include "arm_interfaces/action/detail/pick_place__traits.hpp"

namespace arm_interfaces
{

namespace action
{

inline void to_flow_style_yaml(
  const PickPlace_SendGoal_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: goal_id
  {
    out << "goal_id: ";
    to_flow_style_yaml(msg.goal_id, out);
    out << ", ";
  }

  // member: goal
  {
    out << "goal: ";
    to_flow_style_yaml(msg.goal, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const PickPlace_SendGoal_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: goal_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "goal_id:\n";
    to_block_style_yaml(msg.goal_id, out, indentation + 2);
  }

  // member: goal
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "goal:\n";
    to_block_style_yaml(msg.goal, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const PickPlace_SendGoal_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace arm_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use arm_interfaces::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const arm_interfaces::action::PickPlace_SendGoal_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  arm_interfaces::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use arm_interfaces::action::to_yaml() instead")]]
inline std::string to_yaml(const arm_interfaces::action::PickPlace_SendGoal_Request & msg)
{
  return arm_interfaces::action::to_yaml(msg);
}

template<>
inline const char * data_type<arm_interfaces::action::PickPlace_SendGoal_Request>()
{
  return "arm_interfaces::action::PickPlace_SendGoal_Request";
}

template<>
inline const char * name<arm_interfaces::action::PickPlace_SendGoal_Request>()
{
  return "arm_interfaces/action/PickPlace_SendGoal_Request";
}

template<>
struct has_fixed_size<arm_interfaces::action::PickPlace_SendGoal_Request>
  : std::integral_constant<bool, has_fixed_size<arm_interfaces::action::PickPlace_Goal>::value && has_fixed_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct has_bounded_size<arm_interfaces::action::PickPlace_SendGoal_Request>
  : std::integral_constant<bool, has_bounded_size<arm_interfaces::action::PickPlace_Goal>::value && has_bounded_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct is_message<arm_interfaces::action::PickPlace_SendGoal_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__traits.hpp"

namespace arm_interfaces
{

namespace action
{

inline void to_flow_style_yaml(
  const PickPlace_SendGoal_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: accepted
  {
    out << "accepted: ";
    rosidl_generator_traits::value_to_yaml(msg.accepted, out);
    out << ", ";
  }

  // member: stamp
  {
    out << "stamp: ";
    to_flow_style_yaml(msg.stamp, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const PickPlace_SendGoal_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: accepted
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "accepted: ";
    rosidl_generator_traits::value_to_yaml(msg.accepted, out);
    out << "\n";
  }

  // member: stamp
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "stamp:\n";
    to_block_style_yaml(msg.stamp, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const PickPlace_SendGoal_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace arm_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use arm_interfaces::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const arm_interfaces::action::PickPlace_SendGoal_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  arm_interfaces::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use arm_interfaces::action::to_yaml() instead")]]
inline std::string to_yaml(const arm_interfaces::action::PickPlace_SendGoal_Response & msg)
{
  return arm_interfaces::action::to_yaml(msg);
}

template<>
inline const char * data_type<arm_interfaces::action::PickPlace_SendGoal_Response>()
{
  return "arm_interfaces::action::PickPlace_SendGoal_Response";
}

template<>
inline const char * name<arm_interfaces::action::PickPlace_SendGoal_Response>()
{
  return "arm_interfaces/action/PickPlace_SendGoal_Response";
}

template<>
struct has_fixed_size<arm_interfaces::action::PickPlace_SendGoal_Response>
  : std::integral_constant<bool, has_fixed_size<builtin_interfaces::msg::Time>::value> {};

template<>
struct has_bounded_size<arm_interfaces::action::PickPlace_SendGoal_Response>
  : std::integral_constant<bool, has_bounded_size<builtin_interfaces::msg::Time>::value> {};

template<>
struct is_message<arm_interfaces::action::PickPlace_SendGoal_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<arm_interfaces::action::PickPlace_SendGoal>()
{
  return "arm_interfaces::action::PickPlace_SendGoal";
}

template<>
inline const char * name<arm_interfaces::action::PickPlace_SendGoal>()
{
  return "arm_interfaces/action/PickPlace_SendGoal";
}

template<>
struct has_fixed_size<arm_interfaces::action::PickPlace_SendGoal>
  : std::integral_constant<
    bool,
    has_fixed_size<arm_interfaces::action::PickPlace_SendGoal_Request>::value &&
    has_fixed_size<arm_interfaces::action::PickPlace_SendGoal_Response>::value
  >
{
};

template<>
struct has_bounded_size<arm_interfaces::action::PickPlace_SendGoal>
  : std::integral_constant<
    bool,
    has_bounded_size<arm_interfaces::action::PickPlace_SendGoal_Request>::value &&
    has_bounded_size<arm_interfaces::action::PickPlace_SendGoal_Response>::value
  >
{
};

template<>
struct is_service<arm_interfaces::action::PickPlace_SendGoal>
  : std::true_type
{
};

template<>
struct is_service_request<arm_interfaces::action::PickPlace_SendGoal_Request>
  : std::true_type
{
};

template<>
struct is_service_response<arm_interfaces::action::PickPlace_SendGoal_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__traits.hpp"

namespace arm_interfaces
{

namespace action
{

inline void to_flow_style_yaml(
  const PickPlace_GetResult_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: goal_id
  {
    out << "goal_id: ";
    to_flow_style_yaml(msg.goal_id, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const PickPlace_GetResult_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: goal_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "goal_id:\n";
    to_block_style_yaml(msg.goal_id, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const PickPlace_GetResult_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace arm_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use arm_interfaces::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const arm_interfaces::action::PickPlace_GetResult_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  arm_interfaces::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use arm_interfaces::action::to_yaml() instead")]]
inline std::string to_yaml(const arm_interfaces::action::PickPlace_GetResult_Request & msg)
{
  return arm_interfaces::action::to_yaml(msg);
}

template<>
inline const char * data_type<arm_interfaces::action::PickPlace_GetResult_Request>()
{
  return "arm_interfaces::action::PickPlace_GetResult_Request";
}

template<>
inline const char * name<arm_interfaces::action::PickPlace_GetResult_Request>()
{
  return "arm_interfaces/action/PickPlace_GetResult_Request";
}

template<>
struct has_fixed_size<arm_interfaces::action::PickPlace_GetResult_Request>
  : std::integral_constant<bool, has_fixed_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct has_bounded_size<arm_interfaces::action::PickPlace_GetResult_Request>
  : std::integral_constant<bool, has_bounded_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct is_message<arm_interfaces::action::PickPlace_GetResult_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'result'
// already included above
// #include "arm_interfaces/action/detail/pick_place__traits.hpp"

namespace arm_interfaces
{

namespace action
{

inline void to_flow_style_yaml(
  const PickPlace_GetResult_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: status
  {
    out << "status: ";
    rosidl_generator_traits::value_to_yaml(msg.status, out);
    out << ", ";
  }

  // member: result
  {
    out << "result: ";
    to_flow_style_yaml(msg.result, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const PickPlace_GetResult_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: status
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "status: ";
    rosidl_generator_traits::value_to_yaml(msg.status, out);
    out << "\n";
  }

  // member: result
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "result:\n";
    to_block_style_yaml(msg.result, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const PickPlace_GetResult_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace arm_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use arm_interfaces::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const arm_interfaces::action::PickPlace_GetResult_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  arm_interfaces::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use arm_interfaces::action::to_yaml() instead")]]
inline std::string to_yaml(const arm_interfaces::action::PickPlace_GetResult_Response & msg)
{
  return arm_interfaces::action::to_yaml(msg);
}

template<>
inline const char * data_type<arm_interfaces::action::PickPlace_GetResult_Response>()
{
  return "arm_interfaces::action::PickPlace_GetResult_Response";
}

template<>
inline const char * name<arm_interfaces::action::PickPlace_GetResult_Response>()
{
  return "arm_interfaces/action/PickPlace_GetResult_Response";
}

template<>
struct has_fixed_size<arm_interfaces::action::PickPlace_GetResult_Response>
  : std::integral_constant<bool, has_fixed_size<arm_interfaces::action::PickPlace_Result>::value> {};

template<>
struct has_bounded_size<arm_interfaces::action::PickPlace_GetResult_Response>
  : std::integral_constant<bool, has_bounded_size<arm_interfaces::action::PickPlace_Result>::value> {};

template<>
struct is_message<arm_interfaces::action::PickPlace_GetResult_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<arm_interfaces::action::PickPlace_GetResult>()
{
  return "arm_interfaces::action::PickPlace_GetResult";
}

template<>
inline const char * name<arm_interfaces::action::PickPlace_GetResult>()
{
  return "arm_interfaces/action/PickPlace_GetResult";
}

template<>
struct has_fixed_size<arm_interfaces::action::PickPlace_GetResult>
  : std::integral_constant<
    bool,
    has_fixed_size<arm_interfaces::action::PickPlace_GetResult_Request>::value &&
    has_fixed_size<arm_interfaces::action::PickPlace_GetResult_Response>::value
  >
{
};

template<>
struct has_bounded_size<arm_interfaces::action::PickPlace_GetResult>
  : std::integral_constant<
    bool,
    has_bounded_size<arm_interfaces::action::PickPlace_GetResult_Request>::value &&
    has_bounded_size<arm_interfaces::action::PickPlace_GetResult_Response>::value
  >
{
};

template<>
struct is_service<arm_interfaces::action::PickPlace_GetResult>
  : std::true_type
{
};

template<>
struct is_service_request<arm_interfaces::action::PickPlace_GetResult_Request>
  : std::true_type
{
};

template<>
struct is_service_response<arm_interfaces::action::PickPlace_GetResult_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__traits.hpp"
// Member 'feedback'
// already included above
// #include "arm_interfaces/action/detail/pick_place__traits.hpp"

namespace arm_interfaces
{

namespace action
{

inline void to_flow_style_yaml(
  const PickPlace_FeedbackMessage & msg,
  std::ostream & out)
{
  out << "{";
  // member: goal_id
  {
    out << "goal_id: ";
    to_flow_style_yaml(msg.goal_id, out);
    out << ", ";
  }

  // member: feedback
  {
    out << "feedback: ";
    to_flow_style_yaml(msg.feedback, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const PickPlace_FeedbackMessage & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: goal_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "goal_id:\n";
    to_block_style_yaml(msg.goal_id, out, indentation + 2);
  }

  // member: feedback
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "feedback:\n";
    to_block_style_yaml(msg.feedback, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const PickPlace_FeedbackMessage & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace arm_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use arm_interfaces::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const arm_interfaces::action::PickPlace_FeedbackMessage & msg,
  std::ostream & out, size_t indentation = 0)
{
  arm_interfaces::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use arm_interfaces::action::to_yaml() instead")]]
inline std::string to_yaml(const arm_interfaces::action::PickPlace_FeedbackMessage & msg)
{
  return arm_interfaces::action::to_yaml(msg);
}

template<>
inline const char * data_type<arm_interfaces::action::PickPlace_FeedbackMessage>()
{
  return "arm_interfaces::action::PickPlace_FeedbackMessage";
}

template<>
inline const char * name<arm_interfaces::action::PickPlace_FeedbackMessage>()
{
  return "arm_interfaces/action/PickPlace_FeedbackMessage";
}

template<>
struct has_fixed_size<arm_interfaces::action::PickPlace_FeedbackMessage>
  : std::integral_constant<bool, has_fixed_size<arm_interfaces::action::PickPlace_Feedback>::value && has_fixed_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct has_bounded_size<arm_interfaces::action::PickPlace_FeedbackMessage>
  : std::integral_constant<bool, has_bounded_size<arm_interfaces::action::PickPlace_Feedback>::value && has_bounded_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct is_message<arm_interfaces::action::PickPlace_FeedbackMessage>
  : std::true_type {};

}  // namespace rosidl_generator_traits


namespace rosidl_generator_traits
{

template<>
struct is_action<arm_interfaces::action::PickPlace>
  : std::true_type
{
};

template<>
struct is_action_goal<arm_interfaces::action::PickPlace_Goal>
  : std::true_type
{
};

template<>
struct is_action_result<arm_interfaces::action::PickPlace_Result>
  : std::true_type
{
};

template<>
struct is_action_feedback<arm_interfaces::action::PickPlace_Feedback>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits


#endif  // ARM_INTERFACES__ACTION__DETAIL__PICK_PLACE__TRAITS_HPP_

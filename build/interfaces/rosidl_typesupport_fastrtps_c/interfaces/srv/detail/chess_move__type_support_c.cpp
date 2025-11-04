// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from interfaces:srv/ChessMove.idl
// generated code does not contain a copyright notice
#include "interfaces/srv/detail/chess_move__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "interfaces/srv/detail/chess_move__struct.h"
#include "interfaces/srv/detail/chess_move__functions.h"
#include "fastcdr/Cdr.h"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

// includes and forward declarations of message dependencies and their conversion functions

#if defined(__cplusplus)
extern "C"
{
#endif

#include "rosidl_runtime_c/string.h"  // user_move
#include "rosidl_runtime_c/string_functions.h"  // user_move

// forward declare type support functions


using _ChessMove_Request__ros_msg_type = interfaces__srv__ChessMove_Request;

static bool _ChessMove_Request__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _ChessMove_Request__ros_msg_type * ros_message = static_cast<const _ChessMove_Request__ros_msg_type *>(untyped_ros_message);
  // Field name: user_move
  {
    const rosidl_runtime_c__String * str = &ros_message->user_move;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  return true;
}

static bool _ChessMove_Request__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _ChessMove_Request__ros_msg_type * ros_message = static_cast<_ChessMove_Request__ros_msg_type *>(untyped_ros_message);
  // Field name: user_move
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->user_move.data) {
      rosidl_runtime_c__String__init(&ros_message->user_move);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->user_move,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'user_move'\n");
      return false;
    }
  }

  return true;
}  // NOLINT(readability/fn_size)

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_interfaces
size_t get_serialized_size_interfaces__srv__ChessMove_Request(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _ChessMove_Request__ros_msg_type * ros_message = static_cast<const _ChessMove_Request__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name user_move
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->user_move.size + 1);

  return current_alignment - initial_alignment;
}

static uint32_t _ChessMove_Request__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_interfaces__srv__ChessMove_Request(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_interfaces
size_t max_serialized_size_interfaces__srv__ChessMove_Request(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;

  // member: user_move
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = interfaces__srv__ChessMove_Request;
    is_plain =
      (
      offsetof(DataType, user_move) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static size_t _ChessMove_Request__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_interfaces__srv__ChessMove_Request(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_ChessMove_Request = {
  "interfaces::srv",
  "ChessMove_Request",
  _ChessMove_Request__cdr_serialize,
  _ChessMove_Request__cdr_deserialize,
  _ChessMove_Request__get_serialized_size,
  _ChessMove_Request__max_serialized_size
};

static rosidl_message_type_support_t _ChessMove_Request__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_ChessMove_Request,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, interfaces, srv, ChessMove_Request)() {
  return &_ChessMove_Request__type_support;
}

#if defined(__cplusplus)
}
#endif

// already included above
// #include <cassert>
// already included above
// #include <limits>
// already included above
// #include <string>
// already included above
// #include "rosidl_typesupport_fastrtps_c/identifier.h"
// already included above
// #include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
// already included above
// #include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
// already included above
// #include "interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
// already included above
// #include "interfaces/srv/detail/chess_move__struct.h"
// already included above
// #include "interfaces/srv/detail/chess_move__functions.h"
// already included above
// #include "fastcdr/Cdr.h"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

// includes and forward declarations of message dependencies and their conversion functions

#if defined(__cplusplus)
extern "C"
{
#endif

// already included above
// #include "rosidl_runtime_c/string.h"  // robot_move
// already included above
// #include "rosidl_runtime_c/string_functions.h"  // robot_move

// forward declare type support functions


using _ChessMove_Response__ros_msg_type = interfaces__srv__ChessMove_Response;

static bool _ChessMove_Response__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _ChessMove_Response__ros_msg_type * ros_message = static_cast<const _ChessMove_Response__ros_msg_type *>(untyped_ros_message);
  // Field name: robot_move
  {
    const rosidl_runtime_c__String * str = &ros_message->robot_move;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: is_en_passant
  {
    cdr << (ros_message->is_en_passant ? true : false);
  }

  // Field name: is_capture
  {
    cdr << (ros_message->is_capture ? true : false);
  }

  // Field name: is_castling
  {
    cdr << (ros_message->is_castling ? true : false);
  }

  // Field name: is_promotion
  {
    cdr << (ros_message->is_promotion ? true : false);
  }

  return true;
}

static bool _ChessMove_Response__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _ChessMove_Response__ros_msg_type * ros_message = static_cast<_ChessMove_Response__ros_msg_type *>(untyped_ros_message);
  // Field name: robot_move
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->robot_move.data) {
      rosidl_runtime_c__String__init(&ros_message->robot_move);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->robot_move,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'robot_move'\n");
      return false;
    }
  }

  // Field name: is_en_passant
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message->is_en_passant = tmp ? true : false;
  }

  // Field name: is_capture
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message->is_capture = tmp ? true : false;
  }

  // Field name: is_castling
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message->is_castling = tmp ? true : false;
  }

  // Field name: is_promotion
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message->is_promotion = tmp ? true : false;
  }

  return true;
}  // NOLINT(readability/fn_size)

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_interfaces
size_t get_serialized_size_interfaces__srv__ChessMove_Response(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _ChessMove_Response__ros_msg_type * ros_message = static_cast<const _ChessMove_Response__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name robot_move
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->robot_move.size + 1);
  // field.name is_en_passant
  {
    size_t item_size = sizeof(ros_message->is_en_passant);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name is_capture
  {
    size_t item_size = sizeof(ros_message->is_capture);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name is_castling
  {
    size_t item_size = sizeof(ros_message->is_castling);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name is_promotion
  {
    size_t item_size = sizeof(ros_message->is_promotion);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

static uint32_t _ChessMove_Response__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_interfaces__srv__ChessMove_Response(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_interfaces
size_t max_serialized_size_interfaces__srv__ChessMove_Response(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;

  // member: robot_move
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }
  // member: is_en_passant
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: is_capture
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: is_castling
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: is_promotion
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = interfaces__srv__ChessMove_Response;
    is_plain =
      (
      offsetof(DataType, is_promotion) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static size_t _ChessMove_Response__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_interfaces__srv__ChessMove_Response(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_ChessMove_Response = {
  "interfaces::srv",
  "ChessMove_Response",
  _ChessMove_Response__cdr_serialize,
  _ChessMove_Response__cdr_deserialize,
  _ChessMove_Response__get_serialized_size,
  _ChessMove_Response__max_serialized_size
};

static rosidl_message_type_support_t _ChessMove_Response__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_ChessMove_Response,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, interfaces, srv, ChessMove_Response)() {
  return &_ChessMove_Response__type_support;
}

#if defined(__cplusplus)
}
#endif

#include "rosidl_typesupport_fastrtps_cpp/service_type_support.h"
#include "rosidl_typesupport_cpp/service_type_support.hpp"
// already included above
// #include "rosidl_typesupport_fastrtps_c/identifier.h"
// already included above
// #include "interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "interfaces/srv/chess_move.h"

#if defined(__cplusplus)
extern "C"
{
#endif

static service_type_support_callbacks_t ChessMove__callbacks = {
  "interfaces::srv",
  "ChessMove",
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, interfaces, srv, ChessMove_Request)(),
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, interfaces, srv, ChessMove_Response)(),
};

static rosidl_service_type_support_t ChessMove__handle = {
  rosidl_typesupport_fastrtps_c__identifier,
  &ChessMove__callbacks,
  get_service_typesupport_handle_function,
};

const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, interfaces, srv, ChessMove)() {
  return &ChessMove__handle;
}

#if defined(__cplusplus)
}
#endif

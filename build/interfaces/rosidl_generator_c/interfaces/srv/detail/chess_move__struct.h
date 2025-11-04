// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from interfaces:srv/ChessMove.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES__SRV__DETAIL__CHESS_MOVE__STRUCT_H_
#define INTERFACES__SRV__DETAIL__CHESS_MOVE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'user_move'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/ChessMove in the package interfaces.
typedef struct interfaces__srv__ChessMove_Request
{
  rosidl_runtime_c__String user_move;
} interfaces__srv__ChessMove_Request;

// Struct for a sequence of interfaces__srv__ChessMove_Request.
typedef struct interfaces__srv__ChessMove_Request__Sequence
{
  interfaces__srv__ChessMove_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} interfaces__srv__ChessMove_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'robot_move'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in srv/ChessMove in the package interfaces.
typedef struct interfaces__srv__ChessMove_Response
{
  rosidl_runtime_c__String robot_move;
  bool is_en_passant;
  bool is_capture;
  bool is_castling;
  bool is_promotion;
} interfaces__srv__ChessMove_Response;

// Struct for a sequence of interfaces__srv__ChessMove_Response.
typedef struct interfaces__srv__ChessMove_Response__Sequence
{
  interfaces__srv__ChessMove_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} interfaces__srv__ChessMove_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // INTERFACES__SRV__DETAIL__CHESS_MOVE__STRUCT_H_

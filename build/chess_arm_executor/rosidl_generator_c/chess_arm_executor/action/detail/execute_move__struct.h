// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from chess_arm_executor:action/ExecuteMove.idl
// generated code does not contain a copyright notice

#ifndef CHESS_ARM_EXECUTOR__ACTION__DETAIL__EXECUTE_MOVE__STRUCT_H_
#define CHESS_ARM_EXECUTOR__ACTION__DETAIL__EXECUTE_MOVE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Constant 'PAWN'.
enum
{
  chess_arm_executor__action__ExecuteMove_Goal__PAWN = 0
};

/// Constant 'KNIGHT'.
enum
{
  chess_arm_executor__action__ExecuteMove_Goal__KNIGHT = 1
};

/// Constant 'BISHOP'.
enum
{
  chess_arm_executor__action__ExecuteMove_Goal__BISHOP = 2
};

/// Constant 'ROOK'.
enum
{
  chess_arm_executor__action__ExecuteMove_Goal__ROOK = 3
};

/// Constant 'QUEEN'.
enum
{
  chess_arm_executor__action__ExecuteMove_Goal__QUEEN = 4
};

/// Constant 'KING'.
enum
{
  chess_arm_executor__action__ExecuteMove_Goal__KING = 5
};

// Include directives for member types
// Member 'src_square'
// Member 'dst_square'
#include "rosidl_runtime_c/string.h"

/// Struct defined in action/ExecuteMove in the package chess_arm_executor.
typedef struct chess_arm_executor__action__ExecuteMove_Goal
{
  rosidl_runtime_c__String src_square;
  rosidl_runtime_c__String dst_square;
  /// piece type (enum)
  uint8_t piece_type;
} chess_arm_executor__action__ExecuteMove_Goal;

// Struct for a sequence of chess_arm_executor__action__ExecuteMove_Goal.
typedef struct chess_arm_executor__action__ExecuteMove_Goal__Sequence
{
  chess_arm_executor__action__ExecuteMove_Goal * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} chess_arm_executor__action__ExecuteMove_Goal__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'message'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in action/ExecuteMove in the package chess_arm_executor.
typedef struct chess_arm_executor__action__ExecuteMove_Result
{
  bool ok;
  rosidl_runtime_c__String message;
  float z_pick_used;
} chess_arm_executor__action__ExecuteMove_Result;

// Struct for a sequence of chess_arm_executor__action__ExecuteMove_Result.
typedef struct chess_arm_executor__action__ExecuteMove_Result__Sequence
{
  chess_arm_executor__action__ExecuteMove_Result * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} chess_arm_executor__action__ExecuteMove_Result__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'stage'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in action/ExecuteMove in the package chess_arm_executor.
typedef struct chess_arm_executor__action__ExecuteMove_Feedback
{
  rosidl_runtime_c__String stage;
  float z_pick_used;
} chess_arm_executor__action__ExecuteMove_Feedback;

// Struct for a sequence of chess_arm_executor__action__ExecuteMove_Feedback.
typedef struct chess_arm_executor__action__ExecuteMove_Feedback__Sequence
{
  chess_arm_executor__action__ExecuteMove_Feedback * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} chess_arm_executor__action__ExecuteMove_Feedback__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
#include "unique_identifier_msgs/msg/detail/uuid__struct.h"
// Member 'goal'
#include "chess_arm_executor/action/detail/execute_move__struct.h"

/// Struct defined in action/ExecuteMove in the package chess_arm_executor.
typedef struct chess_arm_executor__action__ExecuteMove_SendGoal_Request
{
  unique_identifier_msgs__msg__UUID goal_id;
  chess_arm_executor__action__ExecuteMove_Goal goal;
} chess_arm_executor__action__ExecuteMove_SendGoal_Request;

// Struct for a sequence of chess_arm_executor__action__ExecuteMove_SendGoal_Request.
typedef struct chess_arm_executor__action__ExecuteMove_SendGoal_Request__Sequence
{
  chess_arm_executor__action__ExecuteMove_SendGoal_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} chess_arm_executor__action__ExecuteMove_SendGoal_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.h"

/// Struct defined in action/ExecuteMove in the package chess_arm_executor.
typedef struct chess_arm_executor__action__ExecuteMove_SendGoal_Response
{
  bool accepted;
  builtin_interfaces__msg__Time stamp;
} chess_arm_executor__action__ExecuteMove_SendGoal_Response;

// Struct for a sequence of chess_arm_executor__action__ExecuteMove_SendGoal_Response.
typedef struct chess_arm_executor__action__ExecuteMove_SendGoal_Response__Sequence
{
  chess_arm_executor__action__ExecuteMove_SendGoal_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} chess_arm_executor__action__ExecuteMove_SendGoal_Response__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.h"

/// Struct defined in action/ExecuteMove in the package chess_arm_executor.
typedef struct chess_arm_executor__action__ExecuteMove_GetResult_Request
{
  unique_identifier_msgs__msg__UUID goal_id;
} chess_arm_executor__action__ExecuteMove_GetResult_Request;

// Struct for a sequence of chess_arm_executor__action__ExecuteMove_GetResult_Request.
typedef struct chess_arm_executor__action__ExecuteMove_GetResult_Request__Sequence
{
  chess_arm_executor__action__ExecuteMove_GetResult_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} chess_arm_executor__action__ExecuteMove_GetResult_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'result'
// already included above
// #include "chess_arm_executor/action/detail/execute_move__struct.h"

/// Struct defined in action/ExecuteMove in the package chess_arm_executor.
typedef struct chess_arm_executor__action__ExecuteMove_GetResult_Response
{
  int8_t status;
  chess_arm_executor__action__ExecuteMove_Result result;
} chess_arm_executor__action__ExecuteMove_GetResult_Response;

// Struct for a sequence of chess_arm_executor__action__ExecuteMove_GetResult_Response.
typedef struct chess_arm_executor__action__ExecuteMove_GetResult_Response__Sequence
{
  chess_arm_executor__action__ExecuteMove_GetResult_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} chess_arm_executor__action__ExecuteMove_GetResult_Response__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.h"
// Member 'feedback'
// already included above
// #include "chess_arm_executor/action/detail/execute_move__struct.h"

/// Struct defined in action/ExecuteMove in the package chess_arm_executor.
typedef struct chess_arm_executor__action__ExecuteMove_FeedbackMessage
{
  unique_identifier_msgs__msg__UUID goal_id;
  chess_arm_executor__action__ExecuteMove_Feedback feedback;
} chess_arm_executor__action__ExecuteMove_FeedbackMessage;

// Struct for a sequence of chess_arm_executor__action__ExecuteMove_FeedbackMessage.
typedef struct chess_arm_executor__action__ExecuteMove_FeedbackMessage__Sequence
{
  chess_arm_executor__action__ExecuteMove_FeedbackMessage * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} chess_arm_executor__action__ExecuteMove_FeedbackMessage__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // CHESS_ARM_EXECUTOR__ACTION__DETAIL__EXECUTE_MOVE__STRUCT_H_

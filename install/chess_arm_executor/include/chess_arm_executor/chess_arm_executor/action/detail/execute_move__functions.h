// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from chess_arm_executor:action/ExecuteMove.idl
// generated code does not contain a copyright notice

#ifndef CHESS_ARM_EXECUTOR__ACTION__DETAIL__EXECUTE_MOVE__FUNCTIONS_H_
#define CHESS_ARM_EXECUTOR__ACTION__DETAIL__EXECUTE_MOVE__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "chess_arm_executor/msg/rosidl_generator_c__visibility_control.h"

#include "chess_arm_executor/action/detail/execute_move__struct.h"

/// Initialize action/ExecuteMove message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * chess_arm_executor__action__ExecuteMove_Goal
 * )) before or use
 * chess_arm_executor__action__ExecuteMove_Goal__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
bool
chess_arm_executor__action__ExecuteMove_Goal__init(chess_arm_executor__action__ExecuteMove_Goal * msg);

/// Finalize action/ExecuteMove message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
void
chess_arm_executor__action__ExecuteMove_Goal__fini(chess_arm_executor__action__ExecuteMove_Goal * msg);

/// Create action/ExecuteMove message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * chess_arm_executor__action__ExecuteMove_Goal__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
chess_arm_executor__action__ExecuteMove_Goal *
chess_arm_executor__action__ExecuteMove_Goal__create();

/// Destroy action/ExecuteMove message.
/**
 * It calls
 * chess_arm_executor__action__ExecuteMove_Goal__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
void
chess_arm_executor__action__ExecuteMove_Goal__destroy(chess_arm_executor__action__ExecuteMove_Goal * msg);

/// Check for action/ExecuteMove message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
bool
chess_arm_executor__action__ExecuteMove_Goal__are_equal(const chess_arm_executor__action__ExecuteMove_Goal * lhs, const chess_arm_executor__action__ExecuteMove_Goal * rhs);

/// Copy a action/ExecuteMove message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
bool
chess_arm_executor__action__ExecuteMove_Goal__copy(
  const chess_arm_executor__action__ExecuteMove_Goal * input,
  chess_arm_executor__action__ExecuteMove_Goal * output);

/// Initialize array of action/ExecuteMove messages.
/**
 * It allocates the memory for the number of elements and calls
 * chess_arm_executor__action__ExecuteMove_Goal__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
bool
chess_arm_executor__action__ExecuteMove_Goal__Sequence__init(chess_arm_executor__action__ExecuteMove_Goal__Sequence * array, size_t size);

/// Finalize array of action/ExecuteMove messages.
/**
 * It calls
 * chess_arm_executor__action__ExecuteMove_Goal__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
void
chess_arm_executor__action__ExecuteMove_Goal__Sequence__fini(chess_arm_executor__action__ExecuteMove_Goal__Sequence * array);

/// Create array of action/ExecuteMove messages.
/**
 * It allocates the memory for the array and calls
 * chess_arm_executor__action__ExecuteMove_Goal__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
chess_arm_executor__action__ExecuteMove_Goal__Sequence *
chess_arm_executor__action__ExecuteMove_Goal__Sequence__create(size_t size);

/// Destroy array of action/ExecuteMove messages.
/**
 * It calls
 * chess_arm_executor__action__ExecuteMove_Goal__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
void
chess_arm_executor__action__ExecuteMove_Goal__Sequence__destroy(chess_arm_executor__action__ExecuteMove_Goal__Sequence * array);

/// Check for action/ExecuteMove message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
bool
chess_arm_executor__action__ExecuteMove_Goal__Sequence__are_equal(const chess_arm_executor__action__ExecuteMove_Goal__Sequence * lhs, const chess_arm_executor__action__ExecuteMove_Goal__Sequence * rhs);

/// Copy an array of action/ExecuteMove messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
bool
chess_arm_executor__action__ExecuteMove_Goal__Sequence__copy(
  const chess_arm_executor__action__ExecuteMove_Goal__Sequence * input,
  chess_arm_executor__action__ExecuteMove_Goal__Sequence * output);

/// Initialize action/ExecuteMove message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * chess_arm_executor__action__ExecuteMove_Result
 * )) before or use
 * chess_arm_executor__action__ExecuteMove_Result__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
bool
chess_arm_executor__action__ExecuteMove_Result__init(chess_arm_executor__action__ExecuteMove_Result * msg);

/// Finalize action/ExecuteMove message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
void
chess_arm_executor__action__ExecuteMove_Result__fini(chess_arm_executor__action__ExecuteMove_Result * msg);

/// Create action/ExecuteMove message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * chess_arm_executor__action__ExecuteMove_Result__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
chess_arm_executor__action__ExecuteMove_Result *
chess_arm_executor__action__ExecuteMove_Result__create();

/// Destroy action/ExecuteMove message.
/**
 * It calls
 * chess_arm_executor__action__ExecuteMove_Result__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
void
chess_arm_executor__action__ExecuteMove_Result__destroy(chess_arm_executor__action__ExecuteMove_Result * msg);

/// Check for action/ExecuteMove message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
bool
chess_arm_executor__action__ExecuteMove_Result__are_equal(const chess_arm_executor__action__ExecuteMove_Result * lhs, const chess_arm_executor__action__ExecuteMove_Result * rhs);

/// Copy a action/ExecuteMove message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
bool
chess_arm_executor__action__ExecuteMove_Result__copy(
  const chess_arm_executor__action__ExecuteMove_Result * input,
  chess_arm_executor__action__ExecuteMove_Result * output);

/// Initialize array of action/ExecuteMove messages.
/**
 * It allocates the memory for the number of elements and calls
 * chess_arm_executor__action__ExecuteMove_Result__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
bool
chess_arm_executor__action__ExecuteMove_Result__Sequence__init(chess_arm_executor__action__ExecuteMove_Result__Sequence * array, size_t size);

/// Finalize array of action/ExecuteMove messages.
/**
 * It calls
 * chess_arm_executor__action__ExecuteMove_Result__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
void
chess_arm_executor__action__ExecuteMove_Result__Sequence__fini(chess_arm_executor__action__ExecuteMove_Result__Sequence * array);

/// Create array of action/ExecuteMove messages.
/**
 * It allocates the memory for the array and calls
 * chess_arm_executor__action__ExecuteMove_Result__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
chess_arm_executor__action__ExecuteMove_Result__Sequence *
chess_arm_executor__action__ExecuteMove_Result__Sequence__create(size_t size);

/// Destroy array of action/ExecuteMove messages.
/**
 * It calls
 * chess_arm_executor__action__ExecuteMove_Result__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
void
chess_arm_executor__action__ExecuteMove_Result__Sequence__destroy(chess_arm_executor__action__ExecuteMove_Result__Sequence * array);

/// Check for action/ExecuteMove message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
bool
chess_arm_executor__action__ExecuteMove_Result__Sequence__are_equal(const chess_arm_executor__action__ExecuteMove_Result__Sequence * lhs, const chess_arm_executor__action__ExecuteMove_Result__Sequence * rhs);

/// Copy an array of action/ExecuteMove messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
bool
chess_arm_executor__action__ExecuteMove_Result__Sequence__copy(
  const chess_arm_executor__action__ExecuteMove_Result__Sequence * input,
  chess_arm_executor__action__ExecuteMove_Result__Sequence * output);

/// Initialize action/ExecuteMove message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * chess_arm_executor__action__ExecuteMove_Feedback
 * )) before or use
 * chess_arm_executor__action__ExecuteMove_Feedback__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
bool
chess_arm_executor__action__ExecuteMove_Feedback__init(chess_arm_executor__action__ExecuteMove_Feedback * msg);

/// Finalize action/ExecuteMove message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
void
chess_arm_executor__action__ExecuteMove_Feedback__fini(chess_arm_executor__action__ExecuteMove_Feedback * msg);

/// Create action/ExecuteMove message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * chess_arm_executor__action__ExecuteMove_Feedback__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
chess_arm_executor__action__ExecuteMove_Feedback *
chess_arm_executor__action__ExecuteMove_Feedback__create();

/// Destroy action/ExecuteMove message.
/**
 * It calls
 * chess_arm_executor__action__ExecuteMove_Feedback__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
void
chess_arm_executor__action__ExecuteMove_Feedback__destroy(chess_arm_executor__action__ExecuteMove_Feedback * msg);

/// Check for action/ExecuteMove message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
bool
chess_arm_executor__action__ExecuteMove_Feedback__are_equal(const chess_arm_executor__action__ExecuteMove_Feedback * lhs, const chess_arm_executor__action__ExecuteMove_Feedback * rhs);

/// Copy a action/ExecuteMove message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
bool
chess_arm_executor__action__ExecuteMove_Feedback__copy(
  const chess_arm_executor__action__ExecuteMove_Feedback * input,
  chess_arm_executor__action__ExecuteMove_Feedback * output);

/// Initialize array of action/ExecuteMove messages.
/**
 * It allocates the memory for the number of elements and calls
 * chess_arm_executor__action__ExecuteMove_Feedback__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
bool
chess_arm_executor__action__ExecuteMove_Feedback__Sequence__init(chess_arm_executor__action__ExecuteMove_Feedback__Sequence * array, size_t size);

/// Finalize array of action/ExecuteMove messages.
/**
 * It calls
 * chess_arm_executor__action__ExecuteMove_Feedback__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
void
chess_arm_executor__action__ExecuteMove_Feedback__Sequence__fini(chess_arm_executor__action__ExecuteMove_Feedback__Sequence * array);

/// Create array of action/ExecuteMove messages.
/**
 * It allocates the memory for the array and calls
 * chess_arm_executor__action__ExecuteMove_Feedback__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
chess_arm_executor__action__ExecuteMove_Feedback__Sequence *
chess_arm_executor__action__ExecuteMove_Feedback__Sequence__create(size_t size);

/// Destroy array of action/ExecuteMove messages.
/**
 * It calls
 * chess_arm_executor__action__ExecuteMove_Feedback__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
void
chess_arm_executor__action__ExecuteMove_Feedback__Sequence__destroy(chess_arm_executor__action__ExecuteMove_Feedback__Sequence * array);

/// Check for action/ExecuteMove message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
bool
chess_arm_executor__action__ExecuteMove_Feedback__Sequence__are_equal(const chess_arm_executor__action__ExecuteMove_Feedback__Sequence * lhs, const chess_arm_executor__action__ExecuteMove_Feedback__Sequence * rhs);

/// Copy an array of action/ExecuteMove messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
bool
chess_arm_executor__action__ExecuteMove_Feedback__Sequence__copy(
  const chess_arm_executor__action__ExecuteMove_Feedback__Sequence * input,
  chess_arm_executor__action__ExecuteMove_Feedback__Sequence * output);

/// Initialize action/ExecuteMove message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * chess_arm_executor__action__ExecuteMove_SendGoal_Request
 * )) before or use
 * chess_arm_executor__action__ExecuteMove_SendGoal_Request__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
bool
chess_arm_executor__action__ExecuteMove_SendGoal_Request__init(chess_arm_executor__action__ExecuteMove_SendGoal_Request * msg);

/// Finalize action/ExecuteMove message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
void
chess_arm_executor__action__ExecuteMove_SendGoal_Request__fini(chess_arm_executor__action__ExecuteMove_SendGoal_Request * msg);

/// Create action/ExecuteMove message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * chess_arm_executor__action__ExecuteMove_SendGoal_Request__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
chess_arm_executor__action__ExecuteMove_SendGoal_Request *
chess_arm_executor__action__ExecuteMove_SendGoal_Request__create();

/// Destroy action/ExecuteMove message.
/**
 * It calls
 * chess_arm_executor__action__ExecuteMove_SendGoal_Request__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
void
chess_arm_executor__action__ExecuteMove_SendGoal_Request__destroy(chess_arm_executor__action__ExecuteMove_SendGoal_Request * msg);

/// Check for action/ExecuteMove message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
bool
chess_arm_executor__action__ExecuteMove_SendGoal_Request__are_equal(const chess_arm_executor__action__ExecuteMove_SendGoal_Request * lhs, const chess_arm_executor__action__ExecuteMove_SendGoal_Request * rhs);

/// Copy a action/ExecuteMove message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
bool
chess_arm_executor__action__ExecuteMove_SendGoal_Request__copy(
  const chess_arm_executor__action__ExecuteMove_SendGoal_Request * input,
  chess_arm_executor__action__ExecuteMove_SendGoal_Request * output);

/// Initialize array of action/ExecuteMove messages.
/**
 * It allocates the memory for the number of elements and calls
 * chess_arm_executor__action__ExecuteMove_SendGoal_Request__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
bool
chess_arm_executor__action__ExecuteMove_SendGoal_Request__Sequence__init(chess_arm_executor__action__ExecuteMove_SendGoal_Request__Sequence * array, size_t size);

/// Finalize array of action/ExecuteMove messages.
/**
 * It calls
 * chess_arm_executor__action__ExecuteMove_SendGoal_Request__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
void
chess_arm_executor__action__ExecuteMove_SendGoal_Request__Sequence__fini(chess_arm_executor__action__ExecuteMove_SendGoal_Request__Sequence * array);

/// Create array of action/ExecuteMove messages.
/**
 * It allocates the memory for the array and calls
 * chess_arm_executor__action__ExecuteMove_SendGoal_Request__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
chess_arm_executor__action__ExecuteMove_SendGoal_Request__Sequence *
chess_arm_executor__action__ExecuteMove_SendGoal_Request__Sequence__create(size_t size);

/// Destroy array of action/ExecuteMove messages.
/**
 * It calls
 * chess_arm_executor__action__ExecuteMove_SendGoal_Request__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
void
chess_arm_executor__action__ExecuteMove_SendGoal_Request__Sequence__destroy(chess_arm_executor__action__ExecuteMove_SendGoal_Request__Sequence * array);

/// Check for action/ExecuteMove message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
bool
chess_arm_executor__action__ExecuteMove_SendGoal_Request__Sequence__are_equal(const chess_arm_executor__action__ExecuteMove_SendGoal_Request__Sequence * lhs, const chess_arm_executor__action__ExecuteMove_SendGoal_Request__Sequence * rhs);

/// Copy an array of action/ExecuteMove messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
bool
chess_arm_executor__action__ExecuteMove_SendGoal_Request__Sequence__copy(
  const chess_arm_executor__action__ExecuteMove_SendGoal_Request__Sequence * input,
  chess_arm_executor__action__ExecuteMove_SendGoal_Request__Sequence * output);

/// Initialize action/ExecuteMove message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * chess_arm_executor__action__ExecuteMove_SendGoal_Response
 * )) before or use
 * chess_arm_executor__action__ExecuteMove_SendGoal_Response__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
bool
chess_arm_executor__action__ExecuteMove_SendGoal_Response__init(chess_arm_executor__action__ExecuteMove_SendGoal_Response * msg);

/// Finalize action/ExecuteMove message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
void
chess_arm_executor__action__ExecuteMove_SendGoal_Response__fini(chess_arm_executor__action__ExecuteMove_SendGoal_Response * msg);

/// Create action/ExecuteMove message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * chess_arm_executor__action__ExecuteMove_SendGoal_Response__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
chess_arm_executor__action__ExecuteMove_SendGoal_Response *
chess_arm_executor__action__ExecuteMove_SendGoal_Response__create();

/// Destroy action/ExecuteMove message.
/**
 * It calls
 * chess_arm_executor__action__ExecuteMove_SendGoal_Response__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
void
chess_arm_executor__action__ExecuteMove_SendGoal_Response__destroy(chess_arm_executor__action__ExecuteMove_SendGoal_Response * msg);

/// Check for action/ExecuteMove message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
bool
chess_arm_executor__action__ExecuteMove_SendGoal_Response__are_equal(const chess_arm_executor__action__ExecuteMove_SendGoal_Response * lhs, const chess_arm_executor__action__ExecuteMove_SendGoal_Response * rhs);

/// Copy a action/ExecuteMove message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
bool
chess_arm_executor__action__ExecuteMove_SendGoal_Response__copy(
  const chess_arm_executor__action__ExecuteMove_SendGoal_Response * input,
  chess_arm_executor__action__ExecuteMove_SendGoal_Response * output);

/// Initialize array of action/ExecuteMove messages.
/**
 * It allocates the memory for the number of elements and calls
 * chess_arm_executor__action__ExecuteMove_SendGoal_Response__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
bool
chess_arm_executor__action__ExecuteMove_SendGoal_Response__Sequence__init(chess_arm_executor__action__ExecuteMove_SendGoal_Response__Sequence * array, size_t size);

/// Finalize array of action/ExecuteMove messages.
/**
 * It calls
 * chess_arm_executor__action__ExecuteMove_SendGoal_Response__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
void
chess_arm_executor__action__ExecuteMove_SendGoal_Response__Sequence__fini(chess_arm_executor__action__ExecuteMove_SendGoal_Response__Sequence * array);

/// Create array of action/ExecuteMove messages.
/**
 * It allocates the memory for the array and calls
 * chess_arm_executor__action__ExecuteMove_SendGoal_Response__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
chess_arm_executor__action__ExecuteMove_SendGoal_Response__Sequence *
chess_arm_executor__action__ExecuteMove_SendGoal_Response__Sequence__create(size_t size);

/// Destroy array of action/ExecuteMove messages.
/**
 * It calls
 * chess_arm_executor__action__ExecuteMove_SendGoal_Response__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
void
chess_arm_executor__action__ExecuteMove_SendGoal_Response__Sequence__destroy(chess_arm_executor__action__ExecuteMove_SendGoal_Response__Sequence * array);

/// Check for action/ExecuteMove message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
bool
chess_arm_executor__action__ExecuteMove_SendGoal_Response__Sequence__are_equal(const chess_arm_executor__action__ExecuteMove_SendGoal_Response__Sequence * lhs, const chess_arm_executor__action__ExecuteMove_SendGoal_Response__Sequence * rhs);

/// Copy an array of action/ExecuteMove messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
bool
chess_arm_executor__action__ExecuteMove_SendGoal_Response__Sequence__copy(
  const chess_arm_executor__action__ExecuteMove_SendGoal_Response__Sequence * input,
  chess_arm_executor__action__ExecuteMove_SendGoal_Response__Sequence * output);

/// Initialize action/ExecuteMove message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * chess_arm_executor__action__ExecuteMove_GetResult_Request
 * )) before or use
 * chess_arm_executor__action__ExecuteMove_GetResult_Request__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
bool
chess_arm_executor__action__ExecuteMove_GetResult_Request__init(chess_arm_executor__action__ExecuteMove_GetResult_Request * msg);

/// Finalize action/ExecuteMove message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
void
chess_arm_executor__action__ExecuteMove_GetResult_Request__fini(chess_arm_executor__action__ExecuteMove_GetResult_Request * msg);

/// Create action/ExecuteMove message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * chess_arm_executor__action__ExecuteMove_GetResult_Request__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
chess_arm_executor__action__ExecuteMove_GetResult_Request *
chess_arm_executor__action__ExecuteMove_GetResult_Request__create();

/// Destroy action/ExecuteMove message.
/**
 * It calls
 * chess_arm_executor__action__ExecuteMove_GetResult_Request__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
void
chess_arm_executor__action__ExecuteMove_GetResult_Request__destroy(chess_arm_executor__action__ExecuteMove_GetResult_Request * msg);

/// Check for action/ExecuteMove message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
bool
chess_arm_executor__action__ExecuteMove_GetResult_Request__are_equal(const chess_arm_executor__action__ExecuteMove_GetResult_Request * lhs, const chess_arm_executor__action__ExecuteMove_GetResult_Request * rhs);

/// Copy a action/ExecuteMove message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
bool
chess_arm_executor__action__ExecuteMove_GetResult_Request__copy(
  const chess_arm_executor__action__ExecuteMove_GetResult_Request * input,
  chess_arm_executor__action__ExecuteMove_GetResult_Request * output);

/// Initialize array of action/ExecuteMove messages.
/**
 * It allocates the memory for the number of elements and calls
 * chess_arm_executor__action__ExecuteMove_GetResult_Request__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
bool
chess_arm_executor__action__ExecuteMove_GetResult_Request__Sequence__init(chess_arm_executor__action__ExecuteMove_GetResult_Request__Sequence * array, size_t size);

/// Finalize array of action/ExecuteMove messages.
/**
 * It calls
 * chess_arm_executor__action__ExecuteMove_GetResult_Request__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
void
chess_arm_executor__action__ExecuteMove_GetResult_Request__Sequence__fini(chess_arm_executor__action__ExecuteMove_GetResult_Request__Sequence * array);

/// Create array of action/ExecuteMove messages.
/**
 * It allocates the memory for the array and calls
 * chess_arm_executor__action__ExecuteMove_GetResult_Request__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
chess_arm_executor__action__ExecuteMove_GetResult_Request__Sequence *
chess_arm_executor__action__ExecuteMove_GetResult_Request__Sequence__create(size_t size);

/// Destroy array of action/ExecuteMove messages.
/**
 * It calls
 * chess_arm_executor__action__ExecuteMove_GetResult_Request__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
void
chess_arm_executor__action__ExecuteMove_GetResult_Request__Sequence__destroy(chess_arm_executor__action__ExecuteMove_GetResult_Request__Sequence * array);

/// Check for action/ExecuteMove message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
bool
chess_arm_executor__action__ExecuteMove_GetResult_Request__Sequence__are_equal(const chess_arm_executor__action__ExecuteMove_GetResult_Request__Sequence * lhs, const chess_arm_executor__action__ExecuteMove_GetResult_Request__Sequence * rhs);

/// Copy an array of action/ExecuteMove messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
bool
chess_arm_executor__action__ExecuteMove_GetResult_Request__Sequence__copy(
  const chess_arm_executor__action__ExecuteMove_GetResult_Request__Sequence * input,
  chess_arm_executor__action__ExecuteMove_GetResult_Request__Sequence * output);

/// Initialize action/ExecuteMove message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * chess_arm_executor__action__ExecuteMove_GetResult_Response
 * )) before or use
 * chess_arm_executor__action__ExecuteMove_GetResult_Response__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
bool
chess_arm_executor__action__ExecuteMove_GetResult_Response__init(chess_arm_executor__action__ExecuteMove_GetResult_Response * msg);

/// Finalize action/ExecuteMove message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
void
chess_arm_executor__action__ExecuteMove_GetResult_Response__fini(chess_arm_executor__action__ExecuteMove_GetResult_Response * msg);

/// Create action/ExecuteMove message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * chess_arm_executor__action__ExecuteMove_GetResult_Response__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
chess_arm_executor__action__ExecuteMove_GetResult_Response *
chess_arm_executor__action__ExecuteMove_GetResult_Response__create();

/// Destroy action/ExecuteMove message.
/**
 * It calls
 * chess_arm_executor__action__ExecuteMove_GetResult_Response__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
void
chess_arm_executor__action__ExecuteMove_GetResult_Response__destroy(chess_arm_executor__action__ExecuteMove_GetResult_Response * msg);

/// Check for action/ExecuteMove message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
bool
chess_arm_executor__action__ExecuteMove_GetResult_Response__are_equal(const chess_arm_executor__action__ExecuteMove_GetResult_Response * lhs, const chess_arm_executor__action__ExecuteMove_GetResult_Response * rhs);

/// Copy a action/ExecuteMove message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
bool
chess_arm_executor__action__ExecuteMove_GetResult_Response__copy(
  const chess_arm_executor__action__ExecuteMove_GetResult_Response * input,
  chess_arm_executor__action__ExecuteMove_GetResult_Response * output);

/// Initialize array of action/ExecuteMove messages.
/**
 * It allocates the memory for the number of elements and calls
 * chess_arm_executor__action__ExecuteMove_GetResult_Response__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
bool
chess_arm_executor__action__ExecuteMove_GetResult_Response__Sequence__init(chess_arm_executor__action__ExecuteMove_GetResult_Response__Sequence * array, size_t size);

/// Finalize array of action/ExecuteMove messages.
/**
 * It calls
 * chess_arm_executor__action__ExecuteMove_GetResult_Response__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
void
chess_arm_executor__action__ExecuteMove_GetResult_Response__Sequence__fini(chess_arm_executor__action__ExecuteMove_GetResult_Response__Sequence * array);

/// Create array of action/ExecuteMove messages.
/**
 * It allocates the memory for the array and calls
 * chess_arm_executor__action__ExecuteMove_GetResult_Response__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
chess_arm_executor__action__ExecuteMove_GetResult_Response__Sequence *
chess_arm_executor__action__ExecuteMove_GetResult_Response__Sequence__create(size_t size);

/// Destroy array of action/ExecuteMove messages.
/**
 * It calls
 * chess_arm_executor__action__ExecuteMove_GetResult_Response__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
void
chess_arm_executor__action__ExecuteMove_GetResult_Response__Sequence__destroy(chess_arm_executor__action__ExecuteMove_GetResult_Response__Sequence * array);

/// Check for action/ExecuteMove message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
bool
chess_arm_executor__action__ExecuteMove_GetResult_Response__Sequence__are_equal(const chess_arm_executor__action__ExecuteMove_GetResult_Response__Sequence * lhs, const chess_arm_executor__action__ExecuteMove_GetResult_Response__Sequence * rhs);

/// Copy an array of action/ExecuteMove messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
bool
chess_arm_executor__action__ExecuteMove_GetResult_Response__Sequence__copy(
  const chess_arm_executor__action__ExecuteMove_GetResult_Response__Sequence * input,
  chess_arm_executor__action__ExecuteMove_GetResult_Response__Sequence * output);

/// Initialize action/ExecuteMove message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * chess_arm_executor__action__ExecuteMove_FeedbackMessage
 * )) before or use
 * chess_arm_executor__action__ExecuteMove_FeedbackMessage__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
bool
chess_arm_executor__action__ExecuteMove_FeedbackMessage__init(chess_arm_executor__action__ExecuteMove_FeedbackMessage * msg);

/// Finalize action/ExecuteMove message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
void
chess_arm_executor__action__ExecuteMove_FeedbackMessage__fini(chess_arm_executor__action__ExecuteMove_FeedbackMessage * msg);

/// Create action/ExecuteMove message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * chess_arm_executor__action__ExecuteMove_FeedbackMessage__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
chess_arm_executor__action__ExecuteMove_FeedbackMessage *
chess_arm_executor__action__ExecuteMove_FeedbackMessage__create();

/// Destroy action/ExecuteMove message.
/**
 * It calls
 * chess_arm_executor__action__ExecuteMove_FeedbackMessage__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
void
chess_arm_executor__action__ExecuteMove_FeedbackMessage__destroy(chess_arm_executor__action__ExecuteMove_FeedbackMessage * msg);

/// Check for action/ExecuteMove message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
bool
chess_arm_executor__action__ExecuteMove_FeedbackMessage__are_equal(const chess_arm_executor__action__ExecuteMove_FeedbackMessage * lhs, const chess_arm_executor__action__ExecuteMove_FeedbackMessage * rhs);

/// Copy a action/ExecuteMove message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
bool
chess_arm_executor__action__ExecuteMove_FeedbackMessage__copy(
  const chess_arm_executor__action__ExecuteMove_FeedbackMessage * input,
  chess_arm_executor__action__ExecuteMove_FeedbackMessage * output);

/// Initialize array of action/ExecuteMove messages.
/**
 * It allocates the memory for the number of elements and calls
 * chess_arm_executor__action__ExecuteMove_FeedbackMessage__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
bool
chess_arm_executor__action__ExecuteMove_FeedbackMessage__Sequence__init(chess_arm_executor__action__ExecuteMove_FeedbackMessage__Sequence * array, size_t size);

/// Finalize array of action/ExecuteMove messages.
/**
 * It calls
 * chess_arm_executor__action__ExecuteMove_FeedbackMessage__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
void
chess_arm_executor__action__ExecuteMove_FeedbackMessage__Sequence__fini(chess_arm_executor__action__ExecuteMove_FeedbackMessage__Sequence * array);

/// Create array of action/ExecuteMove messages.
/**
 * It allocates the memory for the array and calls
 * chess_arm_executor__action__ExecuteMove_FeedbackMessage__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
chess_arm_executor__action__ExecuteMove_FeedbackMessage__Sequence *
chess_arm_executor__action__ExecuteMove_FeedbackMessage__Sequence__create(size_t size);

/// Destroy array of action/ExecuteMove messages.
/**
 * It calls
 * chess_arm_executor__action__ExecuteMove_FeedbackMessage__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
void
chess_arm_executor__action__ExecuteMove_FeedbackMessage__Sequence__destroy(chess_arm_executor__action__ExecuteMove_FeedbackMessage__Sequence * array);

/// Check for action/ExecuteMove message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
bool
chess_arm_executor__action__ExecuteMove_FeedbackMessage__Sequence__are_equal(const chess_arm_executor__action__ExecuteMove_FeedbackMessage__Sequence * lhs, const chess_arm_executor__action__ExecuteMove_FeedbackMessage__Sequence * rhs);

/// Copy an array of action/ExecuteMove messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_chess_arm_executor
bool
chess_arm_executor__action__ExecuteMove_FeedbackMessage__Sequence__copy(
  const chess_arm_executor__action__ExecuteMove_FeedbackMessage__Sequence * input,
  chess_arm_executor__action__ExecuteMove_FeedbackMessage__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // CHESS_ARM_EXECUTOR__ACTION__DETAIL__EXECUTE_MOVE__FUNCTIONS_H_

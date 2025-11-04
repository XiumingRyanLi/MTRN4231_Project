// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from interfaces:srv/ChessMove.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES__SRV__DETAIL__CHESS_MOVE__STRUCT_HPP_
#define INTERFACES__SRV__DETAIL__CHESS_MOVE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__interfaces__srv__ChessMove_Request __attribute__((deprecated))
#else
# define DEPRECATED__interfaces__srv__ChessMove_Request __declspec(deprecated)
#endif

namespace interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct ChessMove_Request_
{
  using Type = ChessMove_Request_<ContainerAllocator>;

  explicit ChessMove_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->user_move = "";
    }
  }

  explicit ChessMove_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : user_move(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->user_move = "";
    }
  }

  // field types and members
  using _user_move_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _user_move_type user_move;

  // setters for named parameter idiom
  Type & set__user_move(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->user_move = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    interfaces::srv::ChessMove_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const interfaces::srv::ChessMove_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<interfaces::srv::ChessMove_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<interfaces::srv::ChessMove_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      interfaces::srv::ChessMove_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<interfaces::srv::ChessMove_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      interfaces::srv::ChessMove_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<interfaces::srv::ChessMove_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<interfaces::srv::ChessMove_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<interfaces::srv::ChessMove_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__interfaces__srv__ChessMove_Request
    std::shared_ptr<interfaces::srv::ChessMove_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__interfaces__srv__ChessMove_Request
    std::shared_ptr<interfaces::srv::ChessMove_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ChessMove_Request_ & other) const
  {
    if (this->user_move != other.user_move) {
      return false;
    }
    return true;
  }
  bool operator!=(const ChessMove_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ChessMove_Request_

// alias to use template instance with default allocator
using ChessMove_Request =
  interfaces::srv::ChessMove_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace interfaces


#ifndef _WIN32
# define DEPRECATED__interfaces__srv__ChessMove_Response __attribute__((deprecated))
#else
# define DEPRECATED__interfaces__srv__ChessMove_Response __declspec(deprecated)
#endif

namespace interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct ChessMove_Response_
{
  using Type = ChessMove_Response_<ContainerAllocator>;

  explicit ChessMove_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->robot_move = "";
      this->is_en_passant = false;
      this->is_capture = false;
      this->is_castling = false;
      this->is_promotion = false;
    }
  }

  explicit ChessMove_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : robot_move(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->robot_move = "";
      this->is_en_passant = false;
      this->is_capture = false;
      this->is_castling = false;
      this->is_promotion = false;
    }
  }

  // field types and members
  using _robot_move_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _robot_move_type robot_move;
  using _is_en_passant_type =
    bool;
  _is_en_passant_type is_en_passant;
  using _is_capture_type =
    bool;
  _is_capture_type is_capture;
  using _is_castling_type =
    bool;
  _is_castling_type is_castling;
  using _is_promotion_type =
    bool;
  _is_promotion_type is_promotion;

  // setters for named parameter idiom
  Type & set__robot_move(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->robot_move = _arg;
    return *this;
  }
  Type & set__is_en_passant(
    const bool & _arg)
  {
    this->is_en_passant = _arg;
    return *this;
  }
  Type & set__is_capture(
    const bool & _arg)
  {
    this->is_capture = _arg;
    return *this;
  }
  Type & set__is_castling(
    const bool & _arg)
  {
    this->is_castling = _arg;
    return *this;
  }
  Type & set__is_promotion(
    const bool & _arg)
  {
    this->is_promotion = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    interfaces::srv::ChessMove_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const interfaces::srv::ChessMove_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<interfaces::srv::ChessMove_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<interfaces::srv::ChessMove_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      interfaces::srv::ChessMove_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<interfaces::srv::ChessMove_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      interfaces::srv::ChessMove_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<interfaces::srv::ChessMove_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<interfaces::srv::ChessMove_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<interfaces::srv::ChessMove_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__interfaces__srv__ChessMove_Response
    std::shared_ptr<interfaces::srv::ChessMove_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__interfaces__srv__ChessMove_Response
    std::shared_ptr<interfaces::srv::ChessMove_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ChessMove_Response_ & other) const
  {
    if (this->robot_move != other.robot_move) {
      return false;
    }
    if (this->is_en_passant != other.is_en_passant) {
      return false;
    }
    if (this->is_capture != other.is_capture) {
      return false;
    }
    if (this->is_castling != other.is_castling) {
      return false;
    }
    if (this->is_promotion != other.is_promotion) {
      return false;
    }
    return true;
  }
  bool operator!=(const ChessMove_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ChessMove_Response_

// alias to use template instance with default allocator
using ChessMove_Response =
  interfaces::srv::ChessMove_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace interfaces

namespace interfaces
{

namespace srv
{

struct ChessMove
{
  using Request = interfaces::srv::ChessMove_Request;
  using Response = interfaces::srv::ChessMove_Response;
};

}  // namespace srv

}  // namespace interfaces

#endif  // INTERFACES__SRV__DETAIL__CHESS_MOVE__STRUCT_HPP_

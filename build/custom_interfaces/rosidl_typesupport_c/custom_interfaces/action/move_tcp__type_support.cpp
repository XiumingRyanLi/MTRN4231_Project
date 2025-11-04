// generated from rosidl_typesupport_c/resource/idl__type_support.cpp.em
// with input from custom_interfaces:action/MoveTCP.idl
// generated code does not contain a copyright notice

#include "cstddef"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "custom_interfaces/action/detail/move_tcp__struct.h"
#include "custom_interfaces/action/detail/move_tcp__type_support.h"
#include "rosidl_typesupport_c/identifier.h"
#include "rosidl_typesupport_c/message_type_support_dispatch.h"
#include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_c/visibility_control.h"
#include "rosidl_typesupport_interface/macros.h"

namespace custom_interfaces
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _MoveTCP_Goal_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _MoveTCP_Goal_type_support_ids_t;

static const _MoveTCP_Goal_type_support_ids_t _MoveTCP_Goal_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _MoveTCP_Goal_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _MoveTCP_Goal_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _MoveTCP_Goal_type_support_symbol_names_t _MoveTCP_Goal_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, custom_interfaces, action, MoveTCP_Goal)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, custom_interfaces, action, MoveTCP_Goal)),
  }
};

typedef struct _MoveTCP_Goal_type_support_data_t
{
  void * data[2];
} _MoveTCP_Goal_type_support_data_t;

static _MoveTCP_Goal_type_support_data_t _MoveTCP_Goal_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _MoveTCP_Goal_message_typesupport_map = {
  2,
  "custom_interfaces",
  &_MoveTCP_Goal_message_typesupport_ids.typesupport_identifier[0],
  &_MoveTCP_Goal_message_typesupport_symbol_names.symbol_name[0],
  &_MoveTCP_Goal_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t MoveTCP_Goal_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_MoveTCP_Goal_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace custom_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, custom_interfaces, action, MoveTCP_Goal)() {
  return &::custom_interfaces::action::rosidl_typesupport_c::MoveTCP_Goal_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "custom_interfaces/action/detail/move_tcp__struct.h"
// already included above
// #include "custom_interfaces/action/detail/move_tcp__type_support.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace custom_interfaces
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _MoveTCP_Result_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _MoveTCP_Result_type_support_ids_t;

static const _MoveTCP_Result_type_support_ids_t _MoveTCP_Result_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _MoveTCP_Result_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _MoveTCP_Result_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _MoveTCP_Result_type_support_symbol_names_t _MoveTCP_Result_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, custom_interfaces, action, MoveTCP_Result)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, custom_interfaces, action, MoveTCP_Result)),
  }
};

typedef struct _MoveTCP_Result_type_support_data_t
{
  void * data[2];
} _MoveTCP_Result_type_support_data_t;

static _MoveTCP_Result_type_support_data_t _MoveTCP_Result_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _MoveTCP_Result_message_typesupport_map = {
  2,
  "custom_interfaces",
  &_MoveTCP_Result_message_typesupport_ids.typesupport_identifier[0],
  &_MoveTCP_Result_message_typesupport_symbol_names.symbol_name[0],
  &_MoveTCP_Result_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t MoveTCP_Result_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_MoveTCP_Result_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace custom_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, custom_interfaces, action, MoveTCP_Result)() {
  return &::custom_interfaces::action::rosidl_typesupport_c::MoveTCP_Result_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "custom_interfaces/action/detail/move_tcp__struct.h"
// already included above
// #include "custom_interfaces/action/detail/move_tcp__type_support.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace custom_interfaces
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _MoveTCP_Feedback_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _MoveTCP_Feedback_type_support_ids_t;

static const _MoveTCP_Feedback_type_support_ids_t _MoveTCP_Feedback_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _MoveTCP_Feedback_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _MoveTCP_Feedback_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _MoveTCP_Feedback_type_support_symbol_names_t _MoveTCP_Feedback_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, custom_interfaces, action, MoveTCP_Feedback)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, custom_interfaces, action, MoveTCP_Feedback)),
  }
};

typedef struct _MoveTCP_Feedback_type_support_data_t
{
  void * data[2];
} _MoveTCP_Feedback_type_support_data_t;

static _MoveTCP_Feedback_type_support_data_t _MoveTCP_Feedback_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _MoveTCP_Feedback_message_typesupport_map = {
  2,
  "custom_interfaces",
  &_MoveTCP_Feedback_message_typesupport_ids.typesupport_identifier[0],
  &_MoveTCP_Feedback_message_typesupport_symbol_names.symbol_name[0],
  &_MoveTCP_Feedback_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t MoveTCP_Feedback_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_MoveTCP_Feedback_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace custom_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, custom_interfaces, action, MoveTCP_Feedback)() {
  return &::custom_interfaces::action::rosidl_typesupport_c::MoveTCP_Feedback_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "custom_interfaces/action/detail/move_tcp__struct.h"
// already included above
// #include "custom_interfaces/action/detail/move_tcp__type_support.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace custom_interfaces
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _MoveTCP_SendGoal_Request_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _MoveTCP_SendGoal_Request_type_support_ids_t;

static const _MoveTCP_SendGoal_Request_type_support_ids_t _MoveTCP_SendGoal_Request_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _MoveTCP_SendGoal_Request_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _MoveTCP_SendGoal_Request_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _MoveTCP_SendGoal_Request_type_support_symbol_names_t _MoveTCP_SendGoal_Request_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, custom_interfaces, action, MoveTCP_SendGoal_Request)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, custom_interfaces, action, MoveTCP_SendGoal_Request)),
  }
};

typedef struct _MoveTCP_SendGoal_Request_type_support_data_t
{
  void * data[2];
} _MoveTCP_SendGoal_Request_type_support_data_t;

static _MoveTCP_SendGoal_Request_type_support_data_t _MoveTCP_SendGoal_Request_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _MoveTCP_SendGoal_Request_message_typesupport_map = {
  2,
  "custom_interfaces",
  &_MoveTCP_SendGoal_Request_message_typesupport_ids.typesupport_identifier[0],
  &_MoveTCP_SendGoal_Request_message_typesupport_symbol_names.symbol_name[0],
  &_MoveTCP_SendGoal_Request_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t MoveTCP_SendGoal_Request_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_MoveTCP_SendGoal_Request_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace custom_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, custom_interfaces, action, MoveTCP_SendGoal_Request)() {
  return &::custom_interfaces::action::rosidl_typesupport_c::MoveTCP_SendGoal_Request_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "custom_interfaces/action/detail/move_tcp__struct.h"
// already included above
// #include "custom_interfaces/action/detail/move_tcp__type_support.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace custom_interfaces
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _MoveTCP_SendGoal_Response_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _MoveTCP_SendGoal_Response_type_support_ids_t;

static const _MoveTCP_SendGoal_Response_type_support_ids_t _MoveTCP_SendGoal_Response_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _MoveTCP_SendGoal_Response_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _MoveTCP_SendGoal_Response_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _MoveTCP_SendGoal_Response_type_support_symbol_names_t _MoveTCP_SendGoal_Response_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, custom_interfaces, action, MoveTCP_SendGoal_Response)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, custom_interfaces, action, MoveTCP_SendGoal_Response)),
  }
};

typedef struct _MoveTCP_SendGoal_Response_type_support_data_t
{
  void * data[2];
} _MoveTCP_SendGoal_Response_type_support_data_t;

static _MoveTCP_SendGoal_Response_type_support_data_t _MoveTCP_SendGoal_Response_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _MoveTCP_SendGoal_Response_message_typesupport_map = {
  2,
  "custom_interfaces",
  &_MoveTCP_SendGoal_Response_message_typesupport_ids.typesupport_identifier[0],
  &_MoveTCP_SendGoal_Response_message_typesupport_symbol_names.symbol_name[0],
  &_MoveTCP_SendGoal_Response_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t MoveTCP_SendGoal_Response_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_MoveTCP_SendGoal_Response_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace custom_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, custom_interfaces, action, MoveTCP_SendGoal_Response)() {
  return &::custom_interfaces::action::rosidl_typesupport_c::MoveTCP_SendGoal_Response_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "custom_interfaces/action/detail/move_tcp__type_support.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
#include "rosidl_typesupport_c/service_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace custom_interfaces
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _MoveTCP_SendGoal_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _MoveTCP_SendGoal_type_support_ids_t;

static const _MoveTCP_SendGoal_type_support_ids_t _MoveTCP_SendGoal_service_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _MoveTCP_SendGoal_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _MoveTCP_SendGoal_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _MoveTCP_SendGoal_type_support_symbol_names_t _MoveTCP_SendGoal_service_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, custom_interfaces, action, MoveTCP_SendGoal)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, custom_interfaces, action, MoveTCP_SendGoal)),
  }
};

typedef struct _MoveTCP_SendGoal_type_support_data_t
{
  void * data[2];
} _MoveTCP_SendGoal_type_support_data_t;

static _MoveTCP_SendGoal_type_support_data_t _MoveTCP_SendGoal_service_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _MoveTCP_SendGoal_service_typesupport_map = {
  2,
  "custom_interfaces",
  &_MoveTCP_SendGoal_service_typesupport_ids.typesupport_identifier[0],
  &_MoveTCP_SendGoal_service_typesupport_symbol_names.symbol_name[0],
  &_MoveTCP_SendGoal_service_typesupport_data.data[0],
};

static const rosidl_service_type_support_t MoveTCP_SendGoal_service_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_MoveTCP_SendGoal_service_typesupport_map),
  rosidl_typesupport_c__get_service_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace custom_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_c, custom_interfaces, action, MoveTCP_SendGoal)() {
  return &::custom_interfaces::action::rosidl_typesupport_c::MoveTCP_SendGoal_service_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "custom_interfaces/action/detail/move_tcp__struct.h"
// already included above
// #include "custom_interfaces/action/detail/move_tcp__type_support.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace custom_interfaces
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _MoveTCP_GetResult_Request_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _MoveTCP_GetResult_Request_type_support_ids_t;

static const _MoveTCP_GetResult_Request_type_support_ids_t _MoveTCP_GetResult_Request_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _MoveTCP_GetResult_Request_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _MoveTCP_GetResult_Request_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _MoveTCP_GetResult_Request_type_support_symbol_names_t _MoveTCP_GetResult_Request_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, custom_interfaces, action, MoveTCP_GetResult_Request)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, custom_interfaces, action, MoveTCP_GetResult_Request)),
  }
};

typedef struct _MoveTCP_GetResult_Request_type_support_data_t
{
  void * data[2];
} _MoveTCP_GetResult_Request_type_support_data_t;

static _MoveTCP_GetResult_Request_type_support_data_t _MoveTCP_GetResult_Request_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _MoveTCP_GetResult_Request_message_typesupport_map = {
  2,
  "custom_interfaces",
  &_MoveTCP_GetResult_Request_message_typesupport_ids.typesupport_identifier[0],
  &_MoveTCP_GetResult_Request_message_typesupport_symbol_names.symbol_name[0],
  &_MoveTCP_GetResult_Request_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t MoveTCP_GetResult_Request_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_MoveTCP_GetResult_Request_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace custom_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, custom_interfaces, action, MoveTCP_GetResult_Request)() {
  return &::custom_interfaces::action::rosidl_typesupport_c::MoveTCP_GetResult_Request_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "custom_interfaces/action/detail/move_tcp__struct.h"
// already included above
// #include "custom_interfaces/action/detail/move_tcp__type_support.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace custom_interfaces
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _MoveTCP_GetResult_Response_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _MoveTCP_GetResult_Response_type_support_ids_t;

static const _MoveTCP_GetResult_Response_type_support_ids_t _MoveTCP_GetResult_Response_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _MoveTCP_GetResult_Response_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _MoveTCP_GetResult_Response_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _MoveTCP_GetResult_Response_type_support_symbol_names_t _MoveTCP_GetResult_Response_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, custom_interfaces, action, MoveTCP_GetResult_Response)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, custom_interfaces, action, MoveTCP_GetResult_Response)),
  }
};

typedef struct _MoveTCP_GetResult_Response_type_support_data_t
{
  void * data[2];
} _MoveTCP_GetResult_Response_type_support_data_t;

static _MoveTCP_GetResult_Response_type_support_data_t _MoveTCP_GetResult_Response_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _MoveTCP_GetResult_Response_message_typesupport_map = {
  2,
  "custom_interfaces",
  &_MoveTCP_GetResult_Response_message_typesupport_ids.typesupport_identifier[0],
  &_MoveTCP_GetResult_Response_message_typesupport_symbol_names.symbol_name[0],
  &_MoveTCP_GetResult_Response_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t MoveTCP_GetResult_Response_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_MoveTCP_GetResult_Response_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace custom_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, custom_interfaces, action, MoveTCP_GetResult_Response)() {
  return &::custom_interfaces::action::rosidl_typesupport_c::MoveTCP_GetResult_Response_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "custom_interfaces/action/detail/move_tcp__type_support.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/service_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace custom_interfaces
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _MoveTCP_GetResult_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _MoveTCP_GetResult_type_support_ids_t;

static const _MoveTCP_GetResult_type_support_ids_t _MoveTCP_GetResult_service_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _MoveTCP_GetResult_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _MoveTCP_GetResult_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _MoveTCP_GetResult_type_support_symbol_names_t _MoveTCP_GetResult_service_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, custom_interfaces, action, MoveTCP_GetResult)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, custom_interfaces, action, MoveTCP_GetResult)),
  }
};

typedef struct _MoveTCP_GetResult_type_support_data_t
{
  void * data[2];
} _MoveTCP_GetResult_type_support_data_t;

static _MoveTCP_GetResult_type_support_data_t _MoveTCP_GetResult_service_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _MoveTCP_GetResult_service_typesupport_map = {
  2,
  "custom_interfaces",
  &_MoveTCP_GetResult_service_typesupport_ids.typesupport_identifier[0],
  &_MoveTCP_GetResult_service_typesupport_symbol_names.symbol_name[0],
  &_MoveTCP_GetResult_service_typesupport_data.data[0],
};

static const rosidl_service_type_support_t MoveTCP_GetResult_service_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_MoveTCP_GetResult_service_typesupport_map),
  rosidl_typesupport_c__get_service_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace custom_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_c, custom_interfaces, action, MoveTCP_GetResult)() {
  return &::custom_interfaces::action::rosidl_typesupport_c::MoveTCP_GetResult_service_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "custom_interfaces/action/detail/move_tcp__struct.h"
// already included above
// #include "custom_interfaces/action/detail/move_tcp__type_support.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace custom_interfaces
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _MoveTCP_FeedbackMessage_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _MoveTCP_FeedbackMessage_type_support_ids_t;

static const _MoveTCP_FeedbackMessage_type_support_ids_t _MoveTCP_FeedbackMessage_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _MoveTCP_FeedbackMessage_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _MoveTCP_FeedbackMessage_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _MoveTCP_FeedbackMessage_type_support_symbol_names_t _MoveTCP_FeedbackMessage_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, custom_interfaces, action, MoveTCP_FeedbackMessage)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, custom_interfaces, action, MoveTCP_FeedbackMessage)),
  }
};

typedef struct _MoveTCP_FeedbackMessage_type_support_data_t
{
  void * data[2];
} _MoveTCP_FeedbackMessage_type_support_data_t;

static _MoveTCP_FeedbackMessage_type_support_data_t _MoveTCP_FeedbackMessage_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _MoveTCP_FeedbackMessage_message_typesupport_map = {
  2,
  "custom_interfaces",
  &_MoveTCP_FeedbackMessage_message_typesupport_ids.typesupport_identifier[0],
  &_MoveTCP_FeedbackMessage_message_typesupport_symbol_names.symbol_name[0],
  &_MoveTCP_FeedbackMessage_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t MoveTCP_FeedbackMessage_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_MoveTCP_FeedbackMessage_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace custom_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, custom_interfaces, action, MoveTCP_FeedbackMessage)() {
  return &::custom_interfaces::action::rosidl_typesupport_c::MoveTCP_FeedbackMessage_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

#include "action_msgs/msg/goal_status_array.h"
#include "action_msgs/srv/cancel_goal.h"
#include "custom_interfaces/action/move_tcp.h"
// already included above
// #include "custom_interfaces/action/detail/move_tcp__type_support.h"

static rosidl_action_type_support_t _custom_interfaces__action__MoveTCP__typesupport_c;

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_action_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__ACTION_SYMBOL_NAME(
  rosidl_typesupport_c, custom_interfaces, action, MoveTCP)()
{
  // Thread-safe by always writing the same values to the static struct
  _custom_interfaces__action__MoveTCP__typesupport_c.goal_service_type_support =
    ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(
    rosidl_typesupport_c, custom_interfaces, action, MoveTCP_SendGoal)();
  _custom_interfaces__action__MoveTCP__typesupport_c.result_service_type_support =
    ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(
    rosidl_typesupport_c, custom_interfaces, action, MoveTCP_GetResult)();
  _custom_interfaces__action__MoveTCP__typesupport_c.cancel_service_type_support =
    ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(
    rosidl_typesupport_c, action_msgs, srv, CancelGoal)();
  _custom_interfaces__action__MoveTCP__typesupport_c.feedback_message_type_support =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c, custom_interfaces, action, MoveTCP_FeedbackMessage)();
  _custom_interfaces__action__MoveTCP__typesupport_c.status_message_type_support =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c, action_msgs, msg, GoalStatusArray)();

  return &_custom_interfaces__action__MoveTCP__typesupport_c;
}

#ifdef __cplusplus
}
#endif

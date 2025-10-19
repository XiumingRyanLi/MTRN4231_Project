# generated from rosidl_generator_py/resource/_idl.py.em
# with input from chess_arm_executor:action/ExecuteMove.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_ExecuteMove_Goal(type):
    """Metaclass of message 'ExecuteMove_Goal'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
        'MOVE': 0,
        'GO_HOME': 1,
        'PAWN': 0,
        'KNIGHT': 1,
        'BISHOP': 2,
        'ROOK': 3,
        'QUEEN': 4,
        'KING': 5,
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('chess_arm_executor')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'chess_arm_executor.action.ExecuteMove_Goal')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__execute_move__goal
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__execute_move__goal
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__execute_move__goal
            cls._TYPE_SUPPORT = module.type_support_msg__action__execute_move__goal
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__execute_move__goal

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
            'MOVE': cls.__constants['MOVE'],
            'GO_HOME': cls.__constants['GO_HOME'],
            'PAWN': cls.__constants['PAWN'],
            'KNIGHT': cls.__constants['KNIGHT'],
            'BISHOP': cls.__constants['BISHOP'],
            'ROOK': cls.__constants['ROOK'],
            'QUEEN': cls.__constants['QUEEN'],
            'KING': cls.__constants['KING'],
        }

    @property
    def MOVE(self):
        """Message constant 'MOVE'."""
        return Metaclass_ExecuteMove_Goal.__constants['MOVE']

    @property
    def GO_HOME(self):
        """Message constant 'GO_HOME'."""
        return Metaclass_ExecuteMove_Goal.__constants['GO_HOME']

    @property
    def PAWN(self):
        """Message constant 'PAWN'."""
        return Metaclass_ExecuteMove_Goal.__constants['PAWN']

    @property
    def KNIGHT(self):
        """Message constant 'KNIGHT'."""
        return Metaclass_ExecuteMove_Goal.__constants['KNIGHT']

    @property
    def BISHOP(self):
        """Message constant 'BISHOP'."""
        return Metaclass_ExecuteMove_Goal.__constants['BISHOP']

    @property
    def ROOK(self):
        """Message constant 'ROOK'."""
        return Metaclass_ExecuteMove_Goal.__constants['ROOK']

    @property
    def QUEEN(self):
        """Message constant 'QUEEN'."""
        return Metaclass_ExecuteMove_Goal.__constants['QUEEN']

    @property
    def KING(self):
        """Message constant 'KING'."""
        return Metaclass_ExecuteMove_Goal.__constants['KING']


class ExecuteMove_Goal(metaclass=Metaclass_ExecuteMove_Goal):
    """
    Message class 'ExecuteMove_Goal'.

    Constants:
      MOVE
      GO_HOME
      PAWN
      KNIGHT
      BISHOP
      ROOK
      QUEEN
      KING
    """

    __slots__ = [
        '_mode',
        '_src_square',
        '_dst_square',
        '_piece_type',
    ]

    _fields_and_field_types = {
        'mode': 'uint8',
        'src_square': 'string',
        'dst_square': 'string',
        'piece_type': 'uint8',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.mode = kwargs.get('mode', int())
        self.src_square = kwargs.get('src_square', str())
        self.dst_square = kwargs.get('dst_square', str())
        self.piece_type = kwargs.get('piece_type', int())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.mode != other.mode:
            return False
        if self.src_square != other.src_square:
            return False
        if self.dst_square != other.dst_square:
            return False
        if self.piece_type != other.piece_type:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def mode(self):
        """Message field 'mode'."""
        return self._mode

    @mode.setter
    def mode(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'mode' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'mode' field must be an unsigned integer in [0, 255]"
        self._mode = value

    @builtins.property
    def src_square(self):
        """Message field 'src_square'."""
        return self._src_square

    @src_square.setter
    def src_square(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'src_square' field must be of type 'str'"
        self._src_square = value

    @builtins.property
    def dst_square(self):
        """Message field 'dst_square'."""
        return self._dst_square

    @dst_square.setter
    def dst_square(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'dst_square' field must be of type 'str'"
        self._dst_square = value

    @builtins.property
    def piece_type(self):
        """Message field 'piece_type'."""
        return self._piece_type

    @piece_type.setter
    def piece_type(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'piece_type' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'piece_type' field must be an unsigned integer in [0, 255]"
        self._piece_type = value


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_ExecuteMove_Result(type):
    """Metaclass of message 'ExecuteMove_Result'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('chess_arm_executor')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'chess_arm_executor.action.ExecuteMove_Result')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__execute_move__result
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__execute_move__result
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__execute_move__result
            cls._TYPE_SUPPORT = module.type_support_msg__action__execute_move__result
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__execute_move__result

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class ExecuteMove_Result(metaclass=Metaclass_ExecuteMove_Result):
    """Message class 'ExecuteMove_Result'."""

    __slots__ = [
        '_ok',
        '_message',
    ]

    _fields_and_field_types = {
        'ok': 'boolean',
        'message': 'string',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.ok = kwargs.get('ok', bool())
        self.message = kwargs.get('message', str())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.ok != other.ok:
            return False
        if self.message != other.message:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def ok(self):
        """Message field 'ok'."""
        return self._ok

    @ok.setter
    def ok(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'ok' field must be of type 'bool'"
        self._ok = value

    @builtins.property
    def message(self):
        """Message field 'message'."""
        return self._message

    @message.setter
    def message(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'message' field must be of type 'str'"
        self._message = value


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_ExecuteMove_Feedback(type):
    """Metaclass of message 'ExecuteMove_Feedback'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('chess_arm_executor')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'chess_arm_executor.action.ExecuteMove_Feedback')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__execute_move__feedback
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__execute_move__feedback
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__execute_move__feedback
            cls._TYPE_SUPPORT = module.type_support_msg__action__execute_move__feedback
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__execute_move__feedback

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class ExecuteMove_Feedback(metaclass=Metaclass_ExecuteMove_Feedback):
    """Message class 'ExecuteMove_Feedback'."""

    __slots__ = [
        '_stage',
    ]

    _fields_and_field_types = {
        'stage': 'string',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.stage = kwargs.get('stage', str())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.stage != other.stage:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def stage(self):
        """Message field 'stage'."""
        return self._stage

    @stage.setter
    def stage(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'stage' field must be of type 'str'"
        self._stage = value


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_ExecuteMove_SendGoal_Request(type):
    """Metaclass of message 'ExecuteMove_SendGoal_Request'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('chess_arm_executor')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'chess_arm_executor.action.ExecuteMove_SendGoal_Request')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__execute_move__send_goal__request
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__execute_move__send_goal__request
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__execute_move__send_goal__request
            cls._TYPE_SUPPORT = module.type_support_msg__action__execute_move__send_goal__request
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__execute_move__send_goal__request

            from chess_arm_executor.action import ExecuteMove
            if ExecuteMove.Goal.__class__._TYPE_SUPPORT is None:
                ExecuteMove.Goal.__class__.__import_type_support__()

            from unique_identifier_msgs.msg import UUID
            if UUID.__class__._TYPE_SUPPORT is None:
                UUID.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class ExecuteMove_SendGoal_Request(metaclass=Metaclass_ExecuteMove_SendGoal_Request):
    """Message class 'ExecuteMove_SendGoal_Request'."""

    __slots__ = [
        '_goal_id',
        '_goal',
    ]

    _fields_and_field_types = {
        'goal_id': 'unique_identifier_msgs/UUID',
        'goal': 'chess_arm_executor/ExecuteMove_Goal',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['unique_identifier_msgs', 'msg'], 'UUID'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['chess_arm_executor', 'action'], 'ExecuteMove_Goal'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from unique_identifier_msgs.msg import UUID
        self.goal_id = kwargs.get('goal_id', UUID())
        from chess_arm_executor.action._execute_move import ExecuteMove_Goal
        self.goal = kwargs.get('goal', ExecuteMove_Goal())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.goal_id != other.goal_id:
            return False
        if self.goal != other.goal:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def goal_id(self):
        """Message field 'goal_id'."""
        return self._goal_id

    @goal_id.setter
    def goal_id(self, value):
        if __debug__:
            from unique_identifier_msgs.msg import UUID
            assert \
                isinstance(value, UUID), \
                "The 'goal_id' field must be a sub message of type 'UUID'"
        self._goal_id = value

    @builtins.property
    def goal(self):
        """Message field 'goal'."""
        return self._goal

    @goal.setter
    def goal(self, value):
        if __debug__:
            from chess_arm_executor.action._execute_move import ExecuteMove_Goal
            assert \
                isinstance(value, ExecuteMove_Goal), \
                "The 'goal' field must be a sub message of type 'ExecuteMove_Goal'"
        self._goal = value


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_ExecuteMove_SendGoal_Response(type):
    """Metaclass of message 'ExecuteMove_SendGoal_Response'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('chess_arm_executor')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'chess_arm_executor.action.ExecuteMove_SendGoal_Response')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__execute_move__send_goal__response
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__execute_move__send_goal__response
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__execute_move__send_goal__response
            cls._TYPE_SUPPORT = module.type_support_msg__action__execute_move__send_goal__response
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__execute_move__send_goal__response

            from builtin_interfaces.msg import Time
            if Time.__class__._TYPE_SUPPORT is None:
                Time.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class ExecuteMove_SendGoal_Response(metaclass=Metaclass_ExecuteMove_SendGoal_Response):
    """Message class 'ExecuteMove_SendGoal_Response'."""

    __slots__ = [
        '_accepted',
        '_stamp',
    ]

    _fields_and_field_types = {
        'accepted': 'boolean',
        'stamp': 'builtin_interfaces/Time',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['builtin_interfaces', 'msg'], 'Time'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.accepted = kwargs.get('accepted', bool())
        from builtin_interfaces.msg import Time
        self.stamp = kwargs.get('stamp', Time())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.accepted != other.accepted:
            return False
        if self.stamp != other.stamp:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def accepted(self):
        """Message field 'accepted'."""
        return self._accepted

    @accepted.setter
    def accepted(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'accepted' field must be of type 'bool'"
        self._accepted = value

    @builtins.property
    def stamp(self):
        """Message field 'stamp'."""
        return self._stamp

    @stamp.setter
    def stamp(self, value):
        if __debug__:
            from builtin_interfaces.msg import Time
            assert \
                isinstance(value, Time), \
                "The 'stamp' field must be a sub message of type 'Time'"
        self._stamp = value


class Metaclass_ExecuteMove_SendGoal(type):
    """Metaclass of service 'ExecuteMove_SendGoal'."""

    _TYPE_SUPPORT = None

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('chess_arm_executor')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'chess_arm_executor.action.ExecuteMove_SendGoal')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_srv__action__execute_move__send_goal

            from chess_arm_executor.action import _execute_move
            if _execute_move.Metaclass_ExecuteMove_SendGoal_Request._TYPE_SUPPORT is None:
                _execute_move.Metaclass_ExecuteMove_SendGoal_Request.__import_type_support__()
            if _execute_move.Metaclass_ExecuteMove_SendGoal_Response._TYPE_SUPPORT is None:
                _execute_move.Metaclass_ExecuteMove_SendGoal_Response.__import_type_support__()


class ExecuteMove_SendGoal(metaclass=Metaclass_ExecuteMove_SendGoal):
    from chess_arm_executor.action._execute_move import ExecuteMove_SendGoal_Request as Request
    from chess_arm_executor.action._execute_move import ExecuteMove_SendGoal_Response as Response

    def __init__(self):
        raise NotImplementedError('Service classes can not be instantiated')


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_ExecuteMove_GetResult_Request(type):
    """Metaclass of message 'ExecuteMove_GetResult_Request'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('chess_arm_executor')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'chess_arm_executor.action.ExecuteMove_GetResult_Request')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__execute_move__get_result__request
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__execute_move__get_result__request
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__execute_move__get_result__request
            cls._TYPE_SUPPORT = module.type_support_msg__action__execute_move__get_result__request
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__execute_move__get_result__request

            from unique_identifier_msgs.msg import UUID
            if UUID.__class__._TYPE_SUPPORT is None:
                UUID.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class ExecuteMove_GetResult_Request(metaclass=Metaclass_ExecuteMove_GetResult_Request):
    """Message class 'ExecuteMove_GetResult_Request'."""

    __slots__ = [
        '_goal_id',
    ]

    _fields_and_field_types = {
        'goal_id': 'unique_identifier_msgs/UUID',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['unique_identifier_msgs', 'msg'], 'UUID'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from unique_identifier_msgs.msg import UUID
        self.goal_id = kwargs.get('goal_id', UUID())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.goal_id != other.goal_id:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def goal_id(self):
        """Message field 'goal_id'."""
        return self._goal_id

    @goal_id.setter
    def goal_id(self, value):
        if __debug__:
            from unique_identifier_msgs.msg import UUID
            assert \
                isinstance(value, UUID), \
                "The 'goal_id' field must be a sub message of type 'UUID'"
        self._goal_id = value


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_ExecuteMove_GetResult_Response(type):
    """Metaclass of message 'ExecuteMove_GetResult_Response'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('chess_arm_executor')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'chess_arm_executor.action.ExecuteMove_GetResult_Response')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__execute_move__get_result__response
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__execute_move__get_result__response
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__execute_move__get_result__response
            cls._TYPE_SUPPORT = module.type_support_msg__action__execute_move__get_result__response
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__execute_move__get_result__response

            from chess_arm_executor.action import ExecuteMove
            if ExecuteMove.Result.__class__._TYPE_SUPPORT is None:
                ExecuteMove.Result.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class ExecuteMove_GetResult_Response(metaclass=Metaclass_ExecuteMove_GetResult_Response):
    """Message class 'ExecuteMove_GetResult_Response'."""

    __slots__ = [
        '_status',
        '_result',
    ]

    _fields_and_field_types = {
        'status': 'int8',
        'result': 'chess_arm_executor/ExecuteMove_Result',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('int8'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['chess_arm_executor', 'action'], 'ExecuteMove_Result'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.status = kwargs.get('status', int())
        from chess_arm_executor.action._execute_move import ExecuteMove_Result
        self.result = kwargs.get('result', ExecuteMove_Result())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.status != other.status:
            return False
        if self.result != other.result:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def status(self):
        """Message field 'status'."""
        return self._status

    @status.setter
    def status(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'status' field must be of type 'int'"
            assert value >= -128 and value < 128, \
                "The 'status' field must be an integer in [-128, 127]"
        self._status = value

    @builtins.property
    def result(self):
        """Message field 'result'."""
        return self._result

    @result.setter
    def result(self, value):
        if __debug__:
            from chess_arm_executor.action._execute_move import ExecuteMove_Result
            assert \
                isinstance(value, ExecuteMove_Result), \
                "The 'result' field must be a sub message of type 'ExecuteMove_Result'"
        self._result = value


class Metaclass_ExecuteMove_GetResult(type):
    """Metaclass of service 'ExecuteMove_GetResult'."""

    _TYPE_SUPPORT = None

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('chess_arm_executor')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'chess_arm_executor.action.ExecuteMove_GetResult')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_srv__action__execute_move__get_result

            from chess_arm_executor.action import _execute_move
            if _execute_move.Metaclass_ExecuteMove_GetResult_Request._TYPE_SUPPORT is None:
                _execute_move.Metaclass_ExecuteMove_GetResult_Request.__import_type_support__()
            if _execute_move.Metaclass_ExecuteMove_GetResult_Response._TYPE_SUPPORT is None:
                _execute_move.Metaclass_ExecuteMove_GetResult_Response.__import_type_support__()


class ExecuteMove_GetResult(metaclass=Metaclass_ExecuteMove_GetResult):
    from chess_arm_executor.action._execute_move import ExecuteMove_GetResult_Request as Request
    from chess_arm_executor.action._execute_move import ExecuteMove_GetResult_Response as Response

    def __init__(self):
        raise NotImplementedError('Service classes can not be instantiated')


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_ExecuteMove_FeedbackMessage(type):
    """Metaclass of message 'ExecuteMove_FeedbackMessage'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('chess_arm_executor')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'chess_arm_executor.action.ExecuteMove_FeedbackMessage')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__execute_move__feedback_message
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__execute_move__feedback_message
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__execute_move__feedback_message
            cls._TYPE_SUPPORT = module.type_support_msg__action__execute_move__feedback_message
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__execute_move__feedback_message

            from chess_arm_executor.action import ExecuteMove
            if ExecuteMove.Feedback.__class__._TYPE_SUPPORT is None:
                ExecuteMove.Feedback.__class__.__import_type_support__()

            from unique_identifier_msgs.msg import UUID
            if UUID.__class__._TYPE_SUPPORT is None:
                UUID.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class ExecuteMove_FeedbackMessage(metaclass=Metaclass_ExecuteMove_FeedbackMessage):
    """Message class 'ExecuteMove_FeedbackMessage'."""

    __slots__ = [
        '_goal_id',
        '_feedback',
    ]

    _fields_and_field_types = {
        'goal_id': 'unique_identifier_msgs/UUID',
        'feedback': 'chess_arm_executor/ExecuteMove_Feedback',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['unique_identifier_msgs', 'msg'], 'UUID'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['chess_arm_executor', 'action'], 'ExecuteMove_Feedback'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from unique_identifier_msgs.msg import UUID
        self.goal_id = kwargs.get('goal_id', UUID())
        from chess_arm_executor.action._execute_move import ExecuteMove_Feedback
        self.feedback = kwargs.get('feedback', ExecuteMove_Feedback())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.goal_id != other.goal_id:
            return False
        if self.feedback != other.feedback:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def goal_id(self):
        """Message field 'goal_id'."""
        return self._goal_id

    @goal_id.setter
    def goal_id(self, value):
        if __debug__:
            from unique_identifier_msgs.msg import UUID
            assert \
                isinstance(value, UUID), \
                "The 'goal_id' field must be a sub message of type 'UUID'"
        self._goal_id = value

    @builtins.property
    def feedback(self):
        """Message field 'feedback'."""
        return self._feedback

    @feedback.setter
    def feedback(self, value):
        if __debug__:
            from chess_arm_executor.action._execute_move import ExecuteMove_Feedback
            assert \
                isinstance(value, ExecuteMove_Feedback), \
                "The 'feedback' field must be a sub message of type 'ExecuteMove_Feedback'"
        self._feedback = value


class Metaclass_ExecuteMove(type):
    """Metaclass of action 'ExecuteMove'."""

    _TYPE_SUPPORT = None

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('chess_arm_executor')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'chess_arm_executor.action.ExecuteMove')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_action__action__execute_move

            from action_msgs.msg import _goal_status_array
            if _goal_status_array.Metaclass_GoalStatusArray._TYPE_SUPPORT is None:
                _goal_status_array.Metaclass_GoalStatusArray.__import_type_support__()
            from action_msgs.srv import _cancel_goal
            if _cancel_goal.Metaclass_CancelGoal._TYPE_SUPPORT is None:
                _cancel_goal.Metaclass_CancelGoal.__import_type_support__()

            from chess_arm_executor.action import _execute_move
            if _execute_move.Metaclass_ExecuteMove_SendGoal._TYPE_SUPPORT is None:
                _execute_move.Metaclass_ExecuteMove_SendGoal.__import_type_support__()
            if _execute_move.Metaclass_ExecuteMove_GetResult._TYPE_SUPPORT is None:
                _execute_move.Metaclass_ExecuteMove_GetResult.__import_type_support__()
            if _execute_move.Metaclass_ExecuteMove_FeedbackMessage._TYPE_SUPPORT is None:
                _execute_move.Metaclass_ExecuteMove_FeedbackMessage.__import_type_support__()


class ExecuteMove(metaclass=Metaclass_ExecuteMove):

    # The goal message defined in the action definition.
    from chess_arm_executor.action._execute_move import ExecuteMove_Goal as Goal
    # The result message defined in the action definition.
    from chess_arm_executor.action._execute_move import ExecuteMove_Result as Result
    # The feedback message defined in the action definition.
    from chess_arm_executor.action._execute_move import ExecuteMove_Feedback as Feedback

    class Impl:

        # The send_goal service using a wrapped version of the goal message as a request.
        from chess_arm_executor.action._execute_move import ExecuteMove_SendGoal as SendGoalService
        # The get_result service using a wrapped version of the result message as a response.
        from chess_arm_executor.action._execute_move import ExecuteMove_GetResult as GetResultService
        # The feedback message with generic fields which wraps the feedback message.
        from chess_arm_executor.action._execute_move import ExecuteMove_FeedbackMessage as FeedbackMessage

        # The generic service to cancel a goal.
        from action_msgs.srv._cancel_goal import CancelGoal as CancelGoalService
        # The generic message for get the status of a goal.
        from action_msgs.msg._goal_status_array import GoalStatusArray as GoalStatusMessage

    def __init__(self):
        raise NotImplementedError('Action classes can not be instantiated')

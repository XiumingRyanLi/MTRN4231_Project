# generated from rosidl_generator_py/resource/_idl.py.em
# with input from interfaces:srv/ChessMove.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_ChessMove_Request(type):
    """Metaclass of message 'ChessMove_Request'."""

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
            module = import_type_support('interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'interfaces.srv.ChessMove_Request')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__chess_move__request
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__chess_move__request
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__chess_move__request
            cls._TYPE_SUPPORT = module.type_support_msg__srv__chess_move__request
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__chess_move__request

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class ChessMove_Request(metaclass=Metaclass_ChessMove_Request):
    """Message class 'ChessMove_Request'."""

    __slots__ = [
        '_user_move',
    ]

    _fields_and_field_types = {
        'user_move': 'string',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.user_move = kwargs.get('user_move', str())

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
        if self.user_move != other.user_move:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def user_move(self):
        """Message field 'user_move'."""
        return self._user_move

    @user_move.setter
    def user_move(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'user_move' field must be of type 'str'"
        self._user_move = value


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_ChessMove_Response(type):
    """Metaclass of message 'ChessMove_Response'."""

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
            module = import_type_support('interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'interfaces.srv.ChessMove_Response')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__chess_move__response
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__chess_move__response
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__chess_move__response
            cls._TYPE_SUPPORT = module.type_support_msg__srv__chess_move__response
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__chess_move__response

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class ChessMove_Response(metaclass=Metaclass_ChessMove_Response):
    """Message class 'ChessMove_Response'."""

    __slots__ = [
        '_robot_move',
        '_is_en_passant',
        '_is_capture',
        '_is_castling',
        '_is_promotion',
    ]

    _fields_and_field_types = {
        'robot_move': 'string',
        'is_en_passant': 'boolean',
        'is_capture': 'boolean',
        'is_castling': 'boolean',
        'is_promotion': 'boolean',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.robot_move = kwargs.get('robot_move', str())
        self.is_en_passant = kwargs.get('is_en_passant', bool())
        self.is_capture = kwargs.get('is_capture', bool())
        self.is_castling = kwargs.get('is_castling', bool())
        self.is_promotion = kwargs.get('is_promotion', bool())

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
        if self.robot_move != other.robot_move:
            return False
        if self.is_en_passant != other.is_en_passant:
            return False
        if self.is_capture != other.is_capture:
            return False
        if self.is_castling != other.is_castling:
            return False
        if self.is_promotion != other.is_promotion:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def robot_move(self):
        """Message field 'robot_move'."""
        return self._robot_move

    @robot_move.setter
    def robot_move(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'robot_move' field must be of type 'str'"
        self._robot_move = value

    @builtins.property
    def is_en_passant(self):
        """Message field 'is_en_passant'."""
        return self._is_en_passant

    @is_en_passant.setter
    def is_en_passant(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'is_en_passant' field must be of type 'bool'"
        self._is_en_passant = value

    @builtins.property
    def is_capture(self):
        """Message field 'is_capture'."""
        return self._is_capture

    @is_capture.setter
    def is_capture(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'is_capture' field must be of type 'bool'"
        self._is_capture = value

    @builtins.property
    def is_castling(self):
        """Message field 'is_castling'."""
        return self._is_castling

    @is_castling.setter
    def is_castling(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'is_castling' field must be of type 'bool'"
        self._is_castling = value

    @builtins.property
    def is_promotion(self):
        """Message field 'is_promotion'."""
        return self._is_promotion

    @is_promotion.setter
    def is_promotion(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'is_promotion' field must be of type 'bool'"
        self._is_promotion = value


class Metaclass_ChessMove(type):
    """Metaclass of service 'ChessMove'."""

    _TYPE_SUPPORT = None

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'interfaces.srv.ChessMove')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_srv__srv__chess_move

            from interfaces.srv import _chess_move
            if _chess_move.Metaclass_ChessMove_Request._TYPE_SUPPORT is None:
                _chess_move.Metaclass_ChessMove_Request.__import_type_support__()
            if _chess_move.Metaclass_ChessMove_Response._TYPE_SUPPORT is None:
                _chess_move.Metaclass_ChessMove_Response.__import_type_support__()


class ChessMove(metaclass=Metaclass_ChessMove):
    from interfaces.srv._chess_move import ChessMove_Request as Request
    from interfaces.srv._chess_move import ChessMove_Response as Response

    def __init__(self):
        raise NotImplementedError('Service classes can not be instantiated')

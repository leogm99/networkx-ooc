import enum
import struct

from networkx.structures.out_of_core_dict import OutOfCoreDict


# Add more types here
# note: ! -> big endian (binary keys are read in "natural" order)
class PrimitiveType(str, enum.Enum):
    INTEGER = "!i"
    FLOAT = "!f"
    DOUBLE = "!d"
    ULONG = "!L"
    EDGE = "@ll" # two elements tuple
    TUPLE = EDGE


class PrimitiveDict(OutOfCoreDict):
    def __init__(self, key_primitive_type: PrimitiveType, value_primitive_type: PrimitiveType):
        super().__init__()
        self._key_format = key_primitive_type.value
        self._value_format = value_primitive_type.value

    def __setitem__(self, key, value):
        super().__setitem__(
            self.__serialize_key(key),
            self.__serialize_value(value),
        )

    def __getitem__(self, key):
        return self.__deserialize_value(super().__getitem__(self.__serialize_key(key)))

    def __iter__(self):
        yield from map(self.__deserialize_key, super().__iter__())

    def __delitem__(self, key) -> None:
        super().__delitem__(self.__serialize_key(key))

    def __contains__(self, key):
        return super().__contains__(key)

    def prefix_iter(self, prefix):
        yield from map(self.__deserialize_key, super().prefix_iter(self.__serialize_key(prefix)))

    def __serialize_key(self, key):
        if key is None:
            return bytes()
        return struct.pack(self._key_format, key)

    def __serialize_value(self, value):
        if value is None:
            return bytes()
        return struct.pack(self._value_format, value)

    def __deserialize_key(self, key):
        if key == bytes():
            return None
        return struct.unpack(self._key_format, key)[0]

    def __deserialize_value(self, value):
        if value == bytes():
            return None
        return struct.unpack(self._value_format, value)[0]


class IntDict(PrimitiveDict):
    def __init__(self):
        super().__init__(PrimitiveType.INTEGER, PrimitiveType.INTEGER)

    def copy(self, c=None):
        return super().copy(IntDict())

class IntFloatDict(PrimitiveDict):
    def __init__(self):
        super().__init__(PrimitiveType.INTEGER, PrimitiveType.FLOAT)

    def copy(self, c=None):
        return super().copy(IntFloatDict())

# class EdgesDict(PrimitiveDict):
#     def __init__(self, key_primitive_type: PrimitiveType = PrimitiveType.EDGE, value_primitive_type: PrimitiveType = PrimitiveType.INTEGER):
#         if key_primitive_type != PrimitiveType.EDGE and value_primitive_type != PrimitiveType.EDGE:
#             raise ValueError("Key or value type must be EDGE")
#         super().__init__(key_primitive_type, value_primitive_type)

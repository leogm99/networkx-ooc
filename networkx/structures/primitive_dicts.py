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


class PrimiviteDict(OutOfCoreDict):
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
        for k in super().__iter__():
            yield self.__deserialize_key(k)

    def __delitem__(self, key) -> None:
        super().__delitem__(self.__serialize_key(key))

    def prefix_iter(self, prefix):
        for k in super().prefix_iter(self.__serialize_key(prefix)):
            yield self.__deserialize_key(k)

    def __serialize_key(self, key):
        return struct.pack(self._key_format, key)

    def __serialize_value(self, value):
        return struct.pack(self._value_format, value)

    def __deserialize_key(self, key):
        return struct.unpack(self._value_format, key)[0]

    def __deserialize_value(self, value):
        return struct.unpack(self._value_format, value)[0]


class IntDict(PrimiviteDict):
    def __init__(self):
        super().__init__(PrimitiveType.INTEGER, PrimitiveType.INTEGER)


class IntFloatDict(PrimiviteDict):
    def __init__(self):
        super().__init__(PrimitiveType.INTEGER, PrimitiveType.FLOAT)

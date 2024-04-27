import struct

from networkx.structures.out_of_core_dict import OutOfCoreDict
from networkx.structures.primitive_dicts import PrimitiveType

__all__ = ["EdgesDict"]

class EdgesDict(OutOfCoreDict):
    def __init__(self, key_primitive_type: PrimitiveType = PrimitiveType.EDGE, value_primitive_type: PrimitiveType = PrimitiveType.INTEGER):
        if key_primitive_type != PrimitiveType.EDGE and value_primitive_type != PrimitiveType.EDGE:
            raise ValueError("Key or value type must be EDGE")
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
        if key is None or key == (None, None):
            return b'\x00' * struct.calcsize(self._key_format)
        if self._key_format == PrimitiveType.EDGE:
            return struct.pack(self._key_format, *key)

        return struct.pack(self._key_format, key)

    def __serialize_value(self, value):
        if value is None or value == (None, None):
            return b'\x00' * struct.calcsize(self._value_format)
        if self._value_format == PrimitiveType.EDGE:
            return struct.pack(self._value_format, *value)

        return struct.pack(self._value_format, value)

    def __deserialize_key(self, key):
        if key == b'\x00' * struct.calcsize(self._key_format):
            return 0 if self._key_format != PrimitiveType.EDGE else (None, None)
        if self._key_format == PrimitiveType.EDGE:
            return struct.unpack(self._key_format, key)

        return struct.unpack(self._key_format, key)[0]

    def __deserialize_value(self, value):
        if value == b'\x00' * struct.calcsize(self._value_format):
             return 0 if self._value_format != PrimitiveType.EDGE else (None, None)
        if self._value_format == PrimitiveType.EDGE:
            return struct.unpack(self._value_format, value)

        return struct.unpack(self._value_format, value)[0]

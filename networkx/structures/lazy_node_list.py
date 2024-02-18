import pickle
import struct
from collections.abc import MutableMapping

from networkx.structures.out_of_core_dict import OutOfCoreDict
from typing import Hashable


class LazyNodeList(MutableMapping):
    def __delitem__(self, key):
        self._inner.__delitem__(LazyNodeList.__serialize_node(key))

    def __getitem__(self, key):
        if not isinstance(key, Hashable):
            raise TypeError("Key must be hashable")
        data = self._inner[LazyNodeList.__serialize_node(key)]
        if data == b"":
            data = {}
            self._inner[LazyNodeList.__serialize_node(key)] = LazyNodeList.__serialize_node_attr(data)
            return data
        return LazyNodeList.__deserialize_node_attr(data)

    def __len__(self):
        return len(self._inner)

    def __iter__(self):
        for k in self._inner:
            yield LazyNodeList.__deserialize_node(k)

    def __init__(self):
        self._inner = OutOfCoreDict()

    def __setitem__(self, key, value):
        if value == b"":
            self._inner[LazyNodeList.__serialize_node(key)] = value
        else:
            self._inner[
                LazyNodeList.__serialize_node(key)
            ] = LazyNodeList.__serialize_node_attr(value)

    def add_node(self, key, value=None):
        if value:
            self.__setitem__(key, value)
            return
        self.__setitem__(key, b"")

    @staticmethod
    def __serialize_node(u):
        return struct.pack('@l', u)

    @staticmethod
    def __deserialize_node(data):
        return struct.unpack('@l', data)[0]

    @staticmethod
    def __serialize_node_attr(attr):
        return pickle.dumps(attr)

    @staticmethod
    def __deserialize_node_attr(data):
        return pickle.loads(data)

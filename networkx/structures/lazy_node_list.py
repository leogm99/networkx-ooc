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

    def __setitem__(self, key, **attr):
        if len(attr) == 0:
            self._inner[LazyNodeList.__serialize_node(key)] = b""
        else:
            try:
                dd = LazyNodeList.__deserialize_node_attr(self._inner[LazyNodeList.__serialize_node(key)])
            except KeyError:
                dd = {}
            dd.update(attr)
            self._inner[
                LazyNodeList.__serialize_node(key)
            ] = LazyNodeList.__serialize_node_attr(dd)

    def add_node(self, key, **attr):
        self.__setitem__(key, **attr)

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

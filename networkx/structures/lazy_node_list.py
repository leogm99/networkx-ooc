import pickle
import struct
from collections.abc import MutableMapping

from networkx.structures.out_of_core_dict import OutOfCoreDict
from networkx.structures.lazy_node import LazyNode
from typing import Hashable


class LazyNodeList(MutableMapping):
    def __delitem__(self, key, ):
        self._inner.__delitem__(LazyNodeList.__serialize_node(key))

    def __getitem__(self, key):
        if not isinstance(key, Hashable):
            raise TypeError("Key must be hashable")
        _ = self._inner[LazyNodeList.__serialize_node(key)]
        return LazyNode(key, self._inner)

    def __len__(self):
        return len(self._inner)

    def __iter__(self):
        for k in self._inner:
            yield LazyNodeList.__deserialize_node(k)

    def __init__(self, enable_attrs: bool = False):
        self._inner = OutOfCoreDict()
        self._enable_attrs = enable_attrs

    def __setitem__(self, key, **attr):
        if len(attr) != 0:
            self._enable_attrs = True
        if self._enable_attrs:
            try:
                dd = self._inner[LazyNodeList.__serialize_node(key)]
                if len(attr) == 0:
                    return
                if dd != b'':
                    dd = LazyNodeList.__deserialize_node_attr(dd)
                    dd.update(**attr)
                    dd = LazyNodeList.__serialize_node_attr(attr)
                else:
                    dd = LazyNodeList.__serialize_node_attr(attr)
            except KeyError:
                if len(attr) == 0:
                    dd = b''
                else:
                    dd = LazyNodeList.__serialize_node_attr(attr)
            self._inner[
                LazyNodeList.__serialize_node(key)
            ] = dd
        else:
            try:
                dd = LazyNodeList.__deserialize_node_attr(self._inner[LazyNodeList.__serialize_node(key)])
            except KeyError:
                if (len(attr) == 0):
                    dd = b''
                else:
                    dd = {}
                    dd.update(attr)
            self._inner[
                LazyNodeList.__serialize_node(key)
            ] = LazyNodeList.__serialize_node_attr(dd)

    def add_node(self, key, **attr):
        self.__setitem__(key, **attr)

    @staticmethod
    def __serialize_node(u):
        return struct.pack('!l', u)

    @staticmethod
    def __deserialize_node(data):
        return struct.unpack('!l', data)[0]

    @staticmethod
    def __serialize_node_attr(attr):
        if attr == b'':
            return b''
        return pickle.dumps(attr)

    @staticmethod
    def __deserialize_node_attr(data):
        if data == b'':
            return {}
        return pickle.loads(data)

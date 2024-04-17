import pickle
import struct
from typing import MutableMapping


class LazyNode(MutableMapping):
    def __init__(self, node, store):
        self._node = LazyNode.__serialize_node(node)
        self._store = store

    def __setitem__(self, key, value):
        data = self._store[self._node]
        if data == b"":
            data = {}
            self._store[self._node][LazyNode.__serialize_node(key)] = LazyNode.__serialize_attr(data)
        else:
            LazyNode.__deserialize_attr(data)
        data[key] = value
        self._store[self._node][LazyNode.__serialize_node(key)] = LazyNode.__serialize_attr(data)

    def __delitem__(self, key):
        data = self._store[self._node]
        if data == b"":
            data = {}
            self._store[self._node][LazyNode.__serialize_node(key)] = LazyNode.__serialize_attr(data)
        else:
            LazyNode.__deserialize_attr(data)
        del data[key]
        self._store[self._node][LazyNode.__serialize_node(key)] = LazyNode.__serialize_attr(data)

    def __getitem__(self, key):
        data = self._store[self._node]
        if data == b"":
            raise KeyError(key)
        return LazyNode.__deserialize_attr(data)[key]

    def __len__(self):
        data = self._store[self._node]
        if data == b"":
            return 0
        else:
            data = LazyNode.__deserialize_attr(data)
            return len(data)

    def __iter__(self):
        data = self._store[self._node]
        if data == b"":
            data = {}
            self._store[self._node] = LazyNode.__serialize_attr(data)
        else:
            data = LazyNode.__deserialize_attr(data)
        yield data

    def __eq__(self, other):
        data = self._store[self._node]
        if data == b"":
            data = {}
        else:
            data = LazyNode.__deserialize_attr(data)
        return data == other

    @staticmethod
    def __serialize_node(u):
        return struct.pack('!l', u)

    @staticmethod
    def __deserialize_node(data):
        return struct.unpack('!l', data)[0]

    @staticmethod
    def __serialize_attr(attr):
        return pickle.dumps(attr)

    @staticmethod
    def __deserialize_attr(data):
        return pickle.loads(data)

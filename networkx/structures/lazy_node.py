from typing import MutableMapping

from networkx.classes.lazygraph_serializer import LazyGraphSerializer


class LazyNode(MutableMapping):
    def __init__(self, node, store, serializer: LazyGraphSerializer):
        self._node = serializer.serialize_node(node)
        self._store = store
        self._serializer = serializer

    def __setitem__(self, key, value):
        data = self._store[self._node]
        if data == b"":
            data = {key: value}
        else:
            data = self._serializer.deserialize_attr(data)
            data[key] = value
        self._store[self._node] = self._serializer.serialize_attr(data)

    def __delitem__(self, key):
        data = self._store[self._node]
        if data == b"":
            raise KeyError(key)
        data = self._serializer.deserialize_attr(data)
        del data[key]
        self._store[self._node] = self._serializer.serialize_attr(data)

    def __getitem__(self, key):
        data = self._store[self._node]
        if data == b"":
            raise KeyError(key)
        return self._serializer.deserialize_attr(data)[key]

    def __len__(self):
        data = self._store[self._node]
        if data == b"":
            return 0
        return len(self._serializer.deserialize_attr(data))

    def __iter__(self):
        data = self._store[self._node]
        if data == b"":
            data = {}
            # do we need to store anything here?
            # self._store[self._node] = self._serializer.serialize_attr(data)
        else:
            data = self._serializer.deserialize_attr(data)
        yield data

    def __eq__(self, other):
        data = self._store[self._node]
        if data == b"":
            data = {}
        else:
            data = self._serializer.deserialize_attr(data)
        return data == other

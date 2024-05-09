import pickle
import struct
from collections.abc import MutableMapping


class LazyEdge(MutableMapping):
    def __init__(self, source_node, store):
        self._source_node = source_node
        self._store = store

    def __setitem__(self, key, **attr):
        pass

    def __delitem__(self, key):
        pass

    def __getitem__(self, v):
        edge_key = LazyEdge.__serialize_edge(self._source_node, v)
        inner_attr = self._store[LazyEdge.__serialize_edge(self._source_node, v)]
        if inner_attr is None or inner_attr == b"":
            inner_attr = {}
            self._store[edge_key] = LazyEdge.__serialize_attr(inner_attr)
        else:
            inner_attr = LazyEdge.__deserialize_attr(inner_attr)
        return inner_attr

    def __len__(self):
        count = 0
        for _ in self._store.prefix_iter(prefix=struct.pack('!l', self._source_node)):
            count += 1
        return count

    def __iter__(self):
        prefix = struct.pack('!l', self._source_node)
        # yield from map(lambda k: struct.unpack('!l', k)[0], self._store.prefix_iter(prefix=prefix))
        for k in self._store.prefix_iter(prefix=prefix):
            try:
                yield struct.unpack('!l', k)[0]
            except struct.error:
                continue

    @staticmethod
    def __serialize_edge(u, v):
        return struct.pack('!2l', u, v)

    @staticmethod
    def __deserialize_edge(data: bytes):
        return struct.unpack('!2l', data)

    @staticmethod
    def __serialize_attr(attr):
        return pickle.dumps(attr)

    @staticmethod
    def __deserialize_attr(data):
        return pickle.loads(data)

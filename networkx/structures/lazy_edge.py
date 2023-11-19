import pickle
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
        if inner_attr is None:
            inner_attr = {}
            self._store[edge_key] = LazyEdge.__serialize_attr(inner_attr)
        else:
            inner_attr = LazyEdge.__deserialize_attr(inner_attr)
        return inner_attr

    def __len__(self):
        count = 0
        for _ in self._store.prefix_iter(prefix=self._source_node.encode() + b"\x00"):
            count += 1
        return count

    def __iter__(self):
        for k, _ in self._store.prefix_iter(
            prefix=self._source_node.encode() + b"\x00"
        ):
            yield k.decode()

    @staticmethod
    def __serialize_edge(u, v):
        return u.encode() + b"\x00" + v.encode()

    @staticmethod
    def __deserialize_edge(data: bytes):
        sep = data.find(b"\x00")
        return data[:sep].decode(), data[sep + 1 :].decode()

    @staticmethod
    def __serialize_attr(attr):
        return pickle.dumps(attr)

    @staticmethod
    def __deserialize_attr(data):
        return pickle.loads(data)

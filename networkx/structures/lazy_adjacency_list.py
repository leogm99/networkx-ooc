import pickle
import struct
import typing
from collections.abc import MutableMapping

from networkx.structures.lazy_edge import LazyEdge
from networkx.structures.out_of_core_dict import OutOfCoreDict


class LazyAdjacencyList(MutableMapping):
    def __init__(self):
        self._inner = OutOfCoreDict()

    def __setitem__(self, key, value):
        # Nothing to really do here
        pass

    def __delitem__(self, key):
        for k in self._inner:
            if k == key:
                del self._inner[k]

    def add_edge(self, u, v, **attr):
        if len(attr) == 0:
            self._inner[LazyAdjacencyList.__serialize_edge(u, v)] = b""
        else:
            try:
                dd = LazyAdjacencyList.__deserialize_attr(self._inner[LazyAdjacencyList.__serialize_edge(u, v)])
            except (KeyError, EOFError):
                dd = {}

            dd.update(attr)
            self._inner[
                LazyAdjacencyList.__serialize_edge(u, v)
            ] = LazyAdjacencyList.__serialize_attr(dd)

    def __getitem__(self, u):
        if not isinstance(u, typing.Hashable):
            raise TypeError(f"unhashable type: {type(u)}")
        # hackish
        try:
            next(self._inner.prefix_iter(struct.pack('!l', u)))
        except StopIteration:
            raise KeyError(f"Node {u} not found")
        return LazyEdge(source_node=u, store=self._inner)

    def __len__(self):
        # directed or undirected?
        return self._inner.__len__()

    def __iter__(self):
        # hackish
        last_seen = None
        for k in self._inner:
            u, v = LazyAdjacencyList.__deserialize_edge(k)
            if u == last_seen:
                continue
            last_seen = u
            yield u

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

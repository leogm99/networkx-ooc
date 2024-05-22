import typing
from collections.abc import Mapping

from networkx.classes.lazygraph_serializer import LazyGraphSerializer
from networkx.structures.lazy_edge import LazyEdge
from networkx.structures.out_of_core_dict import OutOfCoreDict


class LazyAdjacencyList(Mapping):
    def __init__(self, serializer=LazyGraphSerializer()):
        self._serializer = serializer
        self._inner = OutOfCoreDict()

    def __delitem__(self, key):
        for k in self._inner:
            if k == key:
                del self._inner[k]

    def add_edge(self, u, v, **attr):
        if len(attr) == 0:
            self._inner[self._serializer.serialize_edge(u, v)] = b""
        else:
            try:
                dd = self._serializer.deserialize_attr(self._inner[self._serializer.serialize_edge(u, v)])
                if dd == b'':
                    dd = {}
            except (KeyError, EOFError):
                dd = {}

            dd.update(attr)
            self._inner[
                self._serializer.serialize_edge(u, v)
            ] = self._serializer.serialize_attr(dd)

    def __getitem__(self, u):
        if not isinstance(u, typing.Hashable):
            raise TypeError(f"unhashable type: {type(u)}")
        # hackish
        try:
            next(self._inner.prefix_iter(self._serializer.serialize_node(u)))
        except StopIteration:
            raise KeyError(f"Node {u} not found")
        return LazyEdge(source_node=u, store=self._inner, serializer=self._serializer)

    def __len__(self):
        # directed or undirected?
        return self._inner.__len__()

    def __iter__(self):
        # hackish
        last_seen = None
        for k in self._inner:
            u, v = self._serializer.deserialize_edge(k)
            if u == last_seen:
                continue
            last_seen = u
            yield u
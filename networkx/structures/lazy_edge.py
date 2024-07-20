from collections.abc import Mapping

from networkx.classes.out_of_core_graph_serializer import OutOfCoreGraphSerializer


class LazyEdge(Mapping):
    def __init__(self, source_node, store, serializer: OutOfCoreGraphSerializer):
        self._source_node = source_node
        self._store = store
        self.__serializer = serializer

    def __getitem__(self, v):
        edge_key = self.__serializer.serialize_edge(self._source_node, v)
        inner_attr = self._store[edge_key]
        if inner_attr is None or inner_attr == b"":
            inner_attr = {}
            self._store[edge_key] = self.__serializer.serialize_attr(inner_attr)
        else:
            inner_attr = self.__serializer.deserialize_attr(inner_attr)
        return inner_attr

    def __len__(self):
        count = 0
        for _ in self._store.prefix_iter(prefix=self.__serializer.serialize_node(self._source_node)):
            count += 1
        return count

    def __iter__(self):
        prefix = self.__serializer.serialize_node(self._source_node)
        yield from map(self.__serializer.deserialize_node, self._store.prefix_iter(prefix=prefix))

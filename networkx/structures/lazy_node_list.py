from collections.abc import MutableMapping

from networkx.classes.out_of_core_graph_serializer import OutOfCoreGraphSerializer
from networkx.structures.out_of_core_dict import OutOfCoreDict
from networkx.structures.lazy_node import LazyNode
from typing import Hashable


class LazyNodeList(MutableMapping):
    def __init__(self, serializer=OutOfCoreGraphSerializer(), enable_attrs: bool = False):
        self._serializer = serializer
        self._inner = OutOfCoreDict()
        self._enable_attrs = enable_attrs

    def __delitem__(self, key, ):
        self._inner.__delitem__(self._serializer.serialize_node(key))

    def __getitem__(self, key):
        if not isinstance(key, Hashable):
            raise TypeError("Key must be hashable")
        _ = self._inner[self._serializer.serialize_node(key)]
        return LazyNode(key, self._inner, self._serializer)

    def __len__(self):
        return len(self._inner)

    def __iter__(self):
        for k in self._inner:
            yield self._serializer.deserialize_node(k)

    def __setitem__(self, key, **attr):
        if len(attr) != 0:
            self._enable_attrs = True
        if self._enable_attrs:
            try:
                dd = self._inner[self._serializer.serialize_node(key)]
                if len(attr) == 0:
                    return
                if dd != b'':
                    dd = self._serializer.deserialize_attr(dd)
                    dd.update(**attr)
                    dd = self._serializer.serialize_attr(attr)
                else:
                    dd = self._serializer.serialize_attr(attr)
            except KeyError:
                if len(attr) == 0:
                    dd = b''
                else:
                    dd = self._serializer.serialize_attr(attr)
            self._inner[
                self._serializer.serialize_node(key)
            ] = dd
        else:
            try:
                dd = self._serializer.deserialize_attr(self._inner[self._serializer.serialize_node(key)])
            except KeyError:
                if len(attr) == 0:
                    dd = b''
                else:
                    dd = {}
                    dd.update(attr)
            self._inner[
                self._serializer.serialize_node(key)
            ] = self._serializer.serialize_attr(dd)

    def add_node(self, key, **attr):
        self.__setitem__(key, **attr)

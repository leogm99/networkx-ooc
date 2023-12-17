import pickle
from collections.abc import MutableMapping

from networkx.structures.out_of_core_dict import OutOfCoreDict


class LazyNodeList(MutableMapping):
    def __delitem__(self, key):
        self._inner.__delitem__(LazyNodeList.__serialize_node(key))

    def __getitem__(self, key):
        return self._inner[LazyNodeList.__serialize_node(key)]

    def __len__(self):
        return len(self._inner)

    def __iter__(self):
        for k in self._inner:
            yield LazyNodeList.__deserialize_node(k)

    def __init__(self):
        self._inner = OutOfCoreDict()

    def __setitem__(self, key, value):
        if value == b"":
            self._inner[LazyNodeList.__serialize_node(key)] = value
        else:
            self._inner[
                LazyNodeList.__serialize_node(key)
            ] = LazyNodeList.__serialize_node_attr(value)

    def add_node(self, key):
        self.__setitem__(key, b"")

    @staticmethod
    def __serialize_node(u):
        return u.encode()

    @staticmethod
    def __deserialize_node(data):
        return data.decode()

    @staticmethod
    def __serialize_node_attr(attr):
        return pickle.dumps(attr)

    @staticmethod
    def __deserialize_node_attr(data):
        return pickle.loads(data)

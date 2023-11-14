from typing import MutableMapping

from networkx.structures.lazy_edge import LazyEdge
from networkx.structures.out_of_core_dict import OutOfCoreDict, OutOfCoreDictKeyMode
from cachetools import LRUCache


class LazyAdjacencyList(MutableMapping):
    def __init__(self):
        self._inner = OutOfCoreDict(mode=OutOfCoreDictKeyMode.COMPOSITE)
        self._cache = LRUCache(1024)

    def __setitem__(self, key, value):
        # Nothing to really do here
        pass

    def __delitem__(self, key):
        for k in self._inner.keys():
            u, v = k
            if key in (u, v):
                del self._inner[k]

    def __getitem__(self, key):
        if not key in self._cache:
            self._cache[key] = LazyEdge(inner_dict=self._inner, key=key)
        return self._cache[key]

    def __len__(self):
        # directed or undirected?
        return self._inner.__len__()

    def __iter__(self):
        # hackish
        last_seen = None
        for k in self._inner:
            if k == last_seen:
                continue
            last_seen = k
            yield k

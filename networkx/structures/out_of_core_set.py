from typing import MutableSet
from pyroaring import BitMap

__all__ = ["OutOfCoreSet"]

class OutOfCoreSet(MutableSet):
    def __init__(self, node_to_id_mapping):
        self._node_to_id_mapping = node_to_id_mapping
        self._bitmap = BitMap()

    def add(self, node):
        mapping = self._node_to_id_mapping.get_mapping(node)
        self._bitmap.add(mapping)

    def discard(self, node):
        mapping = self._node_to_id_mapping.get_mapping(node)
        self._bitmap.discard(mapping)

    def __len__(self):
        return len(self._bitmap)
    
    def __contains__(self, item):
        mapping = self._node_to_id_mapping.get_mapping(item)
        return mapping in self._bitmap

    def __iter__(self):
        for k in self._bitmap:
            yield self._node_to_id_mapping.get_node(k)

from typing import MutableSet
from pyroaring import BitMap
from networkx.structures.out_of_core_dict import OutOfCoreDict

__all__ = ["OutOfCoreSet", "BitmapSet"]

class OutOfCoreSet(MutableSet):
    def __init__(self, initial_list = None):
        self._out_of_core_dict = OutOfCoreDict()

        if (initial_list != None):
            for node in initial_list:
                self.add(node)

    def add(self, node):
        self._out_of_core_dict[node] = None

    def discard(self, node):
        if (node in self._out_of_core_dict):
            del self._out_of_core_dict[node]

    def __len__(self):
        return len(self._out_of_core_dict)
    
    def __contains__(self, node):
        return node in self._out_of_core_dict

    def __iter__(self):
        for k in self._out_of_core_dict:
            yield k

class BitmapSet(MutableSet):
    def __init__(self, initial_list = None):
        self._bitmap = BitMap(initial_list)

    def add(self, node):
        self._bitmap.add(node)
    
    def discard(self, node):
        if (node in self._bitmap):
            self._bitmap.discard(node)

    def __len__(self):
        return len(self._bitmap)
    
    def __contains__(self, item):
        return item in self._bitmap
    
    def __iter__(self):
        for k in self._bitmap:
            yield k

from typing import MutableSet
from pyroaring import BitMap
from networkx.structures.out_of_core_dict import OutOfCoreDict

__all__ = ["OutOfCoreSet", "OutOfCoreDictSet", "BitmapSet"]

DUAL = "dual"
OUT_OF_CORE_DICT = "out_of_core_dict"
BITMAP = "bitmap"

class OutOfCoreSet(MutableSet):
    def __init__(self, initial_list = None):
        self._mode = BITMAP
        self._set = BitmapSet() if self._mode != OUT_OF_CORE_DICT else OutOfCoreDictSet()
        self._int_type = self._mode != OUT_OF_CORE_DICT
        
        if (initial_list != None):
            for node in initial_list:
                self.add(node)

    def add(self, node):
        if self._mode == DUAL and self._int_type and not isinstance(node, int):
            self._set_out_of_core_dict_set()
        self._set.add(node)

    def _set_out_of_core_dict_set(self):
        out_of_core_dict_set = OutOfCoreDictSet()
        for k in self._set:
            out_of_core_dict_set.add(k)
        self._set = out_of_core_dict_set
        self._int_type = False

    def discard(self, node):
        self._set.discard(node)

    def __len__(self):
        return len(self._set)
    
    def __contains__(self, node):
        return node in self._set
    
    def __iter__(self):
        for k in self._set:
            yield k

class OutOfCoreDictSet(MutableSet):
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

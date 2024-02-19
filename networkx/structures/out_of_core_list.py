from typing import MutableSequence
from networkx.structures.out_of_core_dict import OutOfCorePickleDict

__all__ = ["OutOfCoreList"]

'''
#TODO
Ver como se usan las listas para ver como conviene implementarla, buscar en internet listas ooc ya hechas.
'''

'''
Esta implementacion de Lista out of core deberia usarse unicamente para algoritmos que solo realicen las operaciones de set, get,
append, len e iter. Operaciones como insert o delete son muy costosas debido al uso de pickle y deberian evitarse.
'''
class OutOfCoreList(MutableSequence):
    def __init__(self, initial_list = None):
        self._out_of_core_dict = OutOfCorePickleDict()
        self._next_id = 0

        if (initial_list != None):
            for item in initial_list:
                self.append(item)

    def __len__(self):
        return self._next_id

    def __getitem__(self, index):
        if index < 0 or index >= self._next_id:
            raise IndexError("list index out of range")
        return self._out_of_core_dict[index]
    
    def __setitem__(self, index, item):
        if index < 0 or index >= self._next_id:
            raise IndexError("list index out of range")
        self._out_of_core_dict[index] = item
    
    def __delitem__(self, index):
        if index < 0 or index >= self._next_id:
            raise IndexError("list index out of range")
        del self._out_of_core_dict[index]
        for i in range(index + 1, self._next_id):
            self._out_of_core_dict[i - 1] = self._out_of_core_dict[i]
        self._next_id -= 1

    def append(self, item):
        self._out_of_core_dict[self._next_id] = item
        self._next_id += 1

    def insert(self, index, item):
        if index < 0 or index > self._next_id:
            raise IndexError("list index out of range")
        for i in range(self._next_id, index, -1):
            self._out_of_core_dict[i] = self._out_of_core_dict[i - 1]
        self._out_of_core_dict[index] = item
        self._next_id += 1

    def __str__(self):
        return str([self._out_of_core_dict[i] for i in range(self._next_id)])
    
    def __iter__(self):
        for i in range(self._next_id):
            yield self._out_of_core_dict[i]

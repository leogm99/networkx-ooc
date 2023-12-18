from typing import MutableSequence
from networkx.structures.out_of_core_dict import OutOfCoreDict

import pickle

__all__ = ["OutOfCoreList"]

'''
#TODO
Ver como se usan las listas para ver como conviene implementarla, buscar en internet listas ooc ya hechas.
'''

class OutOfCoreList(MutableSequence):
    def __init__(self, initial_list = None):
        self._out_of_core_dict = OutOfCoreDict()
        self._next_id = 0

        if (initial_list != None):
            for item in initial_list:
                self.append(item)

    def __len__(self):
        return self._next_id

    def __getitem__(self, index):
        if index < 0 or index >= self._next_id:
            raise IndexError("list index out of range")
        return self.__from_bytes(self._out_of_core_dict[self.__to_bytes(index)])
    
    def __setitem__(self, index, item):
        if index < 0 or index >= self._next_id:
            raise IndexError("list index out of range")
        self._out_of_core_dict[self.__to_bytes(index)] = self.__to_bytes(item)
    
    def __delitem__(self, index):
        if index < 0 or index >= self._next_id:
            raise IndexError("list index out of range")
        del self._out_of_core_dict[self.__to_bytes(index)]
        for i in range(index + 1, self._next_id):
            self._out_of_core_dict[self.__to_bytes(i - 1)] = self._out_of_core_dict[self.__to_bytes(i)]
        self._next_id -= 1

    def append(self, item):
        self._out_of_core_dict[self.__to_bytes(self._next_id)] = self.__to_bytes(item)
        self._next_id += 1

    def insert(self, index, item):
        if index < 0 or index > self._next_id:
            raise IndexError("list index out of range")
        for i in range(self._next_id, index, -1):
            self._out_of_core_dict[self.__to_bytes(i)] = self._out_of_core_dict[self.__to_bytes(i - 1)]
        self._out_of_core_dict[self.__to_bytes(index)] = self.__to_bytes(item)
        self._next_id += 1

    def __str__(self):
        return str([self.__from_bytes(self._out_of_core_dict[self.__to_bytes(i)]) for i in range(self._next_id)])
    
    def __iter__(self):
        for i in range(self._next_id):
            yield self.__from_bytes(self._out_of_core_dict[self.__to_bytes(i)])

    @staticmethod
    def __to_bytes(_any):
        return pickle.dumps(_any)

    @staticmethod
    def __from_bytes(any_bytes):
        return pickle.loads(any_bytes)

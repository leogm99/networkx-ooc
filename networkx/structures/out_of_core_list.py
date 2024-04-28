from typing import MutableSequence
from networkx.structures.edges_dict import BiTupleDict, EdgesDict
from networkx.structures.out_of_core_dict import IOutOfCoreDict
from networkx.structures.primitive_dicts import IntFloatDict, PrimitiveType

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
    def __init__(self, initial_list = None, value_primitive_type = PrimitiveType.INTEGER):
        self._out_of_core_dict = None
        if value_primitive_type == PrimitiveType.INTEGER:
            self._out_of_core_dict = IOutOfCoreDict()
        elif value_primitive_type == PrimitiveType.FLOAT:
            self._out_of_core_dict = IntFloatDict()
        elif value_primitive_type == PrimitiveType.TUPLE:
            self._out_of_core_dict = BiTupleDict(PrimitiveType.INTEGER, PrimitiveType.TUPLE)
        else:
            raise NotImplementedError("This functionality is not implemented yet.")

        self._next_id = 0
        self._value_primitive_type = value_primitive_type

        if (initial_list != None):
            for item in initial_list:
                self.append(item)

    def __len__(self):
        return self._next_id

    def __getitem__(self, index):
        if (isinstance(index, slice)): return self.__slice__getitem__(index)
        if index < 0:
            index += self._next_id
            if index < 0:
                raise IndexError("list index out of range")
        if index >= self._next_id:
            raise IndexError("list index out of range")
        return self._out_of_core_dict[index]
    
    def __slice__getitem__(self, index):
        start, stop, step = index.indices(len(self))
        if step != 1:
            if step == -1:
                return self.__reversed__()
            else:
                raise ValueError("Slice step other than 1 is not supported")
        l = OutOfCoreList(value_primitive_type=self._value_primitive_type)
        for i in range(start, stop, step):
            l.append(self._out_of_core_dict[i])
        return l
    
    def __setitem__(self, index, item):
        if index < 0 or index >= self._next_id:
            raise IndexError("list index out of range")
        self._out_of_core_dict[index] = item
    
    def __delitem__(self, index):
        if index < 0:
            index += self._next_id
            if index < 0 or index >= self._next_id:
                raise IndexError("list index out of range")
        elif index >= self._next_id:
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

    def __add__(self, other):
        if not isinstance(other, OutOfCoreList) and not isinstance(other, list):
            raise TypeError("Unsupported operand type(s) for +: 'OutOfCoreList' and '{}'".format(type(other).__name__))

        result = OutOfCoreList(value_primitive_type=self._value_primitive_type)
        result.extend(self)
        result.extend(other)
        return result

    def __eq__(self, other):
        if not isinstance(other, OutOfCoreList) and not isinstance(other, list):
            return False
        if len(self) != len(other):
            return False
        for item1, item2 in zip(self, other):
            if item1 != item2:
                return False
        return True

    def __lt__(self, other):
        if not isinstance(other, OutOfCoreList) and not isinstance(other, list):
            raise TypeError("Unsupported operand type(s) for <: 'OutOfCoreList' and '{}'".format(type(other).__name__))

        min_len = min(len(self), len(other))
        for i in range(min_len):
            if self[i] < other[i]:
                return True
            elif self[i] > other[i]:
                return False
        return len(self) < len(other)

    def __gt__(self, other):
        if not isinstance(other, OutOfCoreList) and not isinstance(other, list):
            raise TypeError("Unsupported operand type(s) for >: 'OutOfCoreList' and '{}'".format(type(other).__name__))

        min_len = min(len(self), len(other))
        for i in range(min_len):
            if self[i] > other[i]:
                return True
            elif self[i] < other[i]:
                return False
        return len(self) > len(other)

    def __reversed__(self):
        l = OutOfCoreList(value_primitive_type=self._value_primitive_type)
        for i in range(len(self) - 1, -1, -1):
            l.append(self[i])
        return l

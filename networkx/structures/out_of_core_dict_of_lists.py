import os
import shutil
import struct
import tempfile
from networkx.structures.out_of_core_dict import OutOfCoreDict
from networkx.structures.out_of_core_list import OutOfCoreList
from networkx.structures.primitive_dicts import PrimitiveType

__all__ = ["OutOfCoreDictOfLists"]

class LazyList:
    def  __init__(self, store, value_primitive_type):
        self.store = store
        self.value_primitive_type = value_primitive_type

    def __setitem__(self, index, value):
        path = self.store
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
        
        with open(path, 'r') as f, temp_file:
            for i, line in enumerate(f):
                if i == index:
                    temp_file.write(str(value) + '\n')
                else:
                    temp_file.write(line)

        os.remove(path)
        shutil.move(temp_file.name, path)

    def __getitem__(self, index):
        if (isinstance(index, slice)): return self.__slice__getitem__(index)

        path = self.store
        if index < 0:
            index += len(self)
            if index < 0:
                raise IndexError("Index out of range")
        with open(path, 'r') as f:
            for _ in range(index):
                try:
                    f.readline()
                except StopIteration:
                    raise IndexError("Index out of range")
            line = f.readline()
            if line:
                return self._parse_value(line.strip())
            else:
                raise IndexError("Index out of range")
    
    def __slice__getitem__(self, index):
        start, stop, step = index.indices(len(self))
        if step != 1:
            if step == -1:
                raise NotImplemented("Slice step other than 1 is not supported")
                # return self.__reversed__()
            else:
                raise ValueError("Slice step other than 1 is not supported")
        l = OutOfCoreList(value_primitive_type=self.value_primitive_type)
        for i in range(start, stop, step):
            l.append(self[i])
        return l

    def _parse_value(self, value_str):
        if self.value_primitive_type == PrimitiveType.INTEGER:
            return int(value_str)
        elif self.value_primitive_type == PrimitiveType.FLOAT:
            return float(value_str)
        
    def __len__(self):
        path = self.store
        with open(path, 'r') as f:
            return sum(1 for _ in f)

    def append(self, value):
        path = self.store
        with open(path, 'a+') as f:
            f.seek(0, 2)
            if f.tell() > 0:
                f.write('\n')
            f.write(str(value))

    def __iter__(self):
        path = self.store
        with open(path, 'r') as f:
            for line in f:
                if (self.value_primitive_type == PrimitiveType.INTEGER):
                    yield int(line.strip())
                elif (self.value_primitive_type == PrimitiveType.FLOAT):
                    yield float(line.strip())

    def __str__(self) -> str:
        return str([i for i in self])

    def __add__(self, other):
        result = OutOfCoreList(value_primitive_type=self.value_primitive_type)
        for i in self:
            result.append(i)
        result.extend(other)
        return result
    
    def __eq__(self, value) -> bool:
        l = OutOfCoreList(value_primitive_type=self.value_primitive_type)
        
        for i in self:
            l.append(i)
        return value == l
    
    def pop(self):
        path = self.store
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
        popped_value = None

        with open(path, 'r') as f, temp_file:
            line = next(f, None)
            while line is not None:
                next_line = next(f, None)
                if next_line is not None:
                    temp_file.write(line)
                else:
                    popped_value = self._parse_value(line.strip())
                line = next_line

        os.remove(path)
        shutil.move(temp_file.name, path)

        return popped_value

class OutOfCoreDictOfLists(OutOfCoreDict):
    def __init__(self, value_primitive_type = PrimitiveType.INTEGER):
        super().__init__()
        self._value_primitive_type = value_primitive_type

    def __setitem__(self, key, value):
        if super().__contains__(key):
            path = self._get_list_path(key)
        else:
            path = self._get_new_path()
        super().__setitem__(self.__key_to_bytes(key), self.__list_to_bytes(path, value))

    def __getitem__(self, key):
        path = self._get_list_path(key)
        return LazyList(path, self._value_primitive_type)
    
    def __iter__(self):
        for k in super().__iter__():
            yield self.__key_from_bytes(k)

    def __del__(self):
        for k in super().__iter__():
            path = OutOfCoreDictOfLists.__str_from_bytes(super().__getitem__(k))
            try:
                os.remove(path)
            except FileNotFoundError:
                print(f"File {path} not found")
        super().__del__()

    def __delitem__(self, index):
        path = self._get_list_path(index)
        os.remove(path)
        super().__delitem__(self.__key_to_bytes(index))

    def __eq__(self, other):
        if not isinstance(other, OutOfCoreDictOfLists) and not isinstance(other, dict):
            return False

        if len(self) != len(other):
            return False

        for key, value in self.items():
            if key not in other or self[key] != other[key]:
                return False

        return True
    
    def __str__(self) -> str:
        return str({k for k in self})

    def _get_new_path(self):
        fd, path = tempfile.mkstemp()
        os.close(fd)
        return path

    def _get_list_path(self, key):
        return OutOfCoreDictOfLists.__str_from_bytes(super().__getitem__(self.__key_to_bytes(key)))

    @staticmethod
    def __key_to_bytes(k):
        return struct.pack('@l', k)
    
    @staticmethod
    def __key_from_bytes(b: bytes):
        return struct.unpack('@l', b)[0]

    @staticmethod
    def __list_to_bytes(path, l):
        with open(path, 'w') as f:
            f.write('\n'.join(map(str, l)))

        return OutOfCoreDictOfLists.__str_to_bytes(path)

    @staticmethod
    def __list_from_bytes(b, type):
        path = OutOfCoreDictOfLists.__str_from_bytes(b)
        l = OutOfCoreList(value_primitive_type=type)
        with open(path, 'r') as f:
            for line in f:
                if (type == PrimitiveType.INTEGER):
                    l.append(int(line.strip()))
                elif ( type == PrimitiveType.FLOAT):
                    l.append(float(line.strip()))
        return l
    
    @staticmethod
    def __str_to_bytes(s: str):
        return s.encode('utf-8')

    @staticmethod
    def __str_from_bytes(b: bytes):
        return b.decode('utf-8')

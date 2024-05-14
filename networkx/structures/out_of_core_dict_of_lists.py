import mmap
import os
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
        with open(path, 'r+b') as f:
            file_size = os.path.getsize(path)
            if file_size == 0:
                raise IndexError("list assignment index out of range")

            element_position = index * 4

            if element_position >= file_size or index < 0:
                raise IndexError("list assignment index out of range")

            with mmap.mmap(f.fileno(), 0) as m:
                value_bytes = struct.pack(self.value_primitive_type, value)
                m[element_position:element_position + 4] = value_bytes

    def __getitem__(self, index):
        if (isinstance(index, slice)): return self.__slice__getitem__(index)

        path = self.store
        if index < 0:
            index += len(self)
            if index < 0:
                raise IndexError("Index out of range")
        with open(path, 'rb') as f:
            with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as m:
                start_index = index * 4
                end_index = start_index + 4
                byte_data = m[start_index:end_index]
                if len(byte_data) == 4:
                    return struct.unpack(self.value_primitive_type, byte_data)[0]
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
        
    def __len__(self):
        path = self.store
        if os.path.getsize(path) == 0:
            return 0
        with open(path, 'rb') as f:
            with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as m:
                element_size = 4
                return len(m) // element_size

    def append(self, value):
        path = self.store
        with open(path, 'a+b') as f:
            f.seek(0, 2)
            f.write(struct.pack(self.value_primitive_type, value))

    def __iter__(self):
        path = self.store
        if os.path.getsize(path) == 0:
            return iter([])
        with open(path, 'rb') as f:
            with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as m:
                for i in range(0, len(m), 4):
                    data = m[i:i+4]
                    if len(data) == 4:
                        value = struct.unpack(self.value_primitive_type, data)[0]
                        yield value

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
        popped_value = None

        with open(path, 'r+b') as f:
            file_size = os.path.getsize(path)
            if file_size == 0:
                raise IndexError("pop from empty list")

            with mmap.mmap(f.fileno(), 0) as m:
                last_element_position = file_size - 4
                last_element_bytes = m[last_element_position:last_element_position + 4]
                popped_value = struct.unpack(self.value_primitive_type, last_element_bytes)[0]

                f.truncate(last_element_position)

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
        super().__setitem__(self.__key_to_bytes(key), self.__list_to_bytes(path, value, self._value_primitive_type))

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
    def __list_to_bytes(path, l, type):
        with open(path, 'wb') as f:
            for data in l:
                f.write(struct.pack(type, data))

        return OutOfCoreDictOfLists.__str_to_bytes(path)

    @staticmethod
    def __str_to_bytes(s: str):
        return s.encode('utf-8')

    @staticmethod
    def __str_from_bytes(b: bytes):
        return b.decode('utf-8')

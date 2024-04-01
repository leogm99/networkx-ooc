import os
import struct
import tempfile
from networkx.structures.out_of_core_dict import OutOfCoreDict
from networkx.structures.out_of_core_list import OutOfCoreList

__all__ = ["OutOfCoreDictOfLists"]

class OutOfCoreDictOfLists(OutOfCoreDict):
    def __init__(self):
        super().__init__()

    def __setitem__(self, key, value):
        if super().__contains__(key):
            path = self._get_list_path(key)
        else:
            path = self._get_new_path()
        super().__setitem__(self.__key_to_bytes(key), self.__list_to_bytes(path, value))

    def __getitem__(self, key):
        return self.__list_from_bytes(super().__getitem__(self.__key_to_bytes(key)))
    
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
    
    def append(self, key, value):
        path = self._get_list_path(key)
        with open(path, 'a+') as f:
            f.seek(0, 2)
            if f.tell() > 0:
                f.write('\n')
            f.write(str(value))

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
        #_, path = tempfile.mkstemp()
        with open(path, 'w') as f:
            f.write('\n'.join(map(str, l)))
            #Esta ok guardar como str? O seria mejor por ej en bytes?

        return OutOfCoreDictOfLists.__str_to_bytes(path)

    @staticmethod
    def __list_from_bytes(b):
        path = OutOfCoreDictOfLists.__str_from_bytes(b)
        l = OutOfCoreList()
        with open(path, 'r') as f:
            for line in f:
                l.append(int(line.strip()))
        return l
    
    @staticmethod
    def __str_to_bytes(s: str):
        return s.encode('utf-8')

    @staticmethod
    def __str_from_bytes(b: bytes):
        return b.decode('utf-8')

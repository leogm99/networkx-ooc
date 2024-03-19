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
        super().__setitem__(self.__key_to_bytes(key), self.__list_to_bytes(value))

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

    @staticmethod
    def __key_to_bytes(k):
        return struct.pack('@l', k)
    
    @staticmethod
    def __key_from_bytes(b: bytes):
        return struct.unpack('@l', b)[0]

    @staticmethod
    def __list_to_bytes(l):
        _, path = tempfile.mkstemp()
        #TODO se podria armar una logica de append dependiendo que operacion se le hizo a la lista
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


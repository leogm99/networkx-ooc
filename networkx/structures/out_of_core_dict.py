import tempfile
import plyvel
import pickle

class OutOfCoreDict:
    def __init__(self) -> None:
        self._temp = tempfile.TemporaryDirectory()
        self._inner = plyvel.DB(f'{self._temp.name}', create_if_missing=True)
        self._count = 0

    @staticmethod
    def __to_bytes(_any):
        return pickle.dumps(_any)

    @staticmethod
    def __from_bytes(any_bytes):
        return pickle.loads(any_bytes)

    def __getitem__(self, key):
        if not key in self:
            raise KeyError(f'{key}')
        key_b = OutOfCoreDict.__to_bytes(key)
        return OutOfCoreDict.__from_bytes(self._inner.get(key_b))

    def __setitem__(self, key, value):
        key_b = OutOfCoreDict.__to_bytes(key)
        value_b = OutOfCoreDict.__to_bytes(value)
        if not key in self:
            self._count += 1
        self._inner.put(key_b, value_b, sync=True)

    def __len__(self):
        return self._count
    
    def __contains__(self, key):
        # TODO: refactor
        # self._inner.__contains__ is not implemented
        # maybe using iterators?
        key_b = OutOfCoreDict.__to_bytes(key)
        maybe_key = self._inner.get(key_b)
        return maybe_key is not None
    
    def __inner_iter_items(self):
        for k, v in self._inner:
            yield OutOfCoreDict.__from_bytes(k), OutOfCoreDict.__from_bytes(v)
    
    def __iter__(self):
        for k, _ in self.__inner_iter_items():
            yield k

    def items(self):
        yield from self.__inner_iter_items()


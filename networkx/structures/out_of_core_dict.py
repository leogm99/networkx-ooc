import tempfile
from typing import MutableMapping

import plyvel
import pickle

from networkx.structures.proxy_dict import ProxyDict


class OutOfCoreDict(MutableMapping):
    def __init__(self) -> None:
        self._temp = tempfile.TemporaryDirectory()
        self._inner = plyvel.DB(f"{self._temp.name}", create_if_missing=True)
        self._count = 0

    @staticmethod
    def __to_bytes(_any):
        return pickle.dumps(_any)

    @staticmethod
    def __from_bytes(any_bytes):
        return pickle.loads(any_bytes)

    def __getitem__(self, key):
        key_b = OutOfCoreDict.__to_bytes(key)
        if self._inner.get(key_b) is None:
            raise KeyError(key)
        item = OutOfCoreDict.__from_bytes(self._inner.get(key_b))
        if isinstance(item, dict):
            return ProxyDict(context_key=key, context=self, inner=item)
        return item

    def __setitem__(self, key, value):
        key_b = OutOfCoreDict.__to_bytes(key)
        value_b = OutOfCoreDict.__to_bytes(value)
        if self._inner.get(key_b) is None:
            self._count += 1
        self._inner.put(key_b, value_b, sync=True)

    def __len__(self):
        return self._count

    def __inner_iter_items(self):
        for k, v in self._inner:
            yield OutOfCoreDict.__from_bytes(k), OutOfCoreDict.__from_bytes(v)

    def __iter__(self):
        for k, _ in self.__inner_iter_items():
            yield k

    def __del__(self):
        self.__dealloc()

    def __delitem__(self, key) -> None:
        key_b = OutOfCoreDict.__to_bytes(key)
        if not self._inner.get(key_b):
            raise KeyError(key)
        self._inner.delete(key_b)
        self._count -= 1

    def __dealloc(self):
        self._inner.close()
        self._temp.cleanup()

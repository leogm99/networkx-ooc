import pickle
import tempfile
from collections.abc import MutableMapping

import plyvel


class OutOfCoreDict(MutableMapping):
    # search by pairs of keys

    def __setitem__(self, key, value):
        self._inner.put(key, value)

    def __getitem__(self, key):
        data = self._inner.get(key)
        if data is None:
            raise KeyError(key)
        return data

    def __init__(self) -> None:
        self._temp = tempfile.TemporaryDirectory()
        self._inner = plyvel.DB(
            f"{self._temp.name}",
            create_if_missing=True,
        )

    def __len__(self):
        count = 0
        with self._inner.iterator(
            include_key=False, include_value=False, fill_cache=False
        ) as it:
            for _ in it:
                count += 1
        return count

    def __inner_iter_items(self):
        yield from self._inner

    def __iter__(self):
        for k, _ in self.__inner_iter_items():
            yield k

    def __del__(self):
        self.__dealloc()

    def __delitem__(self, key) -> None:
        if not self._inner.get(key):
            raise KeyError(key)
        self._inner.delete(key)

    def __dealloc(self):
        self._inner.close()
        self._temp.cleanup()

    def prefix_iter(self, prefix):
        yield from self._inner.prefixed_db(prefix)


class OutOfCorePickleDict(OutOfCoreDict):
    def __init__(self) -> None:
        super().__init__()

    def __setitem__(self, key, value):
        super().__setitem__(self.__to_bytes(key), self.__to_bytes(value))

    def __getitem__(self, key):
        return self.__from_bytes(super().__getitem__(self.__to_bytes(key)))
    
    def __iter__(self):
        for k in super().__iter__():
            yield self.__from_bytes(k)
    
    @staticmethod
    def __to_bytes(_any):
        return pickle.dumps(_any)

    @staticmethod
    def __from_bytes(any_bytes):
        return pickle.loads(any_bytes)

import pickle
import struct
import tempfile
from collections.abc import MutableMapping

import plyvel


class OutOfCoreDict(MutableMapping):
    def __setitem__(self, key, value):
        # self._wb.put(key, value)
        self._wb[key] = value
        if len(self._wb) > 4000:
            self._flush_write_batch()

    def _flush_write_batch(self):
        if not self._wb:
            return
        with self._inner.write_batch(sync=False) as wb:
            for k, v in self._wb.items():
                wb.put(k, v)
        self._wb.clear()

    def __getitem__(self, key):
        value = self._wb.get(key)
        if value is not None:
            return value
        data = self._inner.get(key, fill_cache=False)
        if data is None:
            raise KeyError(key)
        return data

    def __init__(self) -> None:
        self._temp = tempfile.TemporaryDirectory()
        self._inner = plyvel.DB(
            f"{self._temp.name}",
            create_if_missing=True,
        )
        self._wb = {}

    def __len__(self):
        self._flush_write_batch()
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
        self._flush_write_batch()
        with self._inner.iterator(include_value=False, fill_cache=False) as it:
            yield from it

    def __del__(self):
        self.__dealloc()

    def __delitem__(self, key) -> None:
        self._flush_write_batch()
        if self._inner.get(key) is None:
            raise KeyError(key)
        self._inner.delete(key)

    def __dealloc(self):
        self._inner.close()
        self._temp.cleanup()

    def prefix_iter(self, prefix):
        self._flush_write_batch()
        yield from self._inner.prefixed_db(prefix).iterator(fill_cache=False, include_value=False)

    def copy(self, c=None):
        if c is None:
            c = OutOfCoreDict()
        for i in self:
            c[i] = self.__getitem__(i)
        return c

class IOutOfCoreDict(OutOfCoreDict):
    def __init__(self, initial_values = None) -> None:
        super().__init__()

        if (initial_values != None):
            super().update(initial_values)

    def __setitem__(self, key, value):
        super().__setitem__(self.__to_bytes(key), self.__to_bytes(value))

    def __getitem__(self, key):
        return self.__from_bytes(super().__getitem__(self.__to_bytes(key)))
    
    def __iter__(self):
        for k in super().__iter__():
            yield self.__from_bytes(k)

    def __delitem__(self, index):
        super().__delitem__(self.__to_bytes(index))

    def copy(self, c=None):
        return super().copy(IOutOfCoreDict())

    @staticmethod
    def __to_bytes(i: int):
        return struct.pack('@l', i)

    @staticmethod
    def __from_bytes(b: bytes):
        return struct.unpack('@l', b)[0]

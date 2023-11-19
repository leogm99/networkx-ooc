import tempfile
from collections.abc import MutableMapping

import plyvel


class OutOfCoreDict(MutableMapping):
    # search by pairs of keys

    def __setitem__(self, key, value):
        if self._inner.get(key) is None:
            self._count += 1
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
            write_buffer_size=0,
            lru_cache_size=0,
        )
        self._count = 0

    def __len__(self):
        return self._count

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
        self._count -= 1

    def __dealloc(self):
        self._inner.close()
        self._temp.cleanup()

    def prefix_iter(self, prefix):
        yield from self._inner.prefixed_db(prefix)

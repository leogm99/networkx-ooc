import tempfile
from collections.abc import MutableMapping

import plyvel


class OutOfCoreDict(MutableMapping):
    def __setitem__(self, key, value):
        self._wb.put(key, value)
        if self._wb.approximate_size() > 32 * 1024:
            self._wb.write()
            self._wb.clear()

    def __getitem__(self, key):
        self._wb.write()
        self._wb.clear()
        data = self._inner.get(key)
        if data is None:
            raise KeyError(key)
        return data

    def __init__(self) -> None:
        self._temp = tempfile.TemporaryDirectory()
        self._inner = plyvel.DB(
            f"{self._temp.name}",
            create_if_missing=True,
            write_buffer_size=24*1024*1024,
            compression='snappy'
        )
        self._wb = self._inner.write_batch(sync=False)

    def __len__(self):
        self._wb.write()
        self._wb.clear()
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
        self._wb.write()
        self._wb.clear()
        for k, _ in self.__inner_iter_items():
            yield k

    def __del__(self):
        self.__dealloc()

    def __delitem__(self, key) -> None:
        self._wb.write()
        self._wb.clear()
        if not self._inner.get(key):
            raise KeyError(key)
        self._inner.delete(key)

    def __dealloc(self):
        self._inner.close()
        self._temp.cleanup()

    def prefix_iter(self, prefix):
        self._wb.write()
        self._wb.clear()
        yield from self._inner.prefixed_db(prefix)

from os import path, getenv, mkdir
import tempfile
from collections.abc import MutableMapping

import plyvel

DB_DIR = getenv(key='OOC_DICT_TMPDIR', default='./db')


class OutOfCoreDict(MutableMapping):
    def __init__(self, dir_=DB_DIR) -> None:
        if not path.isdir(dir_):
            mkdir(dir_)
        self._temp = tempfile.TemporaryDirectory(dir=dir_)
        self._inner = plyvel.DB(
            f"{self._temp.name}",
            create_if_missing=True,
        )
        self._dir = dir_
        self._wb = {}

    @property
    def dir(self):
        return self._dir

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

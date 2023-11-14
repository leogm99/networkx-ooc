import enum
import tempfile
from typing import MutableMapping
from functools import lru_cache

import plyvel
import pickle


MAX_CACHE_SIZE = 2**10


class OutOfCoreDictKeyMode(enum.Enum):
    SINGLE = 0
    COMPOSITE = 1


class OutOfCoreDict(MutableMapping):
    # search by pairs of keys

    def __setitem__(self, key, value):
        if self._mode == OutOfCoreDictKeyMode.SINGLE:
            self.__single_key_set_item(key, value)
        elif self._mode == OutOfCoreDictKeyMode.COMPOSITE:
            self.__composite_key_set_item(key, value)

    def __getitem__(self, key):
        if self._mode == OutOfCoreDictKeyMode.SINGLE:
            return self.__single_key_get_item(key)
        elif self._mode == OutOfCoreDictKeyMode.COMPOSITE:
            return self.__composite_key_get_item(key)

    def __init__(
        self, mode=OutOfCoreDictKeyMode.SINGLE
    ) -> None:
        self._temp = tempfile.TemporaryDirectory()
        self._inner = plyvel.DB(f"{self._temp.name}", create_if_missing=True)
        self._count = 0
        self._cache = {}
        self._mode = mode

    @staticmethod
    def __to_bytes(_any):
        return pickle.dumps(_any, protocol=pickle.HIGHEST_PROTOCOL)

    @staticmethod
    @lru_cache(maxsize=1024)
    def __from_bytes(any_bytes):
        return pickle.loads(any_bytes)

    def __len__(self):
        self.__flush()
        return self._count

    def __inner_iter_items(self):
        self.__flush()
        for k, v in self._inner:
            yield OutOfCoreDict.__from_bytes(k), OutOfCoreDict.__from_bytes(v)

    def __iter__(self):
        self.__flush()
        for k, _ in self.__inner_iter_items():
            yield k

    def __del__(self):
        self.__dealloc()

    def __delitem__(self, key) -> None:
        self.__flush()
        key_b = OutOfCoreDict.__to_bytes(key)
        if not self._inner.get(key_b):
            raise KeyError(key)
        self._inner.delete(key_b)
        self._count -= 1

    def __dealloc(self):
        self._inner.close()
        self._temp.cleanup()

    def prefix_iter(self, prefix):
        assert self._mode == OutOfCoreDictKeyMode.COMPOSITE
        for k, v in self._inner.prefixed_db(OutOfCoreDict.__to_bytes(prefix)):
            yield OutOfCoreDict.__from_bytes(k), OutOfCoreDict.__from_bytes(v)

    def __single_key_set_item(self, key, value):
        assert (
            not isinstance(key, list)
            and not isinstance(key, tuple)
            and self._mode == OutOfCoreDictKeyMode.SINGLE
        )
        self.__put(self._inner, key, value)

    def __composite_key_set_item(self, key, value):
        assert (
            isinstance(key, list) or isinstance(key, tuple)
        ) and self._mode == OutOfCoreDictKeyMode.COMPOSITE

        concat_key = bytearray(OutOfCoreDict.__to_bytes(key[0]))
        concat_key.extend(OutOfCoreDict.__to_bytes(key[1]))
        exists_in_db = self._inner.get(bytes(concat_key)) is not None
        if self._cache.get(key) is None and not exists_in_db:
            self._count += 1

        self._cache[key] = value
        if len(self._cache) == MAX_CACHE_SIZE:
            self.__flush()

    def __flush(self):
        with self._inner.write_batch() as wb:
            self._cache = dict(sorted(self._cache.items()))
            for k, v in self._cache.items():
                concat_key = bytearray(OutOfCoreDict.__to_bytes(k[0]))
                concat_key.extend(OutOfCoreDict.__to_bytes(k[1]))
                wb.put(bytes(concat_key), OutOfCoreDict.__to_bytes(v))
            self._cache.clear()

    def __put(self, db, key, value):
        key_b = OutOfCoreDict.__to_bytes(key)
        value_b = OutOfCoreDict.__to_bytes(value)
        if db.get(key_b) is None:
            self._count += 1
        db.put(key_b, value_b)

    def __get(self, db, key):
        key_b = OutOfCoreDict.__to_bytes(key)
        if db.get(key_b) is None:
            raise KeyError(key)
        return OutOfCoreDict.__from_bytes(db.get(key_b))

    def __single_key_get_item(self, key):
        assert (
            not isinstance(key, list)
            and not isinstance(key, tuple)
            and self._mode == OutOfCoreDictKeyMode.SINGLE
        )
        return self.__get(self._inner, key)

    def __composite_key_get_item(self, key):
        assert (
            isinstance(key, list) or isinstance(key, tuple)
        ) and self._mode == OutOfCoreDictKeyMode.COMPOSITE
        if key in self._cache:
            return self._cache[key]
        prefix, key = key
        db = self._inner.prefixed_db(OutOfCoreDict.__to_bytes(prefix))
        return self.__get(db, key)

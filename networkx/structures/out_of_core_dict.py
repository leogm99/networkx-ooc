import enum
import tempfile
from collections import OrderedDict
from typing import MutableMapping

import plyvel
import pickle


MAX_CACHE_SIZE = 2048


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
        self, mode=OutOfCoreDictKeyMode.SINGLE, max_cache_size=MAX_CACHE_SIZE
    ) -> None:
        self._temp = tempfile.TemporaryDirectory()
        self._inner = plyvel.DB(f"{self._temp.name}", create_if_missing=True)
        self._count = 0
        self._cache = OrderedDict()
        self._mode = mode

    @staticmethod
    def __to_bytes(_any):
        return pickle.dumps(_any, protocol=pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def __from_bytes(any_bytes):
        return pickle.loads(any_bytes)

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

        prefix, key = key
        db = self._inner.prefixed_db(OutOfCoreDict.__to_bytes(prefix))

        self.__put(db, key, value)

    def __put(self, db, key, value):
        key_b = OutOfCoreDict.__to_bytes(key)
        value_b = OutOfCoreDict.__to_bytes(value)
        if db.get(key_b) is None:
            self._count += 1
        db.put(key_b, value_b, sync=True)

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
        prefix, key = key
        db = self._inner.prefixed_db(OutOfCoreDict.__to_bytes(prefix))
        return self.__get(db, key)

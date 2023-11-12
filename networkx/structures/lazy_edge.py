from typing import MutableMapping


class LazyEdge(MutableMapping):
    def __init__(self, inner_dict, key):
        self._inner_dict = inner_dict
        self._base_key = key

    def __setitem__(self, key, value):
        self._inner_dict[(self._base_key, key)] = value

    def __delitem__(self, key):
        del self._inner_dict[(self._base_key, key)]

    def __getitem__(self, key):
        return self._inner_dict[(self._base_key, key)]

    def __len__(self):
        count = 0
        for _ in self._inner_dict.prefix_iter(prefix=self._base_key):
            count += 1
        return count

    def __iter__(self):
        for key, _ in self._inner_dict.prefix_iter(prefix=self._base_key):
            yield key

    def values(self):
        for _, value in self._inner_dict.prefix_iter(prefix=self._base_key):
            yield value

import pickle
from typing import MutableMapping


class ProxyDict(MutableMapping):
    # Node or Edge?
    def __init__(self, context, inner_dict, key):
        self._context = context
        self._inner_dict = inner_dict
        self._key = key

    def __setitem__(self, key, value):
        self._inner_dict[key] = value
        self._context[self._key] = self._inner_dict

    def __delitem__(self, key):
        del self._inner_dict[key]
        self._context[self._key] = self._inner_dict

    def __getitem__(self, key):
        return self._inner_dict[key]

    def __len__(self):
        return len(self._inner_dict)

    def __iter__(self):
        return iter(self._inner_dict)

    def __repr__(self):
        return repr(self._inner_dict)

    def __str__(self):
        return str(self._inner_dict)

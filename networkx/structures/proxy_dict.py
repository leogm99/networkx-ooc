from typing import MutableMapping


class ProxyDict(MutableMapping):
    def __init__(self, context, context_key, inner):
        self._context = context
        self._context_key = context_key
        self._inner = inner

    def __setitem__(self, key, value):
        self._inner[key] = value
        self._context[self._context_key] = self._inner

    def __delitem__(self, key):
        del self._inner[key]
        self._context[self._context_key] = self._inner

    def __getitem__(self, key):
        return self._inner[key]

    def __len__(self):
        return len(self._inner)

    def __iter__(self):
        return self._inner.__iter__()

    def __repr__(self):
        return self._inner.__repr__()

    def __str__(self):
        return self._inner.__str__()


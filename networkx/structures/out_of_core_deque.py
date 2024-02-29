import struct

from networkx.structures.out_of_core_dict import OutOfCoreDict


def to_bytes(i: int):
    return struct.pack('@l', i)


def from_bytes(b: bytes):
    return struct.unpack('@l', b)[0]


class OutOfCoreDeque:
    """
    An out of core implementation of a deque.
    This implementation follows the same behavior as the standard python deque,
    with a catch: it's not possible to insert elements at arbitrary positions
    """
    def __init__(self, maxlen=None):
        self._ooc = OutOfCoreDict()
        self._left = self._right = 0
        self._maxlen = maxlen
        if maxlen is not None and maxlen < 0:
            raise ValueError('maxlen must be non-negative')

    def append(self, v):
        self._ooc[to_bytes(self._right)] = to_bytes(v)
        self._right += 1
        if self._maxlen is not None and self.__len__() > self._maxlen:
            self._left += 1

    def appendleft(self, v):
        self._left -= 1
        self._ooc[to_bytes(self._left)] = to_bytes(v)
        if self._maxlen is not None and self.__len__() > self._maxlen:
            self._right -= 1

    def pop(self):
        if self.empty:
            raise IndexError('pop from an empty queue')
        self._right -= 1
        item = self._ooc[to_bytes(self._right)]
        return from_bytes(item)

    def popleft(self):
        if self.empty:
            raise IndexError('pop from an empty queue')
        item = self._ooc[to_bytes(self._left)]
        self._left += 1
        return from_bytes(item)

    @property
    def empty(self):
        return self._right == self._left

    def __len__(self):
        return self._right - self._left

    def __bool__(self):
        return not self.empty

    def __iter__(self):
        for i in range(self._left, self._right):
            yield from_bytes(self._ooc[to_bytes(i)])

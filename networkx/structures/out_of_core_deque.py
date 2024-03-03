import struct

from networkx.structures.primitive_dicts import IntDict


class OutOfCoreDeque:
    """
    An out of core implementation of a deque.
    This implementation follows the same behavior as the standard python deque,
    with a catch: it's not possible to insert elements at arbitrary positions
    """

    def __init__(self, maxlen=None, _dict=None):
        self._dict = _dict() if _dict else IntDict()
        self._left = self._right = 0
        self._maxlen = maxlen
        if maxlen is not None and maxlen < 0:
            raise ValueError('maxlen must be non-negative')

    def append(self, v):
        self._dict[self._right] = v
        self._right += 1
        if self._maxlen is not None and self.__len__() > self._maxlen:
            self._left += 1

    def appendleft(self, v):
        self._left -= 1
        self._dict[self._left] = v
        if self._maxlen is not None and self.__len__() > self._maxlen:
            self._right -= 1

    def pop(self):
        if self.empty:
            raise IndexError('pop from an empty queue')
        self._right -= 1
        return self._dict[self._right]

    def popleft(self):
        if self.empty:
            raise IndexError('pop from an empty queue')
        item = self._dict[self._left]
        self._left += 1
        return item

    @property
    def empty(self):
        return self._right == self._left

    def __len__(self):
        return self._right - self._left

    def __bool__(self):
        return not self.empty

    def __iter__(self):
        for i in range(self._left, self._right):
            yield self._dict[i]

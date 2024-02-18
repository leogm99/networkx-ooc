import pytest

from networkx.structures.out_of_core_dict import OutOfCoreDict


class TestOutOfCoreDict:
    def test_add_value(self):
        nd = OutOfCoreDict()
        nd[b"a"] = b"1"
        assert len(nd) == 1

    def test_add_values(self):
        nd = OutOfCoreDict()
        nd[b"a"] = b"1"
        nd[b"b"] = b"2"
        nd[b"c"] = b"3"
        nd[b"a"] = b"4"
        assert len(nd) == 3

    def test_get_value(self):
        nd = OutOfCoreDict()
        nd[b"a"] = b"1"
        assert nd[b"a"] == b"1"
        nd[b"a"] = b"2"
        assert nd[b"a"] == b"2"
        assert len(nd) == 1
        nd[b"b"] = b"3"
        assert nd[b"a"] == b"2"
        assert nd[b"b"] == b"3"
        assert len(nd) == 2

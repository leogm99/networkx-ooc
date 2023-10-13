import pytest
from networkx.structures.out_of_core_dict import OutOfCoreDict


class TestOutOfCoreDict:
    def test_add_value(self):
        nd = OutOfCoreDict()
        nd["a"] = 1
        assert len(nd) == 1

    def test_add_values(self):
        nd = OutOfCoreDict()
        nd["a"] = 1
        nd["b"] = 2
        nd["c"] = 3
        nd["a"] = 4
        assert len(nd) == 3

    def test_get_value(self):
        nd = OutOfCoreDict()
        nd['a'] = 1
        assert nd['a'] == 1
        nd['a'] = 2
        assert nd['a'] == 2
        assert len(nd) == 1
        nd['b'] = 3
        assert nd['a'] == 2
        assert nd['b'] == 3
        assert len(nd) == 2

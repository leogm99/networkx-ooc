import pytest
import networkx as nx
from networkx.classes.tests.test_graph import TestGraph
from networkx.structures.out_of_core_dict import OutOfCoreDict


def raises(exception):
    def inner(func):
        def __inner(*args, **kwargs):
            with pytest.raises(exception) as _:
                return func(*args, **kwargs)

        return __inner

    return inner


class TestLazyGraph(TestGraph):
    def setup_method(self):
        self.Graph = nx.LazyGraph
        # build dict-of-dict-of-dict K3
        ed1, ed2, ed3 = ({}, {}, {})
        adj = OutOfCoreDict()
        adj[0] = {1: ed1, 2: ed2}
        adj[1] = {0: ed1, 2: ed3}
        adj[2] = {0: ed2, 1: ed3}
        self.k3adj = adj
        self.k3edges = [(0, 1), (0, 2), (1, 2)]
        self.k3nodes = [0, 1, 2]
        self.K3 = self.Graph()
        self.K3._adj = self.k3adj
        self.K3._node = OutOfCoreDict()
        self.K3._node[0] = {}
        self.K3._node[1] = {}
        self.K3._node[2] = {}

    @raises(nx.NotSupportedForLazyGraph)
    def test_add_edge(self):
        return super().test_add_edge()

    @raises(nx.NotSupportedForLazyGraph)
    def test_add_edges_from(self):
        return super().test_add_edges_from()

    @raises(nx.NotSupportedForLazyGraph)
    def test_add_node(self):
        return super().test_add_node()

    @raises(nx.NotSupportedForLazyGraph)
    def test_add_nodes_from(self):
        return super().test_add_nodes_from()

    @raises(nx.NotSupportedForLazyGraph)
    def test_remove_node(self):
        return super().test_remove_node()

    @raises(nx.NotSupportedForLazyGraph)
    def test_remove_nodes_from(self):
        return super().test_remove_nodes_from()

    @raises(nx.NotSupportedForLazyGraph)
    def test_remove_edge(self):
        return super().test_remove_edge()

    @raises(nx.NotSupportedForLazyGraph)
    def test_remove_edges_from(self):
        return super().test_remove_edges_from()

    @raises(nx.NotSupportedForLazyGraph)
    def test_none_node(self):
        return super().test_none_node()

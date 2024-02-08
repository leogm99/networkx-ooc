import pytest
import networkx as nx
from networkx.classes.tests.test_graph import BaseAttrGraphTester
from networkx.structures.lazy_adjacency_list import LazyAdjacencyList
from networkx.structures.lazy_node_list import LazyNodeList


def raises(exception):
    def inner(func):
        def __inner(*args, **kwargs):
            with pytest.raises(exception) as _:
                return func(*args, **kwargs)

        return __inner

    return inner


class TestLazyGraph(BaseAttrGraphTester):
    def setup_method(self):
        self.Graph = nx.LazyGraph
        adj = LazyAdjacencyList()
        # build dict-of-dict-of-dict K3
        adj.add_edge(0, 1)
        adj.add_edge(0, 2)
        adj.add_edge(1, 0)
        adj.add_edge(1, 2)
        adj.add_edge(2, 0)
        adj.add_edge(2, 1)
        self.k3adj = adj
        self.k3edges = [(0, 1), (0, 2), (1, 2)]
        self.k3nodes = [0, 1, 2]
        self.K3 = self.Graph()
        self.K3._adj = self.k3adj
        self.K3._node = LazyNodeList()
        self.K3._node.add_node(0)
        self.K3._node.add_node(1)
        self.K3._node.add_node(2)

    def test_nodes(self):
        G = self.K3
        assert isinstance(G._node, G.node_dict_factory)
        assert isinstance(G._adj, G.adjlist_outer_dict_factory)
        assert sorted(G.nodes()) == self.k3nodes
        assert sorted(G.nodes(data=True)) == [(0, {}), (1, {}), (2, {})]

    def test_contains(self):
        G = self.K3
        assert 1 in G
        assert 4 not in G
        # TODO: maybe raise?
        # assert "b" not in G
        # assert [] not in G  # no exception for nonhashable
        # assert {1: 1} not in G  # no exception for nonhashable

    def test_has_node(self):
        G = self.K3
        assert G.has_node(1)
        assert not G.has_node(4)
        # TODO: maybe raise?
        # assert not G.has_node([])  # no exception for nonhashable
        # assert not G.has_node({1: 1})  # no exception for nonhashable

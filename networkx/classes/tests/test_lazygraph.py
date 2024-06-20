import pytest
import networkx as nx
from networkx.classes.tests.test_graph import BaseAttrGraphTester
from networkx.structures.lazy_adjacency_list import LazyAdjacencyList
from networkx.structures.lazy_node_list import LazyNodeList
from utils import nodes_equal


def graphs_equal(self, H, G):
    assert G._adj == H._adj
    assert G._node == H._node
    assert G.graph == H.graph
    assert G.name == H.name
    # the graph is deep copied so no identity should be checked
    if G.is_directed() or H.is_directed():
        if not G.is_directed():
            G._pred = G._adj
            G._succ = G._adj
        if not H.is_directed():
            H._pred = H._adj
            H._succ = H._adj
        assert G._pred == H._pred
        assert G._succ == H._succ
        # assert H._succ[1][2] is H._pred[2][1]
        # assert G._succ[1][2] is G._pred[2][1]


def raises(exception):
    def inner(func):
        def __inner(*args, **kwargs):
            with pytest.raises(exception) as _:
                return func(*args, **kwargs)

        return __inner

    return inner


class TestLazyGraph(BaseAttrGraphTester):
    def setup_method(self):
        self.Graph = nx.OutOfCoreGraph
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
        assert [] not in G  # no exception for nonhashable
        assert {1: 1} not in G  # no exception for nonhashable
    
    def test_nbunch_iter(self):
        G = self.K3
        assert nodes_equal(G.nbunch_iter(), self.k3nodes)  # all nodes
        assert nodes_equal(G.nbunch_iter(0), [0])  # single node
        assert nodes_equal(G.nbunch_iter([0, 1]), [0, 1])  # sequence
        # sequence with none in graph
        assert nodes_equal(G.nbunch_iter([-1]), [])
        # strings not supported (yet)
        # assert nodes_equal(G.nbunch_iter("foo"), [])
        # node not in graph doesn't get caught upon creation of iterator
        bunch = G.nbunch_iter(-1)
        # but gets caught when iterator used
        with pytest.raises(nx.NetworkXError, match="is not a node or a sequence"):
            list(bunch)
        # unhashable doesn't get caught upon creation of iterator
        bunch = G.nbunch_iter([0, 1, 2, {}])
        # but gets caught when iterator hits the unhashable
        with pytest.raises(
            nx.NetworkXError, match="in sequence nbunch is not a valid node"
        ):
            list(bunch)

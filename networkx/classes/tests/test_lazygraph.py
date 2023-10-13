import networkx as nx
from networkx.classes.tests.test_graph import TestGraph


class TestLazyGraph(TestGraph):

    def setup_method(self):
        self.Graph = nx.LazyGraph
        # build dict-of-dict-of-dict K3
        ed1, ed2, ed3 = ({}, {}, {})
        self.k3adj = {0: {1: ed1, 2: ed2}, 1: {0: ed1, 2: ed3}, 2: {0: ed2, 1: ed3}}
        self.k3edges = [(0, 1), (0, 2), (1, 2)]
        self.k3nodes = [0, 1, 2]
        self.K3 = self.Graph()
        self.K3._adj = self.k3adj
        self.K3._node = {}
        self.K3._node[0] = {}
        self.K3._node[1] = {}
        self.K3._node[2] = {}

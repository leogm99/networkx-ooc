import networkx as nx
from networkx.algorithms import bipartite


class TestMinEdgeCover:
    """Tests for :func:`networkx.algorithms.bipartite.min_edge_cover`"""

    def test_empty_graph(self):
        G = nx.Graph()
        assert bipartite.min_edge_cover(G) == set()

    def test_graph_single_edge(self):
        G = nx.Graph()
        G.add_edge(0, 1)
        assert bipartite.min_edge_cover(G) == {(0, 1), (1, 0)}

    def test_bipartite_default(self):
        G = nx.Graph()
        G.add_nodes_from([1, 2, 3, 4], bipartite=0)
        G.add_nodes_from([10, 11, 12], bipartite=1)
        G.add_edges_from([(1, 10), (1, 11), (2, 11), (2, 12), (3, 12), (4, 10)])
        min_cover = bipartite.min_edge_cover(G)
        assert nx.is_edge_cover(G, min_cover)
        assert len(min_cover) == 8

    def test_bipartite_explicit(self):
        G = nx.Graph()
        G.add_nodes_from([1, 2, 3, 4], bipartite=0)
        G.add_nodes_from([11, 12, 13], bipartite=1)
        G.add_edges_from([(1, 11), (1, 12), (2, 12), (2, 13), (3, 13), (4, 11)])
        min_cover = bipartite.min_edge_cover(G, bipartite.eppstein_matching)
        assert nx.is_edge_cover(G, min_cover)
        assert len(min_cover) == 8

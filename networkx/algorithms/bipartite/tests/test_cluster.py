import pytest

import networkx as nx
from networkx.algorithms import bipartite
from networkx.algorithms.bipartite.cluster import cc_dot, cc_max, cc_min

from networkx.classes.lazygraph import LazyGraph
from networkx.structures.out_of_core_set import OutOfCoreSet


def test_pairwise_bipartite_cc_functions():
    # Test functions for different kinds of bipartite clustering coefficients
    # between pairs of nodes using 3 example graphs from figure 5 p. 40
    # Latapy et al (2008)
    G1 = nx.Graph([(0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (1, 5), (1, 6), (1, 7)])
    LazyG1 = LazyGraph()
    for u, v in G1.edges():
        LazyG1.add_edge(u, v)
    G2 = nx.Graph([(0, 2), (0, 3), (0, 4), (1, 3), (1, 4), (1, 5)])
    LazyG2 = LazyGraph()
    for u, v in G2.edges():
        LazyG2.add_edge(u, v)
    G3 = nx.Graph(
        [(0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9)]
    )
    LazyG3 = LazyGraph()
    for u, v in G3.edges():
        LazyG3.add_edge(u, v)
    result = {
        0: [1 / 3.0, 2 / 3.0, 2 / 5.0],
        1: [1 / 2.0, 2 / 3.0, 2 / 3.0],
        2: [2 / 8.0, 2 / 5.0, 2 / 5.0],
    }
    for i, G in enumerate([LazyG1, LazyG2, LazyG3]):
        assert bipartite.is_bipartite(G)
        assert cc_dot(OutOfCoreSet(G[0]), OutOfCoreSet(G[1])) == result[i][0]
        assert cc_min(OutOfCoreSet(G[0]), OutOfCoreSet(G[1])) == result[i][1]
        assert cc_max(OutOfCoreSet(G[0]), OutOfCoreSet(G[1])) == result[i][2]


def test_star_graph():
    G = nx.star_graph(3)
    LazyG = LazyGraph()
    for u, v in G.edges():
        LazyG.add_edge(u, v)
    # all modes are the same
    answer = {0: 0, 1: 1, 2: 1, 3: 1}
    assert bipartite.clustering(LazyG, mode="dot") == answer
    assert bipartite.clustering(LazyG, mode="min") == answer
    assert bipartite.clustering(LazyG, mode="max") == answer


def test_not_bipartite():
    with pytest.raises(nx.NetworkXError):
        bipartite.clustering(_get_ooc_complete_graph())


def test_bad_mode():
    with pytest.raises(nx.NetworkXError):
        bipartite.clustering(_get_ooc_path_graph(), mode="foo")


def test_path_graph():
    G = _get_ooc_path_graph()
    answer = {0: 0.5, 1: 0.5, 2: 0.5, 3: 0.5}
    assert bipartite.clustering(G, mode="dot") == answer
    assert bipartite.clustering(G, mode="max") == answer
    answer = {0: 1, 1: 1, 2: 1, 3: 1}
    assert bipartite.clustering(G, mode="min") == answer


def test_average_path_graph():
    G = _get_ooc_path_graph()
    assert bipartite.average_clustering(G, mode="dot") == 0.5
    assert bipartite.average_clustering(G, mode="max") == 0.5
    assert bipartite.average_clustering(G, mode="min") == 1


# def test_ra_clustering_davis():
#     G = nx.davis_southern_women_graph()
#     cc4 = round(bipartite.robins_alexander_clustering(G), 3)
#     assert cc4 == 0.468


def test_ra_clustering_square():
    G = _get_ooc_path_graph()
    G.add_edge(0, 3)
    assert bipartite.robins_alexander_clustering(G) == 1.0


def test_ra_clustering_zero():
    G = LazyGraph()
    assert bipartite.robins_alexander_clustering(G) == 0
    G.add_nodes_from(range(4))
    assert bipartite.robins_alexander_clustering(G) == 0
    G.add_edges_from([(0, 1), (2, 3), (3, 4)])
    assert bipartite.robins_alexander_clustering(G) == 0
    G.add_edge(1, 2)
    assert bipartite.robins_alexander_clustering(G) == 0

@staticmethod
def _get_ooc_path_graph():
    G = nx.path_graph(4)
    LazyG = LazyGraph()
    for u, v in G.edges():
        LazyG.add_edge(u, v)
    return LazyG

@staticmethod
def _get_ooc_complete_graph():
    G = nx.complete_graph(4)
    LazyG = LazyGraph()
    for u, v in G.edges():
        LazyG.add_edge(u, v)
    return LazyG

"""Unit tests for the :mod:`networkx.algorithms.bipartite.redundancy` module.

"""

import pytest

from networkx import NetworkXError, cycle_graph
from networkx.algorithms.bipartite import complete_bipartite_graph, node_redundancy

from networkx.classes.lazygraph import LazyGraph
from networkx.structures.out_of_core_set import OutOfCoreSet


def test_no_redundant_nodes():
    G = _get_complete_bipartite_graph(2, 2)

    # when nodes is None
    rc = node_redundancy(G)
    assert all(redundancy == 1 for redundancy in rc.values())

    # when set of nodes is specified
    rc = node_redundancy(G, (2, 3))
    assert rc == {2: 1.0, 3: 1.0}


def test_redundant_nodes():
    G = cycle_graph(6)
    LazyG = LazyGraph()
    for e in G.edges:
        LazyG.add_edge(*e)
    edge = {0, 3}
    LazyG.add_edge(*edge)
    redundancy = node_redundancy(LazyG)
    for v in edge:
        assert round(redundancy[v], 6) == round(2 / 3, 6)
    for v in OutOfCoreSet(LazyG) - edge:
        assert redundancy[v] == 1


def test_not_enough_neighbors():
    with pytest.raises(NetworkXError):
        G = _get_complete_bipartite_graph(1, 2)
        node_redundancy(G)

@staticmethod
def _get_complete_bipartite_graph(n1, n2):
    G = complete_bipartite_graph(n1, n2)
    LazyG = LazyGraph()
    for e in G.edges:
        LazyG.add_edge(*e)
    return LazyG

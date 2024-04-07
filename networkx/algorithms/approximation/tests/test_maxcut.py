import random

import networkx as nx
from networkx.algorithms.approximation import maxcut

from networkx.classes.lazygraph import LazyGraph
from networkx.structures.out_of_core_set import OutOfCoreSet


def _is_valid_cut(G, set1, set2):
    union = set1.union(set2)
    assert union == OutOfCoreSet(G.nodes)
    assert len(set1) + len(set2) == G.number_of_nodes()


def _cut_is_locally_optimal(G, cut_size, set1):
    # test if cut can be locally improved
    for i, node in enumerate(set1):
        cut_size_without_node = nx.algorithms.cut_size(
            G, set1 - {node}, weight="weight"
        )
        assert cut_size_without_node <= cut_size


def test_random_partitioning():
    G = nx.complete_graph(5)
    LazyG = LazyGraph()
    for e in G.edges:
        LazyG.add_edge(*e)
    _, (set1, set2) = maxcut.randomized_partitioning(LazyG, seed=5)
    _is_valid_cut(LazyG, set1, set2)


def test_random_partitioning_all_to_one():
    G = nx.complete_graph(5)
    LazyG = LazyGraph()
    for e in G.edges:
        LazyG.add_edge(*e)
    _, (set1, set2) = maxcut.randomized_partitioning(LazyG, p=1)
    _is_valid_cut(LazyG, set1, set2)
    assert len(set1) == LazyG.number_of_nodes()
    assert len(set2) == 0


def test_one_exchange_basic():
    G = nx.complete_graph(5)
    random.seed(5)
    for u, v, w in G.edges(data=True):
        w["weight"] = random.randrange(-100, 100, 1) / 10

    LazyG = LazyGraph()
    for u, v, w in G.edges(data=True):
        weight = w["weight"]
        LazyG.add_edge(u, v, weight=weight)

    initial_cut = OutOfCoreSet(random.sample(sorted(LazyG.nodes()), k=5))
    cut_size, (set1, set2) = maxcut.one_exchange(
        LazyG, initial_cut, weight="weight", seed=5
    )

    _is_valid_cut(LazyG, set1, set2)
    _cut_is_locally_optimal(LazyG, cut_size, set1)


def test_one_exchange_optimal():
    # Greedy one exchange should find the optimal solution for this graph (14)
    LazyG = LazyGraph()
    LazyG.add_edge(1, 2, weight=3)
    LazyG.add_edge(1, 3, weight=3)
    LazyG.add_edge(1, 4, weight=3)
    LazyG.add_edge(1, 5, weight=3)
    LazyG.add_edge(2, 3, weight=5)

    cut_size, (set1, set2) = maxcut.one_exchange(LazyG, weight="weight", seed=5)

    _is_valid_cut(LazyG, set1, set2)
    _cut_is_locally_optimal(LazyG, cut_size, set1)
    # check global optimality
    assert cut_size == 14


def test_negative_weights():
    G = nx.complete_graph(5)
    random.seed(5)
    for u, v, w in G.edges(data=True):
        w["weight"] = -1 * random.random()

    LazyG = LazyGraph()
    for u, v, w in G.edges(data=True):
        weight = w["weight"]
        LazyG.add_edge(u, v, weight=weight)

    initial_cut = OutOfCoreSet(random.sample(sorted(LazyG.nodes()), k=5))
    cut_size, (set1, set2) = maxcut.one_exchange(LazyG, initial_cut, weight="weight")

    # make sure it is a valid cut
    _is_valid_cut(LazyG, set1, set2)
    # check local optimality
    _cut_is_locally_optimal(LazyG, cut_size, set1)
    # test that all nodes are in the same partition
    assert len(set1) == len(LazyG.nodes) or len(set2) == len(LazyG.nodes)

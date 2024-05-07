from itertools import combinations

import pytest

import networkx as nx


def path_graph():
    """Return a path graph of length three."""
    G = nx.path_graph(3, create_using=nx.DiGraph)
    G.graph["name"] = "path"
    nx.freeze(G)
    return G


def fork_graph():
    """Return a three node fork graph."""
    G = nx.DiGraph(name="fork")
    G.add_edges_from([(0, 1), (0, 2)])
    nx.freeze(G)
    return G


def collider_graph():
    """Return a collider/v-structure graph with three nodes."""
    G = nx.DiGraph(name="collider")
    G.add_edges_from([(0, 2), (1, 2)])
    nx.freeze(G)
    return G


def naive_bayes_graph():
    """Return a simply Naive Bayes PGM graph."""
    G = nx.DiGraph(name="naive_bayes")
    G.add_edges_from([(0, 1), (0, 2), (0, 3), (0, 4)])
    nx.freeze(G)
    return G


def asia_graph():
    """Return the 'Asia' PGM graph."""
    G = nx.DiGraph(name="asia")
    G.add_edges_from(
        [
            (1, 2),
            (3, 4),
            (3, 5),
            (2, 6),
            (4, 6),
            (6, 7),
            (6, 8),
            (5, 8),
        ]
    )
    nx.freeze(G)
    return G


@pytest.fixture(name="path_graph")
def path_graph_fixture():
    return path_graph()


@pytest.fixture(name="fork_graph")
def fork_graph_fixture():
    return fork_graph()


@pytest.fixture(name="collider_graph")
def collider_graph_fixture():
    return collider_graph()


@pytest.fixture(name="naive_bayes_graph")
def naive_bayes_graph_fixture():
    return naive_bayes_graph()


@pytest.fixture(name="asia_graph")
def asia_graph_fixture():
    return asia_graph()


@pytest.mark.parametrize(
    "graph",
    [path_graph(), fork_graph(), collider_graph(), naive_bayes_graph(), asia_graph()],
)
def test_markov_condition(graph):
    """Test that the Markov condition holds for each PGM graph."""
    for node in graph.nodes:
        parents = set(graph.predecessors(node))
        non_descendants = graph.nodes - nx.descendants(graph, node) - {node} - parents
        assert nx.d_separated(graph, {node}, non_descendants, parents)


def test_path_graph_dsep(path_graph):
    """Example-based test of d-separation for path_graph."""
    assert nx.d_separated(path_graph, {0}, {2}, {1})
    assert not nx.d_separated(path_graph, {0}, {2}, {})


def test_fork_graph_dsep(fork_graph):
    """Example-based test of d-separation for fork_graph."""
    assert nx.d_separated(fork_graph, {1}, {2}, {0})
    assert not nx.d_separated(fork_graph, {1}, {2}, {})


def test_collider_graph_dsep(collider_graph):
    """Example-based test of d-separation for collider_graph."""
    assert nx.d_separated(collider_graph, {0}, {1}, {})
    assert not nx.d_separated(collider_graph, {0}, {1}, {2})


def test_naive_bayes_dsep(naive_bayes_graph):
    """Example-based test of d-separation for naive_bayes_graph."""
    for u, v in combinations(range(1, 5), 2):
        assert nx.d_separated(naive_bayes_graph, {u}, {v}, {0})
        assert not nx.d_separated(naive_bayes_graph, {u}, {v}, {})


def test_asia_graph_dsep(asia_graph):
    """Example-based test of d-separation for asia_graph."""
    assert nx.d_separated(
        asia_graph, {1, 3}, {8, 7}, {5, 6}
    )
    assert nx.d_separated(
        asia_graph, {2, 4}, {5}, {3, 7}
    )


def test_undirected_graphs_are_not_supported():
    """
    Test that undirected graphs are not supported.

    d-separation and its related algorithms do not apply in
    the case of undirected graphs.
    """
    g = nx.path_graph(3, nx.Graph)
    with pytest.raises(nx.NetworkXNotImplemented):
        nx.d_separated(g, {0}, {1}, {2})
    with pytest.raises(nx.NetworkXNotImplemented):
        nx.is_minimal_d_separator(g, {0}, {1}, {2})
    with pytest.raises(nx.NetworkXNotImplemented):
        nx.minimal_d_separator(g, {0}, {1})


def test_cyclic_graphs_raise_error():
    """
    Test that cycle graphs should cause erroring.

    This is because PGMs assume a directed acyclic graph.
    """
    g = nx.cycle_graph(3, nx.DiGraph)
    with pytest.raises(nx.NetworkXError):
        nx.d_separated(g, {0}, {1}, {2})
    with pytest.raises(nx.NetworkXError):
        nx.minimal_d_separator(g, 0, 1)
    with pytest.raises(nx.NetworkXError):
        nx.is_minimal_d_separator(g, 0, 1, {2})


def test_invalid_nodes_raise_error(asia_graph):
    """
    Test that graphs that have invalid nodes passed in raise errors.
    """
    with pytest.raises(nx.NodeNotFound):
        nx.d_separated(asia_graph, {0}, {1}, {2})
    with pytest.raises(nx.NodeNotFound):
        nx.is_minimal_d_separator(asia_graph, 0, 1, {2})
    with pytest.raises(nx.NodeNotFound):
        nx.minimal_d_separator(asia_graph, 0, 1)


def test_minimal_d_separator():
    # Case 1:
    # create a graph A -> B <- C
    # B -> D -> E;
    # B -> F;
    # G -> E;
    edge_list = [(11, 12), (13, 12), (12, 14), (14, 15), (12, 16), (17, 15)]
    G = nx.DiGraph(edge_list)
    assert not nx.d_separated(G, {12}, {15}, set())

    # minimal set of the corresponding graph
    # for B and E should be (D,)
    Zmin = nx.minimal_d_separator(G, 12, 15)

    # the minimal separating set should pass the test for minimality
    assert nx.is_minimal_d_separator(G, 12, 15, Zmin)
    assert Zmin == {14}

    # Case 2:
    # create a graph A -> B -> C
    # B -> D -> C;
    edge_list = [(11, 12), (12, 13), (12, 14), (14, 13)]
    G = nx.DiGraph(edge_list)
    assert not nx.d_separated(G, {11}, {13}, set())
    Zmin = nx.minimal_d_separator(G, 11, 13)

    # the minimal separating set should pass the test for minimality
    assert nx.is_minimal_d_separator(G, 11, 13, Zmin)
    assert Zmin == {12}

    Znotmin = Zmin.union({14})
    assert not nx.is_minimal_d_separator(G, 11, 13, Znotmin)


def test_minimal_d_separator_checks_dsep():
    """Test that is_minimal_d_separator checks for d-separation as well."""
    g = nx.DiGraph()
    g.add_edges_from(
        [
            (11, 12),
            (11, 15),
            (12, 13),
            (12, 14),
            (14, 13),
            (14, 16),
            (15, 14),
            (15, 16),
        ]
    )

    assert not nx.d_separated(g, {13}, {16}, {14})

    # since {'D'} and {} are not d-separators, we return false
    assert not nx.is_minimal_d_separator(g, 13, 16, {14})
    assert not nx.is_minimal_d_separator(g, 13, 16, {})

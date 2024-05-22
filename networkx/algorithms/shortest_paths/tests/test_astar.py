from networkx.algorithms.shortest_paths.tests import app_mode
import pytest

import networkx as nx
from networkx.utils import pairwise


class TestAStar:
    @classmethod
    def setup_class(cls):
        edges = [
            (1, 2, 10),
            (1, 3, 5),
            (2, 4, 1),
            (2, 3, 2),
            (4, 5, 1),
            (3, 2, 3),
            (3, 4, 5),
            (3, 5, 2),
            (5, 1, 7),
            (5, 4, 6),
        ]
        cls.XG = nx.DiGraph()
        cls.XG.add_weighted_edges_from(edges)

    def test_multiple_optimal_paths(self):
        """Tests that A* algorithm finds any of multiple optimal paths"""
        heuristic_values = {1: 1.35, 2: 1.18, 3: 0.67, 4: 0}

        def h(u, v):
            return heuristic_values[u]

        graph = nx.Graph()
        points = [1, 2, 3, 4]
        edges = [(1, 2, 0.18), (1, 3, 0.68), (2, 3, 0.50), (3, 4, 0.67)]

        graph.add_nodes_from(points)
        graph.add_weighted_edges_from(edges)

        path1 = [1, 3, 4]
        path2 = [1, 2, 3, 4]
        assert nx.astar_path(graph, 1, 4, h) in (path1, path2)

    def test_astar_directed(self):
        assert nx.astar_path(self.XG, 1, 4) == [1, 3, 2, 4]
        assert nx.astar_path_length(self.XG, 1, 4) == 9

    def test_astar_directed_weight_function(self):
        w1 = lambda u, v, d: d["weight"]
        assert nx.astar_path(self.XG, 3, 2, weight=w1) == [3, 2]
        assert nx.astar_path_length(self.XG, 3, 2, weight=w1) == 3
        assert nx.astar_path(self.XG, 1, 4, weight=w1) == [1, 3, 2, 4]
        assert nx.astar_path_length(self.XG, 1, 4, weight=w1) == 9

        w2 = lambda u, v, d: None if (u, v) == (3, 2) else d["weight"]
        assert nx.astar_path(self.XG, 3, 2, weight=w2) == [3, 5, 1, 2]
        assert nx.astar_path_length(self.XG, 3, 2, weight=w2) == 19
        assert nx.astar_path(self.XG, 1, 4, weight=w2) == [1, 3, 4]
        assert nx.astar_path_length(self.XG, 1, 4, weight=w2) == 10

        w3 = lambda u, v, d: d["weight"] + 10
        assert nx.astar_path(self.XG, 3, 2, weight=w3) == [3, 2]
        assert nx.astar_path_length(self.XG, 3, 2, weight=w3) == 13
        assert nx.astar_path(self.XG, 1, 4, weight=w3) == [1, 3, 4]
        assert nx.astar_path_length(self.XG, 1, 4, weight=w3) == 30

    def test_astar_multigraph(self):
        G = nx.MultiDiGraph(self.XG)
        G.add_weighted_edges_from((u, v, 1000) for (u, v) in list(G.edges()))
        assert nx.astar_path(G, 1, 4) == [1, 3, 2, 4]
        assert nx.astar_path_length(G, 1, 4) == 9

    def test_astar_undirected(self):
        GG = self.XG.to_undirected()
        # make sure we get lower weight
        # to_undirected might choose either edge with weight 2 or weight 3
        GG[2][3]["weight"] = 2
        GG[5][4]["weight"] = 2
        assert nx.astar_path(GG, 1, 4) == [1, 3, 2, 4]
        assert nx.astar_path_length(GG, 1, 4) == 8

    def test_astar_directed2(self):
        XG2 = nx.DiGraph()
        edges = [
            (1, 4, 1),
            (4, 5, 1),
            (5, 6, 1),
            (6, 3, 1),
            (1, 3, 50),
            (1, 2, 100),
            (2, 3, 100),
        ]
        XG2.add_weighted_edges_from(edges)
        assert nx.astar_path(XG2, 1, 3) == [1, 4, 5, 6, 3]

    def test_astar_undirected2(self):
        XG3 = nx.Graph()
        edges = [(0, 1, 2), (1, 2, 12), (2, 3, 1), (3, 4, 5), (4, 5, 1), (5, 0, 10)]
        XG3.add_weighted_edges_from(edges)
        assert nx.astar_path(XG3, 0, 3) == [0, 1, 2, 3]
        assert nx.astar_path_length(XG3, 0, 3) == 15

    def test_astar_undirected3(self):
        XG4 = nx.Graph()
        edges = [
            (0, 1, 2),
            (1, 2, 2),
            (2, 3, 1),
            (3, 4, 1),
            (4, 5, 1),
            (5, 6, 1),
            (6, 7, 1),
            (7, 0, 1),
        ]
        XG4.add_weighted_edges_from(edges)
        assert nx.astar_path(XG4, 0, 2) == [0, 1, 2]
        assert nx.astar_path_length(XG4, 0, 2) == 4

    """ Tests that A* finds correct path when multiple paths exist
        and the best one is not expanded first (GH issue #3464)
    """

    def test_astar_directed3(self):
        heuristic_values = {1: 36, 2: 4, 3: 0, 4: 0}

        def h(u, v):
            return heuristic_values[u]

        edges = [(1, 3, 11), (1, 2, 9), (2, 3, 1), (3, 4, 32)]
        graph = nx.DiGraph()
        graph.add_weighted_edges_from(edges)
        answer = [1, 2, 3, 4]
        assert nx.astar_path(graph, 1, 4, h) == answer

    """ Tests that parent is not wrongly overridden when a node
        is re-explored multiple times.
    """

    def test_astar_directed4(self):
        edges = [
            (1, 2, 1),
            (1, 3, 1),
            (2, 4, 2),
            (3, 4, 1),
            (4, 5, 1),
        ]
        graph = nx.DiGraph()
        graph.add_weighted_edges_from(edges)
        assert nx.astar_path(graph, 1, 5) == [1, 3, 4, 5]

    # >>> MXG4=NX.MultiGraph(XG4)
    # >>> MXG4.add_edge(0,1,3)
    # >>> NX.dijkstra_path(MXG4,0,2)
    # [0, 1, 2]

    def test_astar_w1(self):
        G = nx.DiGraph()
        G.add_edges_from(
            [
                (1, 2),
                (1, 3),
                (2, 4),
                (2, 3),
                (4, 5),
                (3, 2),
                (3, 6),
                (6, 4),
                (3, 5),
                (5, 1),
                (5, 4),
            ]
        )
        assert nx.astar_path(G, 1, 4) == [1, 2, 4]
        assert nx.astar_path_length(G, 1, 4) == 2

    def test_astar_nopath(self):
        with pytest.raises(nx.NodeNotFound):
            nx.astar_path(self.XG, 1, "moon")

    def test_cycle(self):
        C = nx.cycle_graph(7)
        assert nx.astar_path(C, 0, 3) == [0, 1, 2, 3]
        assert nx.dijkstra_path(C, 0, 4) == [0, 6, 5, 4]

    @pytest.mark.skipif(app_mode == 'lazy', reason="lazy graph does not support this algorithms")
    def test_unorderable_nodes(self):
        """Tests that A* accommodates nodes that are not orderable.

        For more information, see issue #554.

        """
        # Create the cycle graph on four nodes, with nodes represented
        # as (unorderable) Python objects.
        nodes = [object() for n in range(4)]
        G = nx.Graph()
        G.add_edges_from(pairwise(nodes, cyclic=True))
        path = nx.astar_path(G, nodes[0], nodes[2])
        assert len(path) == 3

    @pytest.mark.skipif(app_mode == 'lazy', reason="lazy graph does not support this algorithms")
    def test_astar_NetworkXNoPath(self):
        """Tests that exception is raised when there exists no
        path between source and target"""
        G = nx.gnp_random_graph(10, 0.2, seed=10)
        with pytest.raises(nx.NetworkXNoPath):
            nx.astar_path(G, 4, 9)

    def test_astar_NodeNotFound(self):
        """Tests that exception is raised when either
        source or target is not in graph"""
        G = nx.gnp_random_graph(10, 0.2, seed=10)
        with pytest.raises(nx.NodeNotFound):
            nx.astar_path_length(G, 11, 9)

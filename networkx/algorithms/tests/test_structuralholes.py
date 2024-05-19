"""Unit tests for the :mod:`networkx.algorithms.structuralholes` module."""
import math

from networkx.algorithms.tests import app_mode
import pytest

import networkx as nx
from networkx.classes.tests import dispatch_interface


class TestStructuralHoles:
    """Unit tests for computing measures of structural holes.

    The expected values for these functions were originally computed using the
    proprietary software `UCINET`_ and the free software `IGraph`_ , and then
    computed by hand to make sure that the results are correct.

    .. _UCINET: https://sites.google.com/site/ucinetsoftware/home
    .. _IGraph: http://igraph.org/

    """

    def setup_method(self):
        self.D = nx.DiGraph()
        self.D.add_edges_from([(0, 1), (0, 2), (1, 0), (2, 1)])
        self.D_weights = {(0, 1): 2, (0, 2): 2, (1, 0): 1, (2, 1): 1}
        # Example from http://www.analytictech.com/connections/v20(1)/holes.htm
        self.G = nx.Graph()
        self.G.add_edges_from(
            [
                (11, 12),
                (11, 13),
                (11, 14),
                (11, 15),
                (15, 14),
                (13, 14),
                (12, 14),
                (12, 16),
                (16, 14),
                (14, 17),
            ]
        )
        self.G_weights = {
            (11, 12): 2,
            (11, 13): 3,
            (11, 14): 5,
            (11, 15): 2,
            (15, 14): 8,
            (13, 14): 3,
            (12, 14): 4,
            (12, 16): 1,
            (16, 14): 3,
            (14, 17): 10,
        }

    # This additionally tests the @nx._dispatch mechanism, treating
    # nx.mutual_weight as if it were a re-implementation from another package
    @pytest.mark.parametrize("wrapper", [lambda x: x, dispatch_interface.convert])
    def test_constraint_directed(self, wrapper):
        constraint = nx.constraint(wrapper(self.D))
        assert constraint[0] == pytest.approx(1.003, abs=1e-3)
        assert constraint[1] == pytest.approx(1.003, abs=1e-3)
        assert constraint[2] == pytest.approx(1.389, abs=1e-3)

    @pytest.mark.skipif(app_mode == 'lazy', reason="lazy graph does not support this algorithms")
    def test_effective_size_directed(self):
        effective_size = nx.effective_size(self.D)
        assert effective_size[0] == pytest.approx(1.167, abs=1e-3)
        assert effective_size[1] == pytest.approx(1.167, abs=1e-3)
        assert effective_size[2] == pytest.approx(1, abs=1e-3)

    @pytest.mark.skipif(app_mode == 'lazy', reason="lazy graph does not support this algorithms")
    def test_constraint_weighted_directed(self):
        D = self.D.copy()
        nx.set_edge_attributes(D, self.D_weights, "weight")
        constraint = nx.constraint(D, weight="weight")
        assert constraint[0] == pytest.approx(0.840, abs=1e-3)
        assert constraint[1] == pytest.approx(1.143, abs=1e-3)
        assert constraint[2] == pytest.approx(1.378, abs=1e-3)

    @pytest.mark.skipif(app_mode == 'lazy', reason="lazy graph does not support this algorithms")
    def test_effective_size_weighted_directed(self):
        D = self.D.copy()
        nx.set_edge_attributes(D, self.D_weights, "weight")
        effective_size = nx.effective_size(D, weight="weight")
        assert effective_size[0] == pytest.approx(1.567, abs=1e-3)
        assert effective_size[1] == pytest.approx(1.083, abs=1e-3)
        assert effective_size[2] == pytest.approx(1, abs=1e-3)

    def test_constraint_undirected(self):
        constraint = nx.constraint(self.G)
        assert constraint[14] == pytest.approx(0.400, abs=1e-3)
        assert constraint[11] == pytest.approx(0.595, abs=1e-3)
        assert constraint[17] == pytest.approx(1, abs=1e-3)

    @pytest.mark.skipif(app_mode == 'lazy', reason="lazy graph does not support this algorithms")
    def test_effective_size_undirected_borgatti(self):
        effective_size = nx.effective_size(self.G)
        assert effective_size[14] == pytest.approx(4.67, abs=1e-2)
        assert effective_size[11] == pytest.approx(2.50, abs=1e-2)
        assert effective_size[17] == pytest.approx(1, abs=1e-2)

    @pytest.mark.skipif(app_mode == 'lazy', reason="lazy graph does not support this algorithms")
    def test_effective_size_undirected(self):
        G = self.G.copy()
        nx.set_edge_attributes(G, 1, "weight")
        effective_size = nx.effective_size(G, weight="weight")
        assert effective_size[14] == pytest.approx(4.67, abs=1e-2)
        assert effective_size[11] == pytest.approx(2.50, abs=1e-2)
        assert effective_size[17] == pytest.approx(1, abs=1e-2)

    @pytest.mark.skipif(app_mode == 'lazy', reason="lazy graph does not support this algorithms")
    def test_constraint_weighted_undirected(self):
        G = self.G.copy()
        nx.set_edge_attributes(G, self.G_weights, "weight")
        constraint = nx.constraint(G, weight="weight")
        assert constraint[14] == pytest.approx(0.299, abs=1e-3)
        assert constraint[11] == pytest.approx(0.795, abs=1e-3)
        assert constraint[17] == pytest.approx(1, abs=1e-3)

    @pytest.mark.skipif(app_mode == 'lazy', reason="lazy graph does not support this algorithms")
    def test_effective_size_weighted_undirected(self):
        G = self.G.copy()
        nx.set_edge_attributes(G, self.G_weights, "weight")
        effective_size = nx.effective_size(G, weight="weight")
        assert effective_size[14] == pytest.approx(5.47, abs=1e-2)
        assert effective_size[11] == pytest.approx(2.47, abs=1e-2)
        assert effective_size[17] == pytest.approx(1, abs=1e-2)

    @pytest.mark.skipif(app_mode == 'lazy', reason="lazy graph does not support this algorithms")
    def test_constraint_isolated(self):
        G = self.G.copy()
        G.add_node(1)
        constraint = nx.constraint(G)
        assert math.isnan(constraint[1])

    @pytest.mark.skipif(app_mode == 'lazy', reason="lazy graph does not support this algorithms")
    def test_effective_size_isolated(self):
        G = self.G.copy()
        G.add_node(1)
        nx.set_edge_attributes(G, self.G_weights, "weight")
        effective_size = nx.effective_size(G, weight="weight")
        assert math.isnan(effective_size[1])

    @pytest.mark.skipif(app_mode == 'lazy', reason="lazy graph does not support this algorithms")
    def test_effective_size_borgatti_isolated(self):
        G = self.G.copy()
        G.add_node(1)
        effective_size = nx.effective_size(G)
        assert math.isnan(effective_size[1])

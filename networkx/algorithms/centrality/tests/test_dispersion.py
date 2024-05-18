import networkx as nx
import pytest

from networkx.algorithms.centrality.tests import app_mode

def small_ego_G():
    """The sample network from https://arxiv.org/pdf/1310.6753v1.pdf"""
    edges = [
        (1, 2),
        (1, 3),
        (2, 3),
        (2, 4),
        (2, 5),
        (2, 6),
        (3, 4),
        (3, 6),
        (3, 7),
        (4, 6),
        (5, 6),
        (6, 7),
        (7, 8),
        (7, 9),
        (10, 8),
        (10, 9),
        (8, 9),
        (11, 1),
        (11, 2),
        (11, 3),
        (11, 4),
        (11, 5),
        (11, 6),
        (11, 12),
        (11, 7),
        (11, 10),
        (11, 8),
        (11, 9),
    ]
    G = nx.Graph()
    G.add_edges_from(edges)

    return G


class TestDispersion:
    def test_article(self):
        """our algorithm matches article's"""
        G = small_ego_G()
        disp_uh = nx.dispersion(G, 11, 7, normalized=False)
        disp_ub = nx.dispersion(G, 11, 2, normalized=False)
        assert disp_uh == 4
        assert disp_ub == 1

    def test_results_length(self):
        """there is a result for every node"""
        G = small_ego_G()
        disp = nx.dispersion(G)
        disp_Gu = nx.dispersion(G, 11)
        disp_uv = nx.dispersion(G, 11, 7)
        assert len(disp) == len(G)
        assert len(disp_Gu) == len(G) - 1
        assert isinstance(disp_uv, float)

    def test_dispersion_v_only(self):
        G = small_ego_G()
        disp_G_h = nx.dispersion(G, v=7, normalized=False)
        disp_G_h_normalized = nx.dispersion(G, v=7, normalized=True)
        assert disp_G_h == {3: 0, 6: 0, 8: 0, 9: 0, 11: 4}
        assert disp_G_h_normalized == {3: 0.0, 6: 0.0, 8: 0.0, 9: 0.0, 11: 1.0}

    @pytest.mark.skipif(app_mode == 'lazy', reason="lazy graph does not support strings")
    def test_impossible_things(self):
        G = nx.karate_club_graph()
        disp = nx.dispersion(G)
        for u in disp:
            for v in disp[u]:
                assert disp[u][v] >= 0

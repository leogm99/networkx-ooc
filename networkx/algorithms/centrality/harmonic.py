"""Functions for computing the harmonic centrality of a graph."""
from functools import partial

import networkx as nx

from networkx.structures.out_of_core_set import OutOfCoreSet
from networkx.structures.primitive_dicts import IntFloatDict

__all__ = ["harmonic_centrality"]


@nx._dispatch(edge_attrs="distance")
def harmonic_centrality(G, nbunch=None, distance=None, sources=None):
    r"""Compute harmonic centrality for nodes.

    Harmonic centrality [1]_ of a node `u` is the sum of the reciprocal
    of the shortest path distances from all other nodes to `u`

    .. math::

        C(u) = \sum_{v \neq u} \frac{1}{d(v, u)}

    where `d(v, u)` is the shortest-path distance between `v` and `u`.

    If `sources` is given as an argument, the returned harmonic centrality
    values are calculated as the sum of the reciprocals of the shortest
    path distances from the nodes specified in `sources` to `u` instead
    of from all nodes to `u`.

    Notice that higher values indicate higher centrality.

    Parameters
    ----------
    G : graph
      A NetworkX graph

    nbunch : container (default: all nodes in G)
      Container of nodes for which harmonic centrality values are calculated.

    sources : container (default: all nodes in G)
      Container of nodes `v` over which reciprocal distances are computed.
      Nodes not in `G` are silently ignored.

    distance : edge attribute key, optional (default=None)
      Use the specified edge attribute as the edge distance in shortest
      path calculations.  If `None`, then each edge will have distance equal to 1.

    Returns
    -------
    nodes : dictionary
      Dictionary of nodes with harmonic centrality as the value.

    See Also
    --------
    betweenness_centrality, load_centrality, eigenvector_centrality,
    degree_centrality, closeness_centrality

    Notes
    -----
    If the 'distance' keyword is set to an edge attribute key then the
    shortest-path length will be computed using Dijkstra's algorithm with
    that edge attribute as the edge weight.

    References
    ----------
    .. [1] Boldi, Paolo, and Sebastiano Vigna. "Axioms for centrality."
           Internet Mathematics 10.3-4 (2014): 222-262.
    """

    if nbunch is not None:
        nbunch_ooc = OutOfCoreSet(G.nbunch_iter(nbunch))
    else:
        nbunch_ooc = OutOfCoreSet()
        for v in G.nodes:
            nbunch_ooc.add(v)

    if sources is not None:
        sources_ooc = OutOfCoreSet(G.nbunch_iter(sources))
    else:
        sources_ooc = OutOfCoreSet()
        for v in G.nodes:
            sources_ooc.add(v)

    spl = partial(nx.shortest_path_length, G, weight=distance)
    centrality = IntFloatDict()
    for u in nbunch_ooc:
        centrality[u] = 0
    for v in sources_ooc:
        dist = spl(v)
        for u in nbunch_ooc.intersection(dist):
            d = dist[u]
            if d == 0:  # handle u == v and edges with 0 weight
                continue
            centrality[u] += 1 / d

    return centrality

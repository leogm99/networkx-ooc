from networkx import NetworkXError
from networkx.classes.graph import Graph
from networkx.structures.out_of_core_dict import OutOfCoreDict

__all__ = ["LazyGraph", "NotSupportedForLazyGraph"]

from networkx.structures.lazy_adjacency_list import LazyAdjacencyList
from networkx.structures.lazy_node_list import LazyNodeList


class NotSupportedForLazyGraph(BaseException):
    def __init__(self, message):
        super().__init__(message)


def not_supported(*_, **__):
    raise NotSupportedForLazyGraph("Method not supported")


class LazyGraph(Graph):
    node_dict_factory = LazyNodeList
    adjlist_outer_dict_factory = LazyAdjacencyList
    adjlist_inner_dict_factory = lambda _: None

    # graph_attr_dict_factory = OutOfCoreDict

    def __init__(self, incoming_graph_data=None, **attr):
        super().__init__(incoming_graph_data, **attr)

    @staticmethod
    def read_file_sep(path_to_edgelist, sep=" "):
        with open(path_to_edgelist) as edgelist:
            while True:
                line = edgelist.readline().strip("\n")
                if not line:
                    break

                yield line.split(sep) if sep is not None else line.split()

    @classmethod
    def from_edgelist_file(cls, path_to_edgelist: str, sep: str = None):
        G = cls()
        G.add_edges_from(LazyGraph.read_file_sep(path_to_edgelist, sep))
        return G

    def add_node(self, node_for_adding, **attr):
        if node_for_adding is None:
            raise ValueError("Node cannot be None")
        if node_for_adding not in self._node:
            self._node.add_node(node_for_adding, **attr)

    def add_edge(self, u_of_edge, v_of_edge, **attr):
        if None in (u_of_edge, v_of_edge):
            raise ValueError("")
        if u_of_edge not in self._node:
            self._node.add_node(u_of_edge)
        if v_of_edge not in self._node:
            self._node.add_node(v_of_edge)
        self._adj.add_edge(u_of_edge, v_of_edge)
        self._adj.add_edge(v_of_edge, u_of_edge)

    def add_nodes_from(self, nodes_for_adding, **attr):
        for n in nodes_for_adding:
            if n is None:
                raise ValueError("Node cannot be None")
            self.add_node(n, **attr)

    def add_edges_from(self, ebunch_to_add, **attr):
        for u, v in ebunch_to_add:
            self.add_edge(u, v)

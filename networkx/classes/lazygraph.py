from networkx.classes.graph import Graph
from networkx.structures.lazy_adjacency_list import LazyAdjacencyList
from networkx.structures.lazy_node_list import LazyNodeList

__all__ = ["LazyGraph", "NotSupportedForLazyGraph"]


class NotSupportedForLazyGraph(BaseException):
    def __init__(self, message):
        super().__init__(message)


def not_supported(*_, **__):
    raise NotSupportedForLazyGraph("Method not supported")


class LazyGraph(Graph):
    node_dict_factory = LazyNodeList
    adjlist_outer_dict_factory = LazyAdjacencyList
    adjlist_inner_dict_factory = lambda _: None

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
            if len(n) == 2:
                u, dd = n
            else:
                u = n
                dd = None
            if u is None:
                raise ValueError("Node cannot be None")
            if dd is not None:
                self.add_node(u, **dd)
            else:
                self.add_node(u)

    def add_edges_from(self, ebunch_to_add, **attr):
        for x in ebunch_to_add:
            if len(x) == 3:
                u, v, _ = x
            else:
                u, v = x
            self.add_edge(u, v)

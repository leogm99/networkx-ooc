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

                yield [int(x) for x in line.split(sep)] if sep is not None else [int(x) for x in line.split()]

    @classmethod
    def from_edgelist_file(cls, path_to_edgelist: str, sep: str = None):
        G = cls()
        G.add_edges_from(LazyGraph.read_file_sep(path_to_edgelist, sep))
        return G

    def add_node(self, node_for_adding, **attr):
        if node_for_adding is None:
            raise ValueError("Node cannot be None")
        self._node.add_node(node_for_adding, **attr)

    def add_edge(self, u_of_edge, v_of_edge, **attr):
        if None in (u_of_edge, v_of_edge):
            raise ValueError("")
        # really there is not a fast way to check if a node exists
        # it its cheaper to add it
        self._node.add_node(u_of_edge)
        self._node.add_node(v_of_edge)
        self._adj.add_edge(u_of_edge, v_of_edge, **attr)
        self._adj.add_edge(v_of_edge, u_of_edge, **attr)

    def add_nodes_from(self, nodes_for_adding, **attr):
        for n in nodes_for_adding:
            try:
                u, dd = n
            except TypeError:
                u = n
                dd = None
            if n is None:
                raise ValueError("Node cannot be None")
            if dd is not None:
                self.add_node(u, **dd)
            else:
                self.add_node(u)

    def add_edges_from(self, ebunch_to_add, **attr):
        for i, x in enumerate(ebunch_to_add):
            if i % 10000 == 0:
                print(i)
            if len(x) == 3:
                u, v, data = x
                dd = {}
                dd.update(data)
                dd.update(attr)
                self.add_edge(u, v, **dd)
            else:
                u, v = x
                if len(attr) != 0:
                    self.add_edge(u, v, **attr)
                else:
                    self.add_edge(int(u), int(v))

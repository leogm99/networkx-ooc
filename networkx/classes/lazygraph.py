from networkx.classes.graph import Graph
from networkx.structures.out_of_core_dict import OutOfCoreDict

__all__ = ["LazyGraph", "NotSupportedForLazyGraph"]

from networkx.structures.lazy_adjacency_list import LazyAdjacencyList


class NotSupportedForLazyGraph(BaseException):
    def __init__(self, message):
        super().__init__(message)


def not_supported(*_, **__):
    raise NotSupportedForLazyGraph("Method not supported")


class LazyGraph(Graph):
    node_dict_factory = OutOfCoreDict
    adjlist_outer_dict_factory = LazyAdjacencyList
    adjlist_inner_dict_factory = lambda _: None
    graph_attr_dict_factory = OutOfCoreDict

    def __init__(self, incoming_graph_data=None, **attr):
        super().__init__(incoming_graph_data, **attr)

        self.add_node = (
            self.add_nodes_from
        ) = (
            self.add_edge
        ) = self.add_edges_from = self.add_weighted_edges_from = not_supported

    @classmethod
    def from_edgelist_file(cls, path_to_edgelist: str, sep: str = None):
        def read_file_sep():
            with open(path_to_edgelist, "r") as edgelist:
                while True:
                    line = edgelist.readline().strip("\n")
                    if not line:
                        break

                    yield line.split(sep) if sep is not None else line.split()

        G = cls()
        super(LazyGraph, cls).add_edges_from(G, read_file_sep())
        return G

from typing import MutableSet
from networkx.classes.graph import Graph
from networkx.structures.out_of_core_dict import OutOfCoreDict
from networkx.structures.out_of_core_node_dict import OutOfCoreNodeDict
from networkx.structures.out_of_core_set import OutOfCoreSet

__all__ = ["LazyGraph", "NotSupportedForLazyGraph"]


class NotSupportedForLazyGraph(BaseException):
    def __init__(self, message):
        super().__init__(message)


def not_supported(*_, **__):
    raise NotSupportedForLazyGraph("Method not supported")


class LazyGraph(Graph):
    node_dict_factory = OutOfCoreNodeDict
    adjlist_outer_dict_factory = OutOfCoreDict

    # node_attr_dict_factory = OutOfCoreDict
    # adjlist_inner_dict_factory = partial(shelf_factory, filename="adjlist_inner.db")
    # edge_attr_dict_factory = partial(shelf_factory, filename="edge_attrs.db")
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

                    yield line.split(sep) if sep != None else line.split()

        G = cls()
        super(LazyGraph, cls).add_edges_from(G, read_file_sep())
        return G

    def get_node_set(self, initial_list = None):
        return OutOfCoreSet(self._node, initial_list)

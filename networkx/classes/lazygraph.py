from networkx.classes.graph import Graph
from networkx.structures.edges_dict import EdgesDict
from networkx.structures.lazy_adjacency_list import LazyAdjacencyList
from networkx.structures.lazy_node_list import LazyNodeList
from functools import cached_property
from networkx.classes.reportviews import LazyDegreeView
from networkx.classes.coreviews import LazyAdjacencyView

from networkx.structures.out_of_core_deque import OutOfCoreDeque
from networkx.structures.out_of_core_dict_of_lists import OutOfCoreDictOfLists
from networkx.structures.out_of_core_list import OutOfCoreList
from networkx.structures.out_of_core_set import OutOfCoreSet
from networkx.structures.primitive_dicts import IntDict, IntFloatDict, PrimitiveType



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

    @cached_property
    def degree(self):
        return LazyDegreeView(self)

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
            if n is None:
                raise ValueError("Node cannot be None")
            if attr is not None:
                self.add_node(n, **attr)
            else:
                self.add_node(n)

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
                    self.add_edge(u, v)

    def number_of_edges(self, u=None, v=None) -> int:
        if u is None:
            return int(self.size())
        if u not in self._node:
            raise KeyError(u)
        nbrs_u = self._adj.get(u)
        if nbrs_u is None:
            return 0
        return 1 if v in nbrs_u else 0

    @cached_property
    def adj(self):
        return LazyAdjacencyView(self._adj)

    @classmethod
    def from_graph_edges(cls, G):
        LazyG = cls()
        for e in G.edges:
            LazyG.add_edge(*e)
        return LazyG

    def int_list(self, *args):
        return OutOfCoreList(*args)

    def float_list(self, *args):
        return OutOfCoreList(*args, value_primitive_type=PrimitiveType.FLOAT)
    
    def tuple_list(self, *args):
        return OutOfCoreList(*args, value_primitive_type=PrimitiveType.EDGE)

    def set_(self, *args):
        return OutOfCoreSet(*args)

    def int_dict(self, *args):
        return IntDict(*args)

    def int_float_dict(self, *args):
        return IntFloatDict(*args)

    def int_dict_of_lists(self):
        return OutOfCoreDictOfLists()
    
    def float_dict_of_lists(self):
        return OutOfCoreDictOfLists(PrimitiveType.FLOAT)

    def int_deque(self, *args):
        return OutOfCoreDeque(*args, IntDict())

    def float_deque(self, *args):
        return OutOfCoreDeque(*args, IntFloatDict())
    
    def tuple_int_dict_of_edges(self):
        return EdgesDict()
    
    def tuple_tuple_dict_of_edges(self):
        return EdgesDict(PrimitiveType.EDGE, PrimitiveType.EDGE)

    def int_tuple_dict_of_edges(self):
        return EdgesDict(PrimitiveType.INTEGER, PrimitiveType.EDGE)

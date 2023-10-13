from networkx.classes.graph import Graph
from networkx.structures.out_of_core_dict import OutOfCoreDict

__all__ = ["LazyGraph"]

class LazyGraph(Graph):
    node_dict_factory = OutOfCoreDict

    # node_attr_dict_factory = partial(shelf_factory, filename="node_attrs.db")
    # adjlist_outer_dict_factory = partial(shelf_factory, filename="adjlist_outer.db")
    # adjlist_inner_dict_factory = partial(shelf_factory, filename="adjlist_inner.db")
    # edge_attr_dict_factory = partial(shelf_factory, filename="edge_attrs.db")
    # graph_attr_dict_factory = partial(shelf_factory, filename="graph_attrs.db")

    def __init__(self, incoming_graph_data=None, **attr):
        super().__init__(incoming_graph_data, **attr)
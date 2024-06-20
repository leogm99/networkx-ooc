import pickle
import struct


class OutOfCoreGraphSerializer:
    def __init__(self, node_len: int = 1, format_='l'):
        assert node_len >= 1, "Node length must be greater than or equal to 1"
        self._node_len = node_len
        self._node_struct = struct.Struct(f'!{node_len}{format_}')
        self._edge_struct = struct.Struct(f'!{2 * node_len}{format_}')

    # will assume that the object is sized correctly
    def serialize_node(self, node):
        if self._node_len > 1:
            return self._node_struct.pack(*node)
        return self._node_struct.pack(node)

    def deserialize_node(self, node_data):
        data = self._node_struct.unpack(node_data)
        return data[0] if self._node_len == 1 else data

    def serialize_edge(self, u, v):
        if self._node_len > 1:
            return self._edge_struct.pack(*u, *v)
        return self._edge_struct.pack(u, v)

    def deserialize_edge(self, edge_data):
        edge_data = self._edge_struct.unpack(edge_data)
        if self._node_len == 1:
            return edge_data[0], edge_data[1]
        return edge_data[:self._node_len], edge_data[self._node_len:]

    @staticmethod
    def serialize_attr(attr):
        if attr == b'':
            return b''
        return pickle.dumps(attr)

    @staticmethod
    def deserialize_attr(attr):
        if attr == b'':
            return {}
        return pickle.loads(attr)

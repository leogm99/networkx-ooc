# from networkx.structures.out_of_core_dict import OutOfCoreDict
# from typing import MutableMapping

# class OutOfCoreNodeDict(MutableMapping):
#     def __init__(self):
#         self._node = OutOfCoreDict()
#         self._node_to_id_mapping = OutOfCoreDict()
#         self._id_to_node_mapping = OutOfCoreDict()
#         self._current_id = 0
        
#     def __setitem__(self, key, value):
#         self._node[key] = value
#         if key not in self._node_to_id_mapping:
#             self._node_to_id_mapping[key] = self._current_id
#             self._id_to_node_mapping[self._current_id] = key
#             self._current_id += 1

#     def __getitem__(self, key):
#         return self._node[key]
    
#     def __iter__(self):
#         return iter(self._node)
        
#     def __len__(self):
#         return len(self._node)

#     def __delitem__(self, key):
#         del self._node[key]
#         del self._node_to_id_mapping[key]

#     def get_mapping(self, node):
#         return self._node_to_id_mapping[node]
    
#     def get_node(self, id):
#         return self._id_to_node_mapping[id]



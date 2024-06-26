from random import choice
import sys
import networkx as nx
import time
import math
from networkx.algorithms import approximation as approx

def main(n, p):
    start_time = time.time()
    if n == 0:
        G = nx.read_edgelist('/home/grey/networkx/MemTesting/erdorRenyiTen.txt', nodetype=int)
    if n == 1:
        G = nx.read_edgelist('/home/grey/networkx/MemTesting/erdorRenyiHunderd.txt', nodetype=int)
    if n == 2:
        G = nx.read_edgelist('/home/grey/networkx/MemTesting/erdorRenyiMillon.txt', nodetype=int)
    if n == 3:
        G = nx.read_edgelist('/home/grey/networkx/MemTesting/soc-pokec-relationships.txt', nodetype=int)
    if n == 4:
        G = nx.read_edgelist('/home/grey/networkx/MemTesting/soc-LiveJournal1.txt', nodetype=int)
    if n == 5:
        G = nx.read_edgelist('/home/grey/networkx/MemTesting/1912.edges')

    graphTime = time.time()
    print("graph load done:")
    print(graphTime - start_time)
    print()

    if p == 0:
        print("no algorithm executed")
    if p == 1:
        nx.multi_source_dijkstra_path_length(G, [1])
    if p == 2:
        nx.single_source_bellman_ford(G, 1)
        # lento
    if p == 3:
        nx.degree_centrality(G)
    if p == 4:
        nx.eigenvector_centrality(G)
    if p == 5:
        nx.predecessor(G, 1)
    if p == 6:
        approx.average_clustering(G)
    if p == 7:
        approx.randomized_partitioning(G)
    if p == 8:
        nx.center(G)
        # lento
    if p == 9:
        approx.node_connectivity(G)
        # lento
    if p == 10:
        nx.single_source_dijkstra(G, 1)
    
    end_time = time.time()
    print("Algoritm done:")
    print(end_time - graphTime)
    print()
    print("Total Time:")
    print(end_time - start_time)



if __name__ == '__main__':
    main(int(sys.argv[1]), float(sys.argv[2]))
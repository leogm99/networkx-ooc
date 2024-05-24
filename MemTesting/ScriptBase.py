from random import choice
import sys
import networkx as nx
import time
import math

def main(n, p):
    # G = nx.from_edgelist(read_file_sep('/home/grey/networkx/MemTesting/gplus_combined.txt'))
    # G = nx.read_edgelist("1912.edges", delimiter=" ")
    # G = nx.read_edgelist("soc-pokec-relationships.txt", delimiter="\t")
    # G = nx.erdos_renyi_graph(10000, 2*math.log(10000)/10000)
    # nx.write_edgelist(G, "erdorRenyiTen.txt", data=False)
    # graphTime = time.time()
    # print("graph load done:")
    # print(graphTime - start_time)
    # print(G)
    # G = nx.erdos_renyi_graph(100000, 2*math.log(100000)/100000)
    # nx.write_edgelist(G, "erdorRenyiHunderd.txt", data=False)
    # graphTime = time.time()
    # print("graph load done:")
    # print(graphTime - start_time)
    # print(G)
    # G = nx.erdos_renyi_graph(1000000, 2*math.log(1000000)/1000000)
    # nx.write_edgelist(G, "erdorRenyiMillon.txt", data=False)
    # graphTime = time.time()
    # print("graph load done:")
    # print(graphTime - start_time)
    # print(G)
    # G = nx.erdos_renyi_graph(5000000, 2*math.log(5000000)/5000000)
    # nx.write_edgelist(G, "erdorRenyiFiveMillon.txt", data=False)
    # graphTime = time.time()
    # print("graph load done:")
    # print(graphTime - start_time)
    # print(G)

    start_time = time.time()
    if n == 0:
        G = nx.read_edgelist('/home/grey/networkx/MemTesting/erdorRenyiTen.txt', ' ')
    if n == 1:
        G = nx.read_edgelist('/home/grey/networkx/MemTesting/erdorRenyiHunderd.txt', ' ')
    if n == 2:
        G = nx.read_edgelist('/home/grey/networkx/MemTesting/erdorRenyiMillon.txt', ' ')
    if n == 3:
        G = nx.read_edgelist('/home/grey/networkx/MemTesting/soc-pokec-relationships.txt', '\t')
    if n == 4:
        G = nx.read_edgelist('/home/grey/networkx/MemTesting/1912.edges')
    if n == 5:
        G = nx.read_edgelist('/home/grey/networkx/MemTesting/soc-LiveJournal1.txt')

    graphTime = time.time()
    print("graph load done:")
    print(graphTime - start_time)
    print()

    if p == 0:
        print("no algorithm executed")
    if p == 1:
        nx.single_source_bellman_ford(G, [1])
    if p == 2:
        nx.multi_source_dijkstra_path_length(G, [1])
    if p == 3:
        nx.degree_centrality(G)
    if p == 4:
        nx.eigenvector_centrality(G)
    if p == 5:
        nx.voterank(G)
    if p == 6:
        print("no algorithm executed")
        # nx.percolation_centrality(G)
    if p == 7:
        nx.betweenness_centrality(G)
    if p == 8:
        nx.eccentricity(G)
    if p == 9:
        nx.barycenter(G)
    if p == 10:
        nx.center(G)
    if p == 11:
        nx.node_connectivity(G)
    if p == 12:
        nx.min_weighted_vertex_cover(G)
    if p == 13:
        nx.average_clustering(G)
    
    end_time = time.time()
    print("Algoritm done:")
    print(end_time - graphTime)
    print()
    print("Total Time:")
    print(end_time - start_time)



if __name__ == '__main__':
    # if len(sys.argv) != 3:
    #     print("Usage: python ScriptBase.py <nodes> <probability>")
    #     sys.exit(1)
        
    main(int(sys.argv[1]), float(sys.argv[2]))
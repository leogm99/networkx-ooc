from random import choice
import sys
import networkx as nx
import time
import math

def main(n, p):
    start_time = time.time()
    # G = nx.from_edgelist(read_file_sep('/home/grey/networkx/MemTesting/gplus_combined.txt'))
    # G = nx.read_edgelist("1912.edges", delimiter=" ")
    # G = nx.read_edgelist("soc-pokec-relationships.txt", delimiter="\t")
    G = nx.erdos_renyi_graph(10000, 2*math.log(10000)/10000)
    nx.write_edgelist(G, "erdorRenyiTen.txt", data=False)
    graphTime = time.time()
    print("graph load done:")
    print(graphTime - start_time)
    print(G)
    G = nx.erdos_renyi_graph(100000, 2*math.log(100000)/100000)
    nx.write_edgelist(G, "erdorRenyiHunderd.txt", data=False)
    graphTime = time.time()
    print("graph load done:")
    print(graphTime - start_time)
    print(G)
    G = nx.erdos_renyi_graph(1000000, 2*math.log(1000000)/1000000)
    nx.write_edgelist(G, "erdorRenyiMillon.txt", data=False)
    graphTime = time.time()
    print("graph load done:")
    print(graphTime - start_time)
    print(G)
    G = nx.erdos_renyi_graph(5000000, 2*math.log(5000000)/5000000)
    nx.write_edgelist(G, "erdorRenyiFiveMillon.txt", data=False)
    graphTime = time.time()
    print("graph load done:")
    print(graphTime - start_time)
    print(G)

    # G = nx.erdos_renyi_graph(n, p)
    
    # degree_centrality = nx.degree_centrality(G)
    # rank = dict(sorted(degree_centrality.items(), key=lambda item: item[1], reverse=True)[:5])
    # end_time = time.time()
    # nx.multi_source_dijkstra_path_length(G, [1])




if __name__ == '__main__':
    # if len(sys.argv) != 3:
    #     print("Usage: python ScriptBase.py <nodes> <probability>")
    #     sys.exit(1)
        
    main(int(sys.argv[1]), float(sys.argv[2]))
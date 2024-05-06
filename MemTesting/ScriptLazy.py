import sys
import networkx as nx
import time

def main(n, p):
    # TODO: change path
    start_time = time.time()
    # G = nx.LazyGraph.from_edgelist_file('/home/grey/networkx/MemTesting/1912.edges')
    # G = nx.LazyGraph.from_edgelist_file('/home/grey/networkx/MemTesting/soc-pokec-relationships.txt', '\t')
    if n == 0:
        G = nx.LazyGraph.from_edgelist_file('/home/grey/networkx/MemTesting/erdorRenyiTen.txt', ' ')
    if n == 1:
        G = nx.LazyGraph.from_edgelist_file('/home/grey/networkx/MemTesting/erdorRenyiHunderd.txt', ' ')
    if n == 2:
        G = nx.LazyGraph.from_edgelist_file('/home/grey/networkx/MemTesting/erdorRenyiMillion.txt', ' ')
    if n==3:
        G = nx.LazyGraph.from_edgelist_file('/home/grey/networkx/MemTesting/soc-pokec-relationships.txt', '\t')


    # G = nx.read_edgelist("", delimiter="\t")
    # G = nx.erdos_renyi_graph(n, p, create_using=nx.LazyGraph)
    graphTime = time.time()
    print("graph load done:")
    print(graphTime - start_time)
    print()

    # nx.multi_source_dijkstra_path_length(G, [1])
    nx.single_source_bellman_ford(G, [1])
    # print(G)

    # G = nx.read_edgelist("1912.edges", delimiter=" ")
    # nx.degree_centrality(G)
    # rank = dict(sorted(degree_centrality.items(), key=lambda item: item[1], reverse=True)[:5])
    end_time = time.time()
    print("Algoritm done:")
    print(graphTime - start_time)
    print()
    print("Total Time:")
    print(start_time - start_time)
    # print(rank)
    # print(G)



if __name__ == '__main__':
    # if len(sys.argv) != 3:
    #     print("Usage: python ScriptBase.py <nodes> <probability>")
    #     sys.exit(1)
        
    main(int(sys.argv[1]), float(sys.argv[2]))
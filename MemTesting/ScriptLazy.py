import networkx as nx
import time

def main():
    # TODO: change path
    # start_time = time.time()
    # G = nx.LazyGraph.from_edgelist_file('/home/grey/networkx/MemTesting/1912.edges')
    G = nx.OutOfCoreGraph.from_edgelist_file('/home/grey/networkx/MemTesting/soc-pokec-relationships.txt', '\t')
    # G = nx.read_edgelist("", delimiter="\t")

    # G = nx.read_edgelist("1912.edges", delimiter=" ")
    nx.degree_centrality(G)
    # rank = dict(sorted(degree_centrality.items(), key=lambda item: item[1], reverse=True)[:5])
    # end_time = time.time()
    # print(end_time - start_time)
    # print(rank)
    # print(G)



if __name__ == '__main__':
    main()
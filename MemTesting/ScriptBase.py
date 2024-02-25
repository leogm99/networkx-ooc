import networkx as nx
import time

def main():
    # TODO: change path
    def read_file_sep(path_to_edgelist, sep=None):
        with open(path_to_edgelist, "r") as edgelist:
            while True:
                line = edgelist.readline().strip('\n')
                if not line:
                    break

                yield line.split(sep) if sep != None else line.split()

    # start_time = time.time()
    # G = nx.from_edgelist(read_file_sep('/home/grey/networkx/MemTesting/gplus_combined.txt'))
    # G = nx.read_edgelist("1912.edges", delimiter=" ")
    G = nx.read_edgelist("soc-pokec-relationships.txt", delimiter="\t")
    
    # degree_centrality = nx.degree_centrality(G)
    # rank = dict(sorted(degree_centrality.items(), key=lambda item: item[1], reverse=True)[:5])
    # end_time = time.time()
    # print(end_time - start_time)
    # print(rank)
    # print(G)



if __name__ == '__main__':
    main()
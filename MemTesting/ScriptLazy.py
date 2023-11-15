import networkx as nx



def main():
    # TODO: change path
    # g = nx.LazyGraph.from_edgelist_file('/home/grey/networkx/MemTesting/gplus_combined.txt')
    g = nx.read_edgelist("1912.edges", delimiter=" ")

    print(g)


if __name__ == '__main__':
    main()
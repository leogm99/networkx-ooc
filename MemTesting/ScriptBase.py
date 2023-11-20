import networkx as nx


@profile
def main():
    # TODO: change path
    def read_file_sep(path_to_edgelist, sep=None):
        with open(path_to_edgelist, "r") as edgelist:
            while True:
                line = edgelist.readline().strip('\n')
                if not line:
                    break

                yield line.split(sep) if sep != None else line.split()

    # g = nx.from_edgelist(read_file_sep('/home/grey/networkx/MemTesting/gplus_combined.txt'))
    g = nx.read_edgelist("1912.edges", delimiter=" ")

    print(g)


if __name__ == '__main__':
    main()
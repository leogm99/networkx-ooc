NetworkX OOC Implementation
================================

NetworkX is a Python package for the creation, manipulation, and study of the structure, dynamics, and functions of complex networks.

This project is an implementation of the NetworkX library in an Out-Of-Core (OOC) way. This implementation is useful when you have a large graph that does not fit in memory.

We have implemented the LazyGraph class that is a subclass of the networkX Graph class and you can use it like a normal nx graph. This class is a graph that is stored in disk. We have also implemented the Out-Of-Core (OOC) data structures that are used by the LazyGraph class.

**DISCLAIMER**: This is NOT an official implementation of the Networkx library. This is a project developed by students of the University of Buenos Aires (UBA) as final project to get the degree of Computer Engineers and has no relationship with the original developers of networkx.

Install
--------------

To install the library, you need to follow the next steps:

1. Clone the project to your local computer:

.. code:: bash

    $ git clone git@github.com:leogm99/networkx.git

2. Next, you need to set up your build environment:

.. code:: bash

    # Create a virtualenv named ``networkx-dev`` that lives in the directory of
    # the same name
    python3 -m venv networkx-dev
    # Activate it
    source networkx-dev/bin/activate
    # Install main development and runtime dependencies of networkx
    pip install -r requirements/default.txt -r requirements/test.txt -r requirements/developer.txt -r requirements/ooc.txt
    # Build and install networkx from source
    pip install -e .

3. To run the tests, you can run the following command:

.. code:: bash

    $ pytest

Its important to note that the tests are run in a lazy mode by default. If you want to run the tests in a normal mode, you need to set the parameter `MODE=normal` in the .env file at the root of the project.

Use
-------

Once you have set de virtualenv and installed the dependencies, you can import the lazyGraph class and use it as you would use the networkX Graph class:

.. code:: python

    from networkx import LazyGraph

    G = LazyGraph()

    G.add_edge(1, 2)
    G.add_edge(2, 3)
    G.add_edge(3, 4)

    print(G.nodes)
    print(G.edges)

You can also construct a graph from a file:

.. code:: python

    from networkx import LazyGraph

    G = LazyGraph.from_edgelist_file("path/to/your/file")

    print(G.nodes)
    print(G.edges)

Then, you can use the graph as you would use a normal networkX graph.

Its important to know that the LazyGraph nodes can be **only integers**, you will get an struct.error if you try to add a node that is from another type.

Additionally, LazyGraph does not support the support the following methods:

#. remove_node
#. remove_edge
#. copy


The library works in ooc mode if you use a LazyGraph as an algorithms attribute, and in normal mode if you use an NX Graph as an algorithms attribute.

If you want to use the library in a normal networkx way, you only need to make an instance of the original NX Graph class, an then you can use the algorithm as you would use in a normal networkX graph, using this graph as attribute to algorithm:

.. code:: python

    import networkx as nx
    from networkx import LazyGraph

    G = nx.Graph()
    G.add_edge(1, 2)
    LazyG = LazyGraph()
    LazyG.add_edge(1, 2)

    nx.shortest_path(G, 1, 2) # This will run in normal mode
    nx.shortest_path(LazyG, 1, 2) # This will run in ooc mode



If you want to use the OOC Structs without a LazyGraph, you can import the following classes:

.. code:: python

    from networkx.structures.edges_dict import EdgesDict
    from networkx.structures.out_of_core_deque import OutOfCoreDeque
    from networkx.structures.out_of_core_dict_of_lists import OutOfCoreDictOfLists
    from networkx.structures.out_of_core_list import OutOfCoreList
    from networkx.structures.out_of_core_set import OutOfCoreSet
    from networkx.structures.primitive_dicts import IntDict, IntFloatDict, PrimitiveType

    oocIntDict = IntDict()
    oocIntFloatDict = IntFloatDict()
    oocList = OutOfCoreList()
    oocSet = OutOfCoreSet()
    oocDeque = OutOfCoreDeque()
    oocDictOfLists = OutOfCoreDictOfLists()
    oocEdgesDict = EdgesDict()

Implemented Algorithms
----------------------------

To see the full out of core implemented algorithms list, you can check the following file: `Implemented_algorithms.md <Implemented_algorithms.md>`_.

The rest of the algorithms can work with a LazyGraph as an attribute, if they do not use the functions not implemented for the LazyGraph, but they will not use the OOC Structs.

Common Issues
--------------

- struct.error: required argument is not an integer. This error occurs when you try to add a node that is not an integer. To solve this issue, you need to make sure that the nodes are integers.

- _plyvel.IOError: Too many open files. To solve this issue, you can increase the number of open files by running the following command:

.. code:: pycon

    >>> ulimit -n [value]

We recommend setting the value to 524288.

import networkx as nx

from networkx.classes.out_of_core_graph import OutOfCoreGraph

from dotenv import load_dotenv
import os

load_dotenv()
app_mode = os.getenv('MODE')
if (app_mode == 'ooc'):
    nx.Graph = OutOfCoreGraph

__all__ = ['app_mode']

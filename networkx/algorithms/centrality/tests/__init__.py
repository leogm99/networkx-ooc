import networkx as nx

from networkx.classes.lazygraph import LazyGraph

from dotenv import load_dotenv
import os

load_dotenv()
app_mode = os.getenv('MODE')
print(f"App mode: {app_mode}")
if (app_mode == 'lazy'):
    nx.Graph = LazyGraph

__all__ = ['app_mode']

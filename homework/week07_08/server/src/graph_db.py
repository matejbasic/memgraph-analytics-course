import os
import time

from gqlalchemy import Memgraph

from .logger import log

MEMGRAPH_HOST = os.getenv("MEMGRAPH_HOST", "memgraph-mage")
MEMGRAPH_PORT = int(os.getenv("MEMGRAPH_PORT", "7687"))


def connect() -> Memgraph:
    memgraph = Memgraph(host=MEMGRAPH_HOST, port=MEMGRAPH_PORT)
    
    is_connected = False
    while not is_connected:
        try:
            if memgraph._get_cached_connection().is_active():
                is_connected = True
        except:
            log.info("Memgraph probably isn't running.")
            time.sleep(4)
    
    return memgraph

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


def create_stream(memgraph: Memgraph, stream_name: str, topic: str, transform_procedure: str) -> None:
    try:
        log.info("Creating stream connections on Memgraph")
        memgraph.execute(f"CREATE STREAM {stream_name} TOPICS {topic} TRANSFORM {transform_procedure}")
        memgraph.execute(f"START STREAM {stream_name}")
        log.info("Stream creation succeed")
    except Exception:
        log.error("Stream creation failed or streams already exist", exc_info=True)

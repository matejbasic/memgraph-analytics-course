import time

from gqlalchemy import Memgraph

memgraph = Memgraph()


def establish_connection():
    connection_established = False
    while not connection_established:
        try:
            connection_established = memgraph._get_cached_connection().is_active()
        except:
            time.sleep(3)

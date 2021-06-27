import matplotlib.pyplot as plt
import networkx as nx

G = nx.read_edgelist("dataset/graph-assignment.txt", nodetype=int, data=(("weight", int),), create_using=nx.Graph())


def draw_graph():
    edge_labels = {
        (node_id, other_node_id): data["weight"]
        for node_id in G
        for other_node_id, data in G[node_id].items()
    }

    pos = nx.planar_layout(G)
    nx.draw(G, pos, with_labels=True, node_color="#f86e00")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.show()


def print_shortest_path(source_node=0, target_node=4):
    shortest_path = nx.shortest_path(G, source_node, target_node)
    print("Shortest path between", source_node, "and", target_node, ":", shortest_path)


def draw_tree(source_node=7, algorithm: str = "bfs"):
    if algorithm == "bfs":
        tree = nx.bfs_tree(G, source=source_node)
    elif algorithm == "dfs":
        tree = nx.dfs_tree(G, source=source_node)
    else:
        raise ValueError(f"Unknown algorithm value: '{algorithm}'")

    pos = nx.planar_layout(G)
    nx.draw(tree, pos, with_labels=True)
    plt.show()


def get_highest_ranking_node():
    page_rank = nx.pagerank(G)
    return max(page_rank, key=page_rank.get)


if __name__ == "__main__":
    print(get_highest_ranking_node())

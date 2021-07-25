import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms.community.asyn_fluid import asyn_fluidc

G = nx.read_edgelist("dataset/graph-assignment.txt", nodetype=int, data=(("weight", int),), create_using=nx.Graph())

COLORS = [
    "blue", "gray", "pink", "red", "orange", "purple", "brown", "yellow", "green", "snow", "wheat", "lime", "crimson",
    "maroon", "dodgerblue", "olive", "gold", "hotpink", "palegreen", "peachpuff", "steelblue", "royalblue", "slategray",
    "sandybrown", "lawngreen", "lightgray", "sienna", "khaki", "mistyrose"
]


def color_graph():
    color_indices = nx.greedy_color(G, strategy="smallest_last", interchange=True)
    nx.draw(G, node_color=list(color_indices.values()), with_labels=True)
    plt.show()


def detect_communities(k=3, show_plt=True):
    communities = list(asyn_fluidc(G, k))
    if show_plt:
        node_id2color = {node_id: COLORS[i] for i, community in enumerate(communities) for node_id in community}
        node_colors = [node_id2color[i] for i in sorted(node_id2color.keys())]
        nx.draw(G, node_color=node_colors)
        plt.show()

    return communities


if __name__ == "__main__":
    detect_communities()

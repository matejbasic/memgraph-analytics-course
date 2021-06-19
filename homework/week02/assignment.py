from typing import Dict, List

import matplotlib.pyplot as plt
import networkx as nx

G = nx.read_graphml("dataset/graph.graphml")


def get_node_color(node_label: str) -> str:
    if node_label == "Person":
        return "red"
    if node_label == "Store":
        return "orange"
    return "white"


def get_node_size(node_label: str) -> int:
    if node_label == "Person":
        return 3000
    if node_label == "Pos":
        return 1500
    if node_label == "Store":
        return 2000
    if node_label == "Category":
        return 3500
    return 6000


def get_positions() -> Dict[str, List[int]]:
    return {
        "1": [-1, 1],
        "2": [-0.3, 1.2],
        "6": [0.5, 1.2],
        "5": [1.3, 1.15],
        "3": [.5, 0.9],
        "4": [1.3, 0.9],
        "22": [-0.4, 0.8],
    }


def get_draw_options() -> dict:
    node_labels = nx.get_node_attributes(G, "label").values()
    node_colors = [get_node_color(label) for label in node_labels]
    node_sizes = [get_node_size(label) for label in node_labels]

    return {
        "pos": get_positions(),
        "node_color": node_colors,
        "node_size": node_sizes,
        "edgecolors": "black",
        "with_labels": False,
    }


if __name__ == "__main__":
    draw_options = get_draw_options()
    nx.draw(G, **draw_options)

    node_labels = nx.get_node_attributes(G, "label")
    nx.draw_networkx_labels(G, pos=get_positions(), labels=node_labels, font_size=8, font_family="serif")
    nx.draw_networkx_edges(
        G,
        pos=get_positions(),
        edgelist=[("1", "2")],
        node_size=draw_options["node_size"],
        arrows=True,
        arrowsize=40,
        edge_color="purple",
    )
    plt.margins(0.2)
    plt.show()

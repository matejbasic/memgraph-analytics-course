"""
Create graph with Recipe nodes connected to the Ingredient nodes (CONTAINS edge type).
Add FREQUENT_TOGETHER edge between Ingredient nodes that appear together in the same recipe
more than once.
"""

import matplotlib.pyplot as plt
import networkx as nx

from dataset import dataset

RECIPE_LABEL = "Recipe"
INGREDIENT_LABEL = "Ingredient"

CONTAINS_RELATIONSHIP = "CONTAINS"
FREQUENT_RELATIONSHIP = "FREQUENT_TOGETHER"

G = nx.MultiGraph()


def get_options():
    return {
        "font_size": 6,
        "with_labels": False,
        "node_size": 50,
        "node_color": nx.get_node_attributes(G, "color").values(),
        "edge_color":  nx.get_edge_attributes(G, "color").values(),
        "edgecolors": "black",
        "linewidths": 2,
        "width": 2,
    }


def add_ingredients_nodes(recipes):
    ingredients = list({ingredient for recipe in recipes for ingredient in recipe["ingredients"]})
    G.add_nodes_from(ingredients, label=INGREDIENT_LABEL, color="red")
    return ingredients


def add_recipe_nodes_and_edges(recipes):
    for recipe in recipes:
        G.add_node(recipe["title"], label=RECIPE_LABEL, color="blue")
        for ingredient in recipe["ingredients"]:
            G.add_edge(recipe["title"], ingredient, type=CONTAINS_RELATIONSHIP, color="black")


def add_frequent_together_edges(ingredient_nodes, debug=True):
    all_edges = []
    for i, x in enumerate(ingredient_nodes):
        for y in ingredient_nodes[i + 1:]:
            if x != y:
                neighbors_count = len(list((nx.common_neighbors(G, x, y))))
                if neighbors_count > 1:
                    if debug:
                        print(x, " AND ", y, ": ", neighbors_count)
                    all_edges.append((x, y))
    G.add_edges_from(all_edges, type=FREQUENT_RELATIONSHIP, color="green")


if __name__ == "__main__":
    recipes = dataset.load()
    ingredient_nodes = add_ingredients_nodes(recipes)
    add_recipe_nodes_and_edges(recipes)

    add_frequent_together_edges(ingredient_nodes)

    nx.draw(G, **get_options())
    plt.show()

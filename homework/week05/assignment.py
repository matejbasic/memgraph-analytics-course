import json
import os
import os.path
from typing import List, Dict, Any

import networkx as nx
import numpy as np
from gensim.models import Word2Vec
from sklearn.linear_model import LogisticRegressionCV
from sklearn.metrics import roc_auc_score
from slugify import slugify
from stellargraph import StellarGraph
from stellargraph.data import BiasedRandomWalk
from stellargraph.data import EdgeSplitter

from dataset.enrich_with_tags import TAGS

DIR_PATH: str = os.path.dirname(os.path.realpath(__file__))
DATASET_FILE_PATH: str = f"{DIR_PATH}/dataset/recipes_with_tags.json"

RECIPE_LABEL: str = "Recipe"
INGREDIENT_LABEL: str = "Ingredient"
TAG_LABEL = "Tag"

TAGGED_RELATIONSHIP: str = "TAGGED"
CONTAINS_RELATIONSHIP: str = "CONTAINS"

RecipeType = Dict[str, Any]
RecipesType = List[RecipeType]
EmbeddingsType = Dict[str, List[float]]


def text2node_name(text: str) -> str:
    return slugify(text, separator="_")


def add_tag_nodes(G: nx.MultiGraph):
    G.add_nodes_from(TAGS, label=TAG_LABEL, color="green")


def add_ingredient_nodes(G: nx.MultiGraph, recipes: RecipesType):
    ingredients = list({text2node_name(ingredient) for recipe in recipes for ingredient in recipe["ingredients"]})
    G.add_nodes_from(ingredients, label=INGREDIENT_LABEL, color="red")


def add_recipe_nodes_and_edges(G: nx.MultiGraph, recipes: RecipesType):
    for recipe in recipes:
        recipe_node_name = text2node_name(recipe["title"])
        G.add_node(recipe_node_name, label=RECIPE_LABEL, color="blue")
        for tag in recipe["tags"]:
            G.add_edge(recipe_node_name, tag, type=CONTAINS_RELATIONSHIP, color="green")

        for ingredient in recipe["ingredients"]:
            G.add_edge(recipe_node_name, ingredient, type=CONTAINS_RELATIONSHIP, color="black")


def load_graph(file_path: str) -> StellarGraph:
    with open(file_path, "r") as f:
        recipes = json.load(f)

    G = nx.MultiGraph()
    add_tag_nodes(G)
    add_ingredient_nodes(G, recipes)
    add_recipe_nodes_and_edges(G, recipes)

    return StellarGraph.from_networkx(G)


def is_float(value: str) -> bool:
    try:
        float(value)
        return True
    except ValueError:
        return False


def load_embedding(file_path: str) -> EmbeddingsType:
    embeddings = {}
    with open(file_path) as f:
        next(f)
        for line in f:
            elements = line.strip().split()
            name = " ".join([element for element in elements if not is_float(element)])
            vector = [float(element) for element in elements if is_float(element)]
            embeddings[name] = vector
    return embeddings


def calculate_embeddings(G: StellarGraph, embeddings_file_path: str) -> EmbeddingsType:
    if not os.path.isfile(embeddings_file_path):
        rw = BiasedRandomWalk(G)
        walks = rw.run(nodes=list(G.nodes()), length=32, n=10, p=0.5, q=2.0)
        print("Number of random walks: {}".format(len(walks)))

        str_walks = [[str(n) for n in walk] for walk in walks]

        model = Word2Vec(str_walks, vector_size=128, window=5, min_count=0, sg=1, workers=2, epochs=1)
        model.wv.save_word2vec_format(embeddings_file_path)

    return load_embedding(embeddings_file_path)


def split_data(G: StellarGraph):
    edge_splitter_test = EdgeSplitter(G)

    graph_test, X_test, y_test = edge_splitter_test.train_test_split(p=0.1, method="global")
    edge_splitter_train = EdgeSplitter(graph_test, G)
    _, X_train, y_train = edge_splitter_train.train_test_split(p=0.1, method="global")

    return X_train, y_train, X_test, y_test


def operator_avg(u: List[float], v: List[float]) -> float:
    u = np.array(u)
    v = np.array(v)
    return (u + v) / 2.0


def link_examples_to_features(X_train, embeddings, binary_operator):
    return [
        binary_operator(embeddings[src.strip()], embeddings[dst.strip()])
        for src, dst in X_train
    ]


def train_classifier(X_train, y_train, embeddings, binary_operator):
    clf = LogisticRegressionCV(Cs=10, cv=10, scoring="roc_auc", max_iter=3000)
    X_features = link_examples_to_features(X_train, embeddings, binary_operator)
    clf.fit(X_features, y_train)
    return clf


def evaluate_roc_auc(clf, X_features, y):
    predicted = clf.predict_proba(X_features)
    positive_column = list(clf.classes_).index(1)
    return roc_auc_score(y, predicted[:, positive_column])


def test_classifier(X_test, y_test, embeddings, binary_operator, clf):
    X_features = link_examples_to_features(X_test, embeddings, binary_operator)
    score = evaluate_roc_auc(clf, X_features, y_test)
    print(f"ROC AUC score: {score}")


def main():
    G = load_graph(DATASET_FILE_PATH)
    embeddings = calculate_embeddings(G, "embeddings.txt")
    X_train, y_train, X_test, y_test = split_data(G)
    clf = train_classifier(X_train, y_train, embeddings, operator_avg)
    test_classifier(X_test, y_test, embeddings, operator_avg, clf)


if __name__ == "__main__":
    main()

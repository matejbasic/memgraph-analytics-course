import json
import os
from enum import Enum

from flask import Flask, render_template, Response

from src.cli import args
from src.logger import log, log_time, init_log
from src import graph_db

MEMGRAPH_HOST = os.getenv('MEMGRAPH_HOST', 'memgraph-mage')
MEMGRAPH_PORT = os.getenv('MEMGRAPH_PORT', '7687')


app = Flask(__name__, template_folder=args.template_folder, static_folder=args.static_folder, static_url_path="")

memgraph = graph_db.connect()


class Properties(Enum):
    NAME = "name"


@log_time
@app.route('/graph', methods=['GET'])
def get_graph():
    log.info("Client fetching POS connected components")
    try:
        results = list(memgraph.execute_and_fetch("""MATCH (r:Recipe)-[:USING]->(i:Ingredient) RETURN r, i"""))

        nodes_set = set()
        links_set = set()
        for result in results:
            recipe_name = result["r"].properties[Properties.NAME.value]
            recipe_label = "Recipe"

            ingredient_name = result["i"].properties[Properties.NAME.value]
            ingredient_label = "Ingredient"

            nodes_set.add((recipe_name, recipe_label))
            nodes_set.add((ingredient_name, ingredient_label))

            if (recipe_name, ingredient_name) not in links_set:
                links_set.add((recipe_name, ingredient_name))

        nodes = [{"id": node_name, "label": node_label} for node_name, node_label in nodes_set]
        links = [{"source": n, "target": m} for (n, m) in links_set]

        response = {"nodes": nodes, "links": links}
        return Response(
            json.dumps(response),
            status=200,
            mimetype='application/json')

    except Exception as e:
        log.error(e)
        return "", 500


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


def main():
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        init_log()
    app.run(host=args.app_host, port=args.app_port, debug=args.debug)


if __name__ == "__main__":
    main()

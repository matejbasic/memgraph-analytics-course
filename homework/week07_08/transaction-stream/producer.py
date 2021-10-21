import json
from time import sleep
from typing import List, Dict, Any

from src.logger import init_log
from src.cli import parse_args
from src import graph_db, stream

DATASET_FILE_PATH: str = "./dataset/recipes_with_tags.json"
STREAM_NAME: str = "transaction_stream"
TOPIC_NAME: str = "recipes"


def load_data(file_path: str = DATASET_FILE_PATH) -> List[Dict[str, Any]]:
    with open(file_path, "r") as f:
        data = json.load(f)
    return data


def main():
    init_log()
    args = parse_args()
        
    stream.create_topic(STREAM_NAME, TOPIC_NAME)

    memgraph = graph_db.connect()
    graph_db.create_stream(memgraph, STREAM_NAME, TOPIC_NAME, transform_procedure="recipes.transaction")

    producer = stream.create_producer()

    for recipe in load_data():
        producer.send(TOPIC_NAME, json.dumps(recipe).encode("utf8"))
        sleep(args.interval)


if __name__ == "__main__":
    main()

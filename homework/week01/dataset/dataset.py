import json
import os

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

OUTPUT_FILE_PATH = f"{DIR_PATH}/processed_recipes.json"


def save(data, file_path=OUTPUT_FILE_PATH):
    with open(file_path, "w") as f:
        json.dump(data, f)


def load(file_path=OUTPUT_FILE_PATH):
    with open(file_path, "r") as f:
        data = json.load(f)
    return data

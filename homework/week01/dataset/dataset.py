import json

OUTPUT_FILE_PATH = "processed_recipes.json"


def save(data, file_path=OUTPUT_FILE_PATH):
    with open(file_path, "w") as f:
        json.dump(data, f)


def load(file_path=OUTPUT_FILE_PATH):
    with open(file_path, "r") as f:
        data = json.load(f)
    return data

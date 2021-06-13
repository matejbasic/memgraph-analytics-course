import pickle

OUTPUT_FILE_PATH = "processed_recipes.pickle"


def save(data, file_path=OUTPUT_FILE_PATH):
    with open(file_path, "wb") as f:
        pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)


def load(file_path=OUTPUT_FILE_PATH):
    with open(file_path, "rb") as f:
        data = pickle.load(f)
    return data

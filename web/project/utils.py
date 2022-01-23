import cloudpickle
import json


def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)

def load_pickle(path):
    with open(path, 'rb') as f:
        return cloudpickle.load(f)



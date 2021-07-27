import json
import os

import yaml
from networkx.readwrite import node_link_data, node_link_graph


def load_yaml(filename):
    with open(filename, 'r') as stream:
        file = yaml.safe_load(stream)
    return file


def get_graph(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return node_link_graph(json.load(f))

    return None


def set_graph(filename, graph):
    with open(filename, 'w+') as f:
        json.dump(node_link_data(graph), f)

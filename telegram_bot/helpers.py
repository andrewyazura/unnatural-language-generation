import json
import os

from networkx.readwrite import node_link_data, node_link_graph


def get_user_graph(user_id):
    path = f'user_graphs/{user_id}.json'

    if os.path.exists(path):
        with open(path, 'r') as f:
            return node_link_graph(json.load(f))


def update_user_graph(user_id, graph):
    path = f'user_graphs/{user_id}.json'

    with open(path, 'w+') as f:
        json.dump(node_link_data(graph), f)


def delete_user_graph(user_id):
    path = f'user_graphs/{user_id}.json'
    os.remove(path)

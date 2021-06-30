import functools
import glob
import json
import logging
import os

import yaml
from networkx.readwrite import node_link_data, node_link_graph

with open('telegram_bot/bot_config.yml', 'r') as stream:
    config = yaml.safe_load(stream)


def get_user_graph(user_id):
    path = config['user-graphs-path'].format(user_id)

    if os.path.exists(path):
        with open(path, 'r') as f:
            return node_link_graph(json.load(f))


def get_all_graphs():
    path = config['user-graphs-path'].format('*')
    for filename in glob.glob(path):
        with open(filename, 'r') as f:
            yield os.path.basename(filename).split('.')[0], node_link_graph(
                json.load(f)
            )


def update_user_graph(user_id, graph):
    path = config['user-graphs-path'].format(user_id)

    with open(path, 'w+') as f:
        json.dump(node_link_data(graph), f)


def delete_user_graph(user_id):
    path = config['user-graphs-path'].format(user_id)
    os.remove(path)


def delete_all_graphs():
    path = config['user-graphs-path'].format('*')
    for filename in glob.glob(path):
        os.remove(filename)


def restricted(func):
    @functools.wraps(func)
    def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in config['admin-ids']:
            logging.warn('Unauthorized access denied for {}.'.format(user_id))
            return
        return func(update, context, *args, **kwargs)

    return wrapped

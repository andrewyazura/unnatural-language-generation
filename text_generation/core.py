import random
import string

import networkx as nx


def join_tokens(seq):
    characters = string.punctuation
    seq = iter(seq)
    current = next(seq)

    for nxt in seq:
        if nxt in characters:
            current += nxt
        else:
            yield current
            current = nxt

    yield current


def update_graph(graph, key, value):
    if graph.has_edge(key, value):
        graph[key][value]['weight'] += 1
    else:
        graph.add_edge(key, value, weight=1)


def tokens_to_graph(tokens, order=1, graph=None):
    if graph is None:
        graph = nx.DiGraph()

    for index, token in enumerate(tokens):
        if index >= order:
            pre = ''.join(join_tokens(tokens[index - order : index]))
            update_graph(graph, pre, token)

    return graph


def random_sequence(graph, length, start_token):
    pass

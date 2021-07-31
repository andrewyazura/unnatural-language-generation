import random

import networkx as nx


def join_tokens(tokens):
    result = tokens[0]

    for token in tokens[1:]:
        if token not in '!),.:;?]}':
            result += ' '
        result += token

    return result


def update_graph(graph, key, value):
    if graph.has_edge(key, value):
        graph[key][value]['weight'] += 1
    else:
        graph.add_edge(key, value, weight=1)


def convert_tokens_to_graph(tokens, order=1, graph=None):
    if graph is None:
        graph = nx.DiGraph()

    for index, token in enumerate(tokens):
        if index >= order:
            pre = join_tokens(tokens[index - order : index])
            update_graph(graph, pre, token)

    return graph


def generate_random_sequence(graph, length, start_tokens, order=1):
    order = min(len(start_tokens), order)
    sequence = start_tokens

    for index in range(order, length - order):
        pre = join_tokens(sequence[index - order : index])
        next_tokens = graph[pre]

        if not next_tokens:
            token = '.'
            sequence += token
            continue

        weights = [next_tokens[t]['weight'] for t in next_tokens]
        token = random.choices(list(next_tokens), weights)[0]
        sequence.append(token)

    return sequence

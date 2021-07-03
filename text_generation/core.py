import string

import networkx as nx
import numpy as np
import tokenize_uk as tn


def text_to_tokens(text):
    return [
        token
        for paragraph in tn.tokenize_text(text)
        for sentence in paragraph
        for token in sentence
    ]


def tokens_to_graph(tokens, graph=None):
    if graph is None:
        graph = nx.DiGraph()

    for index, token in enumerate(tokens):
        if index + 1 == len(tokens):
            continue

        weight = graph.get_edge_data(token, tokens[index + 1], default={}).get(
            'weight', 0
        )
        graph.add_edge(token, tokens[index + 1], weight=weight + 1)

    return graph


def random_sentence(graph, start_token, length):
    sentence = start_token
    token = start_token

    for _ in range(length - 1):
        adj = graph[token]
        if not adj:
            token = '.'
            sentence += token
            continue

        weights = [adj[w]['weight'] for w in adj]
        total_weights = sum(weights)
        weights = [w / total_weights for w in weights]
        token = np.random.choice(list(adj), 1, p=weights)[0]

        if not all(i in string.punctuation for i in token):
            sentence += ' '

        sentence += token

    return sentence

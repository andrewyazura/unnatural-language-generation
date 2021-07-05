import random
import string

import networkx as nx
import numpy as np
import tokenize_uk as tn


def text_to_tokens(text):
    return [
        token
        for paragraph in tn.tokenize_text(text.lower())
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
    sentence = start_token.capitalize()
    token = start_token

    for _ in range(length - 1):
        adj = graph[token]
        if not adj:
            token = '.'
            sentence += token
            continue

        token = random.choices(list(adj), (adj[w]['weight'] for w in adj))[0]

        if sentence[-1] == '.':
            token = token.capitalize()

        if not all(i in string.punctuation for i in token):
            sentence += ' '

        sentence += token
        token = token.lower()

    return sentence

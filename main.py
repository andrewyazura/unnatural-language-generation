import random
import re

import networkx as nx
import numpy as np
import tokenize_uk

flatten = lambda t: [item for sublist in t for item in sublist]


def read_text(filename):
    with open(filename, 'r') as f:
        text = f.read().lower()

    return text


def sentences_to_graph(sentences):
    graph = nx.DiGraph()

    for sent in sentences:
        for index, word in enumerate(sent):
            if index + 1 == len(sent):
                continue

            w = graph.get_edge_data(word, sent[index + 1], default={})
            w = w.get('weight', 0)
            graph.add_edge(word, sent[index + 1], weight=w + 1)

    return graph


def random_sentence(graph, start_word, length):
    sentence = start_word
    word = start_word

    while length:
        adj = graph[word]
        weights = [adj[w]['weight'] for w in adj]
        weights = [w / sum(weights) for w in weights]
        word = np.random.choice(list(adj), 1, p=weights)[0]
        sentence += ' ' + word
        length -= 1

    return sentence


if __name__ == '__main__':
    t = read_text('text.txt')

    sentences = [
        sent
        for paragraph in tokenize_uk.tokenize_text(t)
        for sent in paragraph
    ]
    graph = sentences_to_graph(sentences)

    r = random.randint(0, len(graph.nodes))
    word = flatten(sentences)[r]

    generated_sentence = random_sentence(graph, word, 10)
    print(generated_sentence)

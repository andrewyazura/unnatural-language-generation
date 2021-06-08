import random
import re

import networkx as nx
import numpy as np


def read_text(filename, separate_punctuation=True):
    allowed = re.compile(r'[^А-ЯҐЄІЇа-яґєії.,!?’\- ]+')
    punctuation = re.compile(r'([.,!?\-]+)')

    with open(filename, 'r') as f:
        text = allowed.sub(r' ', f.read()).lower()
        if separate_punctuation:
            text = punctuation.sub(r' \1 ', text)

    return text


def text_to_graph(text):
    graph = nx.DiGraph()
    data = text.split()
    data_len = len(data)

    for index, word in enumerate(data):
        if index + 1 == data_len:
            continue

        w = graph.get_edge_data(word, data[index + 1], default={})
        w = w.get('weight', 0)
        graph.add_edge(word, data[index + 1], weight=w + 1)

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
    g = text_to_graph(t)

    r = random.randint(0, len(g.nodes))
    w = t.split()[r]

    s = random_sentence(g, w, 40)
    print(s)

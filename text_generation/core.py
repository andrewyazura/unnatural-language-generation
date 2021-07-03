import string

import networkx as nx
import numpy as np
import tokenize_uk as tn


def text_to_sentences(text):
    return [sent for paragraph in tn.tokenize_text(text) for sent in paragraph]


def sentences_to_graph(sentences, graph=None):
    if graph is None:
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

    for _ in range(length - 1):
        adj = graph[word]
        if not adj:
            break

        weights = [adj[w]['weight'] for w in adj]
        total_weights = sum(weights)
        weights = [w / total_weights for w in weights]
        word = np.random.choice(list(adj), 1, p=weights)[0]

        if not all(i in string.punctuation for i in word):
            sentence += ' '

        sentence += word

    return sentence

import networkx as nx
import numpy as np
import tokenize_uk

flatten = lambda t: [item for sublist in t for item in sublist]


def read_text(filename):
    with open(filename, 'r') as f:
        text = f.read().lower()

    return text


def text_to_sentences(text):
    return [
        sent
        for paragraph in tokenize_uk.tokenize_text(text)
        for sent in paragraph
    ]


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

    while length:
        adj = graph[word]
        if not adj:
            break

        weights = [adj[w]['weight'] for w in adj]
        total_weights = sum(weights)
        weights = [w / total_weights for w in weights]
        word = np.random.choice(list(adj), 1, p=weights)[0]

        sentence += ' ' + word
        length -= 1

    return sentence


if __name__ == '__main__':
    t = read_text('text.txt')
    sentences = text_to_sentences(t)

    graph = sentences_to_graph(sentences)
    word = np.random.choice(graph.nodes)

    generated_sentence = random_sentence(graph, word, 40)
    print(generated_sentence)

import numpy as np

from text_generation import (
    random_sentence,
    sentences_to_graph,
    text_to_sentences,
)

with open('text.txt', 'r') as f:
    t = f.read().lower()

sentences = text_to_sentences(t)

graph = sentences_to_graph(sentences)
word = np.random.choice(graph.nodes)

generated_sentence = random_sentence(graph, word, 40)
print(generated_sentence)

import numpy as np

from text_generation import (
    random_sentence,
    read_text,
    sentences_to_graph,
    text_to_sentences,
)

t = read_text('text.txt')
sentences = text_to_sentences(t)

graph = sentences_to_graph(sentences)
word = np.random.choice(graph.nodes)

generated_sentence = random_sentence(graph, word, 40)
print(generated_sentence)

import numpy as np

from text_generation import (
    random_sentence,
    tokens_to_graph,
    text_to_tokens,
)

with open('tmp/text.txt', 'r') as f:
    t = f.read()

tokens = text_to_tokens(t)
graph = tokens_to_graph(tokens)
word = np.random.choice(graph.nodes)

generated_sentence = random_sentence(graph, word, 40)
print(generated_sentence)

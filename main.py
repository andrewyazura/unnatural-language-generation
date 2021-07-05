import random

import tokenize_uk as tn

from text_generation import join_tokens, random_sequence, tokens_to_graph

with open('tmp/text.txt', 'r') as f:
    t = f.read().lower()

tokens = tn.tokenize_words(t)
graph = tokens_to_graph(tokens, 3)
start = random.choice(
    [n.split() for n in graph.nodes if graph[n] and len(n.split()) == 3]
)
sequence = random_sequence(graph, 200, start, 3)
output = join_tokens(sequence)
print(output)

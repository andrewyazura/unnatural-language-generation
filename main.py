import random

import tokenize_uk as tn

from text_generation import (
    join_tokens,
    generate_random_sequence,
    convert_tokens_to_graph,
)

with open('tmp/text.txt', 'r') as f:
    t = f.read().lower()

order = 3

tokens = tn.tokenize_words(t)
graph = convert_tokens_to_graph(tokens, order)
start = random.choice(
    [n.split() for n in graph.nodes if graph[n] and len(n.split()) == order]
)
sequence = generate_random_sequence(graph, 200, start, order)
output = join_tokens(sequence)
print(output)

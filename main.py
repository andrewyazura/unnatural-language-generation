import glob
import json
import random

import tokenize_uk as tn
from networkx.readwrite import node_link_data

from text_generation import (
    convert_tokens_to_graph,
    generate_random_sequence,
    join_tokens,
)

graph = None
order = 2

for path in glob.glob('tmp/texts/*'):
    with open(path, 'r') as f:
        t = f.read().lower()
        tokens = tn.tokenize_words(t)
        graph = convert_tokens_to_graph(tokens, order, graph)

with open('tmp/generator.json', 'w+') as f:
    json.dump(node_link_data(graph), f)

start = random.choice(
    [n.split() for n in graph.nodes if graph[n] and len(n.split()) == order]
)
sequence = generate_random_sequence(graph, 200, start, order)
output = join_tokens(sequence)
print(output)

import random
from string import punctuation

import networkx as nx


def join_punctuation(seq):
    characters = set(punctuation)
    seq = iter(seq)
    current = next(seq)

    for nxt in seq:
        if nxt in characters:
            current += nxt
        else:
            yield current
            current = nxt

    yield current


def get_random_node(graph: nx.DiGraph, order: int) -> str:
    return random.choice([n for n in graph.nodes if len(n.split()) == order])

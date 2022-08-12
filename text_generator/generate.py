import random

import networkx as nx

from text_generator.helpers import get_random_node


def generate_sequence(graph: nx.DiGraph, words: int, order: int) -> str:
    start = get_random_node(graph, order)
    sequence = [*start.split()]

    for i in range(order, words):
        start = " ".join(sequence[i - order : i])
        edges = graph.edges(start, "count", 1)

        if not edges:
            break

        neighbors = [edge[1] for edge in edges]
        weights = [edge[2] for edge in edges]

        sequence.append(random.choices(neighbors, weights)[0])

    return sequence

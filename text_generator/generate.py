import networkx as nx
import random


def generate_text(graph: nx.DiGraph, words: int, order: int = 3) -> str:
    start = random.choice([n for n in graph.nodes if len(n.split()) == order])
    sequence = [*start.split()]

    for i in range(order, words - order):
        start = " ".join(sequence[i - order : i])
        edges = graph.edges(start, "count", 1)

        if not edges:
            break

        neighbors = [edge[1] for edge in edges]
        weights = [edge[2] for edge in edges]

        sequence.append(random.choices(neighbors, weights)[0])

    return " ".join(sequence)

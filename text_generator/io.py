import json

import networkx as nx


def load_graph(path: str) -> nx.DiGraph:
    with open(path, "r") as file:
        return nx.readwrite.adjacency_graph(
            json.load(file), directed=True, multigraph=False
        )


def dump_graph(graph: nx.DiGraph, path: str) -> None:
    with open(path, "w+") as file:
        json.dump(nx.readwrite.adjacency_data(graph), file)

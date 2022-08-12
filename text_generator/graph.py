from typing import Iterable

import networkx as nx


def graph_from_iterable(
    iterable: Iterable[str], order: int, graph: nx.DiGraph = None
) -> nx.DiGraph:
    graph = graph or nx.DiGraph()

    backlog = []

    for token in iterable:
        if len(backlog) == order:
            edge = (" ".join(backlog), token)
            backlog.pop(0)

            count = graph.get_edge_data(*edge, {}).get("count", 0)
            graph.add_edge(*edge, count=count + 1)

        backlog.append(token)

    return graph

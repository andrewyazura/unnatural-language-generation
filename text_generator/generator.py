import json
import random
from string import punctuation

import networkx as nx
import tokenize_uk as tn
from networkx.readwrite import node_link_data, node_link_graph


class EmptyGeneratorException(Exception):
    """Raised when the generator is empty"""


class Generator:
    def __init__(self, order: int, graph: nx.DiGraph = None) -> None:
        if graph is None:
            graph = nx.DiGraph()

        self.graph = graph
        self.order = order

    def generate(self, length: int) -> str:
        if self.is_empty:
            raise EmptyGeneratorException()

        sequence = random.choice(
            [
                n.split()
                for n in self.graph.nodes
                if self.graph[n] and len(n.split()) == self.order
            ]
        )

        for index in range(self.order, length - self.order):
            pre = self._join_tokens(sequence[index - self.order : index])
            next_tokens = self.graph[pre]

            if not next_tokens:
                token = "."
                sequence.append(token)
                continue

            weights = [next_tokens[t]["weight"] for t in next_tokens]
            token = random.choices(list(next_tokens), weights)[0]
            sequence.append(token)

        return self._join_tokens(sequence)

    def process_text(self, text: str) -> None:
        tokens = tn.tokenize_words(text.lower())
        for index, token in enumerate(tokens):
            if index >= self.order:
                pre = self._join_tokens(tokens[index - self.order : index])
                self._update_edge(pre, token)

    def _update_edge(self, key: str, value: str) -> None:
        if self.graph.has_edge(key, value):
            self.graph[key][value]["weight"] += 1
        else:
            self.graph.add_edge(key, value, weight=1)

    def graph_info(self) -> dict:
        return dict(
            nodes=self.graph.number_of_nodes(),
            edges=self.graph.number_of_edges(),
            weight=int(self.graph.size("weight")),
        )

    def _join_tokens(self, tokens: list[str]) -> None:
        result = tokens[0]

        for token in tokens[1:]:
            if token not in punctuation:
                result += " "
            result += token

        return result

    @property
    def is_empty(self) -> bool:
        return not self.graph or not self.graph.nodes

    @classmethod
    def load_from_json(cls, path: str, *args, **kwargs):
        with open(path, "r") as f:
            return cls(graph=node_link_graph(json.load(f)), *args, **kwargs)

    def dump_to_json(self, path: str) -> None:
        with open(path, "w+") as f:
            json.dump(node_link_data(self.graph), f)

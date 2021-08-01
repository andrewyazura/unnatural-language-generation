import json
import os
import random

import tokenize_uk as tn
from networkx.readwrite import node_link_data, node_link_graph
from text_generation import (
    convert_tokens_to_graph,
    generate_random_sequence,
    join_tokens,
)


class Generator:
    def __init__(self, path, order):
        self.path = path
        self.order = order
        self.load_graph()

    def generate(self, length):
        start = random.choice(
            [
                n.split()
                for n in self.graph.nodes
                if self.graph[n] and len(n.split()) == self.order
            ]
        )
        sequence = generate_random_sequence(
            self.graph, length, start, self.order
        )
        return join_tokens(sequence)

    def load_graph(self):
        if os.path.exists(self.path):
            with open(self.path, 'r') as f:
                self.graph = node_link_graph(json.load(f))
        else:
            self.graph = None

    def dump_graph(self):
        with open(self.path, 'w+') as f:
            json.dump(node_link_data(self.graph), f)

    def delete_graph(self):
        os.remove(self.path)
        self.load_graph()

    def process_text(self, text):
        self.graph = convert_tokens_to_graph(
            tn.tokenize_words(text.lower()), self.order, self.graph
        )
        self.dump_graph()

    def graph_info(self):
        return {
            'nodes': self.graph.number_of_nodes(),
            'edges': self.graph.number_of_edges(),
            'weight': int(self.graph.size('weight')),
            'order': self.order,
        }

    def is_empty(self):
        return not self.graph or not self.graph.nodes

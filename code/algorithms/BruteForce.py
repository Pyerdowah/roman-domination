from itertools import product
import networkx as nx
from .Algorithm import AlgorithmBase

class BruteForce(AlgorithmBase):
    def is_valid_roman_dominating_set(self, graph, node_values):
        for node in graph.nodes:
            if node_values[node] == 0:
                if not any(node_values[neighbor] >= 2 for neighbor in graph.neighbors(node)):
                    return False

        induced_set = set(node for node in graph.nodes if node_values[node] in {1, 2, 3})

        for node in list(induced_set):
            induced_set.update(graph.neighbors(node))

        induced_graph = nx.Graph()
        for node in induced_set:
            if node_values[node] in {1, 2, 3}:
                for neighbor in graph.neighbors(node):
                    if neighbor in induced_set:
                        induced_graph.add_edge(node, neighbor)

        if not nx.is_connected(induced_graph):
            return False

        return True

    def execute(self, graph):
        nodes = list(graph.nodes)
        min_roman_number = float('inf')
        best_node_values = None

        for values in product([0, 1, 2], repeat=len(nodes)):
            node_values = dict(zip(nodes, values))

            if self.is_valid_roman_dominating_set(graph, node_values):
                roman_number = sum(node_values.values())
                if roman_number < min_roman_number:
                    min_roman_number = roman_number
                    best_node_values = node_values.copy()

        return min_roman_number, best_node_values

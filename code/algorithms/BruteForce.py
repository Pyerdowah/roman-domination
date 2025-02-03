from itertools import product

from .Algorithm import AlgorithmBase


class BruteForce(AlgorithmBase):
    def is_valid_roman_dominating_set(self, graph, node_values):
        for node in graph.nodes:
            if node_values[node] == 0:
                if not any(node_values[neighbor] == 2 for neighbor in graph.neighbors(node)):
                    return False

        if sum(1 for node in graph.nodes if node_values[node] in {1, 2}) == 1:
            return True

        for node in graph.nodes:
            if node_values[node] in {1, 2}:
                found_valid_neighbor = False

                for neighbor in graph.neighbors(node):
                    if node_values[neighbor] in {1, 2}:
                        found_valid_neighbor = True
                        break

                    if node_values[neighbor] == 0:
                        for second_neighbor in graph.neighbors(neighbor):
                            if second_neighbor != node and node_values[second_neighbor] in {1, 2}:
                                found_valid_neighbor = True
                                break

                if found_valid_neighbor:
                    continue

                if not found_valid_neighbor:
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
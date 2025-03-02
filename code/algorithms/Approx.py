import networkx as nx
import math
from .Algorithm import AlgorithmBase


class Approx(AlgorithmBase):
    def compute_dominating_set(self, graph):
        """ Przybliżony algorytm wyznaczania zbioru dominującego """
        dominating_set = set()
        uncovered_nodes = set(graph.nodes)

        while uncovered_nodes:
            # Wybierz wierzchołek o największym stopniu wśród niepokrytych
            max_degree_node = max(uncovered_nodes, key=lambda v: graph.degree[v])
            dominating_set.add(max_degree_node)

            # Pokryj ten wierzchołek i jego sąsiadów
            uncovered_nodes.remove(max_degree_node)
            uncovered_nodes -= set(graph.neighbors(max_degree_node))

        return dominating_set

    def execute(self, graph):
        nodes = list(graph.nodes)
        min_roman_number = float('inf')
        best_node_values = None

        # Oblicz zbiór dominujący D
        dominating_set = self.compute_dominating_set(graph)

        # Skonstruuj RDF: przypisz 2 dla D, 0 dla pozostałych
        node_values = {node: 2 if node in dominating_set else 0 for node in nodes}

        # Oblicz wagę Roman Dominating Function
        roman_number = sum(node_values.values())

        # Aktualizuj najlepsze rozwiązanie
        if roman_number < min_roman_number:
            min_roman_number = roman_number
            best_node_values = node_values.copy()

        return min_roman_number, best_node_values

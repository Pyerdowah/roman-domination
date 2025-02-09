import random
import networkx as nx
from .Algorithm import AlgorithmBase

class AntColony(AlgorithmBase):
    def __init__(self, num_ants=100, num_iterations=500, evaporation_rate=0.5, pheromone_init=1.0, alpha=2, beta=10):
        self.num_ants = num_ants  # Liczba mrówek
        self.num_iterations = num_iterations  # Liczba iteracji
        self.evaporation_rate = evaporation_rate  # Współczynnik parowania feromonów
        self.pheromone_init = pheromone_init  # Początkowa wartość feromonów
        self.alpha = alpha  # Wpływ feromonów na decyzję
        self.beta = beta  # Wpływ heurystyki lokalnej

    def initialize_pheromones(self, graph):
        """ Inicjalizuj feromony na wszystkich krawędziach. """
        pheromones = {edge: self.pheromone_init for edge in graph.edges}
        return pheromones

    def heuristic_value(self, neighbors):
        """ Funkcja heurystyczna: preferujemy wierzchołki o dużym stopniu. """
        return len(neighbors)

    def choose_node_value(self, node, pheromones, neighbors):
        """ Losowy wybór wartości (0, 1, 2) dla wierzchołka na podstawie feromonów i heurystyki. """
        values = [0, 1, 2]
        probabilities = []

        for value in values:
            pheromone_level = sum(pheromones.get((min(node, neighbor), max(node, neighbor)), 1) for neighbor in neighbors)
            heuristic = self.heuristic_value(neighbors)
            probability = (pheromone_level ** self.alpha) * (heuristic ** self.beta)
            probabilities.append(probability)

        total = sum(probabilities)
        if total == 0:
            return random.choice(values)

        return random.choices(values, weights=probabilities, k=1)[0]

    def build_solution(self, graph, pheromones):
        """ Budowanie rozwiązania przez mrówkę. """
        node_values = {}
        for node in graph.nodes:
            neighbors = list(graph.neighbors(node))
            node_values[node] = self.choose_node_value(node, pheromones, neighbors)
        return node_values

    def is_valid_roman_dominating_set(self, graph, node_values):
        for node in graph.nodes:
            if node_values[node] == 0:
                if not any(node_values[neighbor] == 2 for neighbor in graph.neighbors(node)):
                    return False

        induced_set = set(node for node in graph.nodes if node_values[node] in {1, 2})

        for node in list(induced_set):
            induced_set.update(graph.neighbors(node))

        induced_graph = nx.Graph()
        for node in induced_set:
            if node_values[node] in {1, 2}:
                for neighbor in graph.neighbors(node):
                    if neighbor in induced_set:
                        induced_graph.add_edge(node, neighbor)

        if not nx.is_connected(induced_graph):
            return False

        return True

    def evaluate_solution(self, graph, node_values):
        """ Ocena rozwiązania - minimalizacja rzymskiej liczby dominowania. """
        if not self.is_valid_roman_dominating_set(graph, node_values):
            return float('inf')

        return sum(node_values[node] for node in graph.nodes)

    def update_pheromones(self, graph, pheromones, solutions):
        """ Aktualizacja feromonów na podstawie najlepszych rozwiązań. """
        for edge in pheromones:
            pheromones[edge] *= (1 - self.evaporation_rate)

        best_solution = min(solutions, key=lambda sol: sol[1])
        for node in best_solution[0]:
            for neighbor in graph.neighbors(node):
                edge = (min(node, neighbor), max(node, neighbor))
                pheromones[edge] += 1 / best_solution[1]

    def execute(self, graph):
        pheromones = self.initialize_pheromones(graph)
        best_solution = None
        best_roman_number = float('inf')

        for _ in range(self.num_iterations):
            solutions = []

            for _ in range(self.num_ants):
                solution = self.build_solution(graph, pheromones)
                roman_number = self.evaluate_solution(graph, solution)
                solutions.append((solution, roman_number))

                if roman_number < best_roman_number:
                    best_roman_number = roman_number
                    best_solution = solution

            self.update_pheromones(graph, pheromones, solutions)

        return best_roman_number, best_solution

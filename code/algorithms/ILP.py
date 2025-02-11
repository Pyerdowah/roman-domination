import networkx as nx
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpInteger, LpBinary, value
from .Algorithm import AlgorithmBase

class ILP(AlgorithmBase):
    def execute(self, graph):
        # Tworzenie problemu programowania liniowego
        problem = LpProblem("RomanWeaklyDominatingSet", LpMinimize)

        # Zmienne decyzyjne: x_i ∈ {0, 1, 2} dla każdego wierzchołka i
        node_vars = {node: LpVariable(f"x_{node}", 0, 2, LpInteger) for node in graph.nodes}

        # Pomocnicze zmienne binarne do wymuszania logicznych ograniczeń
        is_two = {node: LpVariable(f"is_two_{node}", 0, 1, LpBinary) for node in graph.nodes}
        is_one = {node: LpVariable(f"is_one_{node}", 0, 1, LpBinary) for node in graph.nodes}

        # Zmienna binarna do sprawdzania osiągalności między wierzchołkami
        reachable = {node: LpVariable(f"reachable_{node}", 0, 1, LpBinary) for node in graph.nodes}

        # Funkcja celu: minimalizacja wartości rzymskich z wyważonymi karami
        problem += lpSum(2 * is_two[node] + is_one[node] for node in graph.nodes), "Minimize_Roman_Dominating_Number"

        # Ograniczenie pomocnicze: zdefiniowanie wartości 1 i 2
        for node in graph.nodes:
            problem += node_vars[node] == 2 * is_two[node] + is_one[node], f"DefineX_{node}"

        # Ograniczenie ochrony: każdy wierzchołek 0 musi mieć sąsiada z wartością 2
        for node in graph.nodes:
            neighbors = list(graph.neighbors(node))
            if neighbors:
                problem += lpSum(is_two[neighbor] for neighbor in neighbors) >= 1 - node_vars[node], f"Protection_{node}"

        # Ograniczenie osiągalności: wierzchołki z wartościami 1 i 2 muszą być wzajemnie osiągalne
        for node in graph.nodes:
            if graph.degree[node] > 0:  # Sprawdzamy tylko wierzchołki o stopniu > 0
                neighbors = list(graph.neighbors(node))
                # Wymuszenie, że jeśli node jest dominujące, musi być połączone z innym dominującym
                problem += reachable[node] <= lpSum(is_one[neighbor] + is_two[neighbor] for neighbor in neighbors), f"Reachability_{node}"

        # Wymuszenie spójności całego zbioru dominującego
        problem += lpSum(reachable[node] for node in graph.nodes) == lpSum(is_one[node] + is_two[node] for node in graph.nodes), "Connectivity"

        # Rozwiązywanie problemu
        problem.solve()

        # Pobranie wyników przypisania wartości wierzchołkom
        result_values = {node: int(value(node_vars[node])) for node in graph.nodes}

        # Obliczenie minimalnej wartości dominacji rzymskiej
        min_roman_number = sum(result_values.values())

        return min_roman_number, result_values
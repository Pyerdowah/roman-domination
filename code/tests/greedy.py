from itertools import product

import matplotlib.pyplot as plt
import networkx as nx


def is_valid_roman_dominating_set(graph, node_values):
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
                break

            if not found_valid_neighbor:
                return False

    return True


def find_minimal_roman_dominating_set(graph):
    nodes = list(graph.nodes)
    min_roman_number = float('inf')
    best_node_values = None

    # Iterujemy po wszystkich możliwych przypisaniach wartości (0, 1, 2) dla wierzchołków
    for values in product([0, 1, 2], repeat=len(nodes)):
        node_values = dict(zip(nodes, values))

        # Sprawdzanie warunków dominacji rzymskiej
        if is_valid_roman_dominating_set(graph, node_values):
            roman_number = sum(node_values.values())  # Oblicz rzymską wartość zbioru
            if roman_number < min_roman_number:
                min_roman_number = roman_number
                best_node_values = node_values.copy()

    return min_roman_number, best_node_values


def create_graph_from_edges(nodes, edges):
    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    return G


# Tworzenie grafu na podstawie danych wejściowych
# nodes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
# edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (7, 9)]

nodes = [0, 1, 2, 3, 4, 5, 6, 7]
edges = [(0, 1), (0, 4), (0, 5), (0, 7), (1, 3), (1, 5), (1, 7), (2, 3), (2, 4), (2, 6), (2, 7), (3, 4), (3, 5), (3, 7), (4, 6), (4, 7), (5, 6), (5, 7), (6, 7)]

# Tworzenie grafu z danych wejściowych
# G = create_graph_from_edges(nodes, edges)
G = nx.erdos_renyi_graph(8, 0.4)

# Znajdowanie optymalnego zbioru dominującego rzymskiego
min_roman_number, best_node_values = None, None

if nx.is_connected(G):
    min_roman_number, best_node_values = find_minimal_roman_dominating_set(G)

if best_node_values is not None:
    # Przygotowanie kolorów wierzchołków na podstawie ich wartości
    node_colors = ['red' if best_node_values[node] == 2 else
                   'blue' if best_node_values[node] == 1 else 'yellow'
                   for node in G.nodes]

    # Rysowanie grafu
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=800)
    plt.title(f"Minimalny rzymski słabospójny zbiór dominujący (roman_number: {min_roman_number})")
    plt.show()

    # Wypisanie wszystkich krawędzi grafu
    print("\nKrawędzie w grafie:")
    for edge in G.edges:
        u, v = edge
        print(f"({u}, {v}),")

    # Wypisanie krawędzi łączących wierzchołki dominujące (wartość 1 lub 2)
    print("\nKrawędzie łączące wierzchołki dominujące (wartość 1 lub 2):")
    for u, v in G.edges:
        if best_node_values[u] in {1, 2} and best_node_values[v] in {1, 2}:
            print(f"{u} -- {v} (wartości: {best_node_values[u]} - {best_node_values[v]})")

    print(f"\nMinimalna liczba dominowania rzymskiego słabospójnego: {min_roman_number}")
    print("Przypisane wartości wierzchołków:", best_node_values)
else:
    print("Nie znaleziono zbioru dominującego rzymskiego.")

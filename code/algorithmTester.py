import networkx as nx

import graphPlotter
import timeMeasurer
from algorithms.BruteForce import BruteForce
from algorithms.TreeLinear import TreeLinear
from algorithms.AntColony import AntColony


def create_custom_graph():
    # nodes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    # edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (7, 9)]

    # nodes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    # edges = [(0, 1), (0, 8), (0, 10), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (5, 7), (8, 9), (10, 11), (10, 12)]

    nodes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12]
    edges = [(0, 1),(0, 7),(1, 2),(1, 3),(1, 4),(4, 5),(4, 6),(7, 8),(8, 9),(9, 10),(10, 11),(10, 12)]

    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    return G


def create_random_tree():
    tree = nx.random_unlabeled_rooted_tree(13)
    root = 0
    rooted_tree = nx.dfs_tree(tree, source=root)

    mapping = {old_label: new_label for new_label, old_label in enumerate(sorted(rooted_tree.nodes))}
    sorted_tree = nx.relabel_nodes(rooted_tree, mapping)

    return sorted_tree.to_undirected()


def main():
    G = create_random_tree()

    print("\nKrawędzie w grafie:")
    for edge in G.edges:
        u, v = edge
        print(f"({u}, {v}),")

    if not nx.is_connected(G):
        print("Graf nie jest spójny, nie można uruchomić algorytmu.")
        return

    algorithms = [
        BruteForce(),
        TreeLinear(),
        AntColony()
    ]

    results = []

    for algorithm in algorithms:
        (min_roman_number, best_node_values), execution_time = timeMeasurer.measure_execution_time(algorithm, G)
        # graphPlotter.plot_graph(G, best_node_values, min_roman_number)

        algorithm_name = algorithm.__class__.__name__
        print(f"\n{algorithm_name}:")
        print(f"Minimalna liczba dominowania rzymskiego słabospójnego: {min_roman_number}")
        print(f"Czas wykonania algorytmu: {execution_time:.6f} nanosekund")
        print("Przypisane wartości wierzchołków:", best_node_values)

        results.append((algorithm_name, best_node_values, min_roman_number))

    graphPlotter.plot_graphs(G, results)


if __name__ == "__main__":
    main()

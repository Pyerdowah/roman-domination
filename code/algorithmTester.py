import networkx as nx
from tensorboard.summary.v1 import custom_scalar

import graphPlotter
import timeMeasurer
from algorithms.AntColony import AntColony
from algorithms.BruteForce import BruteForce
from algorithms.ILP import ILP
from algorithms.TreeLinear import TreeLinear
from algorithms.ILP2 import ILP2
from algorithms.Approx import Approx


def create_custom_graph():
    # nodes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    # edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (7, 9)]

    # nodes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    # edges = [(0, 1), (0, 8), (0, 10), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (5, 7), (8, 9), (10, 11), (10, 12)]

    # nodes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12]
    # edges = [(0, 1),(0, 7),(1, 2),(1, 3),(1, 4),(4, 5),(4, 6),(7, 8),(8, 9),(9, 10),(10, 11),(10, 12)]

    # nodes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
    #          29, 30]
    # edges = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6), (3, 7), (3, 8), (4, 9), (4, 10), (5, 11), (5, 12), (6, 13),
    #          (6, 14), (7, 15), (7, 16), (8, 17), (8, 18), (9, 19), (9, 20), (10, 21), (10, 22), (11, 23), (11, 24),
    #          (12, 25), (12, 26), (13, 27), (13, 28), (14, 29), (14, 30)]

    nodes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    # edges = [(0, 1), (1, 2), (1, 3), (3, 4), (3, 6), (3, 7), (3, 8), (4, 5), (8, 9)]

    edges = [(0, 1), (0, 2), (0, 4), (2, 3), (4, 5), (4, 9), (5, 6), (6, 7), (7, 8)]

    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    return G


def create_random_tree():
    tree = nx.random_unlabeled_rooted_tree(12)
    root = 0
    rooted_tree = nx.dfs_tree(tree, source=root)

    mapping = {old_label: new_label for new_label, old_label in enumerate(sorted(rooted_tree.nodes))}
    sorted_tree = nx.relabel_nodes(rooted_tree, mapping)

    return sorted_tree.to_undirected()


def main():
    # G = nx.grid_2d_graph(4,10)
    # G = nx.convert_node_labels_to_integers(G)
    G = create_custom_graph()
    # G = nx.erdos_renyi_graph(12,0.4)

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
        AntColony(),
        ILP(),
        ILP2(),
        Approx()
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

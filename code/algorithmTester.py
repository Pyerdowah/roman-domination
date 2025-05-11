import os
import time
from itertools import product

import networkx as nx
from matplotlib import pyplot as plt
from pulp import LpProblem, LpVariable, lpSum, LpMinimize, PULP_CBC_CMD, value
from torch.cuda import graph

import graphPlotter
import timeMeasurer
from algorithms.Approx import Approx
from algorithms.ILP import ILP
from algorithms.ILP2 import ILP2
from algorithms.TreeLinear import TreeLinear
from algorithms.BruteForce import BruteForce

from algorithms.AntColony import AntColony
from algorithms.Greedy import Greedy


def create_custom_graph():
    # nodes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    # edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (7, 9)]

    # nodes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    # edges = [(0, 1), (0, 8), (0, 10), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (5, 7), (8, 9), (10, 11), (10, 12)]

    nodes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    edges = [(0, 1), (0, 7), (1, 2), (1, 3), (1, 4), (4, 5), (4, 6), (7, 8), (8, 9), (9, 10), (10, 11), (10, 12)]

    # nodes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
    #          29, 30]
    # edges = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6), (3, 7), (3, 8), (4, 9), (4, 10), (5, 11), (5, 12), (6, 13),
    #          (6, 14), (7, 15), (7, 16), (8, 17), (8, 18), (9, 19), (9, 20), (10, 21), (10, 22), (11, 23), (11, 24),
    #          (12, 25), (12, 26), (13, 27), (13, 28), (14, 29), (14, 30)]

    # nodes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    # edges = [(0, 1), (1, 2), (1, 3), (3, 4), (3, 6), (3, 7), (3, 8), (4, 5), (8, 9)]

    # edges = [(0, 1), (0, 2), (0, 4), (2, 3), (4, 5), (4, 9), (5, 6), (6, 7), (7, 8)]
    # nodes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    # edges = [(0, 1),
    #          (0, 5),
    #          (0, 9),
    #          (1, 2),
    #          (1, 3),
    #          (3, 4),
    #          (5, 6),
    #          (5, 7),
    #          (7, 8),
    #          (9, 10),
    #          (9, 11)]

    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    return G


def create_random_tree(n):
    tree = nx.random_unlabeled_rooted_tree(n)
    root = 0
    rooted_tree = nx.dfs_tree(tree, source=root)

    mapping = {old_label: new_label for new_label, old_label in enumerate(sorted(rooted_tree.nodes))}
    sorted_tree = nx.relabel_nodes(rooted_tree, mapping)

    return sorted_tree.to_undirected()

def generate_test_graphs_by_size(sizes=[10, 20, 30, 40], instances_per_size=3, seed_base=42, save_folder="saved_graphs"):
    graphs = []
    os.makedirs(save_folder, exist_ok=True)

    for n in sizes:
        for i in range(instances_per_size):
            seed = seed_base + i + n

            def save_and_store(graph, name):
                # path = os.path.join(save_folder, f"{name}.graphml")
                # nx.write_graphml(graph, path)
                graphs.append((name, graph))

            G1 = nx.erdos_renyi_graph(n=n, p=0.3, seed=seed)
            save_and_store(G1, f"ErdosRenyi_sparse_n{n}_i{i}")

            G2 = nx.erdos_renyi_graph(n=n, p=0.7, seed=seed)
            save_and_store(G2, f"ErdosRenyi_dense_n{n}_i{i}")

            T = create_random_tree(n)
            save_and_store(T, f"RandomTree_n{n}_i{i}")

            m = min(5, n // 2)
            SF = nx.barabasi_albert_graph(n=n, m=m, seed=seed)
            save_and_store(SF, f"ScaleFree_n{n}_i{i}")

            side = int(n ** 0.5)
            if side * side == n:
                Ggrid = nx.grid_2d_graph(side, side)
                Ggrid = nx.convert_node_labels_to_integers(Ggrid)
                save_and_store(Ggrid, f"Grid_{side}x{side}_i{i}")

    return graphs


def load_saved_graphs(folder="saved_graphs"):
    graphs = []
    for filename in os.listdir(folder):
        if filename.endswith(".graphml"):
            path = os.path.join(folder, filename)
            G = nx.read_graphml(path)
            G = nx.relabel_nodes(G, lambda x: int(x))
            graphs.append((filename.replace(".graphml", ""), G))

    graphs.sort(key=lambda item: (item[1].number_of_nodes(), item[1].number_of_edges()))
    return graphs



import csv
from statistics import mean

def test_algorithms_on_graph(G, graph_name, n_repeats=5, csv_file="results.csv"):
    if not nx.is_connected(G):
        print(f"Graf {graph_name} nie jest spójny – pomijam.")
        return []

    algorithms = [
        # BruteForce(),
        # TreeLinear(),
        # AntColony(),
        # ILP(),
        # ILP2(),
        Approx(),
        # Greedy()
    ]

    results = []

    for algorithm in algorithms:
        times = []
        min_roman_number = None
        final_node_values = None

        for _ in range(n_repeats):
            (min_roman_number, best_node_values), exec_time = timeMeasurer.measure_execution_time(algorithm, G)
            times.append(exec_time)
            final_node_values = best_node_values

        avg_time = mean(times)

        algorithm_name = algorithm.__class__.__name__
        print(f"\n{algorithm_name} ({graph_name}):")
        print(f"Koszt RDF: {min_roman_number}")
        print(f"Średni czas działania: {avg_time:.2f} ns")

        result_entry = {
            'graph': graph_name,
            'algorithm': algorithm_name,
            'nodes': G.number_of_nodes(),
            'edges': G.number_of_edges(),
            'avg_cost': min_roman_number,
            'avg_time_ns': avg_time,
            'best_node_values': final_node_values
        }
        results.append(result_entry)

        file_exists = os.path.isfile(csv_file)
        with open(csv_file, mode="a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["graph", "algorithm", "nodes", "edges", "avg_cost", "avg_time_ns",
                                                      "best_node_values"])
            if not file_exists:
                writer.writeheader()
            writer.writerow(result_entry)

    return results

def test_ant_colony_configs(graph, graph_name, param_grid):
    results = []
    title = ""

    for alpha, beta, evaporation, ants in product(param_grid['alpha'], param_grid['beta'], param_grid['evaporation_rate'], param_grid['num_ants']):
        algorithm = AntColony(
            alpha=alpha,
            beta=beta,
            evaporation_rate=evaporation,
            num_ants=ants,
            num_iterations=200
        )

        cost, best_node_values = algorithm.execute(graph)

        result = {
            'graph': graph_name,
            'alpha': alpha,
            'beta': beta,
            'evaporation_rate': evaporation,
            'num_ants': ants,
            'avg_cost': cost,
            'best_node_values': best_node_values
        }
        title = (f"[{graph_name}] alpha={alpha}, beta={beta}, evap={evaporation}, ants={ants} -> cost={cost}")
        results.append(result)
        file_exists = os.path.isfile("aco_param_tuning_results.csv")
        with open("aco_param_tuning_results.csv", mode="a", newline="") as file:
            writer = csv.DictWriter(file,
                                    fieldnames=["graph", "alpha", "beta", "evaporation_rate", "num_ants", "avg_cost",
                                                "best_node_values"])
            if not file_exists:
                writer.writeheader()
            writer.writerow(result)

    return results, title

def main():
    sizes = [10, 20, 30, 40, 50]
    instances_per_size = 3
    all_results = []

    # test_graphs = generate_test_graphs_by_size(sizes=sizes, instances_per_size=instances_per_size)
    test_graphs = load_saved_graphs()

    for name, G in test_graphs:
        print(f"\n=== Testowanie grafu: {name} ===")
        results = test_algorithms_on_graph(G, name)
        if results:
            all_results.extend(results)
            graphPlotter.plot_graphs(G, results, name)

def ants():
    param_grid = {
        'alpha': [1, 3],
        'beta': [5, 20],
        'evaporation_rate': [0.5, 0.7],
        'num_ants': [150]
    }

    test_graphs = load_saved_graphs()
    all_results = []

    for name, G in test_graphs:
        print(f"\n=== Testowanie grafu: {name} ===")
        res, title = test_ant_colony_configs(G, name, param_grid)
        if res:
            all_results.extend(res)

# if __name__ == "__main__":
#     main()

# G = nx.Graph()
# edges = [(1,2), (2,3), (1,4), (2,5), (3,6), (4,5), (5,6), (5,7)]
# G.add_edges_from(edges)
#
# # Funkcja klasycznej dominacji
# def classical_domination(graph):
#     V = list(graph.nodes)
#     model = LpProblem("ClassicalDomination", LpMinimize)
#     d = LpVariable.dicts("d", V, cat="Binary")
#     model += lpSum(d[i] for i in V)
#     for v in V:
#         model += lpSum(d[u] for u in [v] + list(graph.neighbors(v))) >= 1
#     model.solve()
#     return {i: int(value(d[i])) for i in V}, int(value(model.objective))
#
# # Funkcja totalnej dominacji
# def total_domination(graph):
#     V = list(graph.nodes)
#     model = LpProblem("TotalDomination", LpMinimize)
#     d = LpVariable.dicts("d", V, cat="Binary")
#     model += lpSum(d[i] for i in V)
#     for v in V:
#         model += lpSum(d[u] for u in graph.neighbors(v)) >= 1
#     model.solve()
#     return {i: int(value(d[i])) for i in V}, int(value(model.objective))
#
# # Funkcja dominowania rzymskiego (słabospójna)
# def wcrdf(graph):
#     V = list(graph.nodes)
#     model = LpProblem("WCRDF", LpMinimize)
#     a = LpVariable.dicts("a", V, cat="Binary")
#     b = LpVariable.dicts("b", V, cat="Binary")
#     model += lpSum([a[i] + b[i] for i in V])
#     for i in V:
#         model += a[i] + lpSum([b[k] for k in graph.neighbors(i)]) >= 1
#         model += b[i] <= a[i]
#     model.solve()
#     return {i: int(value(a[i])) + 2 * int(value(b[i])) for i in V}, int(value(model.objective))
#
# # Porównanie
# classical, classical_cost = classical_domination(G)
# total, total_cost = total_domination(G)
# wcrdf_cost, wcrdf_sol = ILP().execute(G)
#
# print("\\n--- PORÓWNANIE ---")
# print("Klasyczna dominacja:", classical, "Koszt:", classical_cost)
# print("Totalna dominacja:", total, "Koszt:", total_cost)
# print("WCRDF:", wcrdf_sol, "Koszt:", wcrdf_cost)
#
# graphPlotter.plot_graph(G, classical, classical_cost)
# graphPlotter.plot_graph(G, total, total_cost)
# graphPlotter.plot_graph(G, wcrdf_sol, wcrdf_cost)

G = nx.read_edgelist(
    "facebook_combined.txt",
    comments="#",
    delimiter=" ",
    create_using=nx.Graph(),
    nodetype=int
)
# G = nx.karate_club_graph()
print(f"nodes: {G.number_of_nodes()} edges: {G.number_of_edges()}")

start_time = time.perf_counter_ns()
sum, values = ILP().execute(G)
end_time = time.perf_counter_ns()
execution_time = end_time - start_time
print(f"Koszt: {sum}, execution time: {execution_time}")

valid = BruteForce().is_valid_roman_dominating_set(G, values)
print(valid)

color_map = {0: "yellow", 1: "blue", 2: "red", 3: "red"}
node_colors = [color_map[values[n]] for n in G.nodes]

plt.figure(figsize=(10, 8))
pos = nx.spring_layout(G, seed=42)
nx.draw(
    G,
    pos,
    node_color=node_colors,
    edgecolors="black",
    node_size=200,
    edge_color="gray",
    with_labels=False,
    alpha=0.85
)
plt.title(f"Wizualizacja grafu Facebook – WCRDF\n(koszt całkowity = {sum})", fontsize=14, fontweight='bold', loc='center')
plt.show()




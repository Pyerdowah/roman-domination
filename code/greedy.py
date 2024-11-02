import matplotlib.pyplot as plt
import networkx as nx
from itertools import combinations, permutations


def is_dominating_set(graph, node_set):
    dominated = set(node_set)
    for node in node_set:
        dominated.update(graph.neighbors(node))
    return len(dominated) == len(graph.nodes)


def is_connected_subgraph(graph, node_set):
    subgraph = graph.subgraph(node_set)
    return nx.is_connected(subgraph)


def find_all_connected_dominating_sets(graph):
    nodes = list(graph.nodes)
    connected_dominating_sets = []
    for r in range(1, len(nodes) + 1):
        for subset in combinations(nodes, r):
            if is_dominating_set(graph, subset) and is_connected_subgraph(graph, subset):
                connected_dominating_sets.append(set(subset))
    return connected_dominating_sets


# G = nx.binomial_tree(3)
G = nx.erdos_renyi_graph(7, 0.4, seed=42)

all_connected_dominating_sets = find_all_connected_dominating_sets(G)

min_roman_number = float('inf')
best_perm = None
best_dom_set = None
best_node_values = {node: 0 for node in G.nodes}

for dom_set in all_connected_dominating_sets:
    perm = permutations(dom_set, len(dom_set))

    for p in perm:
        roman_number = 0
        G_copy = G.copy()
        node_values = {node: 0 for node in G.nodes}
        for node in p:
            has_only_neighbors_in_dominating_set = all(neighbor in dom_set for neighbor in G_copy.neighbors(node))

            if G_copy.degree(node) > 0 and not has_only_neighbors_in_dominating_set:
                roman_number += 2
                node_values[node] = 2
            else:
                roman_number += 1
                node_values[node] = 1

            G_copy.remove_node(node)

        if roman_number < min_roman_number:
            min_roman_number = roman_number
            best_perm = p
            best_dom_set = dom_set
            best_node_values = node_values.copy()

if best_perm is not None:
    for node in G.nodes:
        if node not in best_dom_set:
            node_values[node] = 0

    node_colors = ['red' if value == 2 else 'blue' if value == 1 else 'yellow' for value in best_node_values.values()]
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=800)
    plt.title(f"Graf z najlepszą permutacją (roman_number: {min_roman_number})")
    plt.show()
    print(f"Minimalna liczba dominowania rzymskiego słabospójnego: {min_roman_number})")
else:
    print("Nie znaleziono zbiorów dominujących.")

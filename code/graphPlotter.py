import matplotlib.pyplot as plt
import networkx as nx
import pydot
from networkx.drawing.nx_pydot import graphviz_layout


def plot_graph(graph, node_values, min_roman_number):
    node_colors = ['red' if node_values[node] == 2 else
                   'blue' if node_values[node] == 1 else 'yellow'
                   for node in graph.nodes]

    pos = nx.spring_layout(graph, seed=42)
    plt.figure(figsize=(8, 6))
    nx.draw(graph, pos, with_labels=True, node_color=node_colors, node_size=800)
    plt.title(f"Minimalny rzymski słabospójny zbiór dominujący (roman_number: {min_roman_number})")
    plt.show()


def plot_graphs(graph, results):
    num_algorithms = len(results)
    fig, axes = plt.subplots(1, num_algorithms, figsize=(5 * num_algorithms, 5))

    if num_algorithms == 1:
        axes = [axes]

    for ax, (algorithm_name, node_values, min_roman_number) in zip(axes, results):
        node_colors = ['red' if node_values[node] == 2 else
                       'blue' if node_values[node] == 1 else 'yellow'
                       for node in graph.nodes]

        # pos = nx.spring_layout(graph, seed=42)
        pos = graphviz_layout(graph, prog="dot")
        nx.draw(graph, pos, with_labels=True, node_color=node_colors, node_size=800, ax=ax)
        ax.set_title(f"{algorithm_name}\nWeakly roman domination number: {min_roman_number}")

    plt.tight_layout()
    plt.show()

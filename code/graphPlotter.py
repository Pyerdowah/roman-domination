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
    cols = 3  # Number of columns in the subplot grid
    rows = -(-num_algorithms // cols)  # Ceiling division to determine number of rows

    fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 5 * rows))

    # Flatten axes array for easy iteration if more than one row exists
    if rows > 1:
        axes = axes.flatten()
    else:
        axes = axes[:]

    for ax, (algorithm_name, node_values, min_roman_number) in zip(axes, results):
        node_colors = ['red' if node_values[node] >= 2 else
                       'blue' if node_values[node] == 1 else 'yellow'
                       for node in graph.nodes]

        # pos = nx.spring_layout(graph, seed=42)
        pos = graphviz_layout(graph, prog="dot")
        nx.draw(graph, pos, with_labels=True, node_color=node_colors, node_size=800, ax=ax)
        ax.set_title(f"{algorithm_name}\nWeak roman domination number: {min_roman_number}")

    # Hide empty subplots if num_algorithms % 3 != 0
    for i in range(num_algorithms, len(axes)):
        fig.delaxes(axes[i])

    plt.tight_layout()
    plt.show()

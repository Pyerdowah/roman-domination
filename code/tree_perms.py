import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations
import numpy as np


def generate_base_tree_edges(size):
    """
    Generate all possible edges for a complete graph of given size.

    Args:
        size (int): Number of vertices in the graph.

    Returns:
        list of tuples: All possible edges in a complete graph.
    """
    edges = [(i, j) for i in range(1, size + 1) for j in range(i + 1, size + 1)]
    return edges


def is_tree(edge_list, size):
    """
    Check if the given edge list forms a tree.

    Args:
        edge_list (list of tuples): List of edges.
        size (int): Number of vertices.

    Returns:
        bool: True if the edge list forms a tree, False otherwise.
    """
    G = nx.Graph()
    G.add_edges_from(edge_list)
    return nx.is_connected(G) and len(edge_list) == size - 1


def canonical_form(G):
    """
    Get the canonical form of a tree using a sorted adjacency matrix.

    Args:
        G (networkx.Graph): The tree graph.

    Returns:
        tuple: Canonical form of the tree as a tuple of tuples.
    """
    adj_matrix = nx.to_numpy_array(G, dtype=int)
    # Canonical form is the sorted rows of the adjacency matrix
    return tuple(map(tuple, np.sort(adj_matrix, axis=1)))


def visualize_unique_trees(size):
    """
    Generate and visualize all unique tree structures for given size.

    Args:
        size (int): Number of vertices in the tree.
    """
    base_edges = generate_base_tree_edges(size)
    edge_combinations = combinations(base_edges, size - 1)

    unique_trees = set()
    unique_graphs = []

    for edges in edge_combinations:
        if is_tree(edges, size):
            G = nx.Graph()
            G.add_edges_from(edges)
            canon = canonical_form(G)
            if canon not in unique_trees:
                unique_trees.add(canon)
                unique_graphs.append(G)

    # Visualize unique trees
    n_cols = 4
    n_rows = (len(unique_graphs) + n_cols - 1) // n_cols
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(20, n_rows * 5))
    axes = axes.flatten()

    for i, G in enumerate(unique_graphs):
        pos = nx.spring_layout(G, seed=42)  # Use a consistent layout for visualization
        nx.draw(G, pos, ax=axes[i], with_labels=True, node_color='lightblue', node_size=800, font_size=10)
        axes[i].set_title(f"Tree {i + 1}")

    # Hide unused axes
    for j in range(len(unique_graphs), len(axes)):
        axes[j].axis('off')

    plt.tight_layout()
    plt.show()


# Example usage
visualize_unique_trees(5)

import os

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pydot
from networkx.drawing.nx_pydot import graphviz_layout


def plot_graph(graph, node_values, min_roman_number):
    node_colors = ['red' if node_values[node] >= 2 else
                   'blue' if node_values[node] == 1 else 'yellow'
                   for node in graph.nodes]

    pos = nx.spring_layout(graph, seed=42)
    plt.figure(figsize=(8, 6))
    nx.draw(graph, pos, with_labels=True, node_color=node_colors, node_size=800)
    plt.title(f"Minimalny rzymski słabospójny zbiór dominujący (roman_number: {min_roman_number})")
    plt.show()


def plot_graphs(graph, results, graph_name):
    pos = graphviz_layout(graph, prog="dot")

    for result in results:
        algorithm_name = result["algorithm"]
        avg_cost = result["avg_cost"]
        node_values = result.get("best_node_values", {})

        node_colors = [
            'red' if node_values.get(node, 0) >= 2 else
            'blue' if node_values.get(node, 0) == 1 else
            'yellow'
            for node in graph.nodes
        ]

        plt.figure(figsize=(6, 6))

        nx.draw(graph, pos, with_labels=True, node_color=node_colors, node_size=800)
        plt.title(f"{algorithm_name}\nWeak roman domination number: {avg_cost}")

        os.makedirs("plots", exist_ok=True)
        os.makedirs(f"plots/{algorithm_name}", exist_ok=True)

        file_path = f"plots/{algorithm_name}/{graph_name}_results.png"
        plt.subplots_adjust(top=0.85)
        # plt.show()
        plt.savefig(file_path, bbox_inches='tight')
        plt.close()


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Wczytanie danych
df = pd.read_csv("results.csv")

# # Obliczenie błędu względnego w procentach
# df["relative_error_%"] = abs(df["estimated_cost"] - df["exact_cost"]) / df["exact_cost"] * 100
#
# # Wyodrębnienie klasy grafu z nazwy
# df["graph_class"] = df["graph"].apply(lambda x: x.split("_n")[0])
#
# plt.figure(figsize=(10, 6))
# sns.scatterplot(x="nodes", y="relative_error_%", hue="graph_class", data=df)
# plt.xlabel("Liczba wierzchołków")
# plt.ylabel("Błąd względny [%]")
# plt.title("Zależność błędu względnego od liczby wierzchołków")
# plt.legend(title="Typ grafu")
# plt.grid(True)
# plt.tight_layout()
# plt.show()

df["relative_error_%"] = abs(df["estimated_cost"] - df["exact_cost"]) / df["exact_cost"] * 100

# Zamiana czasu na sekundy (opcjonalnie)
df["time_s"] = df["avg_time_ns"] / 1e9

# Wykres: czas działania vs błąd względny
plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=df,
    x="time_s",
    y="relative_error_%",
    hue="algorithm",
    style="algorithm",
    s=100
)
plt.xscale("log")
plt.xlabel("Czas działania [s] (log-skala)")
plt.ylabel("Błąd względny [%]")
plt.title("Porównanie algorytmów: czas działania vs błąd względny")
plt.grid(True)
plt.tight_layout()
plt.legend(title="Algorytm")
plt.show()
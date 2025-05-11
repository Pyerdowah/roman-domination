import geopandas as gpd
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import time

from algorithms.Approx import Approx
from algorithms.ILP import ILP
from algorithms.ILP2 import ILP2
from algorithms.TreeLinear import TreeLinear
from algorithms.BruteForce import BruteForce

from algorithms.AntColony import AntColony
from algorithms.Greedy import Greedy

df_nodes = pd.read_csv("wezly_sieci.csv")
df_edges = pd.read_csv("polaczenia_bez_duplikatow.csv")

# Utworzenie grafu z atrybutami węzłów
G = nx.Graph()
positions = {row["name"]: (row["lon"], row["lat"]) for _, row in df_nodes.iterrows()}
for node in positions:
    G.add_node(node)
for _, row in df_edges.iterrows():
    G.add_edge(row["from"], row["to"])

algorithms = [
    # ILP2(),
    # Approx(),
    # Greedy()
]

results = []
execution_time = None

for algorithm in algorithms:
    start_time = time.perf_counter_ns()
    results.append(algorithm.execute(G))
    end_time = time.perf_counter_ns()
    execution_time = end_time - start_time


shp_path = "./ne_50m_admin_0_countries/ne_50m_admin_0_countries.shp"
world = gpd.read_file(shp_path)
poland = world[world["ADMIN"] == "Poland"]

fig, ax = plt.subplots(figsize=(12, 10))
poland.plot(ax=ax, color='white', edgecolor='black')

for u, v in G.edges():
    if u in positions and v in positions:
        x0, y0 = positions[u]
        x1, y1 = positions[v]
        ax.plot([x0, x1], [y0, y1], color='red', linewidth=1)

min_roman_number, node_values = results[0]
valid = BruteForce().is_valid_roman_dominating_set(G, node_values)
print(valid)

print(f"{algorithms[0].__class__.__name__} WCRDF: {min_roman_number}, czas trwania: {execution_time} ")

color_map = {
    0: "yellow",
    1: "blue"
}

for node, (x, y) in positions.items():
    value = node_values.get(node, 0)
    color = color_map.get(value, "red")
    ax.scatter(x, y, color=color, edgecolor='black', s=100, zorder=3)
    ax.text(x + 0.1, y + 0.1, node, fontsize=7)

ax.set_title(f"Sieć przesyłowa 400 kV na tle mapy Polski - {algorithms[0].__class__.__name__} WCRDF: {min_roman_number}", fontsize=14)
ax.set_xlabel("Długość geograficzna")
ax.set_ylabel("Szerokość geograficzna")
ax.grid(True)
plt.tight_layout()
plt.show()


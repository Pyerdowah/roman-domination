# import os
#
# import pandas as pd
# import networkx as nx
# import numpy as np
# from math import log
#
#
# def load_saved_graphs(folder="saved_graphs"):
#     graphs = []
#     for filename in os.listdir(folder):
#         if filename.endswith(".graphml"):
#             path = os.path.join(folder, filename)
#             G = nx.read_graphml(path)
#             G = nx.relabel_nodes(G, lambda x: int(x))
#             graphs.append((filename.replace(".graphml", ""), G))
#
#     graphs.sort(key=lambda item: (item[1].number_of_nodes(), item[1].number_of_edges()))
#     return graphs
# # Parametr epsilon z teorii
# epsilon = 0.1
#
# # Wczytaj grafy
# graphs = load_saved_graphs()  # powinno zwracać listę (name, G)
#
# # Wczytaj dane z wynikami Approx
# results_df = pd.read_csv("results.csv")  # zawiera kolumny: graph, estimated_cost, exact_cost
#
# # Lista wyników
# data = []
#
# for name, G in graphs:
#     print(name)
#     row = results_df[results_df["graph"] == name]
#     if row.empty:
#         continue  # brak wyników dla tego grafu
#
#     estimated = row.iloc[0]["estimated_cost"]
#     exact = row.iloc[0]["exact_cost"]
#
#     if exact == 0:
#         continue  # uniknij dzielenia przez 0
#
#     ratio = estimated / exact
#     delta = max(dict(G.degree()).values())
#
#     if delta <= 1:
#         bound = float('inf')  # log(0) nie istnieje
#     else:
#         bound = 2 * (1 + epsilon) * (1 + log(delta - 1))
#
#     data.append({
#         "graph": name,
#         "estimated_cost": estimated,
#         "exact_cost": exact,
#         "ratio": ratio,
#         "delta": delta,
#         "theoretical_bound": bound,
#         "within_bound": ratio <= bound
#     })
#
# # Przekształć do DataFrame i pokaż wyniki
# df_eval = pd.DataFrame(data)
# print(df_eval[["graph", "ratio", "delta", "theoretical_bound", "within_bound"]])
#
# # Ewentualnie zapisz do pliku CSV
# df_eval.to_csv("approx_ratio_check.csv", index=False)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Wczytanie wyników
df = pd.read_csv("approx_ratio_check.csv")

# Uporządkuj dane wg delta
df = df.sort_values("delta")

# Wykres
plt.figure(figsize=(10, 6))

# Punkty: rzeczywisty współczynnik aproksymacyjny
sns.scatterplot(
    data=df,
    x="delta",
    y="ratio",
    hue="within_bound",
    palette={True: "green", False: "red"},
    style="within_bound",
    s=100
)

# Linia teoretycznej granicy
plt.plot(df["delta"], df["theoretical_bound"], label="Granica teoretyczna", color="black", linestyle="--")

plt.xlabel("Maksymalny stopień w grafie (Δ)")
plt.ylabel("Współczynnik aproksymacyjny (ratio)")
plt.title("Porównanie algorytmu aproksymacyjnego z granicą teoretyczną")
plt.grid(True)
plt.legend(title="Spełnia granicę")
plt.tight_layout()
plt.show()

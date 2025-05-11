import networkx as nx
from pulp import LpProblem, LpVariable, lpSum, LpMinimize, PULP_CBC_CMD, value, LpBinary

from .Algorithm import AlgorithmBase
from .BruteForce import BruteForce


class Approx(AlgorithmBase):
    def compute_dominating_set(self, graph):
        model = LpProblem("MCDS_SCF_Model", LpMinimize)
        V = list(graph.nodes())
        E = list(graph.edges())
        n = len(V)

        # Zmienne decyzyjne
        x = {v: LpVariable(f"x_{v}", cat=LpBinary) for v in V}  # Czy w CDS
        r = {v: LpVariable(f"r_{v}", cat=LpBinary) for v in V}  # Czy root
        f = {}  # Przepływ
        for (u, v) in E:
            f[(u, v)] = LpVariable(f"f_{u}_{v}", lowBound=0)
            f[(v, u)] = LpVariable(f"f_{v}_{u}", lowBound=0)

        # Funkcja celu: minimalizacja liczby wierzchołków w CDS
        model += lpSum(x[v] for v in V), "Minimize_CDS"

        # (4a) Dokładnie jeden root
        model += lpSum(r[v] for v in V) == 1, "SingleRoot"

        # (4b) Root musi należeć do CDS
        for v in V:
            model += r[v] <= x[v], f"RootImpliesCDS_{v}"

        # (4d) Przepływ tylko między wierzchołkami z CDS
        for (u, v) in f:
            model += f[(u, v)] <= x[u] * n, f"FlowCap_from_{u}_{v}"
            model += f[(u, v)] <= x[v] * n, f"FlowCap_to_{u}_{v}"

        # (4e) Brak wpływu do root
        for v in V:
            inflow = lpSum(f[(u, v)] for u in graph.neighbors(v) if (u, v) in f)
            model += inflow <= n * (1 - r[v]), f"NoInflowForRoot_{v}"

        # (Z) Zmienna pomocnicza do r[v] * sum(x)
        total_x = lpSum(x[i] for i in V)
        z = {v: LpVariable(f"z_{v}", lowBound=0, upBound=n) for v in V}

        for v in V:
            # Linearizacja z[v] ≈ r[v] * total_x
            model += z[v] <= n * r[v], f"Z_UB1_{v}"
            model += z[v] <= total_x, f"Z_UB2_{v}"
            model += z[v] >= total_x - n * (1 - r[v]), f"Z_LB_{v}"

        # (4f) Równania bilansu przepływu
        for v in V:
            inflow = lpSum(f[(u, v)] for u in graph.neighbors(v) if (u, v) in f)
            outflow = lpSum(f[(v, u)] for u in graph.neighbors(v) if (v, u) in f)
            model += inflow - outflow == x[v] - z[v], f"FlowBalance_{v}"

        # Dominacja: każdy wierzchołek zdominowany przez siebie lub sąsiada
        for v in V:
            neighbors = list(graph.neighbors(v)) + [v]
            model += lpSum(x[u] for u in neighbors) >= 1, f"Domination_{v}"

        # Rozwiązanie
        solver = PULP_CBC_CMD(msg=False)
        model.solve(solver)

        # Odczyt wyniku
        cds = [v for v in V if value(x[v]) == 1]
        return cds

    def execute(self, graph):
        nodes = list(graph.nodes)
        dominating_set = self.compute_dominating_set(graph)
        node_values = {node: 2 if node in dominating_set else 0 for node in nodes}
        roman_number = sum(node_values.values())
        # self.is_connected_dominating_set(graph, dominating_set)
        return roman_number, node_values

    def is_connected_dominating_set(self, G: nx.Graph, dominating_set: list[int]) -> bool:
        """Sprawdza, czy podany zbiór jest connected dominating set (CDS) grafu G."""

        # 1. Dominacja: każdy wierzchołek musi być w zbiorze lub mieć sąsiada w zbiorze
        for v in G.nodes:
            if v not in dominating_set and not any(u in dominating_set for u in G.neighbors(v)):
                print(f"❌ Wierzchołek {v} nie jest zdominowany.")
                return False

        # 2. Spójność: indukowany podgraf przez dominating_set musi być spójny
        induced_subgraph = G.subgraph(dominating_set)
        if not nx.is_connected(induced_subgraph):
            print(f"❌ Podgraf indukowany przez zbiór dominujący nie jest spójny.")
            return False

        print("✅ Zbiór jest poprawnym Connected Dominating Set.")
        return True

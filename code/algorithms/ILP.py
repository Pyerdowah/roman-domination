import networkx as nx
from pulp import LpProblem, LpVariable, lpSum, LpMinimize, value

from .Algorithm import AlgorithmBase


class ILP(AlgorithmBase):
    def execute(self, graph):
        V = list(graph.nodes)
        E = list(graph.edges)

        model = LpProblem("WCRDP_ILP", LpMinimize)

        x = LpVariable.dicts("x", E, cat="Binary")  # Czy krawedz e nalezy do G'
        y = LpVariable.dicts("y", E, cat="Binary")  # Czy krawedz e nalezy do drzewa T'
        a = LpVariable.dicts("a", V, cat="Binary")  # Wierzcholki V1 ∪ V2
        b = LpVariable.dicts("b", V, cat="Binary")  # Wierzcholki V2

        # Funkcja celu: minimalizacja sumy a + b
        model += lpSum([a[i] + b[i] for i in V])

        # Constraint (2): Kazdy wierzcholek musi byc broniony
        for i in V:
            model += a[i] + lpSum([b[k] for k in graph.neighbors(i)]) >= 1

        # Constraint (3): y[i,j] <= x[i,j]
        for (i, j) in E:
            model += y[i, j] <= x[i, j]

        # Constraint (4): x[i,j] <= a[i] + a[j]
        for (i, j) in E:
            model += x[i, j] <= a[i] + a[j]

        # Constraint (5): liczba krawedzi drzewa = liczba wierzcholkow - 1
        model += lpSum([y[i, j] for (i, j) in E]) == len(V) - 1

        # Constraint (6): Eliminacja cykli przez ograniczenia klik
        subsets = [list(subset) for subset in nx.find_cliques(graph) if len(subset) >= 3]
        for S in subsets:
            model += lpSum([y[i, j] for i in S for j in S if (i, j) in E]) <= len(S) - 1

        # Constraint (7): b[i] <= a[i]
        for i in V:
            model += b[i] <= a[i]

        model.solve()

        solution = {i: round(value(a[i])) + 2 * round(value(b[i])) for i in V}
        return int(value(model.objective)), solution

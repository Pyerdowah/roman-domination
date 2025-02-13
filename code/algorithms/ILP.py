import gurobipy as gp
import networkx as nx
from gurobipy import GRB

from .Algorithm import AlgorithmBase


class ILP(AlgorithmBase):
    def execute(self, graph):
        V = list(graph.nodes)
        E = list(graph.edges)

        model = gp.Model("WCRDP_ILP")
        model.setParam("OutputFlag", 1)

        x = model.addVars(E, vtype=GRB.BINARY, name="x")  # Czy krawędź e należy do G'
        y = model.addVars(E, vtype=GRB.BINARY, name="y")  # Czy krawędź e należy do drzewa rozpinającego T'
        a = model.addVars(V, vtype=GRB.BINARY, name="a")  # Wierzchołki V1 ∪ V2
        b = model.addVars(V, vtype=GRB.BINARY, name="b")  # Wierzchołki V2

        # Funkcja celu: minimalizacja sumy a + b
        model.setObjective(gp.quicksum(a[i] + b[i] for i in V), GRB.MINIMIZE)

        # Constraint (2): Każdy wierzchołek musi być broniony
        for i in V:
            model.addConstr(a[i] + gp.quicksum(b[k] for k in graph.neighbors(i)) >= 1)

        # Constraint (3): Krawędź w drzewie może istnieć tylko, jeśli jest w G'
        for (i, j) in E:
            model.addConstr(y[i, j] <= x[i, j])

        # Constraint (4): Drzewo rozpinające tylko dla połączonych wierzchołków
        for (i, j) in E:
            model.addConstr(x[i, j] <= a[i] + a[j])

        # Constraint (5): Liczba krawędzi drzewa rozpinającego = liczba wierzchołków - 1
        model.addConstr(gp.quicksum(y[i, j] for (i, j) in E) == len(V) - 1)

        # **Constraint (6): Eliminacja cykli w drzewie**
        subsets = [list(subset) for subset in nx.find_cliques(graph) if len(subset) >= 3]
        for S in subsets:
            model.addConstr(gp.quicksum(y[i, j] for i in S for j in S if (i, j) in E) <= len(S) - 1)

        # Constraint (7): Wierzchołki V2 muszą należeć do V1 ∪ V2
        for i in V:
            model.addConstr(b[i] <= a[i])

        model.optimize()

        solution = {i: round(a[i].X) + 2 * round(b[i].X) for i in V}
        return int(model.objVal), solution

import gurobipy as gp
import networkx as nx
from gurobipy import GRB
from pulp import LpProblem, LpVariable, lpSum, LpMinimize


from .Algorithm import AlgorithmBase


class ILP2(AlgorithmBase):
    def execute(self, graph):
        model = LpProblem("Second_ILP_Model", LpMinimize)

        V = graph.nodes
        E = graph.edges
        n = len(V)

        x = {i: LpVariable(f"x_{i}", cat="Binary") for i in V}
        y = {i: LpVariable(f"y_{i}", cat="Binary") for i in V}
        a = {e: LpVariable(f"a_{e}", cat="Binary") for e in E}
        t = {i: LpVariable(f"t_{i}", cat="Binary") for i in V}
        u = {i: LpVariable(f"u_{i}", lowBound=0, cat="Integer") for i in V}
        v = {e: LpVariable(f"v_{e}", lowBound=-n, upBound=n, cat="Continuous") for e in E}

        # Objective function
        model += lpSum(x[i] + y[i] for i in V)

        # Constraints
        for i in V:
            model += x[i] + lpSum(y[j] for j in V if (j, i) in E or (i, j) in E) >= 1
            model += y[i] <= x[i]
            model += lpSum(a[e] for e in E if i in e) >= 1

        for e in E:
            i_e, j_e = e
            model += a[e] <= x[i_e] + x[j_e]
            model += v[e] <= n * a[e]
            model += v[e] >= -n * a[e]

        model += lpSum(t[i] for i in V) == 1

        for i in V:
            model += u[i] <= n * t[i]
            model += u[i] + lpSum(v[e] for e in E if e[1] == i) - lpSum(v[e] for e in E if e[0] == i) == 1

        model.solve()

        solution = {i: round(x[i].varValue) + 2 * round(y[i].varValue) for i in V}
        model_obj_val = model.objective.value()
        return int(model_obj_val), solution
from itertools import product
import networkx as nx
from .Algorithm import AlgorithmBase
from .Approx import Approx
from .BruteForce import BruteForce


class Greedy(AlgorithmBase):
    def execute(self, graph):
        f = {v: 0 for v in graph.nodes}
        secured_nodes = set()
        uncovered_nodes = set(graph.nodes)

        start_node = max(graph.degree, key=lambda x: x[1])[0]
        f[start_node] = 2
        secured_nodes.add(start_node)
        uncovered_nodes.discard(start_node)
        for neighbor in graph.neighbors(start_node):
            secured_nodes.add(neighbor)
            uncovered_nodes.discard(neighbor)

        while uncovered_nodes:
            candidate_nodes = set()
            for v in secured_nodes:
                for neighbor in graph.neighbors(v):
                    if neighbor in uncovered_nodes:
                        candidate_nodes.add(neighbor)

            if not candidate_nodes:
                node = uncovered_nodes.pop()
                f[node] = 2
                secured_nodes.add(node)
                for neighbor in graph.neighbors(node):
                    secured_nodes.add(neighbor)
                    uncovered_nodes.discard(neighbor)
                continue

            node = max(candidate_nodes, key=lambda n: len([nn for nn in graph.neighbors(n) if nn in uncovered_nodes]))

            new_covered_neighbors = len([nn for nn in graph.neighbors(node) if nn in uncovered_nodes])

            if new_covered_neighbors > 0:
                f[node] = 2
            else:
                f[node] = 1

            secured_nodes.add(node)
            uncovered_nodes.discard(node)
            for neighbor in graph.neighbors(node):
                secured_nodes.add(neighbor)
                uncovered_nodes.discard(neighbor)

        # valid = BruteForce().is_valid_roman_dominating_set(graph, f)
        # print(valid)

        return sum(f.values()), f

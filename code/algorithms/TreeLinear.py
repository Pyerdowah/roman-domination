import networkx as nx

from .Algorithm import AlgorithmBase


class TreeLinear(AlgorithmBase):
    def reset_tree(self, T):
        for node in T.nodes:
            T.nodes[node]['n00'] = 0
            T.nodes[node]['n01'] = 0
            T.nodes[node]['n1'] = 0
            T.nodes[node]['n2'] = 0
            T.nodes[node]['ch'] = 0
            T.nodes[node]['R'] = 0
            T.nodes[node]['sw'] = 0
            T.nodes[node]['child'] = 0
            T.nodes[node]['color'] = "white"

    def phase1(self, T, root=0):
        post_order_nodes = list(nx.dfs_postorder_nodes(T, source=root))

        for v in post_order_nodes:
            neighbors = list(T.neighbors(v))
            father = None if v == root else neighbors[0]

            if len(neighbors) == 1 and v != root:  # Liść
                if father is not None:
                    T.nodes[father]['n00'] += 1
                    T.nodes[father]['child'] = v
            else:
                if T.nodes[v]['n00'] == 1 and father is not None and T.nodes[v]['n01'] == 0:
                    T.nodes[father]['sw'] += 1

                if T.nodes[v]['sw'] > 0 and (T.nodes[v]['sw'] + T.nodes[v]['n00'] + T.nodes[v]['n01']) > 1:
                    T.nodes[v]['R'] = 2
                    if father is not None:
                        T.nodes[father]['n2'] += 1
                        if T.nodes[v]['n00'] == 1 and T.nodes[v]['n01'] == 0:
                            T.nodes[father]['sw'] -= 1
                    T.nodes[v]['ch'] = 1

                if T.nodes[v]['sw'] == 0:
                    if T.nodes[v]['n00'] > 1 or (
                            T.nodes[v]['n00'] == 1 and (T.nodes[v]['n2'] == 0 or T.nodes[v]['n01'] > 0)):
                        T.nodes[v]['R'] = 2
                        if father is not None:
                            T.nodes[father]['n2'] += 1

                    elif T.nodes[v]['n00'] == 1:
                        T.nodes[v]['R'] = 0
                        T.nodes[T.nodes[v]['child']]['R'] = 1
                        if father is not None:
                            T.nodes[father]['sw'] -= 1

                    if T.nodes[v]['n00'] == 0 and T.nodes[v]['n01'] > 0:
                        T.nodes[v]['R'] = 1
                        if father is not None:
                            T.nodes[father]['n1'] += 1

                if T.nodes[v]['R'] == 0 and T.nodes[v]['n2'] > 0 and father is not None:
                    T.nodes[father]['n01'] += 1
                if T.nodes[v]['R'] == 0 and T.nodes[v]['n2'] == 0 and father is not None:
                    T.nodes[father]['n00'] += 1

        if T.nodes[root]['n2'] == 0 and T.nodes[root]['R'] == 0:
            T.nodes[root]['R'] = 2

        return T

    def phase2(self, T, root=0):
        post_order_nodes = list(nx.dfs_postorder_nodes(T, source=root))

        for v in post_order_nodes:
            neighbors = list(T.neighbors(v))
            father = None if v == root else neighbors[0]

            if father:
                if T.nodes[v]['n00'] == 1 and T.nodes[father]['ch'] and T.nodes[v]['n01'] == 0:
                    T.nodes[v]['R'] = 0
                    T.nodes[T.nodes[v]['child']]['R'] = 1
                    T.nodes[father]['n00'] += 1

        return T

    def handle_root_special_case(self, graph, root):
        """ Obsługa specjalnego przypadku korzenia z jednym dzieckiem i dzieckiem o R = 1. """
        neighbors = list(graph.neighbors(root))

        if len(neighbors) == 1:
            child = neighbors[0]
            if graph.nodes[child]['R'] == 1:
                graph.nodes[child]['R'] = 2
                graph.nodes[root]['R'] = 0

    def execute(self, graph):
        root = 0
        self.reset_tree(graph)
        graph = self.phase1(graph, root)
        graph = self.phase2(graph, root)

        self.handle_root_special_case(graph, root)

        min_roman_number = sum(graph.nodes[node]['R'] for node in graph.nodes)
        best_node_values = {node: graph.nodes[node]['R'] for node in graph.nodes}
        print(best_node_values)
        return min_roman_number, best_node_values

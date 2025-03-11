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

    def get_father_map(self, T, root):
        father_map = {root: None}
        for parent, child in nx.bfs_edges(T, source=root):
            father_map[child] = parent
        return father_map

    def phase1(self, T, root=0):
        father_map = self.get_father_map(T, root)
        nodes_ids = list(T.nodes)
        for v in reversed(nodes_ids):
            father = father_map[v]

            if len(list(nx.ego_graph(T, v, radius=1).nodes)) - 1 - T.nodes[v]['n1'] == 1 and v != root:  # Liść
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
        if T.nodes[root]['n1'] == len(list(nx.ego_graph(T, root, radius=1).nodes)) - 1:
            T.nodes[root]['R'] = 1

        return T

    def phase2(self, T, root=0):
        father_map = self.get_father_map(T, root)
        nodes_ids = list(T.nodes)
        for v in reversed(nodes_ids):
            father = father_map[v]
            if father is not None:
                # T.nodes[father]['child'] = v
                if T.nodes[v]['n00'] == 1 and T.nodes[father]['ch'] and T.nodes[v]['n01'] == 0:
                    T.nodes[v]['R'] = 0
                    T.nodes[T.nodes[v]['child']]['R'] = 1
                    T.nodes[father]['n00'] += 1

        return T

    def execute(self, graph):
        root = 0
        self.reset_tree(graph)
        graph = self.phase1(graph, root)
        graph = self.phase2(graph, root)

        min_roman_number = sum(graph.nodes[node]['R'] for node in graph.nodes)
        best_node_values = {node: graph.nodes[node]['R'] for node in graph.nodes}
        return min_roman_number, best_node_values

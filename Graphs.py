from itertools import combinations as combs

class Graph:
    @staticmethod
    def complete_graph(n):
        vertices = list(range(1, n + 1))
        edges = [(a, b, 1) for a, b in combs(vertices, 2)]
        return Graph(vertices, edges)

    def __init__(self, vertices, edges, vertex_weights=None):
        for e in edges:
            for v in e[:2]:
                if v not in vertices:
                    raise Exception(f'Nonexistent vertex present in edge list: {v}')
        
        self.vertices = vertices
        self.edges = edges

        if vertex_weights:
            self.weighted_vertices = True
            self.vertex_weights = vertex_weights
        else:
            self.weighted_vertices = False

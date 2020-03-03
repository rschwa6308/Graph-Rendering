from itertools import combinations as combs

class Graph:
    @staticmethod
    def complete_graph(n):
        vertices = list(range(1, n + 1))
        edges = [(a, b, 1) for a, b in combs(vertices, 2)]
        return Graph(vertices, edges)

    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges
        if any(v not in vertices for e in edges for v in e):
            raise Exception('Nonexistent vertex present in edge list')
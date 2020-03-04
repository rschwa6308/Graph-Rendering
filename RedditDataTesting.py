from Render import *
from Graphs import Graph


test_graph = Graph(
    [1, 2, 3, 4, 5],
    [(1, 2, 1), (2, 3, 1), (3, 4, 1), (3, 5, 1), (1, 4, 1)]
)
test_system = System.from_graph(test_graph)

test_graph = Graph.complete_graph(7)
test_system = System.from_graph(test_graph, spring_length=2)

run_system(test_system)

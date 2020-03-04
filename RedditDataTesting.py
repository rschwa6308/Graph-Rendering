from Render import *
from Graphs import Graph


# test_graph = Graph(
#     [1, 2, 3, 4, 5],
#     [(1, 2, 1), (2, 3, 1), (3, 4, 1), (3, 5, 1), (1, 4, 1)]
# )
# test_system = System.from_graph(test_graph)

# test_graph = Graph.complete_graph(7)
# test_system = System.from_graph(test_graph, spring_length=2)

# run_system(test_system)

music_subreddits_graph = Graph(
    ['dubstep', 'metal', 'jazz', 'classical', 'trap', 'vaporwave', 'kpop'],
    [('dubstep', 'trap', 0.049449825393687814), ('dubstep', 'vaporwave', 0.007224307670514909), ('metal', 'jazz', 0.013382617761349636), ('metal', 'classical', 0.010528450787328981), ('jazz', 'classical', 0.03508150248051028), ('jazz', 'vaporwave', 0.011396159650309622), ('classical', 'vaporwave', 0.006986002954653579), ('classical', 'trap', 0.0052301737247131466), ('trap', 'vaporwave', 0.012803972639419682), ('trap', 'kpop', 0.004942939401297305), ('vaporwave', 'kpop', 0.004883442366166037)]
)

system = System.from_graph(music_subreddits_graph, k_function=lambda w: 2 ** (w * 50))
for s in system.springs:
    print(s.k)

run_system(system)
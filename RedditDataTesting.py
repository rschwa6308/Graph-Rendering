from Render import *
from Graphs import Graph


# test_graph = Graph(
#     [1, 2, 3, 4, 5],
#     [(1, 2, 1), (2, 3, 1), (3, 4, 1), (3, 5, 1), (1, 4, 1)]
# )
# test_system = System.from_graph(test_graph)


# test_graph = Graph.complete_graph(6)
# test_system = System.from_graph(test_graph, spring_length_function=lambda w: 2)

# run_system(test_system)


# music_subreddits_graph = Graph(
#     ['dubstep', 'metal', 'jazz', 'classical', 'trap', 'vaporwave', 'kpop'],
#     [('dubstep', 'trap', 0.05333794385252102), ('dubstep', 'vaporwave', 0.008080509726148783), ('metal', 'jazz', 0.015124003293220702), ('metal', 'classical', 0.011521354696961578), ('jazz', 'classical', 0.036549855857683), ('jazz', 'vaporwave', 0.012715953307392997), ('classical', 'vaporwave', 0.00788144449605202), ('classical', 'trap', 0.0057576363688316146), ('trap', 'vaporwave', 0.013880736710186081),
# ('trap', 'kpop', 0.00494641384995878), ('vaporwave', 'kpop', 0.005670890091804969)],
#     vertex_weights=[('dubstep', 16304), ('metal', 56418), ('jazz', 33590), ('classical', 37962), ('trap', 32435), ('vaporwave', 31477), ('kpop', 69961)]
# )

# system = System.from_graph(
#     music_subreddits_graph,
#     k_function=lambda w: 2 ** (w * 50),
#     mass_function=lambda w: w / 20000
# )
# run_system(system)


# candidates_subreddits_graph = Graph(
#     ['JoeBiden', 'ElizabethW', 'SandersFor', 'BaemyKloba', 'YangForPre', 'the_donald'],
#     [('JoeBiden', 'ElizabethW', 0.05190205509400962), ('JoeBiden', 'YangForPre', 0.017636510208446442), ('ElizabethW', 'SandersFor', 0.036517381320316), ('ElizabethW', 'YangForPre', 0.031817025923322015), ('SandersFor', 'YangForPre', 0.054088774181547616), ('SandersFor', 'the_donald', 0.03731128913855287), ('BaemyKloba', 'YangForPre', 0.004462269434357668), ('BaemyKloba', 'the_donald', 0.0013517995517452787), ('YangForPre', 'the_donald', 0.019403920674720767)],
#     vertex_weights=[('JoeBiden', 8467), ('ElizabethW', 15590), ('SandersFor', 127949), ('BaemyKloba', 2212), ('YangForPre', 53388), ('the_donald', 197051)]
# )

# system = System.from_graph(
#     candidates_subreddits_graph,
#     k_function=lambda w: 2 ** (w * 50),
#     mass_function=lambda w: w**0.5 / 100
# )
# run_system(system)


politics_graph = Graph(
    ['worldpoli', 'politics', 'republica', 'democrats', 'obama', 'JoeBiden', 'Elizabeth', 'SandersFo', 'BaemyKlob', 'YangForPr', 'the_donal'],
    [('worldpoli', 'democrats', 0.029163533049218683), ('worldpoli', 'politics', 0.023612856269869063), ('politics', 'the_donal', 0.03617898194676051), ('politics', 'SandersFo', 0.015797700510611693), ('republica', 'democrats', 0.023824353783867953), ('republica', 'the_donal', 0.0109025347332697), ('democrats', 'SandersFo', 0.021058315334773217), ('democrats', 'the_donal', 0.005352199323285143), ('obama','Elizabeth', 0.007621951219512195), ('obama', 'BaemyKlob', 0.006198347107438017), ('JoeBiden', 'BaemyKlob', 0.008), ('JoeBiden', 'Elizabeth', 0.002352941176470588), ('Elizabeth', 'BaemyKlob', 0.008103727714748784), ('Elizabeth', 'YangForPr', 0.008077544426494346), ('SandersFo', 'the_donal', 0.0054911167260211285), ('SandersFo', 'YangForPr', 0.0010518934081346423), ('BaemyKlob', 'YangForPr', 0.006711409395973154), ('BaemyKlob', 'the_donal', 0.000331389183457052), ('YangForPr', 'the_donal', 0.0002429865252926883)],
    vertex_weights=[('worldpoli', 8345), ('politics', 140735), ('republica', 2604), ('democrats', 3971), ('obama', 263), ('JoeBiden', 28), ('Elizabeth', 398), ('SandersFo', 5484), ('BaemyKlob', 224), ('YangForPr', 226), ('the_donal', 45055)]
)

system = System.from_graph(
    politics_graph,
    k_function=lambda w: 2 ** (w * 50),
    mass_function=lambda w: w ** 0.2 / 3
)
run_system(system)
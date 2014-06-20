from collections import defaultdict
G = {
        0: [1, 2],
        1: [2, 3],
        2: [3],
        3: [2],
        4: [5],
        5: [2],
    }

pairs = defaultdict(int)

def find_all_paths(start, path=[]):
    path = path + [start]
    if len(path) > 1:
        current_length = pairs[(path[0], path[-1])]
        if current_length == 0:
            pairs[(path[0], path[-1])] = len(path) - 1
        else:
            pairs[(path[0], path[-1])] = min(len(path) - 1, current_length)
    for node in G[start]:
        if node not in path:
            find_all_paths(node, path)

for n in G:
    find_all_paths(n)
print pairs

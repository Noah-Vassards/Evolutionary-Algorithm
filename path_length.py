from graph import Graph
from TSP import GRAPH, GRAPH2, GRAPH3, GRAPH4
import sys

GRAPH: Graph
GRAPH2: Graph


def path_len(path):
    total_len = 0
    for i, vertex in enumerate(path):
        # print(vertex, path[(i + 1) % len(path)])
        # print(GRAPH2.get_edge_weight((vertex, path[(i + 1) % len(path)])))
        total_len += GRAPH2.get_edge_weight(
            (vertex, path[(i + 1) % len(path)]))
    return total_len

if __name__ == "__main__":
    file = sys.argv[1]

    with open(file, 'r') as f:
        content = f.read().split('\n')
        try:
            for line in content:
                (path, _, _, _) = eval(line)
                print(path_len(eval(path)))
        except SyntaxError:
            f.close()
            exit()

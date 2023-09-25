#!/usr/bin/env python3

from graph import Graph
from evolutionary import evolutionary, evolutionary2
    
GRAPH = Graph()
GRAPH2 = Graph()

GRAPH.add_vertex('A')
GRAPH.add_vertex('B')
GRAPH.add_vertex('C')
GRAPH.add_vertex('D')
GRAPH.add_vertex('E')
# GRAPH.add_vertex('F')

GRAPH.add_edge(('A', 'B'), 13)
GRAPH.add_edge(('B', 'C'), 30)
GRAPH.add_edge(('C', 'D'), 33)
GRAPH.add_edge(('D', 'A'), 66)
GRAPH.add_edge(('E', 'A'), 70)
GRAPH.add_edge(('E', 'B'), 55)
GRAPH.add_edge(('E', 'C'), 42)

GRAPH2.add_vertex('A')
GRAPH2.add_vertex('B')
GRAPH2.add_vertex('C')
GRAPH2.add_vertex('D')
GRAPH2.add_vertex('E')

GRAPH2.add_edge(('A', 'B'), 10)
GRAPH2.add_edge(('A', 'C'), 15)
GRAPH2.add_edge(('A', 'D'), 20)
GRAPH2.add_edge(('A', 'E'), 25)
GRAPH2.add_edge(('B', 'C'), 12)
GRAPH2.add_edge(('B', 'D'), 27)
GRAPH2.add_edge(('B', 'E'), 22)
GRAPH2.add_edge(('C', 'D'), 17)
GRAPH2.add_edge(('C', 'E'), 30)
GRAPH2.add_edge(('D', 'E'), 35)

# GRAPH.add_edge(('E', 'F'))
# GRAPH.add_edge(('F', 'A'))

print(GRAPH.get_verticies())
print(GRAPH.get_edges())
print()

# print(travel_graph(GRAPH, 'A', GOAL))
# print(naive(GRAPH))
def tsp(graph):
    print(evolutionary2(graph))
    print(end='')


if __name__ == "__main__":
    tsp(GRAPH2)

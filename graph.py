class Graph:
    def __init__(self) -> None:
        self.verticies = []
        self.edges = []
        self.weight = []

    def get_verticies(self):
        return [vertex for vertex in self.verticies]

    def get_vertex(self, value):
        for vertex in self.verticies:
            if vertex == value:
                return vertex
        return None

    def get_total_len(self):
        total = 0
        for len in self.weight:
            total += len
        return total

    def get_edge_weight(self, edge: tuple):
        a, b = edge
        for i, _edge in enumerate(self.edges):
            if (a, b) == _edge:
                return self.weight[i]
            if (b, a) == _edge:
                return self.weight[i]
        return -1
    
    def get_edge_weights(self):
        return self.weight

    def add_vertex(self, vertex):
        if vertex in self.verticies:
            return
        self.verticies.append(vertex)

    def add_edge(self, edge, weight):
        edge = set(edge)
        try:
            v1, v2 = tuple(edge)
        except ValueError:
            print('An edge must be a tuple of two different verticies')
            return
        self.add_vertex(v1)
        self.add_vertex(v2)
        if (v1, v2) not in self.edges and (v2, v1) not in self.edges:
            self.edges.append((v1, v2))
            self.weight.append(weight)

    def get_edges(self):
        return [(v1, v2) for (v1, v2) in self.edges]

    def get_neighbours(self, vertex):
        neighbours = []

        if vertex not in self.verticies:
            return []
        for i, (v1, v2) in enumerate(self.edges):
            if v1 == vertex:
                # print('adding', v2.value)
                neighbours.append((v2, self.weight[i]))
            if v2 == vertex:
                # print('adding', v1.value)
                neighbours.append((v1, self.weight[i]))
        # print(neighbours)
        return neighbours

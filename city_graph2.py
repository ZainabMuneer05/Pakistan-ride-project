class City:
    def __init__(self):
        self.locations = {}
    def add_road(self, u, v, weight):
        if u not in self.locations: self.locations[u] = {}
        if v not in self.locations: self.locations[v] = {}
        self.locations[u][v] = abs(weight)
        self.locations[v][u] = abs(weight)
    def get_shortest_path(self, start, end):
        distances = {node: float('inf') for node in self.locations}
        previous = {node: None for node in self.locations}
        distances[start] = 0
        nodes = list(self.locations.keys())
        while nodes:
            current = min(nodes, key=lambda n: distances[n])
            nodes.remove(current)
            if distances[current] == float('inf') or current == end: break
            for neighbor, weight in self.locations[current].items():
                alt = distances[current] + weight
                if alt < distances[neighbor]:
                    distances[neighbor] = alt
                    previous[neighbor] = current
        path, curr = [], end
        while curr:
            path.insert(0, curr)
            curr = previous[curr]
        return path, distances[end]
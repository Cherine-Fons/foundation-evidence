from dataclasses import dataclass


@dataclass
class Edge:
    u: int
    v: int
    multiplicity: int

@dataclass
class Multigraph:
    edges: list
    capacity: dict

    def degrees(self):
        degree = {}
        for e in self.edges:
            if e.u not in degree:
                degree[e.u] = e.multiplicity
            else:
                degree[e.u] = degree[e.u] + e.multiplicity
            if e.v not in degree:
                degree[e.v] = e.multiplicity
            else:
                degree[e.v] = degree[e.v] + e.multiplicity
        return degree    
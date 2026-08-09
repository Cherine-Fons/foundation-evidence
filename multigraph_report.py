from multigraph import Edge, Multigraph
import helpers

edges = [Edge(0, 1, 2), Edge(1, 2, 1), Edge(0, 2, 1)]
g = Multigraph(edges, {0: 3, 1: 2, 2: 2})

degrees = g.degrees()
over = helpers.find_over_capacity(degrees, g.capacity)

print("Degrees:", degrees)
print("Over capacity:", over)
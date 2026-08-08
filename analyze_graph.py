import read_edges
import helpers

good_edges, bad_rows = read_edges.parse_edge_file("edges.txt")
degrees = helpers.count_degrees(good_edges)
print("=== Graph Analysis Report ===")
print(f"Valid edges: {len(good_edges)}")
print(f"Invalid rows: {len(bad_rows)}")
print(f"Degrees: {degrees}")
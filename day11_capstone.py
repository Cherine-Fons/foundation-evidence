positions = [
    {"ticker": "AAPL", "quantity": 10, "price": 150},
    {"ticker": "MSFT", "quantity": 5, "price": 400},
    {"ticker": "NVDA", "quantity": 8, "price": 120},
]
def total_value(positions):
    total = 0
    for p in positions:
        total = total + p["quantity"] * p["price"]
    return total
print(total_value(positions))

def above_threshold(positions, threshold):
    result = []
    for p in positions:
        value = p["quantity"] * p["price"]
        if value > threshold:
            result.append(p["ticker"])
    return result

print(above_threshold(positions, 1500))

edges = [(0, 1), (0, 1), (1, 2), (2, 3), (1, 3)]
# degree convention: each edge (u, v) adds 1 to u's degree and 1 to v's degree
degree = {}
for u, v in edges:
    if u not in degree:
        degree[u] = 1
    else:
        degree[u] = degree[u] + 1
    if v not in degree:
        degree[v] = 1
    else:
        degree[v] = degree[v] + 1
print(degree)

# capacity f[v]: the maximum degree vertex v is allowed
f = {0: 3, 1: 3, 2: 2, 3: 5}
# a vertex is over capacity when its degree strictly exceeds f[v]
over = []
for v in degree:
    if degree[v] > f[v]:
        over.append(v)
print(over)
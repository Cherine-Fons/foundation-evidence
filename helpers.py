def count_degrees(edges):
    degree = {}
    for u , v in edges:
        if u not in degree:
            degree[u] = 1
        else:
            degree[u] = degree[u] + 1
        if v not in degree:
            degree[v] = 1
        else:
            degree[v] = degree[v] + 1
    return degree

def abs_diffs(values):
    diffs = []
    for i in range(1, len(values)):
        diffs.append(abs(values[i] - values[i - 1]))
    return diffs    
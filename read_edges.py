good_edges = []
bad_rows = []

with open("edges.txt") as f:
    for line in f:
        line = line.strip()
        try:
            parts = line.split(",")
            if len(parts) != 2:
                raise ValueError("wrong number of fields")
            u = int(parts[0])
            v = int(parts[1])
            good_edges.append((u, v))
        except (ValueError, IndexError):
            bad_rows.append(line)

print("Good edges:", good_edges)
print("Bad rows:", bad_rows)
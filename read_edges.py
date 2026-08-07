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

total = len(good_edges) + len(bad_rows)
print("=== Edge File Validation Report ===")
print(f"Total rows read: {total}")
print(f"Valid edges:     {len(good_edges)}")
print(f"Invalid rows:    {len(bad_rows)}")
if bad_rows:
    print("Bad rows:")
    for row in bad_rows:
        print(f"  - {row}")
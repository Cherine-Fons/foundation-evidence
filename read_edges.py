with open("edges.txt") as f:
    for line in f:
        line = line.strip()
        parts = line.split(",")
        u = int(parts[0])
        v = int(parts[1])
        print((u, v))
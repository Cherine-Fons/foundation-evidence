exercises = [ "squats" , "bench" , "deadlifts" ]
for name in exercises:
    print(name)

sets = [ 3, 4, 5, 3 ]
total = 0
for count in sets:
    total = total + count
    print(total)

volumes = [1000, 1100, 1050, 1200]
abs_diffs = []
for i in range(1, len(volumes)):
    diff = abs(volumes[i] - volumes[i - 1])
    abs_diffs.append(diff)
print(abs_diffs)

volumes = [1000, 1100, 1050, 1200]
abs_diffs = []
pct_changes = []

for i in range(1, len(volumes)):
    diff = abs(volumes[i] - volumes[i - 1])
    abs_diffs.append(diff)
print(abs_diffs)

for i in range(1, len(volumes)):
    pct = (volumes[i] - volumes[i - 1]) / volumes[i - 1] * 100
    pct_changes.append(pct)
print(pct_changes)

weekly = [1000, 1100, 1050, 1200]
for i in range(len(weekly)):
    print(f"Week {i + 1}: {weekly[i]}")
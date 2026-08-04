# Write the loop building total_sets (exercise → summed sets), your paper prediction first, then run.

{'squat': 5, 'bench': 7, 'deadlift': 1}
sets_by_exercise = [
    ("squat", 3),
    ("bench", 4),
    ("squat", 2),
    ("deadlift", 1),
    ("bench", 3),
]

total_sets = {}

for exercise, sets in sets_by_exercise:
    if exercise not in total_sets:
        total_sets[exercise] = sets
    else:
        total_sets[exercise] = total_sets[exercise] + sets

print(total_sets)
# Write the loop building total_sets (exercise → summed sets), your paper prediction first, then run.
# data: sessions = [
#  {"exercise": "squat", "sets": 5},
#  {"exercise": "bench", "sets": 3}
#  {"exercise": "squat", "sets": 4},
#  {"exercise": "row", "sets": 3},
#  {"exercise": "bench", "sets": 2},
# ]

sessions = [
    {"exercise": "squat", "sets": 5},
    {"exercise": "bench", "sets": 3},
    {"exercise": "squat", "sets": 4},
    {"exercise": "row", "sets": 3},
    {"exercise": "bench", "sets": 2},
]

total_sets = {}

for session in sessions:
    exercise = session["exercise"]
    sets = session["sets"]

    if exercise not in total_sets:
        total_sets[exercise] = sets
    else:
        total_sets[exercise] = total_sets[exercise] + sets

print(total_sets)
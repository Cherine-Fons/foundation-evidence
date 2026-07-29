loads = [100, 105, 130, 98, 75]
target = 100
threshold = 20
for load in loads:
    deviation = abs(load - target)
    if deviation > threshold:
        print(f"FLAG: {load} is {deviation} off target")


readings = [80, 85, 90, None, 100, 105]
for r in readings:
    if r is None:
        break
    print(r)


exercises = ["squat", "bench", "deadlift"]
for i, name in enumerate(exercises):
    print(i, name)            


names = ["squat", "bench", "deadlift"]
weights = [100, 80, 120]
for name, w in zip(names, weights):
    print(f"{name}: {w}kg")


names = ["squat", "bench", "deadlift", "row"]
weights = [100, 80]
for name, w in zip(names, weights):
    print(f"{name}: {w}kg")


# cap: stop as soon as cumulative tonnage would exceed 5000 kg
lifts = [1200, 1500, 1800, 2000, 900]
cap = 5000
total = 0
for lift in lifts:
    if total + lift > cap:
        break
    total = total + lift
    print(f"Added {lift}, total now {total}")


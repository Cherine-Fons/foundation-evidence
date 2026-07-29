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
    

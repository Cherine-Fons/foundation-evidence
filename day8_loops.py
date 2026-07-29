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
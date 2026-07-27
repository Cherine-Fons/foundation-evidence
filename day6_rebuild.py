
def epley_1rm(weight, reps):
    """Estimate a one-repetition maximum using the Epley formula"""
    return weight * (1 + reps / 30)

def classify_intensity(pct_1rm):
    """Return the intensity label (light/moderate/heavy) for a percentage of 1RM.
    Boundaries closed on both ends: moderate is [70, 85]"""
    if pct_1rm  >  85:
        return "heavy"
    elif pct_1rm  >=  70:
        return "moderate"
    else:
        return "light"

def is_admissible(a, b):
    """Return True when a + b is even and a is less than or equal to b; otherwise, return False"""
    return (a + b) % 2 == 0 and a <= b
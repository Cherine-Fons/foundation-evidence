def kg_to_lb(kg):
    """Convert kilograms to pounds"""
    return kg * 2.2046

def volume(sets, reps, weight):
    """Compute training volume"""
    return sets * reps * weight


def session_line(exercise, sets, reps, weight):
    """Return a formatted training-log line for one exercise"""
    return f"{exercise} volume: {volume(sets, reps, weight)}"


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


def can_promote(current_rank, years_at_rank):
    """Check whether a practitioner is eligible for promotion based on their current belt and years at that rank. Use 
    2 years for white and brown belts, and 3 years for blue and purple belts; exact boundary years count as eligible. 
    Return False for black belts or any rank that does not meet the required time"""
    if current_rank == "white" and  years_at_rank  >= 2:
        return True
    elif current_rank == "blue" and  years_at_rank  >= 3:
        return True
    elif current_rank == "purple" and  years_at_rank  >= 3:
        return True
    elif current_rank == "brown" and years_at_rank >= 2:
        return True
    else:
        return False

def is_admissible(a, b):
    """Return True when a + b is even and a is less than or equal to b; otherwise, return False"""
    return (a + b) % 2 == 0 and a <= b

def plan_next_session(last_volume, felt_difficulty):
    """Adjust the next session's volume based on how the last session felt. Use "easy" to increase volume by 5%, "ok" to keep it unchanged,
    and "hard" to reduce it by 10%"""
    if felt_difficulty == "easy":
        return last_volume * 1.05
    elif felt_difficulty == "ok":
        return last_volume * 1.0
    elif felt_difficulty == "hard":
        return last_volume * 0.90

def format_set(exercise, sets, reps, weight, pct_1rm):
    """Take an exercise, sets, reps, weight, and percentage of 1RM, and return them as a formatted workout-set string"""
    intensity = classify_intensity(pct_1rm)
    return f"{exercise}: {sets}×{reps} @ {weight} — {intensity}"

def tempo_seconds(reps, seconds_per_rep):
    """Return total time under tension, or "invalid" for non-positive inputs."""
    if reps <= 0 or seconds_per_rep <= 0:
        return "invalid"

    return reps * seconds_per_rep


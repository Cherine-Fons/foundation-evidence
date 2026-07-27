def tempo_seconds(reps, seconds_per_rep):
    """Return total time under tension, or "invalid" for non-positive inputs."""
    if reps <= 0 or seconds_per_rep <= 0:
        return "invalid"

    return reps * seconds_per_rep
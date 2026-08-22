
# ==================================================================================================
# MOCK EXIT 1 — CREW-ASSIGNMENT INSTANCE
# ==================================================================================================
#
# PURPOSE:
#
# Store the fixed Crew-Assignment Density instance and validate the
# graph-level assumptions required by every later checker component.
#
#
# THIS MODULE CONTAINS:
#
# 1. WORKERS
# 2. SHIFTS
# 3. SKILL_VALUES
# 4. validate_instance()
#
#
# RESPONSIBILITY BOUNDARY:
#
# This module validates the INSTANCE.
#
# It does NOT:
#
#     - judge candidate admissibility,
#     - evaluate the objective,
#     - enumerate candidate pairs,
#     - search for a maximizer.
#
# Those responsibilities belong to later modules.
#
#
# MODULE BEHAVIOR:
#
# This file is intentionally silent.
#
# Importing or directly executing it defines data and functions without
# printing or automatically running validation.
#
# ==================================================================================================


# ==================================================================================================
# WORKERS
# ==================================================================================================
#
# The fixed worker set is:
#
#     {a, b, c, d}
#
# A frozenset is used because:
#
#     - workers form a mathematical set,
#     - order is not mathematically significant,
#     - duplicates should not exist,
#     - membership checks are natural,
#     - the fixed instance should not accidentally mutate this set.
#
# ==================================================================================================


WORKERS = frozenset({"a", "b", "c", "d"})


# ==================================================================================================
# SHIFTS
# ==================================================================================================
#
# Every physical shift copy has the form:
#
#     (shift_id, worker1, worker2)
#
# The fixed instance contains:
#
#     s0 = (a, b)
#     s1 = (a, b)    parallel copy of s0
#     s2 = (b, c)
#     s3 = (c, d)
#
# A list is used because:
#
#     - every physical shift copy remains present,
#     - parallel copies remain distinct,
#     - stable input order is preserved.
#
# IMPORTANT:
#
#     s0 and s1 have the same endpoints,
#
# but:
#
#     s0 != s1
#
# because they are distinct physical shifts.
#
# Parallel copies therefore have:
#
#     same endpoints
#     different IDs
#
# ==================================================================================================


SHIFTS = [
    ("s0", "a", "b"),
    ("s1", "a", "b"),
    ("s2", "b", "c"),
    ("s3", "c", "d"),
]


# ==================================================================================================
# SKILL VALUES
# ==================================================================================================
#
# Skill is a positive-integer function on workers:
#
#     a -> 1
#     b -> 1
#     c -> 2
#     d -> 2
#
# A dictionary represents:
#
#     worker -> skill value
#
# ==================================================================================================


SKILL_VALUES = {
    "a": 1,
    "b": 1,
    "c": 2,
    "d": 2,
}


# ==================================================================================================
# VALIDATE INSTANCE
# ==================================================================================================
#
# PURPOSE:
#
# Reject malformed fixed-instance data before any downstream computation
# is trusted.
#
#
# FAILURE CONTRACT:
#
#     invalid instance -> raise ValueError immediately
#
# The validator is fail-fast:
#
#     the first discovered violation stops execution.
#
# Each failure message names the offending shift or worker whenever there
# is a specific culprit.
#
#
# CHECK 1 — NONEMPTY WORKER SET
#
# Require:
#
#     WORKERS != empty
#
#
# CHECK 2 — NO SELF-PAIRING
#
# Every shift:
#
#     (shift_id, worker1, worker2)
#
# must satisfy:
#
#     worker1 != worker2
#
# Example invalid shift:
#
#     ("s3", "c", "c")
#
#
# CHECK 3 — KNOWN SHIFT ENDPOINTS
#
# Every endpoint appearing in SHIFTS must belong to WORKERS.
#
# Require:
#
#     worker1 in WORKERS
#     worker2 in WORKERS
#
# Example invalid shift:
#
#     ("s3", "c", "x")
#
# where:
#
#     "x" not in WORKERS
#
#
# CHECK 4 — UNIQUE SHIFT IDs
#
# Every physical shift copy must have its own unique ID.
#
# Parallel shifts may have:
#
#     the same endpoints
#
# but must have:
#
#     different IDs.
#
# The uniqueness check uses a seen-set walk:
#
#     seen_shift_ids = set()
#
# For every shift ID:
#
#     if the ID has already been seen:
#         raise ValueError
#
#     otherwise:
#         add the ID to seen_shift_ids
#
# This is a representation invariant.
#
# Later, fringe shifts and candidate S values will represent physical
# shift copies by ID.
#
# Duplicate IDs could therefore cause two distinct physical shifts to
# collapse into one element of a frozenset, silently corrupting |S|.
#
#
# CHECK 5 — POSITIVE INTEGER SKILL VALUES
#
# Every worker must have a skill value.
#
# Every skill value must satisfy:
#
#     type(skill_value) is int
#
# and:
#
#     skill_value > 0
#
# Exact type comparison deliberately rejects Boolean values.
#
#
# IMPORTANT NON-CHECK:
#
# There is NO skill-versus-degree condition in the Crew-Assignment
# Density specification.
#
# The F7 capstone assumption:
#
#     f(v) <= d(v)
#
# must not be imported into this problem.
#
# ==================================================================================================


def validate_instance():
    # Check 1 — the worker set must be nonempty.
    if not WORKERS:
        raise ValueError("WORKERS must be nonempty")

    # Check 2 — no shift may pair a worker with themselves.
    for shift_id, worker1, worker2 in SHIFTS:
        if worker1 == worker2:
            raise ValueError(
                f"shift {shift_id} self-pairs worker {worker1!r}"
            )

    # Check 3 — every shift endpoint must be a known worker.
    for shift_id, worker1, worker2 in SHIFTS:
        if worker1 not in WORKERS:
            raise ValueError(
                f"shift {shift_id} has unknown worker {worker1!r}"
            )

        if worker2 not in WORKERS:
            raise ValueError(
                f"shift {shift_id} has unknown worker {worker2!r}"
            )

    # Check 4 — every physical shift copy must have a unique shift ID.
    seen_shift_ids = set()

    for shift_id, _worker1, _worker2 in SHIFTS:
        if shift_id in seen_shift_ids:
            raise ValueError(f"duplicate shift ID {shift_id!r}")

        seen_shift_ids.add(shift_id)

    # Check 5 — every worker must have a positive integer skill value.
    for worker in WORKERS:
        if worker not in SKILL_VALUES:
            raise ValueError(f"missing skill value for worker {worker!r}")

        skill_value = SKILL_VALUES[worker]

        if type(skill_value) is not int or skill_value <= 0:
            raise ValueError(
                f"skill({worker}) must be a positive integer, "
                f"got {skill_value!r}"
            )
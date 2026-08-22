
# ==================================================================================================
# MOCK EXIT 1 — MATHEMATICAL PRIMITIVES
# ==================================================================================================
#
# PURPOSE:
#
# Implement the small mathematical quantities that later checker layers
# depend on.
#
#
# THE THREE PRIMITIVES ARE:
#
#     1. skill_of(W)
#     2. internal_shift_count(W)
#     3. fringe(W)
#
#
# RESPONSIBILITY BOUNDARY:
#
# These functions compute mathematical quantities associated with a crew W.
#
# They do NOT decide whether a candidate pair (W, S) is admissible.
#
# For example:
#
#     skill_of(empty crew) = 0
#     internal_shift_count(empty crew) = 0
#     fringe(empty crew) = []
#
# even though the later admissibility predicate rejects an empty crew.
#
#
# QUERY VALIDATION:
#
# validate_instance() protects the STORED instance.
#
# These primitives separately reject query crews containing workers
# outside WORKERS.
#
# ==================================================================================================


from mock_instance import SHIFTS, SKILL_VALUES, WORKERS

# ==================================================================================================
# PRIMITIVE 1 — skill_of(W)
# ==================================================================================================
#
# MATHEMATICAL DEFINITION:
#
#     skill(W) = sum of skill(w) over every worker w in W
#
#
# INPUT:
#
#     W
#
# A collection of workers.
#
#
# OUTPUT:
#
#     an integer equal to skill(W)
#
#
# QUERY CONTRACT:
#
# Every worker supplied in W must belong to WORKERS.
#
# Example invalid query:
#
#     W = {"a", "x"}
#
# should raise:
#
#     ValueError: W contains unknown worker 'x'
#
#
# EMPTY-CREW BEHAVIOR:
#
#     skill(empty set) = 0
#
# The primitive does not enforce the later admissibility requirement
# that W be nonempty.
#
#
# COMMENTS-FIRST ALGORITHM:
#
# 1. Start:
#
#        total = 0
#
# 2. For every worker in W:
#
#        verify worker belongs to WORKERS
#
#        if not:
#            raise ValueError naming that worker
#
#        otherwise:
#            add SKILL_VALUES[worker] to total
#
# 3. Return total.
#
#
# HAND-DERIVED PREDICTIONS:
#
#     skill_of({"a", "b", "c"}) = 4
#
#     skill_of({"b", "d"}) = 3
#
#     skill_of(WORKERS) = 6
#
#     skill_of(empty set) = 0
#
# ==================================================================================================


def skill_of(W):
    total = 0

    for worker in W:
        if worker not in WORKERS:
            raise ValueError(f"W contains unknown worker {worker!r}")

        total += SKILL_VALUES[worker]

    return total


# ==================================================================================================
# PRIMITIVE 2 — internal_shift_count(W)
# ==================================================================================================
#
# MATHEMATICAL DEFINITION:
#
#     i(W)
#
# is the number of PHYSICAL SHIFT COPIES whose two endpoints both belong
# to W.
#
#
# INTERNAL-SHIFT CONDITION:
#
# For a physical shift:
#
#     (shift_id, worker1, worker2)
#
# the shift is internal exactly when:
#
#     worker1 in W
#
# AND:
#
#     worker2 in W
#
# In Python:
#
#     worker1 in W and worker2 in W
#
#
# MULTIGRAPH / PARALLEL-COPY RULE:
#
# Parallel shifts count separately.
#
# The fixed instance contains:
#
#     s0 = (a, b)
#     s1 = (a, b)
#
# For:
#
#     W = {a, b}
#
# both physical copies are internal.
#
# Therefore:
#
#     i({a,b}) = 2
#
# This happens naturally because SHIFTS stores s0 and s1 as separate
# list entries and this function scans every entry.
#
#
# SHIFT-ID FIELD:
#
# Internal membership depends on the endpoints rather than the shift ID.
#
# The loop therefore names the first tuple field:
#
#     _shift_id
#
# The leading underscore communicates that the field exists but is
# intentionally unused in this computation.
#
#
# QUERY CONTRACT:
#
# Every worker supplied in W must belong to WORKERS.
#
#
# EMPTY-CREW BEHAVIOR:
#
# No shift can have both endpoints in the empty set.
#
# Therefore:
#
#     i(empty set) = 0
#
#
# COMMENTS-FIRST ALGORITHM:
#
# 1. Verify every worker in W belongs to WORKERS.
#
# 2. Start:
#
#        count = 0
#
# 3. Scan every physical shift copy:
#
#        (shift_id, worker1, worker2)
#
# 4. Ask:
#
#        worker1 in W AND worker2 in W ?
#
# 5. If yes:
#
#        count += 1
#
# 6. Return count.
#
#
# HAND-DERIVED PREDICTIONS:
#
#     internal_shift_count({"a", "b"}) = 2
#
#     internal_shift_count({"a", "b", "c"}) = 3
#
#     internal_shift_count({"b", "c"}) = 1
#
#     internal_shift_count({"a", "c"}) = 0
#
#     internal_shift_count(WORKERS) = 4
#
#     internal_shift_count(empty set) = 0
#
# ==================================================================================================


def internal_shift_count(W):
    for worker in W:
        if worker not in WORKERS:
            raise ValueError(f"W contains unknown worker {worker!r}")

    count = 0

    for _shift_id, worker1, worker2 in SHIFTS:
        if worker1 in W and worker2 in W:
            count += 1

    return count


# ==================================================================================================
# PRIMITIVE 3 — fringe(W)
# ==================================================================================================
#
# MATHEMATICAL DEFINITION:
#
#     ∂(W)
#
# is the collection of PHYSICAL SHIFT COPIES having exactly one endpoint
# inside W.
#
#
# FRINGE CONDITION:
#
# For:
#
#     (shift_id, worker1, worker2)
#
# define the two membership statements:
#
#     worker1 in W
#     worker2 in W
#
# A shift is on the fringe exactly when those two Boolean values differ.
#
# In Python:
#
#     (worker1 in W) != (worker2 in W)
#
#
# BOOLEAN / XOR INTERPRETATION:
#
#     True  != True   -> False
#     False != False  -> False
#     True  != False  -> True
#     False != True   -> True
#
# Therefore:
#
#     both inside   -> not fringe
#     both outside  -> not fringe
#     exactly one inside -> fringe
#
#
# INTERNAL VERSUS FRINGE:
#
#     internal:
#         both endpoints inside
#         AND condition
#
#     fringe:
#         exactly one endpoint inside
#         XOR condition
#
#
# RETURN REPRESENTATION:
#
# fringe(W) returns a LIST OF SHIFT IDs.
#
# Example:
#
#     ["s0", "s1", "s2"]
#
# rather than full:
#
#     (shift_id, worker1, worker2)
#
# triples.
#
#
# WHY SHIFT IDs:
#
# The later candidate S is represented as a set of physical shift IDs.
#
# The future evaluator uses:
#
#     |S|
#
# rather than the selected shifts' endpoints.
#
# Returning IDs therefore aligns the primitive directly with the
# downstream candidate representation.
#
#
# WHY A LIST:
#
# SHIFTS has stable list order:
#
#     s0, s1, s2, s3
#
# fringe(W) scans that list in order and appends matching IDs.
#
# Therefore the returned fringe list inherits deterministic order.
#
# Later:
#
#     itertools.combinations(...)
#
# will preserve that input order while enumerating every subset S.
#
# This gives a deterministic search order, which is necessary for the
# contract:
#
#     first encountered maximizer wins ties.
#
#
# PARALLEL SHIFT COPIES:
#
# For:
#
#     W = {b}
#
# both:
#
#     s0 = (a,b)
#     s1 = (a,b)
#
# are fringe shifts.
#
# Since their IDs are different, the result contains both:
#
#     ["s0", "s1", "s2"]
#
# Physical parallel-copy identity is therefore preserved.
#
#
# QUERY CONTRACT:
#
# Every worker supplied in W must belong to WORKERS.
#
# Example invalid query:
#
#     W = {"c", "x"}
#
# should raise:
#
#     ValueError: W contains unknown worker 'x'
#
#
# EMPTY-CREW BEHAVIOR:
#
# For the empty crew, every shift has both endpoints outside.
#
# Therefore:
#
#     fringe(empty set) = []
#
#
# FULL-CREW BEHAVIOR:
#
# For W = WORKERS, every shift has both endpoints inside.
#
# Therefore:
#
#     fringe(WORKERS) = []
#
#
# COMMENTS-FIRST ALGORITHM:
#
# 1. Verify every worker in W belongs to WORKERS.
#
# 2. Start:
#
#        crossing_shift_ids = []
#
# 3. Scan every physical shift copy in SHIFTS.
#
# 4. For each:
#
#        (shift_id, worker1, worker2)
#
#    evaluate:
#
#        (worker1 in W) != (worker2 in W)
#
# 5. If True:
#
#        append shift_id
#
# 6. Return crossing_shift_ids.
#
#
# HAND-DERIVED PREDICTIONS:
#
#     fringe({"a", "b"})
#
#         = ["s2"]
#
#
#     fringe({"b"})
#
#         = ["s0", "s1", "s2"]
#
#
#     fringe({"a", "c"})
#
#         = ["s0", "s1", "s2", "s3"]
#
#
#     fringe({"a", "b", "c"})
#
#         = ["s3"]
#
#
#     fringe({"b", "c", "d"})
#
#         = ["s0", "s1"]
#
#
#     fringe(WORKERS)
#
#         = []
#
#
#     fringe(empty set)
#
#         = []
#
# ==================================================================================================


def fringe(W):
    for worker in W:
        if worker not in WORKERS:
            raise ValueError(f"W contains unknown worker {worker!r}")

    crossing_shift_ids = []

    for shift_id, worker1, worker2 in SHIFTS:
        if (worker1 in W) != (worker2 in W):
            crossing_shift_ids.append(shift_id)

    return crossing_shift_ids
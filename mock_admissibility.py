
# ==================================================================================================
# MOCK EXIT 1 — CANDIDATE ADMISSIBILITY
# ==================================================================================================
#
# PURPOSE:
#
# Decide whether a candidate pair:
#
#     (W, S)
#
# is admissible for the Crew-Assignment Density optimization problem.
#
#
# A candidate consists of:
#
#     W
#         a crew of workers
#
#     S
#         a collection of physical shift IDs
#
#
# PREDICATE CONTRACT:
#
# This function returns:
#
#     True
#
# when every admissibility condition holds, and:
#
#     False
#
# otherwise.
#
# An inadmissible candidate is normal search behavior.
#
# Therefore:
#
#     inadmissible candidate -> False
#
# rather than:
#
#     inadmissible candidate -> raise exception
#
#
# CONTRAST WITH OTHER LAYERS:
#
#     malformed fixed instance
#         -> validate_instance() raises ValueError
#
#     invalid primitive query
#         -> primitive raises ValueError
#
#     candidate failing admissibility
#         -> is_admissible() returns False
#
#
# ==================================================================================================


from mock_instance import WORKERS
from mock_primitives import fringe, skill_of

# ==================================================================================================
# is_admissible(W, S)
# ==================================================================================================
#
# MATHEMATICAL CONDITIONS — LOCKED ORDER:
#
# CONDITION 1:
#
#     W is nonempty
#
# and:
#
#     W subseteq WORKERS
#
#
# CONDITION 2:
#
#     S subseteq fringe(W)
#
#
# CONDITION 3:
#
#     skill(W) + |S|
#
# is EVEN.
#
#
# CONDITION 4:
#
#     skill(W) + |S| >= 4
#
#
# IMPORTANT:
#
# These are NOT the F7 capstone conditions.
#
# This mock uses:
#
#     EVEN parity
#     lower bound 4
#
# Do not pattern-replay:
#
#     odd
#     lower bound 3
#
#
# ==================================================================================================
# REPRESENTATION DECISIONS
# ==================================================================================================
#
# W:
#
#     converted to frozenset
#
# because W is mathematically a set of workers.
#
#
# S:
#
#     mathematically a set of physical shift IDs.
#
# The search will later generate S as frozenset values.
#
# However, this predicate deliberately handles callers that supply a
# more general collection.
#
#
# DUPLICATE-ID CONTRACT:
#
# A physical shift ID cannot occur twice in mathematical S.
#
# For example:
#
#     ["s0", "s0"]
#
# is rejected.
#
# Parallel copies instead have different IDs:
#
#     "s0"
#     "s1"
#
# and may both be selected.
#
#
# DUPLICATES MUST BE CHECKED BEFORE SET CONVERSION:
#
# If we immediately wrote:
#
#     frozenset(["s0", "s0", "s1"])
#
# the result would be:
#
#     frozenset({"s0", "s1"})
#
# and evidence of the duplicate would be destroyed.
#
# Therefore:
#
#     S_items = list(S)
#
# is created first.
#
# Then:
#
#     len(S_items)
#
# is compared with:
#
#     len(set(S_items))
#
# A difference means the supplied collection contained a repeated ID.
#
#
# ==================================================================================================
# COMMENTS-FIRST ALGORITHM
# ==================================================================================================
#
# 1. Convert W to a frozenset:
#
#        W_set = frozenset(W)
#
#
# 2. CONDITION 1:
#
#        require W_set to be nonempty
#
#        require W_set subseteq WORKERS
#
#    otherwise:
#
#        return False
#
#
# 3. Preserve the supplied S items long enough to detect duplicates:
#
#        S_items = list(S)
#
#
# 4. If the same shift ID occurs more than once:
#
#        return False
#
#
# 5. Convert the duplicate-free supplied S to:
#
#        S_set = frozenset(S_items)
#
#
# 6. CONDITION 2:
#
#        compute fringe(W_set)
#
#        convert that fringe list to a frozenset
#
#        require:
#
#            S_set subseteq fringe_set
#
#    otherwise:
#
#        return False
#
#
# 7. Compute:
#
#        total = skill_of(W_set) + len(S_set)
#
#
# 8. CONDITION 3:
#
#        require total to be EVEN
#
#    If total is odd:
#
#        return False
#
#
# 9. CONDITION 4:
#
#        require total >= 4
#
#    otherwise:
#
#        return False
#
#
# 10. If every guard passed:
#
#        return True
#
#
# ==================================================================================================
# HAND-DERIVED PREDICTIONS
# ==================================================================================================
#
# ACCEPTANCE:
#
#     W = {"a", "b", "c"}
#     S = empty
#
#     skill(W) = 4
#     |S| = 0
#     total = 4
#
#     all four conditions pass
#
#     expected -> True
#
#
# CONDITION 1 REJECTION:
#
#     W = empty
#     S = empty
#
#     expected -> False
#
#
# CONDITION 2 REJECTION:
#
#     W = {"a", "b", "c"}
#     S = {"s0"}
#
#     fringe(W) = {"s3"}
#
#     s0 is an existing shift but is internal rather than fringe
#
#     expected -> False
#
#
# CONDITION 3 REJECTION:
#
#     W = {"a", "b", "c"}
#     S = {"s3"}
#
#     S is a valid fringe subset
#
#     skill(W) + |S|
#         = 4 + 1
#         = 5
#
#     5 is odd
#
#     expected -> False
#
#
# CONDITION 4 REJECTION:
#
#     W = {"a"}
#     S = {"s0"}
#
#     fringe({"a"}) = {"s0", "s1"}
#
#     so Conditions 1 and 2 pass.
#
#     skill(W) + |S|
#         = 1 + 1
#         = 2
#
#     2 is even, so Condition 3 passes.
#
#     But:
#
#         2 < 4
#
#     so Condition 4 alone rejects.
#
#     expected -> False
#
#
# DUPLICATE-S REJECTION:
#
#     W = {"b"}
#
#     S supplied as:
#
#         ["s0", "s0", "s1", "s2"]
#
#     repeated "s0" violates the supplied-S representation contract
#
#     expected -> False
#
# ==================================================================================================


def is_admissible(W, S):
    # Canonical mathematical representation of the crew.
    W_set = frozenset(W)

    # Condition 1 — W must be nonempty and contained in WORKERS.
    if not W_set:
        return False

    if not W_set.issubset(WORKERS):
        return False

    # S is mathematically a set of physical shift IDs.
    #
    # Preserve the supplied collection long enough to detect repeated IDs
    # before converting it to a frozenset.
    S_items = list(S)

    if len(S_items) != len(set(S_items)):
        return False

    S_set = frozenset(S_items)

    # Condition 2 — every selected shift must lie on the fringe of W.
    fringe_set = frozenset(fringe(W_set))

    if not S_set.issubset(fringe_set):
        return False

    # Conditions 3 and 4 use the same total.
    total = skill_of(W_set) + len(S_set)

    # Condition 3 — skill(W) + |S| must be EVEN.
    if total % 2 != 0:
        return False

    # Condition 4 — skill(W) + |S| must be at least 4.
    #
    # The explicit fourth guard deliberately mirrors the numbered
    # mathematical definition, so SIM103 is locally declined.
    if total < 4:  # noqa: SIM103
        return False

    # All four mathematical admissibility conditions hold.
    return True
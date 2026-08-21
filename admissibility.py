# ==================================================================================================
# F7 CAPSTONE — PAIR ADMISSIBILITY
# ==================================================================================================
#
# PURPOSE:
#
# Decide whether a candidate pair:
#
#     (U, F)
#
# belongs to the admissible family A(G).
#
# The four conditions are:
#
#     1. U is nonempty and U ⊆ V(G)
#
#     2. F ⊆ ∂_G(U)
#
#     3. f(U) + |F| is odd
#
#     4. f(U) + |F| >= 3
#
#
# IMPORTANT CONTRACT DISTINCTION:
#
# validate_instance()
#     -> validates the graph itself
#     -> invalid graph data raises ValueError
#
# is_admissible(U, F)
#     -> evaluates an ordinary candidate pair
#     -> inadmissibility is expected during enumeration
#     -> returns True or False
#
# ==================================================================================================


from instance import VERTICES
from primitives import boundary, f_of

# ==================================================================================================
# is_admissible(U, F)
# ==================================================================================================
#
# INPUT:
#
#     U
#         collection of vertices
#
#     F
#         collection of edge-copy IDs
#
#
# CANONICAL REPRESENTATION:
#
# Later enumeration will represent candidates as:
#
#     U = frozenset({...})
#     F = frozenset({...})
#
# A frozenset is appropriate because U and F are mathematical sets:
#
#     order does not matter
#     duplicate elements do not exist
#     the objects should not mutate while being evaluated
#
#
# DUPLICATE EDGE-ID RULE:
#
# F cannot contain the same edge ID twice.
#
# For example:
#
#     ["e2", "e2"]
#
# is not a valid representation of a two-edge set.
#
# There is only one edge copy named e2.
#
# Parallel copies instead have different identities:
#
#     e0
#     e1
#
# so:
#
#     frozenset({"e0", "e1"})
#
# is perfectly valid.
#
#
# COMMENTS-FIRST ALGORITHM:
#
# CONDITION 1:
#
#     Convert U to a frozenset.
#
#     Require:
#
#         U != empty
#
#     and:
#
#         U ⊆ VERTICES
#
#     Otherwise:
#
#         return False
#
#
# CONDITION 2:
#
#     First reject duplicate edge IDs if the supplied F collection
#     contains them.
#
#     Convert F to a frozenset.
#
#     Compute:
#
#         ∂_G(U)
#
#     Convert that boundary list to a set.
#
#     Require:
#
#         F ⊆ ∂_G(U)
#
#     Otherwise:
#
#         return False
#
#
# CONDITION 3:
#
#     Compute:
#
#         total = f(U) + |F|
#
#     Require total to be odd.
#
#     Otherwise:
#
#         return False
#
#
# CONDITION 4:
#
#     Require:
#
#         total >= 3
#
#     Otherwise:
#
#         return False
#
#
# If all four conditions hold:
#
#     return True
#
# ==================================================================================================


def is_admissible(U, F):
    # Convert U to its mathematical set representation.
    U_set = frozenset(U)

    # Condition 1 — U must be nonempty and contained in V(G).
    if not U_set:
        return False

    if not U_set.issubset(VERTICES):
        return False

    # F is mathematically a set of edge copies.
    #
    # If the caller supplied something like:
    #
    #     ["e2", "e2"]
    #
    # reject it rather than allowing the duplicate to affect |F|.
    F_items = list(F)

    if len(F_items) != len(set(F_items)):
        return False

    F_set = frozenset(F_items)

    # Condition 2 — every selected edge copy must belong to ∂_G(U).
    boundary_set = frozenset(boundary(U_set))

    if not F_set.issubset(boundary_set):
        return False

    # Compute the quantity used by both remaining conditions.
    total = f_of(U_set) + len(F_set)

    # Condition 3 — f(U) + |F| must be odd.
    if total % 2 == 0:
        return False

    # Condition 4 — f(U) + |F| must be at least 3.
    if total < 3:  # noqa: SIM103
        return False

    # All four admissibility conditions hold.
    return True
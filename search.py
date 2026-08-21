# ==================================================================================================
# F7 CAPSTONE — EXHAUSTIVE SEARCH
# ==================================================================================================
#
# PURPOSE:
#
# Enumerate every candidate pair:
#
#     (U, F)
#
# where:
#
#     nonempty U ⊆ V(G)
#
# and:
#
#     F ⊆ ∂_G(U)
#
# Filter those candidates through:
#
#     is_admissible(U, F)
#
# evaluate every admissible pair exactly using:
#
#     density(U, F)
#
# and return a maximizer.
#
#
# RESULT CONTRACT:
#
# The search returns an immutable SearchResult with three named fields:
#
#     result.value
#     result.U
#     result.F
#
#
# If at least one admissible pair exists:
#
#     value = exact Fraction giving the maximum density
#     U     = frozenset of maximizing vertices
#     F     = frozenset of maximizing boundary-edge IDs
#
#
# If NO admissible pair exists:
#
#     value = Fraction(0, 1)
#     U     = None
#     F     = None
#
# The None values matter:
#
#     they mean there is no admissible maximizing pair to report.
#
# We do NOT use:
#
#     U = frozenset()
#     F = frozenset()
#
# because that would look like the actual pair (empty set, empty set),
# and empty U is inadmissible.
#
#
# TIE CONTRACT:
#
# If multiple admissible pairs attain the same maximum value,
# keep the FIRST one encountered.
#
# Therefore the best result is replaced only when:
#
#     new_value > best.value
#
# not when:
#
#     new_value >= best.value
#
#
# DETERMINISM:
#
# VERTICES is a frozenset, so its iteration order is not the search order.
#
# Before enumeration we use:
#
#     sorted(VERTICES)
#
# itertools.combinations preserves the order of its input.
#
# boundary(U) also returns edge IDs in stable EDGES order.
#
# Therefore both the U-enumeration and F-enumeration are deterministic,
# which also makes the "first maximizer wins" tie rule deterministic.
#
# ==================================================================================================


import itertools
from dataclasses import dataclass
from fractions import Fraction

from admissibility import is_admissible
from evaluator import density
from instance import VERTICES
from primitives import boundary

# ==================================================================================================
# SEARCH RESULT
# ==================================================================================================
#
# A dataclass gives us a small record with named fields:
#
#     value
#     U
#     F
#
# frozen=True makes a completed result immutable.
#
# U and F are normally frozensets.
#
# They are None only when the admissible family is empty.
#
# ==================================================================================================


@dataclass(frozen=True)
class SearchResult:
    value: Fraction
    U: frozenset | None
    F: frozenset | None


# ==================================================================================================
# find_max_density()
# ==================================================================================================
#
# COMMENTS-FIRST ALGORITHM:
#
# 1. Start with:
#
#        best = None
#
#    None means:
#
#        no admissible pair has been encountered yet.
#
#    We deliberately do NOT initialize best to a zero-valued SearchResult.
#
#    Why?
#
#    An admissible pair could itself have density 0.
#
#    We still need to record its U and F if it is the maximizer.
#
#
# 2. Put the vertices in deterministic order:
#
#        vertices = sorted(VERTICES)
#
#
# 3. Enumerate every NONEMPTY subset U.
#
#    If there are n vertices, U can have sizes:
#
#        1, 2, ..., n
#
#    For every size:
#
#        itertools.combinations(vertices, U_size)
#
#    generates every U of exactly that cardinality.
#
#
# 4. Convert each generated U tuple to:
#
#        frozenset
#
#    because U is mathematically a set.
#
#
# 5. Compute:
#
#        boundary(U)
#
#    ONCE for this U.
#
#    The returned list contains the distinct boundary-edge IDs in
#    deterministic EDGES order.
#
#
# 6. Enumerate every subset F of that boundary.
#
#    If the boundary has b edge copies, F may have sizes:
#
#        0, 1, ..., b
#
#    For each size:
#
#        itertools.combinations(boundary_edges, F_size)
#
#    generates every F of that cardinality.
#
#
# 7. Convert each generated F tuple to:
#
#        frozenset
#
#
# 8. Ask:
#
#        is_admissible(U, F)
#
#    If False:
#
#        continue
#
#    Inadmissible pairs are ordinary search candidates that simply
#    do not participate in the optimization.
#
#
# 9. For an admissible pair, compute:
#
#        value = density(U, F)
#
#    density() returns an exact Fraction.
#
#
# 10. If:
#
#         best is None
#
#     then this is the FIRST admissible pair.
#
#     Save it immediately, even if its density happens to be 0.
#
#
# 11. Otherwise compare exactly:
#
#         value > best.value
#
#     If strictly greater:
#
#         replace best.
#
#     If equal:
#
#         do nothing.
#
#     Therefore the first maximizer encountered wins a tie.
#
#
# 12. After every candidate has been examined:
#
#     if best is still None:
#
#         the admissible family was empty
#
#         return:
#
#             value = Fraction(0, 1)
#             U = None
#             F = None
#
#     otherwise:
#
#         return best
#
# ==================================================================================================


def find_max_density():
    best = None

    vertices = sorted(VERTICES)

    # Enumerate every nonempty vertex subset U.
    for U_size in range(1, len(vertices) + 1):
        for U_combo in itertools.combinations(vertices, U_size):
            U = frozenset(U_combo)

            # Compute ∂_G(U) once for this U.
            boundary_edges = boundary(U)

            # Enumerate every subset F of ∂_G(U), including the empty set.
            for F_size in range(len(boundary_edges) + 1):
                for F_combo in itertools.combinations(boundary_edges, F_size):
                    F = frozenset(F_combo)

                    # Only admissible pairs participate in the optimization.
                    if not is_admissible(U, F):
                        continue

                    # Evaluate the objective using exact rational arithmetic.
                    value = density(U, F)

                    # The first admissible pair becomes the initial best pair.
                    if best is None:
                        best = SearchResult(value=value, U=U, F=F)
                        continue

                    # Replace the current best only on a STRICT improvement.
                    #
                    # Equality leaves the first encountered maximizer in place.
                    if value > best.value:
                        best = SearchResult(value=value, U=U, F=F)

    # No admissible pair was found.
    if best is None:
        return SearchResult(
            value=Fraction(0, 1),
            U=None,
            F=None,
        )

    return best

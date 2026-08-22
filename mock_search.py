
# ==================================================================================================
# MOCK EXIT 1 — EXHAUSTIVE SEARCH
# ==================================================================================================
#
# PURPOSE:
#
# Exhaustively enumerate every candidate pair:
#
#     (W, S)
#
# where:
#
#     nonempty W subseteq WORKERS
#
# and:
#
#     S subseteq fringe(W)
#
# Then:
#
#     1. filter candidates through is_admissible(W, S),
#     2. evaluate admissible candidates exactly,
#     3. retain a maximizing pair,
#     4. return the result with named fields.
#
#
# SEARCH PIPELINE:
#
#     enumerate W
#         ↓
#     compute fringe(W)
#         ↓
#     enumerate S subseteq fringe(W)
#         ↓
#     is_admissible(W, S)
#         ↓
#     if False:
#         skip
#         ↓
#     if True:
#         candidate_value(W, S)
#         ↓
#     compare with current best
#
#
# IMPORTANT:
#
# Candidate evaluation occurs ONLY AFTER admissibility.
#
# This preserves the evaluator's caller contract and prevents invalid
# candidates with unsafe denominators from reaching Fraction arithmetic.
#
# ==================================================================================================


import itertools
from dataclasses import dataclass
from fractions import Fraction

from mock_admissibility import is_admissible
from mock_evaluator import candidate_value
from mock_instance import WORKERS
from mock_primitives import fringe

# ==================================================================================================
# SEARCH RESULT RECORD
# ==================================================================================================
#
# The search specification requires named fields:
#
#     result.value
#     result.W
#     result.S
#
# A dataclass supplies this small named record.
#
# frozen=True makes the completed result immutable.
#
#
# ORDINARY RESULT:
#
#     value = exact Fraction
#     W = frozenset of workers
#     S = frozenset of shift IDs
#
#
# EMPTY-ADMISSIBLE-FAMILY RESULT:
#
#     value = Fraction(0, 1)
#     W = None
#     S = None
#
# None is used because no actual maximizing pair exists in that case.
#
# Using empty frozensets would misleadingly look like the candidate:
#
#     (empty W, empty S)
#
# which is itself inadmissible.
#
# ==================================================================================================


@dataclass(frozen=True)
class SearchResult:
    value: Fraction
    W: frozenset[str] | None
    S: frozenset[str] | None


# ==================================================================================================
# find_max_value()
# ==================================================================================================
#
# CALLER / LIFECYCLE CONTRACT:
#
# This function assumes the fixed data in mock_instance.py has already
# been validated as part of the instance lifecycle.
#
# It does NOT call validate_instance() on every search invocation.
#
# The permanent pytest suite will directly test:
#
#     validate_instance()
#
# so edits that violate fixed-instance invariants fail verification before
# a search result is trusted.
#
#
# ==================================================================================================
# DETERMINISTIC ENUMERATION
# ==================================================================================================
#
# WORKERS is a frozenset, whose iteration order should not define the
# search's tie behavior.
#
# Therefore:
#
#     workers = sorted(WORKERS)
#
# gives the deterministic sequence:
#
#     ["a", "b", "c", "d"]
#
#
# itertools.combinations preserves input order.
#
# fringe(W) also returns shift IDs in stable SHIFTS order.
#
# Therefore both:
#
#     W enumeration
#
# and:
#
#     S enumeration
#
# are deterministic.
#
# This gives a reproducible meaning to:
#
#     first encountered maximizer wins ties.
#
#
# ==================================================================================================
# BEST-RESULT SENTINEL
# ==================================================================================================
#
# Start:
#
#     best = None
#
# None means:
#
#     no admissible pair has been encountered yet.
#
# Do NOT initialize best as a zero-valued SearchResult.
#
# In a general instance, an admissible candidate could itself have value 0.
#
# A None sentinel distinguishes:
#
#     no admissible candidate seen
#
# from:
#
#     admissible candidate seen with value 0.
#
#
# ==================================================================================================
# COMMENTS-FIRST ALGORITHM
# ==================================================================================================
#
# 1. Start:
#
#        best = None
#
#
# 2. Create deterministic worker order:
#
#        workers = sorted(WORKERS)
#
#
# 3. Enumerate every NONEMPTY crew size:
#
#        1, 2, ..., len(workers)
#
#
# 4. For each crew size, generate every worker combination:
#
#        itertools.combinations(workers, W_size)
#
#
# 5. Convert each combination to:
#
#        W = frozenset(W_combo)
#
#
# 6. Compute:
#
#        fringe_shift_ids = fringe(W)
#
#    exactly ONCE for this W.
#
#
# 7. Enumerate every possible S cardinality:
#
#        0, 1, ..., len(fringe_shift_ids)
#
#    Starting at zero is essential because the empty S is a valid subset
#    and is the S-component of the hand-derived optimum.
#
#
# 8. For each size, generate every subset:
#
#        itertools.combinations(fringe_shift_ids, S_size)
#
#
# 9. Convert each generated tuple to:
#
#        S = frozenset(S_combo)
#
#
# 10. Ask:
#
#         is_admissible(W, S)
#
#     If False:
#
#         continue
#
#
# 11. Only for an admissible pair:
#
#         value = candidate_value(W, S)
#
#
# 12. If:
#
#         best is None
#
#     this is the first admissible pair.
#
#     Record:
#
#         SearchResult(value=value, W=W, S=S)
#
#
# 13. Otherwise compare:
#
#         value > best.value
#
#     If strictly greater:
#
#         replace best.
#
#     If equal:
#
#         leave best unchanged.
#
#     Therefore the FIRST encountered maximizer wins a tie.
#
#
# 14. After complete enumeration:
#
#     if best is still None:
#
#         no admissible pair existed
#
#         return:
#
#             value = Fraction(0, 1)
#             W = None
#             S = None
#
#     otherwise:
#
#         return best
#
#
# ==================================================================================================
# HAND-DERIVED ORACLE
# ==================================================================================================
#
# The independently committed oracle proves the unique maximizing pair is:
#
#     W* = {"a", "b", "c"}
#     S* = empty
#
# with:
#
#     value = 3
#
# Therefore:
#
#     find_max_value()
#
# must ultimately return a SearchResult satisfying:
#
#     result.value == Fraction(3, 1)
#
#     result.W == frozenset({"a", "b", "c"})
#
#     result.S == frozenset()
#
# The hand audit also established that every nonwinning crew has best
# value at most 2, so the oracle winner is unique rather than tie-selected.
#
# ==================================================================================================


def find_max_value():
    best = None

    # Deterministic worker order for reproducible subset enumeration.
    workers = sorted(WORKERS)

    # Enumerate every nonempty worker subset W.
    for W_size in range(1, len(workers) + 1):
        for W_combo in itertools.combinations(workers, W_size):
            W = frozenset(W_combo)

            # The fringe depends only on W, so compute it once for this crew.
            fringe_shift_ids = fringe(W)

            # Enumerate every subset S of the fringe, including the empty set.
            for S_size in range(len(fringe_shift_ids) + 1):
                for S_combo in itertools.combinations(
                    fringe_shift_ids, S_size
                ):
                    S = frozenset(S_combo)

                    # Inadmissible candidates do not participate.
                    if not is_admissible(W, S):
                        continue

                    # The evaluator contract is now satisfied.
                    value = candidate_value(W, S)

                    # The first admissible candidate becomes the initial best.
                    if best is None:
                        best = SearchResult(value=value, W=W, S=S)
                        continue

                    # Replace only on STRICT improvement.
                    #
                    # Equal values leave the first encountered maximizer
                    # unchanged, implementing the required tie contract.
                    if value > best.value:
                        best = SearchResult(value=value, W=W, S=S)

    # The admissible family is empty.
    if best is None:
        return SearchResult(
            value=Fraction(0, 1),
            W=None,
            S=None,
        )

    return best
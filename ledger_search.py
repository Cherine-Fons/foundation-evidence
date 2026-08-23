"""Deterministic exhaustive search for the best eligible trader subset."""

from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations

from ledger_eligibility import is_eligible
from ledger_evaluator import candidate_score
from ledger_model import Ledger

# ==================================================================================================
# SEARCH RESULT
# ==================================================================================================
#
# The specification requires the search to return:
#
#     exact value
#     maximizing trader subset
#
# as named fields.
#
#
# ORDINARY RESULT:
#
#     value
#         exact Fraction
#
#     T
#         maximizing frozenset of trader names
#
#
# EMPTY-ELIGIBLE-FAMILY RESULT:
#
#     value = Fraction(0, 1)
#     T = None
#
#
# None does not represent an empty candidate.
#
# It means:
#
#     no eligible candidate exists.
#
# ==================================================================================================


@dataclass(frozen=True)
class SearchResult:
    value: Fraction
    T: frozenset[str] | None


# ==================================================================================================
# find_best_subset()
# ==================================================================================================
#
# INPUT:
#
#     a Ledger containing trusted Trade records
#
#
# SEARCH DOMAIN:
#
#     every nonempty subset T of ledger.traders()
#
#
# PIPELINE:
#
#     deterministic trader list
#             ↓
#     enumerate every nonempty subset T
#             ↓
#     is_eligible(ledger, T)
#             ↓
#       False → skip
#             ↓
#       True
#             ↓
#     candidate_score(ledger, T)
#             ↓
#     compare with current best
#
#
# IMPORTANT:
#
# Eligibility occurs BEFORE evaluation.
#
# Some ineligible candidates still have mechanically computable scores.
#
# Example:
#
#     T = {"bob"}
#
# gives:
#
#     is_eligible(...) = False
#
# but:
#
#     candidate_score(...) = Fraction(59, 3)
#
# Therefore arithmetic computability cannot determine whether a candidate
# is legally allowed to compete.
#
#
# ==================================================================================================
# DETERMINISTIC ENUMERATION
# ==================================================================================================
#
# Ledger.traders() returns a sorted list.
#
# For the fixed ledger:
#
#     ["alice", "bob", "carol", "dana"]
#
# We enumerate subset sizes:
#
#     1, 2, 3, 4
#
# using itertools.combinations.
#
# This gives every nonempty trader subset exactly once in deterministic
# order.
#
#
# ==================================================================================================
# NONE SENTINEL
# ==================================================================================================
#
# Start:
#
#     best = None
#
# This means:
#
#     no eligible candidate has been encountered yet.
#
# It does NOT mean:
#
#     the current best score is zero.
#
# If complete enumeration ends with best still None, the eligible family
# is empty and the specification requires:
#
#     SearchResult(
#         value=Fraction(0, 1),
#         T=None,
#     )
#
#
# ==================================================================================================
# TIE RULE
# ==================================================================================================
#
# The committed oracle states:
#
#     first encountered maximizer wins.
#
# Therefore replacement occurs only when:
#
#     value > best.value
#
# Strict improvement preserves the earlier result on equal scores.
#
# Using:
#
#     >=
#
# would incorrectly implement last-on-tie behavior.
#
#
# ==================================================================================================
# HAND-DERIVED ORACLE
# ==================================================================================================
#
# EXIT_ORACLE.md proves the UNIQUE optimum is:
#
#     T* = {"alice"}
#
# with:
#
#     score(T*) = 30
#
# Therefore:
#
#     find_best_subset(ledger)
#
# must produce:
#
#     result.value == Fraction(30, 1)
#
#     result.T == frozenset({"alice"})
#
#
# The full finite-domain audit is:
#
#     4 traders
#         ↓
#     15 nonempty subsets
#         ↓
#     7 eligible subsets
#         ↓
#     1 unique maximizing subset
#
# ==================================================================================================


def find_best_subset(ledger: Ledger) -> SearchResult:
    best = None

    # Ledger.traders() already returns a deterministic sorted list.
    traders = ledger.traders()

    # Enumerate every nonempty trader subset.
    for subset_size in range(1, len(traders) + 1):
        for subset_tuple in combinations(traders, subset_size):
            T = frozenset(subset_tuple)

            # A candidate must be legally eligible before its arithmetic
            # score may participate in optimization.
            if not is_eligible(ledger, T):
                continue

            value = candidate_score(ledger, T)

            # The first eligible candidate becomes the initial best.
            if best is None:
                best = SearchResult(
                    value=value,
                    T=T,
                )
                continue

            # Replace only on strict improvement.
            #
            # Equal values preserve the first encountered maximizer.
            if value > best.value:
                best = SearchResult(
                    value=value,
                    T=T,
                )

    # No eligible candidate existed.
    if best is None:
        return SearchResult(
            value=Fraction(0, 1),
            T=None,
        )

    return best
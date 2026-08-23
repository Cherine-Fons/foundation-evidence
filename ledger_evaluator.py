"""Exact rational evaluator for eligible ledger trader subsets."""

from collections.abc import Iterable
from fractions import Fraction

from ledger_eligibility import trade_count, trade_volume
from ledger_model import Ledger

# ==================================================================================================
# candidate_score()
# ==================================================================================================
#
# OBJECTIVE:
#
# For an eligible trader subset T:
#
#               vol(T)
#     ---------------------------
#          2 * count(T) - 1
#
#
# CALLER CONTRACT:
#
# This function TRUSTS the caller to have already established:
#
#     is_eligible(ledger, T) is True
#
# It does not repeat the eligibility guards.
#
#
# Intended use:
#
#     if not is_eligible(ledger, T):
#         continue
#
#     value = candidate_score(ledger, T)
#
#
# RESPONSIBILITY SPLIT:
#
#     is_eligible(...)
#         decides whether T may compete
#
#     candidate_score(...)
#         computes the exact score of an already-eligible T
#
#
# ==================================================================================================
# DENOMINATOR SAFETY
# ==================================================================================================
#
# Eligibility requires:
#
#     count(T) is odd.
#
# Since 0 is even, an eligible candidate must satisfy:
#
#     count(T) >= 1.
#
# Therefore:
#
#     2 * count(T) - 1
#         >= 2 * 1 - 1
#         = 1.
#
# Thus every legitimately supplied candidate has a positive denominator.
#
#
# ==================================================================================================
# EXACT ARITHMETIC
# ==================================================================================================
#
# Construct Fraction directly from integer numerator and denominator:
#
#     Fraction(volume, denominator)
#
# Do NOT first calculate:
#
#     volume / denominator
#
# because `/` would produce a float before Fraction ever saw the value.
#
# The desired pipeline is:
#
#     integer numerator
#     integer denominator
#          ↓
#     Fraction(...)
#          ↓
#     exact rational
#
#
# ==================================================================================================
# HAND-DERIVED PREDICTIONS
# ==================================================================================================
#
# The committed EXIT_ORACLE.md predicts:
#
#     {"alice"}
#         count = 1
#         volume = 30
#
#         score = 30 / (2*1 - 1)
#               = 30
#
#         -> Fraction(30, 1)
#
#
#     {"carol"}
#         count = 1
#         volume = 27
#
#         -> Fraction(27, 1)
#
#
#     {"alice", "bob"}
#         count = 3
#         volume = 89
#
#         score = 89 / (2*3 - 1)
#               = 89 / 5
#
#         -> Fraction(89, 5)
#
#
#     {"bob", "carol"}
#         count = 3
#         volume = 86
#
#         -> Fraction(86, 5)
#
#
#     {"bob", "dana"}
#         count = 3
#         volume = 71
#
#         -> Fraction(71, 5)
#
#
#     {"alice", "carol", "dana"}
#         count = 3
#         volume = 69
#
#         -> Fraction(69, 5)
#
#
#     {"alice", "bob", "carol", "dana"}
#         count = 5
#         volume = 128
#
#         score = 128 / (2*5 - 1)
#               = 128 / 9
#
#         -> Fraction(128, 9)
#
#
# ==================================================================================================
# CONTRACT-VIOLATION EXAMPLE
# ==================================================================================================
#
# T = {"bob"} is INELIGIBLE because:
#
#     count(T) = 2
#
# is even.
#
# But direct evaluator arithmetic would still produce:
#
#     volume = 59
#     denominator = 2*2 - 1 = 3
#
#     Fraction(59, 3)
#
# This is not an evaluator failure.
#
# It demonstrates why the caller must filter candidates before scoring.
#
# A value can be arithmetically computable while being irrelevant to the
# legal optimization domain.
#
# ==================================================================================================


def candidate_score(ledger: Ledger, T: Iterable[str]) -> Fraction:
    count = trade_count(ledger, T)
    volume = trade_volume(ledger, T)

    numerator = volume
    denominator = 2 * count - 1

    return Fraction(numerator, denominator)
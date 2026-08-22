
# ==================================================================================================
# MOCK EXIT 1 — EXACT OBJECTIVE EVALUATOR
# ==================================================================================================
#
# PURPOSE:
#
# Evaluate the Crew-Assignment Density objective exactly:
#
#                         2*i(W) + |S|
#     value(W, S) = ---------------------------
#                      skill(W) + |S| - 2
#
# for a candidate pair:
#
#     (W, S)
#
#
# EXACTNESS CONTRACT:
#
# The objective is rational.
#
# This module therefore uses:
#
#     fractions.Fraction
#
# and constructs the result directly from an integer numerator and
# integer denominator.
#
#
# DO NOT:
#
#     numerator / denominator
#
# before constructing the Fraction.
#
# Ordinary `/` creates a float and therefore introduces approximation
# before exact rational construction.
#
#
# RESPONSIBILITY BOUNDARY:
#
# is_admissible(W, S)
#
#     decides whether a candidate may participate in the optimization.
#
# candidate_value(W, S)
#
#     computes the exact objective value of a candidate that the caller
#     has already established as admissible.
#
#
# candidate_value() does NOT call is_admissible() again.
#
# Its caller contract is:
#
#     supply an admissible candidate pair.
#
#
# DENOMINATOR SAFETY:
#
# Admissibility Condition 4 guarantees:
#
#     skill(W) + |S| >= 4
#
# Therefore:
#
#     skill(W) + |S| - 2 >= 2
#
# so every admissible pair has a positive nonzero denominator.
#
#
# IMPORTANT MOCK-SPECIFICATION WARNING:
#
# The numerator is:
#
#     2*i(W) + |S|
#
# NOT:
#
#     2*(i(W) + |S|)
#
# Only internal shifts are doubled.
#
# Selected fringe shifts contribute coefficient 1.
#
# The denominator subtracts:
#
#     2
#
# not:
#
#     1
#
# ==================================================================================================


from fractions import Fraction

from mock_primitives import internal_shift_count, skill_of

# ==================================================================================================
# candidate_value(W, S)
# ==================================================================================================
#
# COMMENTS-FIRST ALGORITHM:
#
# 1. Compute:
#
#        internal_count = i(W)
#
#
# 2. Compute:
#
#        crew_skill = skill(W)
#
#
# 3. Compute:
#
#        S_size = |S|
#
#
# 4. Build the numerator exactly as specified:
#
#        numerator = 2 * internal_count + S_size
#
#
# 5. Build the denominator exactly as specified:
#
#        denominator = crew_skill + S_size - 2
#
#
# 6. Return:
#
#        Fraction(numerator, denominator)
#
#
# ==================================================================================================
# HAND-DERIVED PREDICTIONS
# ==================================================================================================
#
# ORACLE WINNER:
#
#     W = {"a", "b", "c"}
#     S = empty
#
#     internal_count = 3
#     crew_skill = 4
#     S_size = 0
#
#     numerator = 2*3 + 0 = 6
#     denominator = 4 + 0 - 2 = 2
#
#     value = Fraction(6, 2)
#           = Fraction(3, 1)
#
#
# SINGLETON b WITH FULL FRINGE:
#
#     W = {"b"}
#     S = {"s0", "s1", "s2"}
#
#     internal_count = 0
#     crew_skill = 1
#     S_size = 3
#
#     numerator = 2*0 + 3 = 3
#     denominator = 1 + 3 - 2 = 2
#
#     value = Fraction(3, 2)
#
# This case detects the incorrect capstone-shaped numerator:
#
#     2*(internal_count + S_size)
#
# which would incorrectly produce:
#
#     2*(0+3) = 6
#
#
# CREW {"b", "c"} WITH S={"s0"}:
#
#     internal_count = 1
#     crew_skill = 3
#     S_size = 1
#
#     numerator = 2*1 + 1 = 3
#     denominator = 3 + 1 - 2 = 2
#
#     value = Fraction(3, 2)
#
#
# RUNNER-UP CREW:
#
#     W = {"a", "b", "d"}
#     S = empty
#
#     internal_count = 2
#     crew_skill = 4
#     S_size = 0
#
#     numerator = 4
#     denominator = 2
#
#     value = Fraction(2, 1)
#
#
# NONTERMINATING-DECIMAL RATIONAL:
#
#     W = {"a", "c", "d"}
#     S = {"s0", "s1", "s2"}
#
#     internal_count = 1
#     crew_skill = 5
#     S_size = 3
#
#     numerator = 2*1 + 3 = 5
#     denominator = 5 + 3 - 2 = 6
#
#     value = Fraction(5, 6)
#
# Exact Fraction arithmetic preserves:
#
#     5/6
#
# rather than approximating it as a float.
#
# ==================================================================================================


def candidate_value(W, S):
    internal_count = internal_shift_count(W)
    crew_skill = skill_of(W)
    S_size = len(S)

    numerator = 2 * internal_count + S_size
    denominator = crew_skill + S_size - 2

    return Fraction(numerator, denominator)
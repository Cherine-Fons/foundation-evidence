# ==================================================================================================
# F7 CAPSTONE — EXACT OBJECTIVE EVALUATOR
# ==================================================================================================
#
# PURPOSE:
#
# Evaluate the modified set-pair density:
#
#                         2(e(U) + |F|)
#     rho_f(U, F) = ---------------------------
#                      f(U) + |F| - 1
#
# for a candidate pair:
#
#     (U, F)
#
#
# EXACTNESS RULE:
#
# This checker must use exact rational arithmetic.
#
# Ordinary Python division:
#
#     numerator / denominator
#
# produces a float.
#
# Some rational numbers cannot be represented exactly as binary floating-point
# numbers. For example:
#
#     4 / 3
#
# becomes approximately:
#
#     1.3333333333333333
#
# But the mathematics of this problem is rational arithmetic, and the checker
# must compare candidate values exactly.
#
# Therefore this evaluator constructs:
#
#     Fraction(numerator, denominator)
#
# using Python's standard-library fractions module.
#
#
# RESPONSIBILITY SEPARATION:
#
# is_admissible(U, F)
#
#     decides whether a candidate pair is allowed to compete.
#
# density(U, F)
#
#     evaluates the objective exactly.
#
# density() does NOT repeat the admissibility test.
#
# Its contract is:
#
#     the caller must supply an admissible pair.
#
# The later search loop will therefore have the shape:
#
#     if is_admissible(U, F):
#         value = density(U, F)
#
#
# CONSEQUENCE OF THAT CONTRACT:
#
# If a caller ignores the contract and supplies an inadmissible pair with:
#
#     f(U) + |F| - 1 = 0
#
# then Fraction will raise ZeroDivisionError.
#
# If an inadmissible pair happens to have a nonzero denominator, density() may
# mechanically return a rational value, but that value is not a valid candidate
# for the optimization problem.
#
# ==================================================================================================


from fractions import Fraction

from primitives import f_of, internal_edge_count

# ==================================================================================================
# density(U, F)
# ==================================================================================================
#
# COMMENTS-FIRST ALGORITHM:
#
# 1. Compute the number of internal edge copies:
#
#        e_U = e(U)
#
#
# 2. Compute:
#
#        f_U = f(U)
#
#
# 3. Compute the number of selected boundary edge copies:
#
#        F_size = |F|
#
#
# 4. Build the numerator:
#
#        numerator = 2 * (e_U + F_size)
#
#
# 5. Build the denominator:
#
#        denominator = f_U + F_size - 1
#
#
# 6. Construct and return the EXACT rational value:
#
#        Fraction(numerator, denominator)
#
#
# IMPORTANT:
#
# Do NOT write:
#
#        numerator / denominator
#
# because that would produce a float.
#
#
# HAND-DERIVED CHECKPOINTS:
#
# WINNER:
#
#     U = {0,1}
#     F = {e2}
#
#     e(U) = 2
#     f(U) = 2
#     |F|  = 1
#
#     numerator   = 2(2 + 1) = 6
#     denominator = 2 + 1 - 1 = 2
#
#     density = Fraction(6, 2)
#             = Fraction(3, 1)
#
#
# TRIANGLE:
#
#     U = {2,3,4}
#     F = {e2}
#
#     e(U) = 3
#     f(U) = 6
#     |F|  = 1
#
#     numerator   = 2(3 + 1) = 8
#     denominator = 6 + 1 - 1 = 6
#
#     density = Fraction(8, 6)
#             = Fraction(4, 3)
#
#
# TIGHT COMPETITOR:
#
#     U = {0,1,2}
#     F = {e3}
#
#     e(U) = 3
#     f(U) = 4
#     |F|  = 1
#
#     numerator   = 2(3 + 1) = 8
#     denominator = 4 + 1 - 1 = 4
#
#     density = Fraction(8, 4)
#             = Fraction(2, 1)
#
# ==================================================================================================


def density(U, F):
    e_U = internal_edge_count(U)
    f_U = f_of(U)
    F_size = len(F)

    numerator = 2 * (e_U + F_size)
    denominator = f_U + F_size - 1

    return Fraction(numerator, denominator)

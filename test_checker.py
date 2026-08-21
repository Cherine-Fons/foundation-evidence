# ==================================================================================================
# F7 CAPSTONE — EXACT CHECKER TEST SUITE
# ==================================================================================================
#
# PURPOSE:
#
# Turn the hand-derived examples and interactive guard checks into permanent,
# automatically repeatable tests.
#
# The suite checks:
#
#     1. a known admissible pair is accepted
#     2. condition 1 rejects empty U
#     3. condition 2 rejects an edge outside the boundary
#     4. condition 3 rejects even f(U) + |F|
#     5. condition 4 rejects an odd total below 3
#     6. parallel edge copies are counted separately
#     7. exhaustive search reproduces the hand-derived exact optimum
#
# Exact rational results use Fraction.
#
# No floating-point approximation belongs in the oracle test.
# ==================================================================================================

from fractions import Fraction

from admissibility import is_admissible
from instance import validate_instance
from primitives import boundary, internal_edge_count
from search import find_max_density

# ==================================================================================================
# TEST 1 — THE LOCKED INSTANCE ITSELF IS VALID
# ==================================================================================================
#
# The checker assumes that instance.py satisfies all graph-level invariants.
#
# validate_instance() is fail-fast:
#
#     invalid instance -> raises ValueError
#     valid instance   -> returns normally
#
# Therefore this test passes simply by reaching the end of the function
# without an exception.
#
# This gives the search contract teeth:
#
#     find_max_density() trusts validated instance data,
#
# while the test suite guarantees that the locked instance actually passes
# that validation.
# ==================================================================================================


def test_instance_is_valid():
    validate_instance()

# ==================================================================================================
# TEST 2 — ACCEPT A KNOWN ADMISSIBLE PAIR
# ==================================================================================================
#
# Hand-derived winner:
#
#     U = {0, 1}
#     F = {e2}
#
# Check:
#
#     U is nonempty and valid
#     boundary(U) = {e2}
#     f(U) + |F| = 2 + 1 = 3
#     3 is odd
#     3 >= 3
#
# Therefore the pair must be admissible.
# ==================================================================================================


def test_accepts_valid_pair():
    U = frozenset({0, 1})
    F = frozenset({"e2"})

    assert is_admissible(U, F) is True


# ==================================================================================================
# TEST 3 — CONDITION 1: REJECT EMPTY U
# ==================================================================================================
#
# U must be nonempty.
#
# The empty set violates condition 1 immediately.
# ==================================================================================================


def test_rejects_empty_U():
    U = frozenset()
    F = frozenset()

    assert is_admissible(U, F) is False


# ==================================================================================================
# TEST 4 — CONDITION 2: REJECT NONBOUNDARY EDGE
# ==================================================================================================
#
# For:
#
#     U = {0, 1}
#
# the boundary is:
#
#     {e2}
#
# Edge e3 exists in the graph, but:
#
#     e3 = (2, 3)
#
# has neither endpoint in U.
#
# Therefore:
#
#     e3 not in boundary(U)
#
# and:
#
#     F = {e3}
#
# violates:
#
#     F ⊆ boundary(U)
# ==================================================================================================


def test_rejects_nonboundary_edge_in_F():
    U = frozenset({0, 1})
    F = frozenset({"e3"})

    assert is_admissible(U, F) is False


# ==================================================================================================
# TEST 5 — CONDITION 3: REJECT EVEN f(U) + |F|
# ==================================================================================================
#
# We deliberately choose a pair where the parity condition is the
# relevant failure:
#
#     U = {2}
#     F = {e2, e3}
#
# For U = {2}:
#
#     boundary(U) = {e2, e3, e5}
#
# so F is a valid subset of the boundary.
#
# Also:
#
#     f(U) = 2
#     |F|  = 2
#
# therefore:
#
#     f(U) + |F| = 4
#
# Condition 1 passes.
# Condition 2 passes.
# Condition 3 fails because 4 is even.
#
# Notice:
#
#     4 >= 3
#
# so the lower-bound condition would pass.
#
# This isolates the parity guard cleanly.
# ==================================================================================================


def test_rejects_even_fU_plus_F_size():
    U = frozenset({2})
    F = frozenset({"e2", "e3"})

    assert is_admissible(U, F) is False


# ==================================================================================================
# TEST 6 — CONDITION 4: REJECT TOTAL BELOW THREE
# ==================================================================================================
#
# Use the banked guard-isolation example:
#
#     U = {0}
#     F = empty
#
# Then:
#
#     f(U) = 1
#     |F|  = 0
#
# so:
#
#     f(U) + |F| = 1
#
# Condition 1:
#
#     U is nonempty and valid
#
#     PASS
#
# Condition 2:
#
#     empty F is a subset of every boundary
#
#     PASS
#
# Condition 3:
#
#     1 is odd
#
#     PASS
#
# Condition 4:
#
#     1 >= 3
#
#     FAIL
#
# Therefore this test actually reaches and exercises the fourth guard.
# ==================================================================================================


def test_rejects_total_below_three():
    U = frozenset({0})
    F = frozenset()

    assert is_admissible(U, F) is False


# ==================================================================================================
# TEST 7 — PARALLEL EDGE COPIES REMAIN DISTINCT
# ==================================================================================================
#
# The graph contains:
#
#     e0 = (0, 1)
#     e1 = (0, 1)
#
# These are parallel but DISTINCT edge copies.
#
#
# For:
#
#     U = {0, 1}
#
# both copies are internal, so:
#
#     e(U) = 2
#
#
# For:
#
#     U = {1}
#
# both copies cross the boundary, along with e2:
#
#     boundary({1}) = ["e0", "e1", "e2"]
#
# If the implementation accidentally collapsed parallel endpoint pairs,
# this test would fail.
# ==================================================================================================


def test_parallel_edge_copies_are_counted_separately():
    assert internal_edge_count(frozenset({0, 1})) == 2

    boundary_edges = boundary(frozenset({1}))

    assert boundary_edges == ["e0", "e1", "e2"]


# ==================================================================================================
# TEST 8 — KNOWN-ANSWER ORACLE
# ==================================================================================================
#
# This is the central end-to-end test.
#
# The exhaustive checker must reproduce the independently hand-derived optimum:
#
#     optimal value = 3
#
#     unique maximizing U:
#
#         {0, 1}
#
#     unique maximizing F:
#
#         {e2}
#
#
# Exactness matters:
#
#     result.value
#
# must equal:
#
#     Fraction(3, 1)
#
# exactly.
#
# No pytest.approx.
# No float comparison.
# ==================================================================================================


def test_bruteforce_checker_returns_hand_derived_optimum():
    result = find_max_density()

    assert result.value == Fraction(3, 1)
    assert result.U == frozenset({0, 1})
    assert result.F == frozenset({"e2"})

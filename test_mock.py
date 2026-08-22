
# ==================================================================================================
# MOCK EXIT 1 — PERMANENT TEST SUITE
# ==================================================================================================
#
# PURPOSE:
#
# Convert the hand-derived oracle and the interactive development checks
# into permanent, repeatable regression tests.
#
#
# THE SUITE TESTS:
#
#     1. the fixed instance is valid
#     2. a known admissible pair is accepted
#     3. admissibility Condition 1 in isolation
#     4. admissibility Condition 2 in isolation
#     5. admissibility Condition 3 in isolation
#     6. admissibility Condition 4 in isolation
#     7. parallel physical shift copies remain distinct
#     8. duplicate IDs in supplied S are deliberately rejected
#     9. the evaluator uses the MOCK objective formula exactly
#    10. exhaustive search reproduces the hand-derived oracle exactly
#
#
# EXACTNESS:
#
# The checker uses Fraction arithmetic.
#
# Therefore exact known-answer tests use:
#
#     ==
#
# rather than:
#
#     pytest.approx(...)
#
# ==================================================================================================


from fractions import Fraction

from mock_admissibility import is_admissible
from mock_evaluator import candidate_value
from mock_instance import validate_instance
from mock_primitives import fringe, internal_shift_count
from mock_search import find_max_value

# ==================================================================================================
# TEST 1 — FIXED INSTANCE IS VALID
# ==================================================================================================
#
# validate_instance() raises ValueError on malformed fixed data.
#
# A valid instance returns normally.
#
# Therefore this test passes simply by reaching the end without an
# exception.
#
# ==================================================================================================


def test_instance_is_valid():
    validate_instance()


# ==================================================================================================
# TEST 2 — ACCEPT THE ORACLE WINNER
# ==================================================================================================
#
# Oracle pair:
#
#     W = {"a", "b", "c"}
#     S = empty
#
# Hand-derived checks:
#
#     W nonempty and valid                 -> pass
#     S subseteq fringe(W)                 -> pass
#     skill(W) + |S| = 4                   -> even
#     4 >= 4                               -> pass
#
# Therefore:
#
#     is_admissible(W, S) is True
#
# ==================================================================================================


def test_accepts_oracle_winner():
    W = frozenset({"a", "b", "c"})
    S = frozenset()

    assert is_admissible(W, S) is True


# ==================================================================================================
# TEST 3 — CONDITION 1: REJECT EMPTY W
# ==================================================================================================
#
# W must be nonempty.
#
# The empty crew fails the first mathematical guard immediately.
#
# ==================================================================================================


def test_rejects_empty_W():
    W = frozenset()
    S = frozenset()

    assert is_admissible(W, S) is False


# ==================================================================================================
# TEST 4 — CONDITION 2: REJECT NON-FRINGE SHIFT
# ==================================================================================================
#
# For:
#
#     W = {"a", "b", "c"}
#
# the hand-derived fringe is:
#
#     {"s3"}
#
# Shift s0 exists in the graph but is internal to this crew.
#
# Thus:
#
#     Condition 1 -> pass
#     Condition 2 -> fail
#
# ==================================================================================================


def test_rejects_nonfringe_shift_in_S():
    W = frozenset({"a", "b", "c"})
    S = frozenset({"s0"})

    assert is_admissible(W, S) is False


# ==================================================================================================
# TEST 5 — CONDITION 3: REJECT ODD skill(W) + |S|
# ==================================================================================================
#
# Use:
#
#     W = {"a", "b", "c"}
#     S = {"s3"}
#
# Here:
#
#     s3 is genuinely on the fringe
#
# so Conditions 1 and 2 pass.
#
# Then:
#
#     skill(W) = 4
#     |S| = 1
#
#     total = 5
#
# Five is odd, so Condition 3 fails.
#
# Since:
#
#     5 >= 4
#
# the lower-bound condition would have passed.
#
# This isolates parity.
#
# ==================================================================================================


def test_rejects_odd_skill_plus_S_size():
    W = frozenset({"a", "b", "c"})
    S = frozenset({"s3"})

    assert is_admissible(W, S) is False


# ==================================================================================================
# TEST 6 — CONDITION 4: REJECT TOTAL BELOW FOUR
# ==================================================================================================
#
# Use the guard-isolated pair:
#
#     W = {"a"}
#     S = {"s0"}
#
# Hand-derived facts:
#
#     skill(W) = 1
#     fringe(W) = {"s0", "s1"}
#
# Therefore:
#
#     Condition 1 -> pass
#     Condition 2 -> pass
#
# and:
#
#     skill(W) + |S|
#         = 1 + 1
#         = 2
#
# Two is even:
#
#     Condition 3 -> pass
#
# but:
#
#     2 < 4
#
# so:
#
#     Condition 4 -> fail
#
# ==================================================================================================


def test_rejects_total_below_four():
    W = frozenset({"a"})
    S = frozenset({"s0"})

    assert is_admissible(W, S) is False


# ==================================================================================================
# TEST 7 — PARALLEL PHYSICAL COPIES REMAIN DISTINCT
# ==================================================================================================
#
# The fixed instance contains:
#
#     s0 = (a,b)
#     s1 = (a,b)
#
# These are parallel but distinct physical shift copies.
#
#
# For:
#
#     W = {"a", "b"}
#
# both are internal, so:
#
#     i(W) = 2
#
#
# For:
#
#     W = {"b"}
#
# both parallel copies are fringe shifts, together with s2.
#
# Stable fringe order should therefore be:
#
#     ["s0", "s1", "s2"]
#
# ==================================================================================================


def test_parallel_shift_copies_are_counted_separately():
    assert internal_shift_count(frozenset({"a", "b"})) == 2

    assert fringe(frozenset({"b"})) == ["s0", "s1", "s2"]


# ==================================================================================================
# TEST 8 — REJECT DUPLICATE IDS IN SUPPLIED S
# ==================================================================================================
#
# Mathematically S is a set of physical shift copies.
#
# The same physical ID therefore cannot be selected twice.
#
# A list is deliberately supplied here because a frozenset would erase
# duplicates before is_admissible() had an opportunity to detect them.
#
# ==================================================================================================


def test_rejects_duplicate_shift_ids_in_supplied_S():
    W = frozenset({"b"})
    S = ["s0", "s0", "s1", "s2"]

    assert is_admissible(W, S) is False


# ==================================================================================================
# TEST 9 — EVALUATOR USES THE MOCK FORMULA
# ==================================================================================================
#
# The mock numerator is:
#
#     2*i(W) + |S|
#
# NOT:
#
#     2*(i(W) + |S|)
#
#
# Use a candidate with nonempty S so the two formulas differ:
#
#     W = {"b"}
#     S = {"s0", "s1", "s2"}
#
# Then:
#
#     i(W) = 0
#     skill(W) = 1
#     |S| = 3
#
# Correct mock arithmetic:
#
#     numerator = 2*0 + 3 = 3
#     denominator = 1 + 3 - 2 = 2
#
#     value = 3/2
#
# The old capstone-shaped numerator would incorrectly produce:
#
#     2*(0+3) = 6
#
# and therefore the wrong value 3.
#
# ==================================================================================================


def test_evaluator_uses_exact_mock_formula():
    W = frozenset({"b"})
    S = frozenset({"s0", "s1", "s2"})

    assert candidate_value(W, S) == Fraction(3, 2)


# ==================================================================================================
# TEST 10 — END-TO-END HAND-DERIVED ORACLE
# ==================================================================================================
#
# The oracle was derived and committed before checker implementation.
#
# It proves that the UNIQUE maximizing pair is:
#
#     W* = {"a", "b", "c"}
#     S* = empty
#
# with exact value:
#
#     3
#
# The exhaustive implementation must therefore reproduce all three
# fields exactly.
#
# No floating-point tolerance is used.
#
# ==================================================================================================


def test_bruteforce_search_returns_hand_derived_optimum():
    result = find_max_value()

    assert result.value == Fraction(3, 1)
    assert result.W == frozenset({"a", "b", "c"})
    assert result.S == frozenset()
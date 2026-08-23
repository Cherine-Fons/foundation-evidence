"""Permanent regression suite for the Foundation Exit Test."""

from fractions import Fraction
from pathlib import Path

from ledger_eligibility import is_eligible
from ledger_evaluator import candidate_score
from ledger_model import Ledger, Trade
from ledger_parser import parse_ledger
from ledger_search import find_best_subset

# ==================================================================================================
# FIXED INPUT
# ==================================================================================================
#
# Resolve ledger.txt relative to this test file rather than relying on the
# shell's current working directory.
#
# ==================================================================================================


LEDGER_PATH = Path(__file__).with_name("ledger.txt")


# ==================================================================================================
# TEST SUPPORT
# ==================================================================================================
#
# Many model and optimization tests need the same trusted Ledger:
#
#     parse fixed input
#         ↓
#     keep good Trade objects
#         ↓
#     construct Ledger
#
# Keep that setup in one small private helper.
#
# ==================================================================================================


def _known_ledger() -> Ledger:
    good_trades, _bad_rows = parse_ledger(LEDGER_PATH)
    return Ledger(good_trades)


# ==================================================================================================
# TEST 1 — PARSER KNOWN ANSWER
# ==================================================================================================
#
# Hand prediction for ledger.txt:
#
#     good rows = 5
#     bad rows  = 3
#
# Good trade IDs:
#
#     t1
#     t2
#     t5
#     t6
#     t8
#
# Specific malformed row:
#
#     line 3
#     t3,alice,sell,x,4
#
# Expected reason:
#
#     quantity must be an integer, got 'x'
#
# ==================================================================================================


def test_parser_known_answer():
    good_trades, bad_rows = parse_ledger(LEDGER_PATH)

    assert len(good_trades) == 5
    assert len(bad_rows) == 3

    assert [trade.trade_id for trade in good_trades] == [
        "t1",
        "t2",
        "t5",
        "t6",
        "t8",
    ]

    assert bad_rows[0].line_number == 3
    assert bad_rows[0].reason == "quantity must be an integer, got 'x'"


# ==================================================================================================
# TEST 2 — ADDITIONAL MALFORMED-ROW CONTRACTS
# ==================================================================================================
#
# ledger.txt already exercises:
#
#     wrong field count
#     noninteger quantity
#     empty quantity
#
# This temporary file exercises the remaining documented parser branches:
#
#     invalid side
#     nonpositive quantity
#     noninteger price
#     nonpositive price
#
# Pytest supplies tmp_path as a temporary pathlib.Path.
#
# ==================================================================================================


def test_parser_rejects_additional_malformed_rows(tmp_path: Path):
    path = tmp_path / "malformed_ledger.txt"

    path.write_text(
        "x1,alice,hold,1,1\n"
        "x2,alice,buy,0,1\n"
        "x3,alice,buy,1,nope\n"
        "x4,alice,buy,1,0\n",
        encoding="utf-8",
    )

    good_trades, bad_rows = parse_ledger(path)

    assert good_trades == []
    assert len(bad_rows) == 4

    assert [bad_row.reason for bad_row in bad_rows] == [
        "side must be 'buy' or 'sell', got 'hold'",
        "quantity must be positive, got 0",
        "price must be an integer, got 'nope'",
        "price must be positive, got 0",
    ]


# ==================================================================================================
# TEST 3 — ELIGIBILITY CONDITION 1
# ==================================================================================================
#
# T must be nonempty.
#
# ==================================================================================================


def test_eligibility_rejects_empty_subset():
    ledger = _known_ledger()

    assert is_eligible(ledger, frozenset()) is False


# ==================================================================================================
# TEST 4 — ELIGIBILITY CONDITION 2
# ==================================================================================================
#
# Use:
#
#     T = {"bob"}
#
# Bob has two good trades.
#
# Therefore:
#
#     Condition 1 -> pass
#     count(T) = 2
#     Condition 2 -> fail because 2 is even
#
# ==================================================================================================


def test_eligibility_rejects_even_trade_count():
    ledger = _known_ledger()
    T = frozenset({"bob"})

    assert is_eligible(ledger, T) is False


# ==================================================================================================
# TEST 5 — ELIGIBILITY CONDITION 3
# ==================================================================================================
#
# Use:
#
#     T = {"dana"}
#
# Then:
#
#     Condition 1:
#         nonempty
#         -> pass
#
#     Condition 2:
#         count(T) = 1
#         1 is odd
#         -> pass
#
#     Condition 3:
#         vol(T) = 12
#         12 < 20
#         -> fail
#
# This isolates the third guard exactly as required.
#
# ==================================================================================================


def test_eligibility_rejects_low_volume_after_first_two_guards():
    ledger = _known_ledger()
    T = frozenset({"dana"})

    assert is_eligible(ledger, T) is False


# ==================================================================================================
# TEST 6 — HAND-COMPUTED NET POSITION
# ==================================================================================================
#
# Bob:
#
#     t2 -> sell 5 -> -5
#     t6 -> buy  7 -> +7
#
# Therefore:
#
#     -5 + 7 = 2
#
# ==================================================================================================


def test_bob_net_position_is_hand_computed_value():
    ledger = _known_ledger()

    assert ledger.net_position("bob") == 2


# ==================================================================================================
# TEST 7 — LEDGER SUMMARY CONTRACT
# ==================================================================================================
#
# Hand-derived:
#
#     total volume = 128
#
# Sorted distinct trader names:
#
#     alice
#     bob
#     carol
#     dana
#
# ==================================================================================================


def test_ledger_summary_matches_hand_computation():
    ledger = _known_ledger()

    assert ledger.total_volume() == 128
    assert ledger.traders() == [
        "alice",
        "bob",
        "carol",
        "dana",
    ]


# ==================================================================================================
# TEST 8 — EXACT FRACTION EVALUATOR
# ==================================================================================================
#
# Full trader set:
#
#     count = 5
#     volume = 128
#
# Therefore:
#
#     score
#         = 128 / (2*5 - 1)
#         = 128 / 9
#
# The result must remain an exact Fraction.
#
# ==================================================================================================


def test_evaluator_returns_exact_fraction():
    ledger = _known_ledger()
    T = frozenset({"alice", "bob", "carol", "dana"})

    value = candidate_score(ledger, T)

    assert isinstance(value, Fraction)
    assert value == Fraction(128, 9)


# ==================================================================================================
# TEST 9 — EMPTY ELIGIBLE FAMILY
# ==================================================================================================
#
# Build a tiny valid in-memory ledger:
#
#     trader = solo
#     quantity = 1
#     price = 1
#
# Its only nonempty trader subset has:
#
#     count = 1
#     volume = 1
#
# So:
#
#     nonempty    -> pass
#     odd count   -> pass
#     volume >=20 -> fail
#
# No eligible candidate exists.
#
# Required search result:
#
#     value = Fraction(0, 1)
#     T = None
#
# ==================================================================================================


def test_search_uses_none_sentinel_when_no_subset_is_eligible():
    ledger = Ledger(
        [
            Trade(
                trade_id="x1",
                trader="solo",
                side="buy",
                quantity=1,
                price=1,
            )
        ]
    )

    result = find_best_subset(ledger)

    assert result.value == Fraction(0, 1)
    assert result.T is None


# ==================================================================================================
# TEST 10 — END-TO-END HAND-DERIVED ORACLE
# ==================================================================================================
#
# EXIT_ORACLE.md was derived and substantively committed before Part C
# implementation.
#
# It proves the unique optimizer is:
#
#     T* = {"alice"}
#
# with exact score:
#
#     30
#
# The search must reproduce every result field exactly.
#
# ==================================================================================================


def test_search_returns_hand_derived_oracle_exactly():
    ledger = _known_ledger()

    result = find_best_subset(ledger)

    assert result.value == Fraction(30, 1)
    assert result.T == frozenset({"alice"})
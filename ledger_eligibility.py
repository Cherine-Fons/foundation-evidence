"""Subset metrics and eligibility for the ledger optimization problem."""

from collections.abc import Iterable

from ledger_model import Ledger

# ==================================================================================================
# PART C DOMAIN
# ==================================================================================================
#
# The mathematical optimization is defined for trader subsets:
#
#     T subseteq ledger.traders()
#
# The future exhaustive search will guarantee that domain structurally by
# generating T only from the ledger's actual traders.
#
# The three eligibility guards below therefore remain exactly the three
# conditions stated in the problem:
#
#     1. T is nonempty
#     2. count(T) is odd
#     3. vol(T) >= 20
#
# No additional "known trader" eligibility guard is invented here.
#
# Incoming iterables are normalized to frozenset because T is
# mathematically a set.
#
# ==================================================================================================


def trade_count(ledger: Ledger, T: Iterable[str]) -> int:
    """Return the number of ledger trades belonging to traders in T."""

    T_set = frozenset(T)

    return sum(
        1
        for trade in ledger.trades
        if trade.trader in T_set
    )


def trade_volume(ledger: Ledger, T: Iterable[str]) -> int:
    """Return total quantity-times-price for trades belonging to T."""

    T_set = frozenset(T)

    return sum(
        trade.quantity * trade.price
        for trade in ledger.trades
        if trade.trader in T_set
    )


# ==================================================================================================
# is_eligible()
# ==================================================================================================
#
# Apply the three mathematical guards in their specified order.
#
#
# GUARD 1:
#
#     T must be nonempty.
#
#
# GUARD 2:
#
#     count(T) must be odd.
#
#
# GUARD 3:
#
#     vol(T) must be at least 20.
#
#
# IMPORTANT:
#
# We deliberately keep the final guard explicit rather than compressing:
#
#     if volume < 20:
#         return False
#     return True
#
# into:
#
#     return volume >= 20
#
# because the ordered guard structure is part of the specification and
# later guard-isolation testing.
#
#
# HAND-DERIVED WITNESSES:
#
# Positive:
#
#     T = {"alice"}
#
#     nonempty
#     count = 1 odd
#     volume = 30
#
#     -> True
#
#
# Guard 1:
#
#     T = empty
#
#     -> False
#
#
# Guard 2:
#
#     T = {"bob"}
#
#     nonempty passes
#     count = 2 even
#
#     -> False
#
#
# Guard 3:
#
#     T = {"dana"}
#
#     nonempty passes
#     count = 1 odd passes
#     volume = 12 < 20
#
#     -> False
#
#
# Additional positive:
#
#     T = {"alice", "bob"}
#
#     count = 3
#     volume = 89
#
#     -> True
#
# ==================================================================================================


def is_eligible(ledger: Ledger, T: Iterable[str]) -> bool:
    T_set = frozenset(T)

    # Guard 1 — T must be nonempty.
    if not T_set:
        return False

    # Guard 2 — the number of matching good trades must be odd.
    count = trade_count(ledger, T_set)

    if count % 2 == 0:
        return False

    # Guard 3 — matching good-trade volume must reach the threshold.
    #
    # This is intentionally kept as an explicit guard for specification
    # visibility and future guard-isolation tests.
    volume = trade_volume(ledger, T_set)

    if volume < 20:  # noqa: SIM103
        return False

    return True
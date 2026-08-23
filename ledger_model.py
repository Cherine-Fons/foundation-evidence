# ==================================================================================================
# EXIT TEST — LEDGER DATA MODEL
# ==================================================================================================
#
# PURPOSE:
#
# Define the small typed records used by the defensive ledger parser.
#
# At this stage the module contains:
#
#     Trade
#     BadRow
#
# Part B will later extend this same module with:
#
#     Ledger
#
#
# MODULE CONTRACT:
#
# This module is silent.
#
# It defines data structures but performs no printing or file I/O.
#
# ==================================================================================================



"""Typed data model for the Foundation Exit Test trading ledger."""

from collections.abc import Iterable
from dataclasses import dataclass

# ==================================================================================================
# TRADE
# ==================================================================================================
#
# A successfully parsed ledger row becomes one Trade object.
#
# The fields correspond exactly to:
#
#     trade_id,trader,side,quantity,price
#
# The parser validates the external text before constructing Trade.
#
# frozen=True means a successfully constructed Trade record cannot have
# its fields reassigned afterward.
#
# ==================================================================================================


@dataclass(frozen=True)
class Trade:
    trade_id: str
    trader: str
    side: str
    quantity: int
    price: int


# ==================================================================================================
# BAD ROW
# ==================================================================================================
#
# A malformed physical input row is skipped by the parser and represented
# by a BadRow record.
#
# The specification requires:
#
#     line number
#     reason
#
# ==================================================================================================


@dataclass(frozen=True)
class BadRow:
    line_number: int
    reason: str


# ==================================================================================================
# LEDGER
# ==================================================================================================
#
# A Ledger is COMPOSED of Trade objects.
#
# Relationship:
#
#     Ledger HAS trades.
#
# It is not inheritance:
#
#     Ledger is NOT a Trade.
#
#
# CONSTRUCTOR CONTRACT:
#
# The Ledger receives trusted Trade objects, normally the `good_trades`
# returned by:
#
#     parse_ledger(...)
#
# Malformed rows have already been rejected by the parser and therefore
# do not enter the Ledger.
#
#
# INTERNAL STORAGE:
#
# The constructor accepts any iterable of Trade objects:
#
#     list
#     tuple
#     generator
#     etc.
#
# and snapshots that iterable into:
#
#     tuple(trades)
#
# This prevents later mutation of the caller's original list from silently
# changing the Ledger's stored trade collection.
#
# ==================================================================================================


class Ledger:
    def __init__(self, trades: Iterable[Trade]) -> None:
        self._trades = tuple(trades)

    # ----------------------------------------------------------------------------------------------
    # trades
    # ----------------------------------------------------------------------------------------------
    #
    # Expose the stored trades for inspection as the immutable tuple held
    # by the Ledger.
    #
    # This is a property because it is stored data rather than a calculation.
    #
    # Caller usage:
    #
    #     ledger.trades
    #
    # rather than:
    #
    #     ledger.trades()
    #
    # ----------------------------------------------------------------------------------------------

    @property
    def trades(self) -> tuple[Trade, ...]:
        return self._trades

    # ----------------------------------------------------------------------------------------------
    # total_volume()
    # ----------------------------------------------------------------------------------------------
    #
    # Definition:
    #
    #     sum of quantity * price over every stored trade
    #
    # Side does NOT change the sign.
    #
    # Both buys and sells contribute positive traded volume.
    #
    #
    # HAND PREDICTION FOR ledger.txt GOOD TRADES:
    #
    #     t1: 10 * 3 = 30
    #     t2:  5 * 2 = 10
    #     t5: 12 * 1 = 12
    #     t6:  7 * 7 = 49
    #     t8:  9 * 3 = 27
    #
    # Total:
    #
    #     30 + 10 + 12 + 49 + 27
    #     = 128
    #
    # Prediction:
    #
    #     ledger.total_volume() == 128
    #
    # ----------------------------------------------------------------------------------------------

    def total_volume(self) -> int:
        return sum(
            trade.quantity * trade.price
            for trade in self._trades
        )

    # ----------------------------------------------------------------------------------------------
    # net_position(trader)
    # ----------------------------------------------------------------------------------------------
    #
    # Definition:
    #
    #     sum quantities of buys
    #     minus
    #     sum quantities of sells
    #
    # for the requested trader.
    #
    # Price is irrelevant to net position.
    #
    #
    # Direction:
    #
    #     buy  -> +quantity
    #     sell -> -quantity
    #
    #
    # HAND PREDICTIONS:
    #
    # Alice:
    #
    #     +10
    #
    #     result = 10
    #
    #
    # Bob:
    #
    #     -5 + 7
    #     = 2
    #
    #
    # Carol:
    #
    #     -9
    #
    #
    # Dana:
    #
    #     +12
    #
    #
    # Unknown trader:
    #
    #     no matching trades
    #     result = 0
    #
    # ----------------------------------------------------------------------------------------------

    def net_position(self, trader: str) -> int:
        position = 0

        for trade in self._trades:
            # Trades belonging to other traders make no contribution.
            if trade.trader != trader:
                continue

            # The parser has already guaranteed that valid Trade objects
            # have side "buy" or "sell".
            if trade.side == "buy":
                position += trade.quantity
            else:
                position -= trade.quantity

        return position

    # ----------------------------------------------------------------------------------------------
    # traders()
    # ----------------------------------------------------------------------------------------------
    #
    # Definition:
    #
    #     sorted list of distinct trader names
    #
    # A set comprehension removes duplicates:
    #
    #     {trade.trader for trade in self._trades}
    #
    # sorted(...) converts the distinct names into the required
    # alphabetically ordered list.
    #
    #
    # GOOD-TRADE NAMES:
    #
    #     alice
    #     bob
    #     dana
    #     bob
    #     carol
    #
    # Distinct:
    #
    #     alice, bob, carol, dana
    #
    # Prediction:
    #
    #     ["alice", "bob", "carol", "dana"]
    #
    # ----------------------------------------------------------------------------------------------

    def traders(self) -> list[str]:
        return sorted(
            {trade.trader for trade in self._trades}
        )
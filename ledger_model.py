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


from dataclasses import dataclass

# ==================================================================================================
# TRADE
# ==================================================================================================
#
# A successfully parsed ledger row becomes one Trade object.
#
# The five fields correspond exactly to the text-file schema:
#
#     trade_id,trader,side,quantity,price
#
# Field meanings:
#
#     trade_id
#         identifier from the ledger row
#
#     trader
#         trader name
#
#     side
#         "buy" or "sell"
#
#     quantity
#         positive integer
#
#     price
#         positive integer
#
#
# frozen=True makes a parsed trade immutable after construction.
#
# The parser is responsible for validating side, quantity, and price
# before constructing a Trade.
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
# A malformed input row is skipped rather than allowed to crash the
# complete parse.
#
# The parser records:
#
#     line_number
#     reason
#
# so the caller can see exactly where and why parsing failed.
#
# Example:
#
#     BadRow(
#         line_number=3,
#         reason="quantity must be an integer, got 'x'",
#     )
#
# ==================================================================================================


@dataclass(frozen=True)
class BadRow:
    line_number: int
    reason: str
# ==================================================================================================
# EXIT TEST — DEFENSIVE LEDGER PARSER
# ==================================================================================================
#
# PURPOSE:
#
# Read a trading-ledger text file and separate its rows into:
#
#     good_trades
#     bad_rows
#
# The public function is:
#
#     parse_ledger(path)
#
# and returns:
#
#     (good_trades, bad_rows)
#
#
# CORE FAILURE CONTRACT:
#
# A malformed ROW:
#
#     - is recorded,
#     - is skipped,
#     - does NOT crash parsing of the remaining file.
#
# A file-level error such as an invalid path is different.
#
# This function does not broadly suppress file I/O exceptions such as
# FileNotFoundError.
#
#
# MODULE BEHAVIOR:
#
# This module is silent.
#
# It defines parsing behavior but performs no top-level parsing or printing.
#
# ==================================================================================================


from pathlib import Path

from ledger_model import BadRow, Trade

# ==================================================================================================
# MALFORMED-ROW CONTRACT
# ==================================================================================================
#
# A row is malformed if any of the following applies.
#
# Checks occur in this exact order:
#
#     1. field count is not exactly 5
#     2. side is not "buy" or "sell"
#     3. quantity cannot be parsed as an integer
#     4. quantity is not positive
#     5. price cannot be parsed as an integer
#     6. price is not positive
#
# The first violation found becomes the row's recorded reason.
#
#
# IMPORTANT:
#
# The specification does not impose additional content rules on:
#
#     trade_id
#     trader
#
# so this parser does not invent them.
#
# ==================================================================================================


# ==================================================================================================
# HAND PREDICTION — ledger.txt
# ==================================================================================================
#
# LINE 1:
#
#     t1,alice,buy,10,3
#
# Five fields.
# Valid side.
# Positive integer quantity and price.
#
# Prediction:
#
#     GOOD
#
#
# LINE 2:
#
#     t2,bob,sell,5,2
#
# Five fields.
# Valid side.
# Positive integer quantity and price.
#
# Prediction:
#
#     GOOD
#
#
# LINE 3:
#
#     t3,alice,sell,x,4
#
# Five fields.
# Valid side.
#
# But:
#
#     quantity_text = "x"
#
# cannot be converted by:
#
#     int("x")
#
# Prediction:
#
#     BAD
#
# Exact reason:
#
#     quantity must be an integer, got 'x'
#
#
# LINE 4:
#
#     t4,carol,buy,8
#
# Splitting on commas gives only four fields.
#
# Prediction:
#
#     BAD
#
# Exact reason:
#
#     expected 5 fields, got 4
#
#
# LINE 5:
#
#     t5,dana,buy,12,1
#
# Everything is valid.
#
# Prediction:
#
#     GOOD
#
#
# LINE 6:
#
#     t6,bob,buy,7,7
#
# Everything is valid.
#
# Prediction:
#
#     GOOD
#
#
# LINE 7:
#
#     t7,alice,buy,,2
#
# There are five comma-separated fields, but the quantity field is:
#
#     ""
#
# Therefore:
#
#     int("")
#
# fails.
#
# Prediction:
#
#     BAD
#
# Exact reason:
#
#     quantity must be an integer, got ''
#
#
# LINE 8:
#
#     t8,carol,sell,9,3
#
# Everything is valid.
#
# Prediction:
#
#     GOOD
#
#
# HAND-PREDICTED TOTALS:
#
#     good rows = 5
#     bad rows  = 3
#
# Good line numbers:
#
#     1, 2, 5, 6, 8
#
# Bad line numbers:
#
#     3, 4, 7
#
# ==================================================================================================


def parse_ledger(path: str | Path) -> tuple[list[Trade], list[BadRow]]:
    # Accumulate successfully parsed Trade objects here.
    good_trades = []

    # Accumulate rejected rows here as named BadRow records.
    bad_rows = []

    ledger_path = Path(path)

    # start=1 makes recorded line numbers match human-visible file lines.
    with ledger_path.open("r", encoding="utf-8") as ledger_file:
        for line_number, raw_line in enumerate(ledger_file, start=1):
            # Remove only newline characters from the physical line.
            #
            # Individual fields are stripped separately below.
            line = raw_line.rstrip("\r\n")

            # Split on commas, then remove surrounding whitespace from
            # each individual field.
            fields = [field.strip() for field in line.split(",")]

            # --------------------------------------------------------------------------------------
            # CHECK 1 — EXACTLY FIVE FIELDS
            # --------------------------------------------------------------------------------------
            #
            # Validate the shape before tuple unpacking.
            #
            # This prevents a malformed row from causing Python's own
            # unpacking exception.
            # --------------------------------------------------------------------------------------

            if len(fields) != 5:
                bad_rows.append(
                    BadRow(
                        line_number=line_number,
                        reason=f"expected 5 fields, got {len(fields)}",
                    )
                )
                continue

            trade_id, trader, side, quantity_text, price_text = fields

            # --------------------------------------------------------------------------------------
            # CHECK 2 — VALID SIDE
            # --------------------------------------------------------------------------------------

            if side not in {"buy", "sell"}:
                bad_rows.append(
                    BadRow(
                        line_number=line_number,
                        reason=(
                            "side must be 'buy' or 'sell', "
                            f"got {side!r}"
                        ),
                    )
                )
                continue

            # --------------------------------------------------------------------------------------
            # CHECK 3 — QUANTITY MUST PARSE AS AN INTEGER
            # --------------------------------------------------------------------------------------
            #
            # ValueError is an expected failure mode when external text
            # cannot be interpreted as an integer.
            # --------------------------------------------------------------------------------------

            try:
                quantity = int(quantity_text)
            except ValueError:
                bad_rows.append(
                    BadRow(
                        line_number=line_number,
                        reason=(
                            "quantity must be an integer, "
                            f"got {quantity_text!r}"
                        ),
                    )
                )
                continue

            # --------------------------------------------------------------------------------------
            # CHECK 4 — QUANTITY MUST BE POSITIVE
            # --------------------------------------------------------------------------------------

            if quantity <= 0:
                bad_rows.append(
                    BadRow(
                        line_number=line_number,
                        reason=f"quantity must be positive, got {quantity}",
                    )
                )
                continue

            # --------------------------------------------------------------------------------------
            # CHECK 5 — PRICE MUST PARSE AS AN INTEGER
            # --------------------------------------------------------------------------------------

            try:
                price = int(price_text)
            except ValueError:
                bad_rows.append(
                    BadRow(
                        line_number=line_number,
                        reason=(
                            "price must be an integer, "
                            f"got {price_text!r}"
                        ),
                    )
                )
                continue

            # --------------------------------------------------------------------------------------
            # CHECK 6 — PRICE MUST BE POSITIVE
            # --------------------------------------------------------------------------------------

            if price <= 0:
                bad_rows.append(
                    BadRow(
                        line_number=line_number,
                        reason=f"price must be positive, got {price}",
                    )
                )
                continue

            # --------------------------------------------------------------------------------------
            # ROW ACCEPTED
            # --------------------------------------------------------------------------------------
            #
            # Only after every required field has passed validation do
            # we construct a trusted Trade object.
            # --------------------------------------------------------------------------------------

            good_trades.append(
                Trade(
                    trade_id=trade_id,
                    trader=trader,
                    side=side,
                    quantity=quantity,
                    price=price,
                )
            )

    return good_trades, bad_rows
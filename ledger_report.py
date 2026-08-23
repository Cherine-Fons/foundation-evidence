
"""Small human-readable report for the Foundation Exit Test ledger."""

from ledger_model import Ledger
from ledger_parser import parse_ledger


def main() -> None:
    # Parse the external text file.
    #
    # The parser separates successfully validated Trade objects from
    # malformed physical rows.
    good_trades, bad_rows = parse_ledger("ledger.txt")

    # Construct the domain model from good trades only.
    #
    # Bad rows never enter the Ledger.
    ledger = Ledger(good_trades)

    # ----------------------------------------------------------------------------------------------
    # SUMMARY
    # ----------------------------------------------------------------------------------------------
    #
    # HAND PREDICTIONS:
    #
    #     good trades  -> 5
    #     bad rows     -> 3
    #     total volume -> 128
    #
    #     traders
    #         -> ["alice", "bob", "carol", "dana"]
    #
    # ----------------------------------------------------------------------------------------------

    print("Good trades:", len(good_trades))
    print("Bad rows:", len(bad_rows))
    print("Total volume:", ledger.total_volume())
    print("Traders:", ledger.traders())

    # ----------------------------------------------------------------------------------------------
    # NET POSITIONS
    # ----------------------------------------------------------------------------------------------
    #
    # The Ledger owns the position calculation.
    #
    # The report merely asks for each actual trader's result.
    #
    # HAND PREDICTIONS:
    #
    #     alice -> 10
    #     bob   -> 2
    #     carol -> -9
    #     dana  -> 12
    #
    # ----------------------------------------------------------------------------------------------

    print()
    print("Net positions:")

    for trader in ledger.traders():
        print(f"{trader}: {ledger.net_position(trader)}")

    # ----------------------------------------------------------------------------------------------
    # BAD-ROW DIAGNOSTICS
    # ----------------------------------------------------------------------------------------------
    #
    # HAND PREDICTIONS:
    #
    #     line 3 -> quantity must be an integer, got 'x'
    #     line 4 -> expected 5 fields, got 4
    #     line 7 -> quantity must be an integer, got ''
    #
    # ----------------------------------------------------------------------------------------------

    print()
    print("Bad rows:")

    for bad_row in bad_rows:
        print(f"line {bad_row.line_number}: {bad_row.reason}")


# ==================================================================================================
# SCRIPT GUARD
# ==================================================================================================
#
# Direct execution:
#
#     python ledger_report.py
#
# causes:
#
#     __name__ == "__main__"
#
# and therefore runs main().
#
#
# Import:
#
#     import ledger_report
#
# gives:
#
#     __name__ == "ledger_report"
#
# and therefore does NOT run main().
#
# This keeps importing the module silent.
#
# ==================================================================================================


if __name__ == "__main__":
    main()
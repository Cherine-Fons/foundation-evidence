import matplotlib.pyplot as plt
import pytest

# ==================================================================================================
# EXIT CHECK 4
# F6 — MATPLOTLIB, BLACK/RUFF, PYTEST, TYPE/NUMERICAL REASONING
# ==================================================================================================


# --------------------------------------------------------------------------------------------------
# Task 1 — labeled, saved, regenerable two-panel figure
# --------------------------------------------------------------------------------------------------
#
# Given:
#
# days    = [1, 2, 3, 4, 5]
# prices  = [100, 103, 101, 105, 104]
# returns = [0.0, 0.03, -0.019, 0.040, -0.010]
#
# Build:
#
# - one Figure
# - two Axes stacked vertically
# - prices on the top panel
# - returns on the bottom panel
# - shared x-axis
# - title
# - y-label on each panel
# - x-label on bottom panel only
# - save to artifacts/exit_check.png
# - display with plt.show()
#
#
# Prediction:
#
# plt.subplots(2, 1, sharex=True)
#
# 2 rows × 1 column means the panels will be stacked:
#
#     TOP
#     Prices
#
#     BOTTOM
#     Returns
#
# Because sharex=True, both panels will use the same Day x-axis.
# The Day tick labels / x-label should appear only on the bottom panel.
#
# Day 4 should align vertically:
#
#     Top panel:    price = 105
#                       |
#                       | same x-position
#                       v
#     Bottom panel: return = 0.040
#
# The completed figure should also be saved permanently as:
#
#     artifacts/exit_check.png


days = [1, 2, 3, 4, 5]
prices = [100, 103, 101, 105, 104]
returns = [0.0, 0.03, -0.019, 0.040, -0.010]


fig, (ax_top, ax_bottom) = plt.subplots(2, 1, sharex=True)


# Top panel — prices
ax_top.plot(days, prices)
ax_top.set_title("Prices and returns")
ax_top.set_ylabel("Price")


# Bottom panel — returns
ax_bottom.plot(days, returns)
ax_bottom.set_ylabel("Return")
ax_bottom.set_xlabel("Day")


# Save the complete labeled figure before displaying it
fig.savefig("artifacts/exit_check.png")


# Display the figure
plt.show()


# Expected:
#
# - two vertically stacked panels
# - prices on top
# - returns on bottom
# - shared Day x-axis
# - Day label only on bottom panel
# - Price / Return y-labels
# - title: "Prices and returns"
# - artifacts/exit_check.png created with non-zero size
#
#
# Run from foundation %:
#
# python exit_check4.py
#
# Then verify:
#
# ls -la artifacts/exit_check.png


# --------------------------------------------------------------------------------------------------
# Task 2 — formatter and linter, unaided
# --------------------------------------------------------------------------------------------------
#
# QUESTION:
#
# Run Black and Ruff on this file from memory.
#
#
# Prediction:
#
# Black is the formatter:
#
#     black exit_check4.py
#
# It may report:
#
#     reformatted exit_check4.py
#
# or:
#
#     exit_check4.py wasn't modified
#
# depending on whether the file already matches Black's canonical formatting.
#
#
# Ruff is the linter:
#
#     ruff check exit_check4.py
#
# If there are no enabled lint violations, I expect:
#
#     All checks passed!
#
#
# If Ruff reports an auto-fixable [*] problem, run:
#
#     ruff check --fix exit_check4.py
#
#
# Core distinction:
#
#     black
#         -> reformats / rewrites layout
#
#     ruff check
#         -> inspects and reports lint problems
#
#     ruff check --fix
#         -> inspects and automatically fixes eligible [*] violations
#
#
# Run from foundation % AFTER Task 1 works:
#
# black exit_check4.py
# ruff check exit_check4.py


# --------------------------------------------------------------------------------------------------
# Task 3 — passing float test, cold
# --------------------------------------------------------------------------------------------------
#
# Write:
#
# - one function that returns a float
# - one pytest test
# - use pytest.approx(...) rather than exact == against a raw float
#
#
# Prediction / hand-derived expected value:
#
# simple_return(100, 110)
#
#     = (110 - 100) / 100
#     = 10 / 100
#     = 0.1
#
# Therefore the expected result is:
#
#     0.1
#
#
# We use:
#
#     pytest.approx(0.1)
#
# because floating-point calculations can contain tiny binary-representation
# differences.
#
# This is the same numerical-tolerance idea from F5:
#
#     np.allclose(...)
#
# and:
#
#     eigenvalues >= -1e-12
#
# rather than demanding exact floating-point equality.


def simple_return(old_price: float, new_price: float) -> float:
    return (new_price - old_price) / old_price


def test_simple_return():
    assert simple_return(100, 110) == pytest.approx(0.1)


# Prediction:
#
# Running pytest on this file should discover:
#
#     test_simple_return
#
# and it should PASS.
#
#
# Run from foundation %:
#
# python -m pytest exit_check4.py -v
#
# Expected:
#
# exit_check4.py::test_simple_return PASSED
#
# 1 passed
#
#
# NOTE:
#
# Running:
#
#     python exit_check4.py
#
# does NOT automatically run the pytest test.
#
# It executes the script normally.
#
# Running:
#
#     python -m pytest exit_check4.py -v
#
# invokes pytest and tells it to collect and execute the test function.


# --------------------------------------------------------------------------------------------------
# Task 4 — NumPy axis reasoning, no code
# --------------------------------------------------------------------------------------------------
#
# GIVEN:
#
# A NumPy array has shape:
#
#     (4, 3)
#
# where:
#
#     4 = days
#     3 = assets
#
# So:
#
#     shape = (4, 3)
#              ^  ^
#              |  |
#            days assets
#
#
# QUESTION:
#
# We want the mean return PER ASSET.
#
# Which axis should disappear?
#
#
# Reasoning:
#
# To obtain one mean for each asset, we must average ACROSS THE DAYS.
#
# The 4-day dimension must disappear.
#
# The rule from F5 is:
#
#     THE NAMED AXIS DISAPPEARS.
#
# Days are axis 0 in shape (4, 3), so:
#
#     axis = 0
#
#
# Therefore:
#
#     (4, 3) --mean(axis=0)--> (3,)
#
#
# Answer:
#
#     axis = 0
#
#     result length = 3
#
#     disappearing dimension = the 4-day dimension
#
#     remaining dimension = the 3 assets
#
#
# Prediction:
#
# One average return per asset gives:
#
#     shape (3,)
#
#
# RULE TO BANK:
#
# For shape (4 days, 3 assets):
#
#     mean(axis=0)
#
# collapses the rows / days and leaves one value for each column / asset.


# ==================================================================================================
# EXIT CHECK 4 — RUN ORDER
# ==================================================================================================
#
# 1. Run the script:
#
#        python exit_check4.py
#
#    Confirm:
#
#        - two-panel figure renders correctly
#        - close the plot window to return to the terminal
#        - artifacts/exit_check.png exists
#
#
# 2. Format:
#
#        black exit_check4.py
#
#
# 3. Lint:
#
#        ruff check exit_check4.py
#
#    If Ruff marks something [*] fixable:
#
#        ruff check --fix exit_check4.py
#
#
# 4. Run the pytest test:
#
#        python -m pytest exit_check4.py -v
#
#    Expected:
#
#        1 passed
#
#
# 5. Run the complete project test suite:
#
#        python -m pytest
#
#    Previous suite size before this exit-check test:
#
#        9 tests
#
#    If pytest also discovers this exit-check test in the way it is invoked,
#    the total may increase accordingly.
#
#
# 6. Check Git:
#
#        git status
#
#
# 7. Stage and commit when the exit check is confirmed:
#
#        git add exit_check4.py
#
#        git commit -m "exit check 4: F6 plotting, tooling, pytest, axis reasoning"
#
#
# ==================================================================================================

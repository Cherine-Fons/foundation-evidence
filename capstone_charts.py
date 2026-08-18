import matplotlib.pyplot as plt

from finance_utils import mean_return

# Shared x-axis values
days = [1, 2, 3, 4, 5]


# Raw price series
asset_a = [100, 102, 101, 104, 103]
asset_b = [30, 31, 33, 32, 34]


# Normalize Asset A to base 100
norm_a = [p / asset_a[0] * 100 for p in asset_a]


# Normalize Asset B to base 100
norm_b = [p / asset_b[0] * 100 for p in asset_b]


# Create one figure with one axes
fig, ax = plt.subplots()


# Plot BOTH normalized price series on the same axes
#
# The label= keyword gives each line a name that ax.legend() can display.
ax.plot(days, norm_a, label="Asset A")
ax.plot(days, norm_b, label="Asset B")


# Display a legend identifying the two lines
ax.legend()


# Label the chart
ax.set_title("Normalized prices (base 100)")
ax.set_xlabel("Day")
ax.set_ylabel("Normalized price")


# Save the completed figure to disk
fig.savefig("artifacts/normalized_prices.png")


# Display the figure
plt.show()


# Two return series
returns_a = [0.02, -0.01, 0.03, -0.01]
returns_b = [0.01, 0.04, -0.02, 0.05]


# Compute the mean return for each asset using our tested Day 33 helper function
mean_a = mean_return(returns_a)
mean_b = mean_return(returns_b)


# Create a NEW figure and axes for Chart 2
fig2, ax2 = plt.subplots()


# Draw one vertical bar for each asset
#
# x-axis categories:
#     "Asset A"
#     "Asset B"
#
# bar heights:
#     mean_a
#     mean_b
ax2.bar(["Asset A", "Asset B"], [mean_a, mean_b])


# Label the chart
ax2.set_title("Mean return by asset")
ax2.set_ylabel("Mean return")


# Save the completed second figure to disk
fig2.savefig("artifacts/mean_returns_bar.png")


# Display the second figure
plt.show()


# ==================================================================================================
# DAY 34 (F6D6) — F6 CAPSTONE
# CHART 1: NORMALIZED-PRICE LINE CHART
# ==================================================================================================
#
# WHAT ARE WE DOING?
# --------------------------------------------------------------------------------------------------
#
# We want to compare the price movement of TWO assets that trade at very different
# raw dollar prices.
#
# Asset A trades around:
#
#     $100
#
# Asset B trades around:
#
#     $30
#
# If we plotted the RAW prices directly, Asset A would sit much higher on the chart
# simply because its dollar price is larger.
#
# That would make it harder to compare how much the two assets actually moved
# RELATIVE TO THEIR OWN STARTING PRICES.
#
# NORMALIZATION fixes this problem.
#
# We rebase BOTH price series so that they begin at:
#
#     100
#
# Once both assets start from the same base value, the chart compares RELATIVE GROWTH
# rather than raw dollar price.
#
#
# --------------------------------------------------------------------------------------------------
# NORMALIZATION FORMULA
# --------------------------------------------------------------------------------------------------
#
# The general formula is:
#
#     normalized = [p / prices[0] * 100 for p in prices]
#
# where:
#
#     p
#         -> the current price being processed
#
#     prices[0]
#         -> the FIRST price in the series
#         -> the starting price
#
#     * 100
#         -> rebases the series so that the starting value becomes 100
#
#
# For the FIRST element:
#
#     prices[0] / prices[0] * 100
#
#     = 1 * 100
#
#     = 100
#
# Therefore, every normalized series begins at exactly:
#
#     100
#
#
# --------------------------------------------------------------------------------------------------
# WHY ARE THERE TWO NORMALIZATION FORMULAS?
# --------------------------------------------------------------------------------------------------
#
# The generic formula:
#
#     normalized = [p / prices[0] * 100 for p in prices]
#
# is applied separately to each asset.
#
# Asset A:
#
#     norm_a = [p / asset_a[0] * 100 for p in asset_a]
#
# Asset B:
#
#     norm_b = [p / asset_b[0] * 100 for p in asset_b]
#
# The formula is IDENTICAL.
#
# The only difference is which price list is being normalized.
#
#
# --------------------------------------------------------------------------------------------------
# NEW MATPLOTLIB PIECES
# --------------------------------------------------------------------------------------------------
#
# Today we plot TWO lines on the SAME axes:
#
#     ax.plot(days, norm_a, label="Asset A")
#     ax.plot(days, norm_b, label="Asset B")
#
# The new keyword argument:
#
#     label="Asset A"
#
# gives the plotted line a name.
#
# Then:
#
#     ax.legend()
#
# reads those labels and displays a legend so we can tell which line represents
# which asset.
#
#
# --------------------------------------------------------------------------------------------------
# DATA
# --------------------------------------------------------------------------------------------------
#
# Both assets have five observations across the same five days.
#
# Asset A:
#
#     100 -> 102 -> 101 -> 104 -> 103
#
# Asset B:
#
#      30 ->  31 ->  33 ->  32 ->  34
#
# Their RAW prices are on very different scales.
#
#
# --------------------------------------------------------------------------------------------------
# PREDICTION 1
# --------------------------------------------------------------------------------------------------
#
# QUESTION:
#
# Asset A begins at:
#
#     100
#
# Asset B begins at:
#
#     30
#
# After normalization, where should BOTH lines begin on the y-axis?
#
#
# PREDICTION:
#
# BOTH lines should begin at:
#
#     100
#
# Asset A:
#
#     100 / 100 * 100
#
#     = 100
#
# Asset B:
#
#     30 / 30 * 100
#
#     = 100
#
# Therefore:
#
#     Asset A starts at normalized value 100
#     Asset B starts at normalized value 100
#
#
# --------------------------------------------------------------------------------------------------
# PREDICTION 2 — WHICH ASSET IS THE BIGGER RELATIVE MOVER?
# --------------------------------------------------------------------------------------------------
#
# We compare the ENDING normalized values.
#
#
# ASSET A:
#
# Raw movement:
#
#     100 -> 103
#
# Normalized ending value:
#
#     103 / 100 * 100
#
#     = 103
#
# Therefore:
#
#     Asset A gained 3%
#
#
# ASSET B:
#
# Raw movement:
#
#     30 -> 34
#
# Normalized ending value:
#
#     34 / 30 * 100
#
#     = approximately 113.33
#
# Therefore:
#
#     Asset B gained approximately 13.33%
#
#
# COMPARISON:
#
#     Asset A ending normalized value = 103.00
#     Asset B ending normalized value = 113.33
#
# Therefore:
#
#     Asset B should appear as the LARGER RELATIVE MOVER.
#
# This is exactly what normalization is designed to reveal.
#
#
# --------------------------------------------------------------------------------------------------
# CODE 
# --------------------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------------------
# EXPECTED RESULT
# --------------------------------------------------------------------------------------------------
#
# The chart should contain:
#
#     TWO lines
#
#     Asset A -> normalized price series
#     Asset B -> normalized price series
#
# BOTH lines should begin at:
#
#     100
#
# Asset A should end at:
#
#     103
#
# Asset B should end at approximately:
#
#     113.33
#
# Therefore, Asset B's line should finish noticeably higher because it experienced
# greater PERCENTAGE growth from its own starting price.
#
#
# CONCEPT TO BANK:
#
# Raw-price comparison asks:
#
#     "What dollar price is each asset trading at?"
#
# Normalized-price comparison asks:
#
#     "How much has each asset moved relative to where it started?"
#
# Normalization puts both series onto the SAME starting scale so their relative
# performance can be compared directly.
#
# ==================================================================================================


# ==================================================================================================
# DAY 34 (F6D6) — F6 CAPSTONE
# CHART 2: MEAN-RETURNS BAR CHART
# ==================================================================================================
#
# IMPORTANT:
# Add this import near the TOP of capstone_charts.py with the other imports:
#
# from finance_utils import mean_return
#
# We are reusing the mean_return() function that we wrote and tested on Day 33.
# That function:
#
#     1. receives a list of returns
#     2. converts the list to a NumPy array
#     3. computes the mean
#     4. returns the result
#
# This is useful because we are now reusing our own tested module instead of
# rewriting the mean calculation inside this plotting script.
#
#
# --------------------------------------------------------------------------------------------------
# WHAT ARE WE DOING?
# --------------------------------------------------------------------------------------------------
#
# Chart 1 compared TWO CONTINUOUS SERIES over time using:
#
#     ax.plot(...)
#
# Chart 2 asks a different question:
#
#     "What is the mean return of each asset, and how do those means compare?"
#
# We no longer need a line through several days.
#
# Instead, we have two DISCRETE CATEGORIES:
#
#     Asset A
#     Asset B
#
# and one numerical quantity for each category:
#
#     mean return
#
# A BAR CHART is appropriate for comparing a quantity across discrete categories.
#
#
# --------------------------------------------------------------------------------------------------
# NEW MATPLOTLIB METHOD
# --------------------------------------------------------------------------------------------------
#
# The new method is:
#
#     ax.bar(categories, values)
#
# It takes TWO arguments:
#
#     categories = what each bar represents on the x-axis
#     values     = how tall each bar should be on the y-axis
#
# For this task:
#
#     categories = ["Asset A", "Asset B"]
#     values     = [mean_a, mean_b]
#
# Therefore:
#
#     ax2.bar(["Asset A", "Asset B"], [mean_a, mean_b])
#
# Matplotlib accepts STRINGS directly as bar-chart x-values.
#
# It will use:
#
#     "Asset A"
#     "Asset B"
#
# as category labels on the x-axis.
#
#
# --------------------------------------------------------------------------------------------------
# WHY ARE WE CREATING fig2 AND ax2?
# --------------------------------------------------------------------------------------------------
#
# Chart 1 already used:
#
#     fig, ax = plt.subplots()
#
# We want Chart 2 to be a COMPLETELY SEPARATE FIGURE.
#
# Therefore we create a NEW figure/axes pair:
#
#     fig2, ax2 = plt.subplots()
#
# This does NOT overwrite Chart 1.
#
# We now have:
#
#     fig / ax   -> Chart 1: normalized-price lines
#
#     fig2 / ax2 -> Chart 2: mean-return bars
#
#
# --------------------------------------------------------------------------------------------------
# DATA
# --------------------------------------------------------------------------------------------------
#
# Asset A has four observed returns:
#
#     0.02   = +2%
#    -0.01   = -1%
#     0.03   = +3%
#    -0.01   = -1%
#
# Asset B has:
#
#     0.01   = +1%
#     0.04   = +4%
#    -0.02   = -2%
#     0.05   = +5%
#
#
# --------------------------------------------------------------------------------------------------
# PREDICTION 1
# --------------------------------------------------------------------------------------------------
#
# QUESTION:
#
# What happens when we give ax2.bar() strings as the x-values?
#
#     ax2.bar(["Asset A", "Asset B"], [mean_a, mean_b])
#
# Will Matplotlib produce an error because the x-values are strings,
# or will it create two labeled category bars?
#
#
# PREDICTION:
#
# It should create TWO BARS.
#
# The x-axis should contain the category labels:
#
#     Asset A        Asset B
#
# Bar charts accept categorical string labels directly.
#
#
# --------------------------------------------------------------------------------------------------
# PREDICTION 2 — COMPUTE THE MEANS BY HAND FIRST
# --------------------------------------------------------------------------------------------------
#
# We should derive the expected values BEFORE trusting mean_return().
#
#
# ASSET A:
#
# mean_a = (0.02 - 0.01 + 0.03 - 0.01) / 4
#
#        = 0.03 / 4
#
#        = 0.0075
#
# Therefore:
#
#     mean_a = 0.0075
#
# which is:
#
#     0.75%
#
#
# ASSET B:
#
# mean_b = (0.01 + 0.04 - 0.02 + 0.05) / 4
#
#        = 0.08 / 4
#
#        = 0.02
#
# Therefore:
#
#     mean_b = 0.02
#
# which is:
#
#     2%
#
#
# COMPARISON:
#
#     Asset A mean = 0.0075 = 0.75%
#     Asset B mean = 0.0200 = 2.00%
#
# Therefore:
#
#     Asset B should have the TALLER BAR.
#
#
# --------------------------------------------------------------------------------------------------
# CODE 
# --------------------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------------------
# EXPECTED RESULT
# --------------------------------------------------------------------------------------------------
#
# The chart should contain:
#
#     TWO vertical bars
#
#     Asset A -> height approximately 0.0075
#     Asset B -> height approximately 0.0200
#
# Asset B's bar should be noticeably taller because:
#
#     0.0200 > 0.0075
#
#
# CONCEPT TO BANK:
#
#     ax.plot(x, y)
#         -> useful for a sequence or series over time
#
#     ax.scatter(x, y)
#         -> useful for relationships between two variables
#
#     ax.hist(data)
#         -> useful for distributions
#
#     ax.bar(categories, values)
#         -> useful for comparing quantities across discrete categories
#
# ==================================================================================================

# Day 34 (F6D6) — F6 Capstone

The F6 capstone contains two charts:

1. **Chart 1 — Normalized-price line chart**
2. **Chart 2 — Mean-returns bar chart**

The first chart introduces **normalization** so assets with different raw price levels can be compared by relative performance.

The second chart introduces **bar charts** for comparing a numerical quantity across discrete categories.

---

# Chart 1 — Normalized-Price Line Chart

## What Are We Doing?

We want to compare the price movement of two assets that trade at very different raw dollar prices.

Asset A trades around:

```text
$100
```

Asset B trades around:

```text
$30
```

If we plotted their raw prices directly, Asset A would sit much higher on the chart simply because its dollar price is larger.

That makes it harder to compare how much the two assets moved **relative to their own starting prices**.

**Normalization fixes this problem.**

We rebase both price series so that they begin at:

```text
100
```

Once both assets start from the same base value, the chart compares **relative growth rather than raw dollar price**.

---

## Normalization Formula

The general formula is:

```python
normalized = [p / prices[0] * 100 for p in prices]
```

where:

- `p` = the current price being processed
- `prices[0]` = the first or starting price in the series
- `* 100` = rebases the series so the starting value becomes 100

For the first element:

```text
prices[0] / prices[0] * 100
= 1 * 100
= 100
```

Therefore, every series normalized to base 100 begins at exactly:

```text
100
```

---

## Why Are There Two Normalization Formulas?

The generic formula:

```python
normalized = [p / prices[0] * 100 for p in prices]
```

is applied separately to each asset.

For Asset A:

```python
norm_a = [p / asset_a[0] * 100 for p in asset_a]
```

For Asset B:

```python
norm_b = [p / asset_b[0] * 100 for p in asset_b]
```

The formula is **identical**.

Only the input price series changes.

> **Same normalization formula, different input list.**

---

## New Matplotlib Pieces

Today we plot **two lines on the same axes**:

```python
ax.plot(days, norm_a, label="Asset A")
ax.plot(days, norm_b, label="Asset B")
```

The new keyword argument:

```python
label="Asset A"
```

gives the plotted line a name.

Then:

```python
ax.legend()
```

reads the labels from the plotted lines and displays a legend identifying them.

> **`label=` names the plotted series. `ax.legend()` displays those names.**

---

## Data

Both assets have five observations across the same five days.

Asset A:

```text
100 → 102 → 101 → 104 → 103
```

Asset B:

```text
30 → 31 → 33 → 32 → 34
```

Their raw prices are on very different scales.

---

## Prediction 1 — Where Will Both Lines Start?

Asset A begins at:

```text
100
```

Asset B begins at:

```text
30
```

After normalization:

### Asset A

```text
100 / 100 * 100
= 100
```

### Asset B

```text
30 / 30 * 100
= 100
```

> **Prediction:** both normalized lines will begin at exactly `100`.

---

## Prediction 2 — Which Asset Is the Bigger Relative Mover?

### Asset A

Raw movement:

```text
100 → 103
```

Normalized ending value:

```text
103 / 100 * 100
= 103
```

Therefore Asset A gained:

```text
3%
```

### Asset B

Raw movement:

```text
30 → 34
```

Normalized ending value:

```text
34 / 30 * 100
≈ 113.33
```

Therefore Asset B gained approximately:

```text
13.33%
```

### Comparison

```text
Asset A ending normalized value = 103.00
Asset B ending normalized value = 113.33
```

> **Prediction:** Asset B will appear as the larger relative mover once the different raw price levels are removed.

This is exactly what normalization is designed to reveal.

---

## Chart 1 Code

The imports for the complete capstone script should include **both Matplotlib and the tested `mean_return` helper that Chart 2 will use**:

```python
import matplotlib.pyplot as plt
from finance_utils import mean_return
```

Then Chart 1 is:

```python
days = [1, 2, 3, 4, 5]

asset_a = [100, 102, 101, 104, 103]
asset_b = [30, 31, 33, 32, 34]

norm_a = [p / asset_a[0] * 100 for p in asset_a]
norm_b = [p / asset_b[0] * 100 for p in asset_b]

fig, ax = plt.subplots()

ax.plot(days, norm_a, label="Asset A")
ax.plot(days, norm_b, label="Asset B")

ax.legend()

ax.set_title("Normalized prices (base 100)")
ax.set_xlabel("Day")
ax.set_ylabel("Normalized price")

fig.savefig("artifacts/normalized_prices.png")

plt.show()
```

---

## Expected Chart 1 Result

The chart should contain:

- two lines
- Asset A and Asset B identified in a legend
- both lines beginning at `100`
- Asset A ending at `103`
- Asset B ending at approximately `113.33`

Asset B should finish noticeably higher because it experienced greater **percentage growth from its own starting price**.

---

## Chart 1 Concept to Bank

Raw-price comparison asks:

> **What dollar price is each asset trading at?**

Normalized-price comparison asks:

> **How much has each asset moved relative to where it started?**

Normalization puts both series onto the same starting scale so their relative performance can be compared directly.

---

# Chart 2 — Mean-Returns Bar Chart

## What Are We Doing?

Chart 1 compared two continuous price series across time using:

```python
ax.plot(...)
```

Chart 2 asks a different question:

> **What is the mean return of each asset, and how do those means compare?**

We no longer need a line connecting values across days.

Instead, we have two **discrete categories**:

```text
Asset A
Asset B
```

and one numerical quantity associated with each:

```text
mean return
```

A **bar chart** is appropriate for comparing a numerical quantity across discrete categories.

---

## New Matplotlib Method

The new method is:

```python
ax.bar(categories, values)
```

It takes two arguments:

```text
categories = what each bar represents
values     = how tall each bar should be
```

For this task:

```python
categories = ["Asset A", "Asset B"]
values = [mean_a, mean_b]
```

Therefore:

```python
ax2.bar(["Asset A", "Asset B"], [mean_a, mean_b])
```

---

## Can the X-Values Be Strings?

Yes.

Unlike the numerical x-axis used in the line charts, Matplotlib bar charts accept categorical strings directly.

Therefore:

```python
["Asset A", "Asset B"]
```

should produce two category labels on the x-axis.

> **Prediction:** Matplotlib will create two labeled bars rather than raising an error.

---

## Why Are We Creating `fig2` and `ax2`?

Chart 1 already uses:

```python
fig, ax = plt.subplots()
```

Chart 2 should be a **separate figure**, not another plot placed onto Chart 1.

Therefore we create another figure/axes pair:

```python
fig2, ax2 = plt.subplots()
```

We now have:

```text
fig / ax
    → Chart 1
    → normalized-price lines

fig2 / ax2
    → Chart 2
    → mean-return bars
```

> One Python script can create multiple independent Matplotlib figures.

---

## Reusing Our Tested Function

Instead of rewriting the mean calculation, Chart 2 uses the `mean_return()` function created and tested on Day 33.

At the top of `capstone_charts.py`:

```python
from finance_utils import mean_return
```

This makes the name:

```python
mean_return
```

available inside the capstone script.

Without this import, Python reaches:

```python
mean_a = mean_return(returns_a)
```

and raises:

```text
NameError: name 'mean_return' is not defined
```

The function exists in `finance_utils.py`, but functions in another module must be explicitly imported before the current script can use them.

---

## Return Data

Asset A:

```python
returns_a = [0.02, -0.01, 0.03, -0.01]
```

Asset B:

```python
returns_b = [0.01, 0.04, -0.02, 0.05]
```

---

## Prediction 1 — What Will `ax2.bar()` Produce?

The call is:

```python
ax2.bar(["Asset A", "Asset B"], [mean_a, mean_b])
```

The strings:

```text
Asset A
Asset B
```

are categorical x-axis values.

> **Prediction:** the chart will contain two vertical bars labeled `Asset A` and `Asset B`.

The height of each bar represents that asset's mean return.

---

## Prediction 2 — Compute the Means by Hand

Before trusting `mean_return()`, derive the expected results independently.

### Asset A

```text
mean_a = (0.02 - 0.01 + 0.03 - 0.01) / 4

       = 0.03 / 4

       = 0.0075
```

Therefore:

```text
mean_a = 0.0075
```

or:

```text
0.75%
```

### Asset B

```text
mean_b = (0.01 + 0.04 - 0.02 + 0.05) / 4

       = 0.08 / 4

       = 0.02
```

Therefore:

```text
mean_b = 0.02
```

or:

```text
2%
```

### Comparison

```text
Asset A mean = 0.0075 = 0.75%
Asset B mean = 0.0200 = 2.00%
```

> **Prediction:** Asset B will have the taller bar because `0.0200 > 0.0075`.

---

## Chart 2 Code

This section goes **after Chart 1's `plt.show()`**:

```python
returns_a = [0.02, -0.01, 0.03, -0.01]
returns_b = [0.01, 0.04, -0.02, 0.05]

mean_a = mean_return(returns_a)
mean_b = mean_return(returns_b)

fig2, ax2 = plt.subplots()

ax2.bar(["Asset A", "Asset B"], [mean_a, mean_b])

ax2.set_title("Mean return by asset")
ax2.set_ylabel("Mean return")

fig2.savefig("artifacts/mean_returns_bar.png")

plt.show()
```

---

## Expected Chart 2 Result

The chart should contain two vertical bars:

```text
Asset A → height approximately 0.0075
Asset B → height approximately 0.0200
```

Asset B's bar should be noticeably taller.

---

# Complete `capstone_charts.py` Executable Code

The complete script should therefore have this structure:

```python
import matplotlib.pyplot as plt
from finance_utils import mean_return


# CHART 1 — NORMALIZED PRICES

days = [1, 2, 3, 4, 5]

asset_a = [100, 102, 101, 104, 103]
asset_b = [30, 31, 33, 32, 34]

norm_a = [p / asset_a[0] * 100 for p in asset_a]
norm_b = [p / asset_b[0] * 100 for p in asset_b]

fig, ax = plt.subplots()

ax.plot(days, norm_a, label="Asset A")
ax.plot(days, norm_b, label="Asset B")

ax.legend()

ax.set_title("Normalized prices (base 100)")
ax.set_xlabel("Day")
ax.set_ylabel("Normalized price")

fig.savefig("artifacts/normalized_prices.png")

plt.show()


# CHART 2 — MEAN RETURNS BAR CHART

returns_a = [0.02, -0.01, 0.03, -0.01]
returns_b = [0.01, 0.04, -0.02, 0.05]

mean_a = mean_return(returns_a)
mean_b = mean_return(returns_b)

fig2, ax2 = plt.subplots()

ax2.bar(["Asset A", "Asset B"], [mean_a, mean_b])

ax2.set_title("Mean return by asset")
ax2.set_ylabel("Mean return")

fig2.savefig("artifacts/mean_returns_bar.png")

plt.show()
```

---

# Chart-Type Concepts to Bank

## Line Plot

```python
ax.plot(x, y)
```

Use for:

```text
sequence over time
```

The order of observations matters, so the points are connected.

---

## Scatter Plot

```python
ax.scatter(x, y)
```

Use for:

```text
relationship between two variables
```

The points remain unconnected because their positions carry the meaning.

---

## Histogram

```python
ax.hist(data)
```

Use for:

```text
distribution of numerical values
```

Matplotlib groups the observations into bins and the bar height represents frequency.

---

## Bar Chart

```python
ax.bar(categories, values)
```

Use for:

```text
comparing quantities across discrete categories
```

Each category receives one bar whose height represents its numerical value.

---

# F6 Capstone Summary

Chart 1 asks:

> **How did the two assets perform relative to their own starting prices?**

Solution:

```text
normalize to base 100
→ plot both lines together
→ compare relative growth
```

Chart 2 asks:

> **Which asset had the higher average return?**

Solution:

```text
compute mean return
→ represent each asset as a category
→ compare bar heights
```

Together, the capstone reinforces the central idea that the **chart type should match the question being asked of the data**.
# Day 25 — 2D arrays and axis reasoning (f5d3). This is the conceptual center of the week: the jump from a flat list of numbers to a **table** of them, and learning how to reduce that table along one direction or the other. Axis reasoning is the single most-confused thing in NumPy, so we build it slowly and concretely.

First, environment. Confirm you're at `>>>` with numpy imported — if you closed the interpreter, relaunch with `python` (not `python3`) from `(.venv)`, then `import numpy as np`. Everything today goes at `>>>`, not `foundation %` (the trap that bit twice — stay in the Python tab).

**Framing — a 2D array is a table.** A 1D array is a row of numbers. A 2D array is rows *and* columns — a small matrix. In finance the convention we'll use: **rows = time steps (days), columns = assets.** So a 3×2 array is three days of returns for two assets.

Build the fixture (this is your data table — type it at `>>>`, mind the nested brackets):

```
data = np.array([[0.01, 0.02],
                 [0.03, 0.04],
                 [0.05, 0.06]])
```

Read it as: day 1 → asset A 0.01, asset B 0.02; day 2 → 0.03, 0.04; day 3 → 0.05, 0.06.

Now predict before running — this is the shape-reading rule from Day 23 (outer bracket = rows, inner length = columns):

`data.shape` → what tuple? And say it in words: how many rows (days), how many columns (assets), and which number is which?

Run:

```
data.shape
```

Give me the prediction with the rows/columns reasoning, then the output. Once the table's on screen and you've confirmed its shape, we frame axis — the part that makes it *do* something.
------------------------------------------------------------------------------------------
# PREDICTION

```python
data.shape
```

should return:

```python
(3, 2)
```

Reasoning: the array is a table with **3 rows** and **2 columns**:

```text
           asset A   asset B
day 1       0.01      0.02
day 2       0.03      0.04
day 3       0.05      0.06
```

So:

```text
(3, 2)
 ↑  ↑
rows columns
days assets
```

Expected output:

```python
>>> data.shape
(3, 2)
```

The rule to keep in mind is:

> **For a 2D NumPy array, `.shape` is `(rows, columns)`.**
---------------------------------------------------------------------------------------------------------

# RESULT

Correct — `(3, 2)`: three rows (days), two columns (assets), outer bracket count first. The table's shape is confirmed.

# NEXT

# Now the piece the whole day turns on: **axis.** This is where nearly everyone stumbles, so we frame it carefully and I want you to fight your first instinct.

When you reduce a 2D array — sum it, average it — you have to tell NumPy *which direction* to collapse. That direction is the **axis**, and the numbering follows the shape tuple you just saw:

- **`axis=0` is the first number in `(3, 2)` — the rows.** It collapses *down* through the rows, leaving one value per column. Three days collapse into a per-asset result. Output length = number of columns = 2.
- **`axis=1` is the second number — the columns.** It collapses *across* the columns, leaving one value per row. Two assets collapse into a per-day result. Output length = number of rows = 3.

The trap, stated so you can brace against it: **`axis=0` does not mean "operate on the rows," it means "collapse the row dimension away."** People read `axis=0` and think "give me row sums" — it's the opposite. `axis=0` eats the rows and hands you column totals. The mnemonic that survives: **the axis you name is the one that disappears.** Name axis 0, the row dimension (the 3) vanishes, you're left with 2 numbers.

Let me make it concrete with your data before you predict. `data` is:

```
day 1:  0.01  0.02
day 2:  0.03  0.04
day 3:  0.05  0.06
```

`data.sum(axis=0)` collapses the day dimension → adds each **column** down through all days → `[0.01+0.03+0.05, 0.02+0.04+0.06]` → one total per asset, length 2.

`data.sum(axis=1)` collapses the asset dimension → adds each **row** across both assets → one total per day, length 3.

Now predict — reason from "the named axis disappears," don't guess:

1. `data.sum(axis=0)` → what array, and what length? Compute the actual numbers.
2. `data.sum(axis=1)` → what array, and what length? Compute the actual numbers.

Run at `>>>`:

```
data.sum(axis=0)
data.sum(axis=1)
```

Both predictions with the numbers and the length reasoning, then the output.
--------------------------------------------------------------------------------------------------
Prediction:

```python
data.sum(axis=0)
```

collapses the **row/day dimension**, so it adds down each column:

```text
asset A: 0.01 + 0.03 + 0.05 = 0.09
asset B: 0.02 + 0.04 + 0.06 = 0.12
```

So:

```python
array([0.09, 0.12])
```

Length = **2**, because axis 0 disappears and the two columns remain.

For:

```python
data.sum(axis=1)
```

it collapses the **column/asset dimension**, so it adds across each row:

```text
day 1: 0.01 + 0.02 = 0.03
day 2: 0.03 + 0.04 = 0.07
day 3: 0.05 + 0.06 = 0.11
```

So:

```python
array([0.03, 0.07, 0.11])
```

Length = **3**, because axis 1 disappears and the three rows remain.

So the expected output is:

```python
>>> data.sum(axis=0)
array([0.09, 0.12])

>>> data.sum(axis=1)
array([0.03, 0.07, 0.11])
```

# The mnemonic is exactly the right one:

> **The axis you name is the dimension NumPy collapses away.**
----------------------------------------------------------------------------------------------------------

Both exactly right — and check them against "the named axis disappears":

- `data.sum(axis=0)` → `array([0.09, 0.12])`, **length 2**. You named axis 0 (the rows, the 3), so the 3 vanished and you're left with 2 — one total per **asset**, summed down through all three days. `0.01+0.03+0.05 = 0.09`, `0.02+0.04+0.06 = 0.12`. ✓
- `data.sum(axis=1)` → `array([0.03, 0.07, 0.11])`, **length 3**. You named axis 1 (the columns, the 2), so the 2 vanished, leaving 3 — one total per **day**, summed across both assets. `0.01+0.02 = 0.03`, etc. ✓

That's axis reasoning working. The shape tuple `(3, 2)` literally tells you the output length before you run it: name axis 0, kill the 3, keep the 2; name axis 1, kill the 2, keep the 3.

Now let's pin it against the trap one more time, because there's a *third* case people forget, and it's the one that catches you in real code. Predict:

`data.sum()` — no axis argument at all. What comes back? Reason: if naming an axis collapses *that* dimension, what does naming *no* axis do? (Hint: how many dimensions are left to collapse?)

And the finance-real one, the actual Day-25 card content (Ch 8 Simple Ex 2 is "mean per asset and per time step"):

`data.mean(axis=0)` — the **average** return per asset across the three days. Which axis, and why that one? Predict the array. (Same axis logic as sum, different reduction.)

Run at `>>>`:

```
data.sum()
data.mean(axis=0)
```

Both predictions with reasoning, then output. After this we do the axis-swap gotcha and commit f5d3.
----------------------------------------------------------------------------------------------------------

# Prediction:

```python
data.sum()
```

With **no axis specified**, NumPy collapses **all dimensions**. The whole 3×2 table becomes one number:

```text
0.01 + 0.02 + 0.03 + 0.04 + 0.05 + 0.06 = 0.21
```

So the result is a **scalar**, not an array:

```python
0.21
```

Depending on NumPy’s display, you may see something like `np.float64(0.21)` or a tiny floating-point artifact such as `0.21000000000000002`; numerically, it is 0.21.

For:

```python
data.mean(axis=0)
```

`axis=0` collapses the **rows/days**, leaving one average per **column/asset**.

Asset A:

```text
(0.01 + 0.03 + 0.05) / 3
= 0.09 / 3
= 0.03
```

Asset B:

```text
(0.02 + 0.04 + 0.06) / 3
= 0.12 / 3
= 0.04
```

So:

```python
array([0.03, 0.04])
```

Expected session:

```python
>>> data.sum()
0.21

>>> data.mean(axis=0)
array([0.03, 0.04])
```

The rule is:

> **No `axis` → collapse everything to one scalar. `axis=0` → collapse the days and keep one result per asset.**

----------------------------------------------------------------------------------------------------------
# FEEDBACK

Both right, and both worth naming precisely:

- `data.sum()` → `0.21`, a **scalar** — no array wrapper, just the number. No axis named means *collapse every dimension*: it flattens the whole table to one total. `0.09 + 0.12 = 0.21` (or equivalently all six values added). The rule completes cleanly: name one axis → drop to fewer dimensions; name no axis → drop to a single number. ✓
- `data.mean(axis=0)` → `array([0.03, 0.04])` — average return **per asset** across the three days. Axis 0 because you're collapsing the *day* dimension (the 3 disappears), leaving one mean per column. Asset A averages `(0.01+0.03+0.05)/3 = 0.03`, asset B `(0.02+0.04+0.06)/3 = 0.04`. ✓ That's "mean per asset," exactly the card's target.

So you've got the full reduction family: `sum`/`mean` with `axis=0` (per column/asset), `axis=1` (per row/day), or no axis (whole-table scalar). Same axis logic, swappable reduction.
----------------------------------------------------------------------------------------------------------

# Now the gotcha that makes axis stick — the **swap test**. This is the one that exposes whether you actually understand it or just memorized "0 is columns." Predict, reason hard, don't pattern-match:

You want the **mean per day** (per time step) instead of per asset — average across the two assets for each day. Two predictions:

1. Which axis? `axis=0` or `axis=1`? Say *why* using "the named axis disappears" — which dimension do you need to collapse to get one number per day?
2. What array comes back, and what length? Compute the numbers.

Run at `>>>`:

```
data.mean(axis=1)
```

Prediction with the axis reasoning and the numbers, then output.
----------------------------------------------------------------------------------------------------------
# ANSWER

You want **one mean per day**, so you need to collapse the **asset/column dimension**.

That means:

```python
axis=1
```

Why? Your shape is:

```python
(3, 2)
 ↑  ↑
days assets
```

Naming `axis=1` makes the second dimension—the `2` assets—disappear, leaving the `3` days. So the output must have **length 3**.

Now compute each row's mean:

```text
day 1: (0.01 + 0.02) / 2 = 0.015
day 2: (0.03 + 0.04) / 2 = 0.035
day 3: (0.05 + 0.06) / 2 = 0.055
```

So I predict:

```python
>>> data.mean(axis=1)
array([0.015, 0.035, 0.055])
```

The key distinction is:

> **Mean per asset → collapse days → `axis=0`**
> **Mean per day → collapse assets → `axis=1`**

Or using your stronger mnemonic: **the axis you name is the one that disappears.**
--------------------------------------------------------------------------------------------
# CONCLUSION

That's the swap test passed. You now have the thing most people carry a cheat-sheet for: you can look at (3, 2), decide what you want one-value-per (asset or day), and pick the axis by asking "which dimension disappears" — no guessing, no trial and error. That skill pays off immediately in Day 26 (covariance matrices) and Day 27 (portfolio variance), where axis mistakes are the #1 silent bug.

# DAY 25 SUMMARY


> **The axis I name is the dimension NumPy collapses away. Whatever dimension I do not name is what remains in the result.**

For a 2D array with shape:

```python
(3, 2)
```

I read that as **3 rows and 2 columns**.

* **`axis=0`** means collapse the row dimension. The `3` disappears, so I am left with `2` values — one result for each column. In the finance table, that means combining the days and getting one result **per asset**.

* **`axis=1`** means collapse the column dimension. The `2` disappears, so I am left with `3` values — one result for each row. In the finance table, that means combining the assets and getting one result **per day**.

My shorthand:

> **`axis=0`: collapse down the days → one value per asset.**
> **`axis=1`: collapse across the assets → one value per day.**


# Day 25 ledger:

1. 2D array = table; convention rows = days, columns = assets; .shape reads outer→inner as (rows, cols)
2. axis = the dimension that disappears: axis=0 kills rows → per-column result; axis=1 kills columns → per-row result; no axis → whole-table scalar
3. sum/mean share the axis logic; reduction swaps, axis rule doesn't
4. output length is predictable from the shape tuple before you run it



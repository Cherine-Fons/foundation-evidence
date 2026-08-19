# Two warm-up recalls, then we open the card:

1. From F5: on a 2D array M, does M.sum(axis=1) give a per-row or per-column total, and what's the rule?
2. From F6: why did the finance-utils tests use pytest.approx instead of ==?

1. # F7 Warm-Up — `M.sum(axis=1)`

For a 2D NumPy array:

```python
M.sum(axis=1)
```

gives a **per-row total**.

Why? Because:

> **The named axis disappears.**

If:

```python
M.shape == (rows, columns)
```

then:

```python
M.sum(axis=1)
```

collapses **axis 1**, which is the **column dimension**.

What remains is one value for each row.

Example:

```python
import numpy as np

M = np.array([
    [1, 2, 3],
    [4, 5, 6]
])
```

Shape:

```text
(2, 3)
 ↑  ↑
rows columns
```

Now:

```python
M.sum(axis=1)
```

computes:

```text
row 1: 1 + 2 + 3 = 6
row 2: 4 + 5 + 6 = 15
```

Result:

```python
array([6, 15])
```

Shape changes:

```text
(2, 3) --sum(axis=1)--> (2,)
```

The **3-column dimension disappears**, leaving **2 row totals**.

> **RULE TO BANK:**
> `axis=0` → collapse rows → one result per column.
> `axis=1` → collapse columns → one result per row.
> **The named axis disappears.**

2. # F7 Warm-Up — Why `pytest.approx` Instead of `==`?

The `finance_utils` tests used:

```python
assert actual == pytest.approx(expected)
```

instead of:

```python
assert actual == expected
```

because the functions return **floating-point numbers**.

## Why Exact `==` Can Be Risky

Floats are stored in binary, and many decimal values cannot be represented exactly.

For example:

```python
0.1 + 0.2
```

is mathematically:

```text
0.3
```

but the stored floating-point result can differ by a tiny amount.

So exact equality can fail even when the numerical calculation is mathematically correct.

---

## What `pytest.approx()` Does

```python
pytest.approx(expected)
```

checks whether the actual value is **sufficiently close** to the expected value within a small numerical tolerance.

For example:

```python
def test_mean_return():
    assert mean_return([0.1, 0.2, 0.3]) == pytest.approx(0.2)
```

means:

> The result should be numerically equal to `0.2` up to ordinary floating-point error.

---

## Connection to F5

It is the same numerical-tolerance principle as:

```python
np.allclose(Sigma, Sigma.T)
```

instead of relying on:

```python
Sigma == Sigma.T
```

for floating-point computations.

And similarly:

```python
np.all(eigenvalues >= -1e-12)
```

allowed tiny numerical noise around mathematical zero.

> **RULE TO BANK:** For floating-point calculations, test **numerical closeness**, not necessarily exact binary equality.

So:

```text
F5 → np.allclose(...) / explicit tolerance
F6 → pytest.approx(...)
```

Same idea, different testing tool.
================================================================================================================================================================

# So before we touch the terminal — one prediction. If a Series holds three daily closing prices, and the labels attached to those three values are the dates 2026-07-13, 2026-07-14, 2026-07-15, what do you think you'd be able to do with a Series that you couldn't easily do with a plain NumPy array of the same three numbers? One sentence, your guess.

>You could look up a closing price directly by its date label, e.g. ask for the value at "2026-07-14", instead of having to remember that July 14 happens to be at integer position 1.

# And hold onto why that matters specifically for you: financial data is indexed by time, and time is exactly the kind of label you want to look things up by, slice by ("everything in July"), and align two series on. A plain array makes you translate every date into an integer position by hand. A Series lets the date do the work. That's why every price series, return series, and portfolio table in CPF is going to be pandas, not raw NumPy.

Now let's make one. Open the % prompt — the (.venv) foundation % one — and first the tooling step, which I can hand you directly since installs are exempt from A24:

pip install pandas

Run it, and tell me what the last line says. (You should see pandas plus a couple of dependencies resolve — watch for whether numpy is already satisfied, since you installed it back in F5. Predict before you read the output: do you expect pip to re-download numpy, or skip it?)

# PREDICTION
>Pandas installs; NumPy is reused from the existing venv rather than downloaded again.

======================

# Task — Import pandas with Its Conventional Alias

## What the Task Is Asking

You need to add the **standard pandas import line** at the top of:

```text
prices_series.py
```

This is the pandas equivalent of:

```python
import numpy as np
```

---

## Prediction

**Prediction:** the conventional pandas alias is:

```text
pd
```

So the import line should be:

```python
import pandas as pd
```

### Why

Just as:

```python
import numpy as np
```

lets you write:

```python
np.array(...)
```

instead of:

```python
numpy.array(...)
```

the pandas convention:

```python
import pandas as pd
```

lets you write:

```python
pd.Series(...)
pd.DataFrame(...)
```

instead of the longer:

```python
pandas.Series(...)
pandas.DataFrame(...)
```

---

## What to Write

At the very top of `prices_series.py`:

```python
import pandas as pd
```

Save the file.

---

> **RULE TO BANK:**
> NumPy is conventionally imported as `np`; pandas is conventionally imported as `pd`.

==========================

# Task — Create Your First pandas `Series`

## What the Task Is Asking

You need to create a pandas **Series** named:

```python
prices
```

It should hold:

```text
100.0
102.0
101.0
```

and each value should be paired with a date label:

```text
2026-07-13
2026-07-14
2026-07-15
```

The values and labels must be in the **same order** so each price lines up with the correct date.

---

## What You Need to Use

The constructor shape is:

```python
pd.Series(values, index=labels)
```

Both the values and the labels go in Python **lists**.

---

## Prediction

### 1. What data structure holds the values?

A list:

```python
[100.0, 102.0, 101.0]
```

### 2. What data structure holds the index labels?

Also a list:

```python
["2026-07-13", "2026-07-14", "2026-07-15"]
```

### Why

The first value pairs with the first label, the second with the second, and so on:

```text
2026-07-13 → 100.0
2026-07-14 → 102.0
2026-07-15 → 101.0
```

The index gives each value a **label-based address**.

---

## What to Write

Below:

```python
import pandas as pd
```

write:

```python
prices = pd.Series(
    [100.0, 102.0, 101.0],
    index=["2026-07-13", "2026-07-14", "2026-07-15"],
)
```

Save the file, but do **not** run it yet.

---

> **RULE TO BANK:**
> A pandas `Series` is a one-dimensional sequence of values paired with an `index` of labels. Values and index labels align by position.

==========================

# Task — Print the pandas `Series` and Predict the Output

## What the Task Is Asking

Right now, `prices_series.py` creates the Series but does not display it.

Because this is a **script**, you need to explicitly print the object:

```python
print(prices)
```

Then run:

```bash
python prices_series.py
```

---

## What You Need to Do

Your file should now look like:

```python
import pandas as pd

prices = pd.Series(
    [100.0, 102.0, 101.0],
    index=["2026-07-13", "2026-07-14", "2026-07-15"],
)

print(prices)
```

Save it, then run:

```bash
python prices_series.py
```

---

## Prediction

I expect pandas to print the **index labels on the left** and the **values on the right**, something like:

```text
2026-07-13    100.0
2026-07-14    102.0
2026-07-15    101.0
dtype: float64
```

### What is the bottom line?

My prediction is:

```text
dtype: float64
```

### Why

You already saw `.dtype` in NumPy.

`dtype` means **data type**: what type NumPy/pandas is using to store the values.

Your Series contains:

```python
[100.0, 102.0, 101.0]
```

Those are floating-point numbers, so pandas should store the Series with a floating-point dtype, most likely:

```text
float64
```

---

## What Is New About the Output?

A NumPy array might print only:

```text
[100. 102. 101.]
```

But the pandas Series should print:

```text
label           value
↓               ↓
2026-07-13      100.0
2026-07-14      102.0
2026-07-15      101.0
```

plus:

```text
dtype: float64
```

That is the key difference you are learning:

> the values now carry **labels** with them.

---

> **RULE TO BANK:**
> Printing a pandas `Series` shows **index labels + values + dtype**.
> The index is part of the object, not something you have to track separately.
==================

# Task — Predict the Dictionary Structure for a DataFrame

## What the Task Is Asking

You are **not building the full DataFrame yet**.

You are only predicting the dictionary structure that would supply two columns:

```text
price
volume
```

In a pandas `DataFrame` built from a dictionary:

> **each dictionary key becomes a column name, and each value is the sequence of values in that column.**

---

## Prediction

The dictionary should look like:

```python
{
    "price": [...],
    "volume": [...],
}
```

More specifically, with the actual data:

```python
{
    "price": [100.0, 102.0, 101.0],
    "volume": [1500, 1800, 1200],
}
```

---

## Why

The mapping is:

```text
dictionary key
    ↓
DataFrame column name

dictionary value
    ↓
values going down that column
```

So:

```python
"price": [100.0, 102.0, 101.0]
```

means:

```text
column name = price
column values = 100.0, 102.0, 101.0
```

And:

```python
"volume": [1500, 1800, 1200]
```

means:

```text
column name = volume
column values = 1500, 1800, 1200
```

---

> **RULE TO BANK:**
> When building a pandas `DataFrame` from a dictionary, **keys become column names and the mapped lists become the column values**.

========================

# Task — Build Your First pandas `DataFrame`

## What the Task Is Asking

You already built a one-dimensional labeled `Series`.

Now you are extending that idea into a **DataFrame** with:

* the same three date labels as the row index
* one `"price"` column
* one `"volume"` column

A DataFrame is essentially several labeled columns sharing the same row index.

---

## What You Need to Do

In `prices_series.py`, below:

```python
print(prices)
```

add:

```python
df = pd.DataFrame(
    {
        "price": [100.0, 102.0, 101.0],
        "volume": [1500, 1800, 1200],
    },
    index=["2026-07-13", "2026-07-14", "2026-07-15"],
)

print(df)
```

Then save the file.

---

## What Is Happening Here?

The dictionary:

```python
{
    "price": [100.0, 102.0, 101.0],
    "volume": [1500, 1800, 1200],
}
```

defines the **columns**.

The `index=` list:

```python
["2026-07-13", "2026-07-14", "2026-07-15"]
```

defines the **row labels**.

So pandas lines everything up like:

```text
             price   volume
2026-07-13   100.0   1500
2026-07-14   102.0   1800
2026-07-15   101.0   1200
```

---

## Prediction — How Will the DataFrame Print Differently From the Series?

**Prediction:** the DataFrame will print as a **two-dimensional table with column headers**.

The Series printed one labeled value column:

```text
2026-07-13    100.0
2026-07-14    102.0
2026-07-15    101.0
dtype: float64
```

The DataFrame should instead show:

```text
             price  volume
2026-07-13   100.0    1500
2026-07-14   102.0    1800
2026-07-15   101.0    1200
```

### Why

A `Series` has one value sequence.

A `DataFrame` has **multiple named columns sharing one index**, so pandas needs to print:

* the index down the left
* column names across the top
* multiple values across each row

One concrete difference is therefore:

> **The DataFrame has named column headers across the top; the Series did not.**

---

## Run It

From:

```text
(.venv) foundation %
```

run:

```bash
python prices_series.py
```

You should see the Series output first, followed by the DataFrame output.

---

> **RULE TO BANK:**
> A `Series` is one labeled column. A `DataFrame` is multiple named columns sharing the same index.

============================

# Task — Add a Daily Returns Column

## What the Task Is Asking

You already have a DataFrame with:

* a `"price"` column
* a `"volume"` column
* dates as the shared index

Now you need to add a third column:

```text
return
```

This column should contain the **day-over-day fractional price change**.

The pandas method that does that is:

```python
df["price"].pct_change()
```

---

## What You Need to Do

Add this line below the DataFrame creation:

```python
df["return"] = df["price"].pct_change()
```

Then add another:

```python
print(df)
```

at the bottom so you can see the updated table.

So the new section is:

```python
df["return"] = df["price"].pct_change()

print(df)
```

---

## What Is Happening Here?

This part:

```python
df["price"]
```

selects the `"price"` column from the DataFrame.

That gives you a pandas `Series`.

Then:

```python
.pct_change()
```

computes the fractional change from each row to the previous row.

Conceptually:

```text
(today - yesterday) / yesterday
```

for every row after the first.

So pandas is effectively doing the repeated comparison for you without an explicit loop.

---

## Prediction 1 — Return on `2026-07-14`

Price moves:

```text
100 → 102
```

So:

```text
(102 - 100) / 100
= 2 / 100
= 0.02
```

**Prediction:**

```text
2026-07-14 → 0.02
```

which means a:

```text
2% gain
```

---

## Prediction 2 — Return on `2026-07-13`

The first row has no previous row.

There is no earlier price available to compute:

```text
(today - yesterday) / yesterday
```

So the first return is undefined.

I expect pandas to display:

```text
NaN
```

for:

```text
2026-07-13
```

### Why

`NaN` means:

> Not a Number

In pandas/NumPy, it is commonly used to represent a missing or undefined numerical value.

Here it means:

> there is no previous day's price, so the return cannot be computed.

---

## Expected Updated Table

Approximately:

```text
             price  volume    return
2026-07-13   100.0    1500       NaN
2026-07-14   102.0    1800  0.020000
2026-07-15   101.0    1200 -0.009804
```

The third-row return is negative because:

```text
102 → 101
```

is a loss.

---

> **RULE TO BANK:**
> `df["column"]` selects a Series; assigning to `df["new_column"]` creates a new DataFrame column.
> `pct_change()` computes row-to-row fractional change, and the first result is `NaN` because there is no previous observation.
=====================================




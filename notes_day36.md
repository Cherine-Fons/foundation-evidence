# Task — Create `loc_iloc.py` and Understand `.loc` vs `.iloc`

## What the Task Is Asking

You are starting **F7D2** with a new file:

```text
loc_iloc.py
```

There are really two things happening here:

1. **Create and verify the new filename**
2. Think about why `.loc` and `.iloc` can point to the same row even though they use different kinds of addressing

---

## Step 1 — Create the File

From:

```text
(.venv) foundation %
```

run:

```bash
code loc_iloc.py
```

Then verify the filename:

```bash
ls loc_iloc.py
```

## Prediction

I expect:

```text
loc_iloc.py
```

### Why

If the file was created with exactly that name, `ls` will echo the exact filename.

If there were a stray space or typo, `ls loc_iloc.py` would fail because that exact file would not exist.

---

> **RULE TO BANK:**
> After creating a new file, verify the exact filename with `ls` before building on it.

---

# Core F7D2 Idea — `.loc` vs `.iloc`

You are comparing:

```python
df.loc["2026-07-15"]
```

and:

```python
df.iloc[2]
```

In your current table, they return the same row.

## Why Do They Coincide Here?

Because the row labeled:

```text
"2026-07-15"
```

currently happens to be the **third row** in the DataFrame.

Python positions start at zero:

```text
position 0 → 2026-07-13
position 1 → 2026-07-14
position 2 → 2026-07-15
```

So:

```python
df.loc["2026-07-15"]
```

means:

> Give me the row whose **label** is `"2026-07-15"`.

While:

```python
df.iloc[2]
```

means:

> Give me the row currently sitting at **integer position 2**.

They reach the same row **by coincidence of current ordering**, not because `.loc` and `.iloc` mean the same thing.

---

## When Would `"2026-07-15"` Stop Being at Position `2`?

If the DataFrame's row order changed.

For example, if you:

* inserted an earlier row
* sorted the DataFrame differently
* rearranged the rows

then `"2026-07-15"` could move to another integer position.

Its **label stays `"2026-07-15"`**, but its **position can change**.

So after reordering, this might still identify the same date:

```python
df.loc["2026-07-15"]
```

while:

```python
df.iloc[2]
```

could now return some completely different row.

---

> **RULE TO BANK:**
> `.loc[...]` selects by **label**.
> `.iloc[...]` selects by **integer position**.
> Labels identify what the row *is*; positions identify where the row *currently sits*.
=========================================================================================


# Task — Rebuild the DataFrame in `loc_iloc.py`

## What the Task Is Asking

`loc_iloc.py` should be **self-contained**, so it needs its own copy of the price/volume table before you can practice `.loc` and `.iloc`.

No returns column is needed today.

## What to Put at the Top of `loc_iloc.py`

```python
import pandas as pd


df = pd.DataFrame(
    {
        "price": [100.0, 102.0, 101.0],
        "volume": [1500, 1800, 1200],
    },
    index=["2026-07-13", "2026-07-14", "2026-07-15"],
)
```

That reconstructs:

```text
             price  volume
2026-07-13   100.0    1500
2026-07-14   102.0    1800
2026-07-15   101.0    1200
```

---

# Reasoning — Why Do `.loc["2026-07-15"]` and `.iloc[2]` Match?

They match **because `"2026-07-15"` currently happens to occupy integer position `2`**.

The table is ordered:

```text
position 0 → "2026-07-13"
position 1 → "2026-07-14"
position 2 → "2026-07-15"
```

So:

```python
df.loc["2026-07-15"]
```

asks for:

> the row whose **label** is `"2026-07-15"`

while:

```python
df.iloc[2]
```

asks for:

> the row currently sitting at **position 2**

They arrive at the same row by two different addressing systems.

## When Would They Stop Matching?

If the rows were reordered, inserted, deleted, or sorted differently.

For example, `"2026-07-15"` might move to position `1`.

Then:

```python
df.loc["2026-07-15"]
```

would still retrieve July 15 because its **label has not changed**.

But:

```python
df.iloc[2]
```

would retrieve whatever row now happens to sit in position `2`.

> **RULE TO BANK:**
> `.loc[...]` = select by **label**.
> `.iloc[...]` = select by **integer position**.
> A row's label identifies it; its position can change.

=====================

# Task — Compare `.loc` and `.iloc` Before Reordering

## What the Task Is Asking

You now want to prove that:

```python
df.loc["2026-07-15"]
```

and:

```python
df.iloc[2]
```

currently return the **same row**.

The important part is that they arrive there in different ways:

* `.loc[...]` uses the **row label**
* `.iloc[...]` uses the **integer position**

Right now, July 15 happens to be sitting at position `2`, so the results should match.

---

## What You Need to Add

Below the DataFrame in `loc_iloc.py`, add:

```python
print("--- before sort ---")
print(df.loc["2026-07-15"])
print(df.iloc[2])
```

Then save the file.

---

## Prediction

I expect both lookups to print the July 15 row:

```text
price      101.0
volume    1200.0
```

or equivalent formatting.

So the two printed blocks should be identical.

### Why

Your current row order is:

```text
position 0 → 2026-07-13
position 1 → 2026-07-14
position 2 → 2026-07-15
```

Therefore:

```python
df.loc["2026-07-15"]
```

selects the row by its label,

while:

```python
df.iloc[2]
```

selects the row at position `2`.

At this moment, those are the same row.

---

## One New Thing to Notice

When pandas returns a **single row** from a DataFrame, it prints vertically like a `Series`:

```text
price      101.0
volume    1200.0
```

That is because the selected row is represented as a Series whose index is now:

```text
price
volume
```

The DataFrame's **column names become the Series index**.

---

## Run It

From:

```text
(.venv) foundation %
```

run:

```bash
python loc_iloc.py
```

Expected structure:

```text
--- before sort ---
price      101.0
volume    1200.0
...

price      101.0
volume    1200.0
...
```

The two blocks should match.

> **RULE TO BANK:**
> A single row selected from a DataFrame is returned as a `Series`; the DataFrame's column names become that Series's index.
> `.loc` selects by label, while `.iloc` selects by position.

===============================

# Task — Sort the DataFrame and Break the `.loc` / `.iloc` Coincidence

## What the Task Is Asking

You are now going to **reorder the rows** by price:

```python
df = df.sort_values("price")
```

Then you will compare:

```python
df.loc["2026-07-15"]
```

with:

```python
df.iloc[2]
```

again.

The point is to prove that:

> `.loc` follows the **label**, while `.iloc` follows the **current position**.

---

## What You Need to Add

At the bottom of `loc_iloc.py`, add:

```python
df = df.sort_values("price")

print("--- after sort by price ---")
print(df.loc["2026-07-15"])
print(df.iloc[2])
```

Then save the file.

---

## What the Sort Does

Your original prices are:

```text
2026-07-13 → 100
2026-07-14 → 102
2026-07-15 → 101
```

Sorting by `"price"` from lowest to highest gives:

```text
position 0 → 2026-07-13 → 100
position 1 → 2026-07-15 → 101
position 2 → 2026-07-14 → 102
```

So `"2026-07-15"` is no longer sitting at position `2`.

---

## Prediction 1 — What Will `df.iloc[2]` Return?

**Prediction:**

```python
df.iloc[2]
```

will return the row for:

```text
2026-07-14
```

because after sorting, July 14 is now the **third row**, which is integer position `2`.

Expected values:

```text
price      102.0
volume    1800.0
```

---

## Prediction 2 — What Will `df.loc["2026-07-15"]` Return?

**Prediction:**

```python
df.loc["2026-07-15"]
```

will still return:

```text
2026-07-15
```

with:

```text
price      101.0
volume    1200.0
```

### Why

Sorting changes the row's **position**, but it does not change its **label**.

So:

```text
.loc
→ follows the label
→ still finds July 15

.iloc
→ follows the position
→ position 2 now contains July 14
```

---

## What I Expect After Running

Run:

```bash
python loc_iloc.py
```

The important section should now look roughly like:

```text
--- after sort by price ---

price      101.0
volume    1200.0
Name: 2026-07-15, dtype: float64

price      102.0
volume    1800.0
Name: 2026-07-14, dtype: float64
```

That is the exact moment where `.loc` and `.iloc` stop agreeing.

> **RULE TO BANK:**
> `.loc[label]` follows the row's identity.
> `.iloc[position]` follows where the row currently sits.
> Sorting can change position without changing label.
===========================

# Task — Predict a pandas Boolean Mask

## What the Task Is Asking

You are comparing every value in the `"volume"` column against:

```python
1400
```

with:

```python
df["volume"] > 1400
```

pandas applies that comparison **element by element** down the entire column and returns a labeled Series of Boolean values.

That Boolean Series is the **mask**.

---

## Data

Your volumes are:

```text
2026-07-13 → 1500
2026-07-14 → 1800
2026-07-15 → 1200
```

The condition is:

```python
df["volume"] > 1400
```

So test each row individually.

---

## Prediction

### `2026-07-13`

```text
1500 > 1400
→ True
```

### `2026-07-14`

```text
1800 > 1400
→ True
```

### `2026-07-15`

```text
1200 > 1400
→ False
```

So I expect:

```text
2026-07-13     True
2026-07-14     True
2026-07-15    False
```

with a Boolean dtype at the bottom, likely:

```text
dtype: bool
```

---

## Why This Is a Mask

The result keeps the same date labels as the original column:

```text
date          keep row?
2026-07-13    True
2026-07-14    True
2026-07-15    False
```

That gives pandas a row-by-row instruction:

```text
True  → keep this row
False → exclude this row
```

This is the same vectorized Boolean-mask idea you used in NumPy, except pandas preserves the **index labels**.

> **RULE TO BANK:**
> A comparison against a pandas column produces a labeled Boolean `Series`, one `True`/`False` per row. That Boolean Series can then be used as a mask to filter the DataFrame.
==============================

# Task — Filter a DataFrame with a Boolean Mask

## What the Task Is Asking

You are taking the Boolean mask idea from NumPy and applying it to a pandas `DataFrame`.

The condition is:

```python
df["volume"] > 1400
```

and the filtering expression is:

```python
df[df["volume"] > 1400]
```

This means:

> Keep only the rows where the `"volume"` condition evaluates to `True`.

---

## What You Need to Do

Create a new file:

```bash
code filtering.py
```

Then verify the name:

```bash
ls filtering.py
```

At the top of `filtering.py`, rebuild the same DataFrame:

```python
import pandas as pd


df = pd.DataFrame(
    {
        "price": [100.0, 102.0, 101.0],
        "volume": [1500, 1800, 1200],
    },
    index=["2026-07-13", "2026-07-14", "2026-07-15"],
)
```

Then add:

```python
print(df[df["volume"] > 1400])
```

---

## What Is Happening Here?

First:

```python
df["volume"] > 1400
```

produces the mask:

```text
2026-07-13     True
2026-07-14     True
2026-07-15    False
```

Then:

```python
df[mask]
```

tells pandas:

```text
True  → keep the row
False → drop the row
```

So:

```python
df[df["volume"] > 1400]
```

combines both steps into one expression.

---

## Prediction

### How many rows survive?

**2 rows.**

### Which dates survive?

```text
2026-07-13
2026-07-14
```

### Why

Their volumes are:

```text
2026-07-13 → 1500 > 1400 → True
2026-07-14 → 1800 > 1400 → True
2026-07-15 → 1200 > 1400 → False
```

So July 15 is removed.

---

## Expected Output

Approximately:

```text
             price  volume
2026-07-13   100.0    1500
2026-07-14   102.0    1800
```

Notice that the **date labels stay attached** to the surviving rows.

---

> **RULE TO BANK:**
> `df[mask]` filters rows.
> `True` rows survive; `False` rows are dropped.
> pandas preserves the labels of the rows that remain.
===================================================================================================================================================

# Task — Build a Tiny Grouping Table and Predict Sector Means

## What the Task Is Asking

You are learning the basic pandas **`groupby`** pattern:

> **split rows into groups → select a column → compute one summary per group**

For this task, the grouping category is:

```text
sector
```

and the numerical quantity being summarized is:

```text
return
```

The target pattern will be:

```python
df.groupby("sector")["return"].mean()
```

But first, build the small table and predict the results by hand.

---

## What You Need to Do

Create the new file:

```bash
code grouping.py
```

Verify the filename:

```bash
ls grouping.py
```

Then put this in `grouping.py`:

```python
import pandas as pd


df = pd.DataFrame(
    {
        "sector": ["tech", "tech", "energy", "energy"],
        "return": [0.02, 0.04, -0.01, 0.03],
    }
)
```

Save it.

---

## What Is Different About This DataFrame?

There is **no explicit `index=`**.

So pandas will assign the default integer index:

```text
0
1
2
3
```

That is fine here because the meaningful category is stored in the `"sector"` column.

The table is conceptually:

```text
   sector   return
0  tech      0.02
1  tech      0.04
2  energy   -0.01
3  energy    0.03
```

---

# Prediction — Mean Return Per Sector

## Tech

Tech has two returns:

```text
0.02
0.04
```

Mean:

```text
(0.02 + 0.04) / 2
= 0.06 / 2
= 0.03
```

**Prediction:**

```text
tech → 0.03
```

or:

```text
3%
```

---

## Energy

Energy has:

```text
-0.01
0.03
```

Mean:

```text
(-0.01 + 0.03) / 2
= 0.02 / 2
= 0.01
```

**Prediction:**

```text
energy → 0.01
```

or:

```text
1%
```

---

## Expected Grouped Result

When you eventually run:

```python
df.groupby("sector")["return"].mean()
```

I expect one value per sector:

```text
sector
energy    0.01
tech      0.03
```

The order may be alphabetical by group key, so `energy` may print before `tech`.

---

## How to Read the Groupby Chain

```python
df.groupby("sector")["return"].mean()
```

reads left to right:

```text
df
↓
group rows by sector
↓
within each group, select return
↓
compute the mean
↓
one result per sector
```

---

> **RULE TO BANK:**
> `groupby` means **split by category, then summarize each group**.
> `df.groupby("sector")["return"].mean()` returns one mean return per sector.

=============================

# Task — Run `groupby` and Predict the Result Shape

## What the Task Is Asking

You already built this DataFrame:

```python
import pandas as pd


df = pd.DataFrame(
    {
        "sector": ["tech", "tech", "energy", "energy"],
        "return": [0.02, 0.04, -0.01, 0.03],
    }
)
```

Now add:

```python
print(df.groupby("sector")["return"].mean())
```

This will:

```text
group by sector
→ select return
→ compute one mean per sector
```

---

## Prediction — How Many Rows Come Back?

You started with:

```text
4 rows
```

but only:

```text
2 distinct sectors
```

So after grouping and averaging, I expect:

```text
2 rows
```

because `groupby` collapses all rows in each category into one summary value.

---

## Prediction — What Appears on the Left?

The grouping column:

```text
sector
```

becomes the **index of the result**.

So the left-hand labels should be the two sector names:

```text
energy
tech
```

Likely in alphabetical order.

---

## Expected Output

Approximately:

```text
sector
energy    0.01
tech      0.03
Name: return, dtype: float64
```

### Why

For energy:

```text
(-0.01 + 0.03) / 2
= 0.01
```

For tech:

```text
(0.02 + 0.04) / 2
= 0.03
```

So the result is a **Series** with:

```text
index  → sector names
values → mean returns
```

---

## Run It

From:

```text
(.venv) foundation %
```

run:

```bash
python grouping.py
```

---

> **RULE TO BANK:**
> `groupby(...).mean()` reduces many rows into **one summary row per group**, and the grouping key becomes the result's index.

===============================
# CONCLUSION
Two rows, not four — each sector collapsed to one number. energy 0.01, tech 0.03, matching your hand arithmetic. And the key structural thing: sector is now the index — it's printed as the label on the left, with Name: return telling you the values came from the return column. groupby took the column you grouped by and made it the index of the summary. It also sorted alphabetically, so energy sits above tech, exactly as called.

# The pattern to bank, because you'll use it constantly in CPF: split by a category, compute one number per group. df.groupby("category")["value"].mean() — and .mean() is just one choice; .sum(), .max(), .count() all work the same way. Average return per sector, total volume per exchange, number of trades per day — all this exact shape.
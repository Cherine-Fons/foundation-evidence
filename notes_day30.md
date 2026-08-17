# Day 30 — F6D2: New Chart Types

## What We Are Doing

Today builds on the **same Matplotlib figure/axes model from Day 29**:

```python
fig, ax = plt.subplots()
```

The new material is learning **two different chart types**:

1. A **histogram** of returns with a zero reference line.
2. A **scatter plot** comparing two return series.

The figure/axes structure does not change. The main difference is the plotting method called on `ax`.

---

## What I Need

I am still using **Matplotlib**:

```python
import matplotlib.pyplot as plt
```

No new library is being introduced today.

I need:

* the active `(.venv)` environment
* a fresh Python script
* `matplotlib.pyplot` imported as `plt`

---

## What Matplotlib Gives Me Today

Yesterday I used:

```python
ax.plot(x, y)
```

for a line chart.

Today I add new plotting methods while keeping the same `fig, ax` structure.

For the first chart:

```python
ax.hist(data)
```

creates a **histogram**.

Unlike:

```python
ax.plot(x, y)
```

which needs both x-values and y-values, a histogram takes **one set of numerical values**.

Matplotlib then groups those values into **bins** and counts how many values fall into each range.

> **Line plot:** preserves the sequence of the data over time.
> **Histogram:** ignores time order and shows the distribution or shape of the values.

For returns, a histogram answers questions such as how returns are spread out and whether they are concentrated around certain ranges.

---

## Environment Setup

Work **script-first**, rather than starting in the REPL.

At:

```text
foundation %
```

create the new script:

```bash
code returns_hist.py
```

Then verify that the filename is correct:

```bash
ls returns_hist.py
```

The script will use:

```python
import matplotlib.pyplot as plt
```

and the same figure/axes model:

```python
fig, ax = plt.subplots()
```

When the script is ready, run it from:

```text
foundation %
```

with:

```bash
python returns_hist.py
```

Because this is a terminal/script environment, the chart appears when:

```python
plt.show()
```

runs, and the window may need to be closed before the terminal becomes available again.

---

# First Task — Returns Histogram

The first chart uses these ten return values:

```python
returns = [
    0.012,
    -0.008,
    0.0,
    0.021,
    -0.015,
    0.006,
    0.009,
    -0.004,
    0.011,
    -0.002
]
```

The script needs these six pieces:

```markdown
1. Import `matplotlib.pyplot as plt`
2. Create the `returns` list
3. Create `fig, ax = plt.subplots()`
4. Plot the histogram with `ax.hist(returns)`
5. Add:
   - title: `"Distribution of returns"`
   - x-axis: `"Return"`
   - y-axis: `"Frequency"`
6. Finish with `plt.show()`
```

The new line is:

```python
ax.hist(returns)
```

It takes **one argument** because Matplotlib itself determines the bins and counts how many returns fall into each one.

---

## My Predictions

### 1. What will `ax.hist(returns)` show?

It should produce **bars rather than a line**.

The ten return values will be grouped into ranges, or **bins**, and each bar will represent one range of returns.

The **height of each bar** will show how many return values fall inside that range.

### 2. What does a tall or short bar mean?

With:

```text
x-axis = Return
y-axis = Frequency
```

a **tall bar near `0.01`** means that several of the observed returns fall around that return range.

A **short bar near `-0.015`** means that fewer observations fall around that negative-return range.

> **Histogram bar height = how frequently values occur within that return range.**

The first run is only the **base histogram**. The zero reference line is added after seeing the initial chart.

==================================================================================================================

>Now the card's actual target: the zero reference line. Framing — a returns histogram is most useful when you can instantly see gains vs losses, so you draw a vertical line at return = 0. Everything left of it is a losing day, everything right is a gaining day.

The method is ax.axvline(x) — "axis vertical line" — it draws a vertical line at the x-value you give. You want it at 0:

ax.axvline(0)

That draws a plain line at x=0. But a bare line is easy to miss against blue bars, so axvline takes optional styling arguments — this is a good moment to learn keyword arguments on a plot call:

ax.axvline(0, color="red", linestyle="--")
color="red" — makes it stand out
linestyle="--" — dashed, so it reads as a reference line, not data

These are keyword arguments (name=value) — optional extras that modify how something's drawn. You'll use them constantly in matplotlib.

Add the ax.axvline(0, color="red", linestyle="--") line to your script — place it after ax.hist(returns) (so the line draws on top of the bars) but before plt.show(). Save, re-run.

# Predict first:

Where will the red dashed line appear on the x-axis?
Looking at your current histogram, roughly how many bars fall left of zero (losses) vs right (gains)? Eyeball it from the chart above.

Add the line, run it (python returns_hist.py, close window to unblock), predict those two, and show me the histogram with the zero line. Then we'll add the savefig and move to the scatter plot.

==================================================================================================================

## Predictions Before Adding the Zero Reference Line

Add this immediately after the histogram:

```python
ax.hist(returns)
ax.axvline(0, color="red", linestyle="--")
```

### 1. Where will the red dashed line appear?

The line will appear **vertically at `x = 0`** on the return axis.

```text
negative returns   |   positive returns
                   |
                   0
```

> **Everything to the left of the red dashed line represents losses; everything to the right represents gains.**

The line itself is a **reference marker**, not another data point.

---

### 2. Roughly how much is on each side?

From the actual return values:

```python
returns = [0.012, -0.008, 0.0, 0.021, -0.015,
           0.006, 0.009, -0.004, 0.011, -0.002]
```

There are:

```text
4 negative returns
1 zero return
5 positive returns
```

So I expect the histogram to have **slightly more data on the right side of zero than on the left**.

Because a histogram groups values into **bins**, the number of visible bars is not necessarily the same as the number of observations. With Matplotlib's current bins, I would expect roughly **3 occupied bars clearly left of zero and 4 clearly right of zero**, with the `0.0` observation sitting in the bin around the reference line.

### 🧠 What the zero line adds

```markdown
> **The histogram shows the distribution; the zero reference line immediately separates losing returns from gaining returns.**
```

And the styling:

```python
color="red"
linestyle="--"
```

are **keyword arguments**: optional `name=value` settings that change how the line is displayed.

==================================================================================================================

## Finish Chart 1 — Save the Histogram

Add this line to `returns_hist.py`:

```python
fig.savefig("artifacts/returns_hist.png")
```

Place it **after** the histogram and zero reference line, but **before** `plt.show()`:

```python
ax.hist(returns)
ax.axvline(0, color="red", linestyle="--")

fig.savefig("artifacts/returns_hist.png")

plt.show()
```

> **`fig.savefig(...)`** saves the completed figure permanently to disk.
> **`plt.show()`** displays the figure temporarily in a window.

Because `artifacts/` already exists and is already ignored by Git, the PNG will be created without adding generated output to version control.

Run the script again:

```bash
python returns_hist.py
```

Then verify the artifacts:

```bash
ls -la artifacts/
```

You should now see both:

```text
prices.png
returns_hist.png
```

---

## New Matplotlib Tools Learned So Far

```python
ax.hist(returns)
```

Creates a **histogram** by grouping numerical values into bins and showing their frequency.

```python
ax.axvline(0, color="red", linestyle="--")
```

Creates a **vertical reference line** at `x = 0`.

```python
ax.axhline(0)
```

Is the corresponding method for a **horizontal reference line**.

### Styling with keyword arguments

```python
color="red"
linestyle="--"
```

These are **keyword arguments**: optional `name=value` settings that modify how something is drawn.

The same pattern generalizes to options such as:

```python
linewidth=...
label=...
color=...
linestyle=...
```

---

# Next: Chart 2 — Scatter Plot

The second chart of F6D2 will use a **scatter plot**.

A scatter plot shows the **relationship between two variables** by drawing individual points rather than connecting them with a line.

The new method will be:

```python
ax.scatter(x, y)
```

Each observation becomes one coordinate pair:

```text
(x, y)
```

For two asset-return series, each point represents the two assets' returns for the same observation.

Create the new file with:

```bash
code returns_scatter.py
```

The scatter script comes next after confirming that `returns_hist.png` was created successfully.

==================================================================================================================

# Chart 2 — Scatter Plot Predictions

## What this chart is asking

The scatter plot compares **Asset A returns** against **Asset B returns** for the same ten observations.

```python
ax.scatter(asset_a, asset_b)
```

Each point is one matched pair:

```python
(asset_a[i], asset_b[i])
```

Unlike a line plot, the points are **not connected**. The goal is to see whether the two return series appear to move together.

---

## Prediction 1 — What shape should the points form?

I expect the dots to form a **rough upward diagonal**.

The two return series are similar: when `asset_a` is positive, `asset_b` is usually positive too, and when `asset_a` is negative, `asset_b` is usually negative too.

For example:

```text
Asset A    Asset B
 0.012      0.010
-0.008     -0.006
 0.021      0.018
-0.015     -0.012
```

So as Asset A's return increases, Asset B's return generally increases as well.

> **Prediction:** the scatter should suggest a **positive relationship / positive correlation**, appearing roughly from lower-left to upper-right.

---

## Prediction 2 — How many dots?

Both lists contain **10 returns**, and each matching pair produces one point.

```text
10 paired observations → 10 dots
```

So I predict:

> **There will be exactly 10 points on the scatter plot.**

---

## Script Structure

```python
import matplotlib.pyplot as plt

asset_a = [0.012, -0.008, 0.0, 0.021, -0.015, 0.006, 0.009, -0.004, 0.011, -0.002]
asset_b = [0.010, -0.006, 0.002, 0.018, -0.012, 0.008, 0.007, -0.003, 0.013, 0.000]

fig, ax = plt.subplots()

ax.scatter(asset_a, asset_b)

ax.set_title("Asset A vs Asset B returns")
ax.set_xlabel("Asset A return")
ax.set_ylabel("Asset B return")

fig.savefig("artifacts/returns_scatter.png")

plt.show()
```

> **`ax.plot(...)` connects observations in sequence. `ax.scatter(...)` leaves each `(x, y)` observation as a separate dot so I can inspect the relationship between the two variables.**

==================================================================================================================

## Run Chart 2 — Scatter Plot

Your `returns_scatter.py` should now be:

```python
import matplotlib.pyplot as plt

asset_a = [0.012, -0.008, 0.0, 0.021, -0.015, 0.006, 0.009, -0.004, 0.011, -0.002]
asset_b = [0.010, -0.006, 0.002, 0.018, -0.012, 0.008, 0.007, -0.003, 0.013, 0.000]

fig, ax = plt.subplots()

ax.scatter(asset_a, asset_b)

ax.set_title("Asset A vs Asset B returns")
ax.set_xlabel("Asset A return")
ax.set_ylabel("Asset B return")

fig.savefig("artifacts/returns_scatter.png")

plt.show()
```

Run from:

```bash
foundation % python returns_scatter.py
```

### What you should see

* **10 isolated dots**
* no connecting lines
* a rough **lower-left → upper-right** pattern
* x-axis: **Asset A return**
* y-axis: **Asset B return**
* title: **Asset A vs Asset B returns**

> **Concept to bank:**
> `plot` = sequence; order matters; points are connected.
> `scatter` = relationship; order does not matter; points remain separate.

After closing the chart window, verify all three artifacts:

```bash
ls -la artifacts/
```

You should now have:

```text
prices.png
returns_hist.png
returns_scatter.png
```

Once you paste the scatter screenshot and `ls -la artifacts/` output, we can close **f6d2** with the notes and commit.

======================================================================================================================

# Day 30 — F6D2: Histograms and Scatter Plots RECAP

## Histogram — Distribution of Values

```python
ax.hist(data)
```

A **histogram** shows the distribution of one set of numerical values.

Unlike:

```python
ax.plot(x, y)
```

which needs x- and y-values, `hist` takes **one data argument**:

```python
ax.hist(returns)
```

Matplotlib divides the values into **bins** and counts how many observations fall into each range.

> **Histogram bar height = frequency, or the number of observations inside that bin.**

For returns, the histogram shows the **shape and spread of the return distribution**, rather than preserving their order over time.

---

## Vertical Reference Line

```python
ax.axvline(0, color="red", linestyle="--")
```

`ax.axvline(x)` draws a **vertical reference line** at a chosen x-value.

For a returns histogram:

```python
ax.axvline(0)
```

marks the break between:

```text
losses       zero       gains
  ←            |           →
               0
```

Placing the line after:

```python
ax.hist(returns)
```

allows it to draw on top of the histogram bars.

---

## Keyword Arguments

```python
color="red"
linestyle="--"
```

These are **keyword arguments**.

They use:

```text
name=value
```

to control optional properties of the plot.

For example:

```python
ax.axvline(0, color="red", linestyle="--")
```

means:

* draw the line at `0`
* make it red
* make it dashed

This styling pattern generalizes across Matplotlib.

---

## Horizontal Reference Line

The corresponding method for a horizontal reference line is:

```python
ax.axhline(0)
```

> `axvline` = vertical reference line
> `axhline` = horizontal reference line

---

# Scatter Plot — Relationship Between Two Variables

```python
ax.scatter(x, y)
```

A **scatter plot** compares two variables by drawing individual `(x, y)` points.

For:

```python
ax.scatter(asset_a, asset_b)
```

each point is:

```python
(asset_a[i], asset_b[i])
```

So one paired observation produces one dot.

With ten matched return observations:

```text
10 pairs → 10 dots
```

The dots are **not connected**.

---

## Reading Correlation From a Scatter Plot

If the points generally move:

```text
lower-left → upper-right
```

the variables show a **positive relationship**.

In today's chart, the dots formed a tight upward diagonal, meaning Asset A and Asset B tended to move together.

> **The closer the dots cluster around an upward-sloping imaginary line, the stronger the visible positive relationship.**

---

# `plot` vs. `scatter`

### Line Plot

```python
ax.plot(x, y)
```

Use when the **sequence or order matters**, such as values over time.

Matplotlib connects the points in list order.

```text
point → point → point → point
```

### Scatter Plot

```python
ax.scatter(x, y)
```

Use when examining the **relationship between two variables**.

The points remain separate because their **positions**, not their order, carry the meaning.

```text
•       •
    •
        •
  •
```

> **`plot` = sequence over time → connect the points.**
> **`scatter` = relationship between variables → do not connect the points.**

---

# Day 30 Artifacts

The histogram script saves:

```python
fig.savefig("artifacts/returns_hist.png")
```

The scatter script saves:

```python
fig.savefig("artifacts/returns_scatter.png")
```

Because:

```gitignore
artifacts/
```

is already in `.gitignore`, the generated PNG files should **not appear in `git status`**.

---

Now save that as:

```text
notes_day30.md
```

Then at `foundation %`, run:

```bash
git status
```

You should expect the relevant untracked files to be:

```text
notes_day30.md
returns_hist.py
returns_scatter.py
```

and **no `artifacts/` directory or PNG files should appear**.

Paste your actual `git status` output here before committing. I can't run Git on your local `foundation` repo from here, but I can verify the status output before you stage anything.

Once it checks out, the commit commands are:

```bash
git add notes_day30.md returns_hist.py returns_scatter.py
git commit -m "f6d2: matplotlib histogram with zero line, scatter plot"
```




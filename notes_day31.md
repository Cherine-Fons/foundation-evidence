# Day 31 — F6D3: Two-Panel Figure

## What We Are Doing

Today builds on the same explicit Matplotlib **figure/axes model** from Days 29–30.

Until now, each figure contained **one axes**:

```python
fig, ax = plt.subplots()
```

Today the figure will contain **two axes**:

* **top panel:** prices
* **bottom panel:** returns

Both panels represent the same days, so they will **share the x-axis** and stay aligned in time.

> **The payoff of the explicit `fig, ax` model:** one Figure can contain multiple independent Axes.

---

## What I Need

No new library is required.

I am still using:

```python
import matplotlib.pyplot as plt
```

I need:

* the active `(.venv)` environment
* a new Python script
* Matplotlib
* the existing `artifacts/` folder for the saved PNG

---

## What Is New Today?

The new idea is changing from:

```python
fig, ax = plt.subplots()
```

which creates **one axes**, to:

```python
fig, (ax_top, ax_bottom) = plt.subplots(2, 1, sharex=True)
```

which creates **two axes inside one figure**.

---

# Understanding the Key Line

```python
fig, (ax_top, ax_bottom) = plt.subplots(2, 1, sharex=True)
```

## `plt.subplots(2, 1)`

The arguments mean:

```text
2 rows
1 column
```

So the layout is:

```text
┌─────────────────────┐
│     top axes        │
├─────────────────────┤
│    bottom axes      │
└─────────────────────┘
```

The two plot areas are **stacked vertically**.

---

## `ax_top` and `ax_bottom`

Instead of receiving one axes object called `ax`, Matplotlib gives me a container holding **two axes objects**.

I unpack them into:

```python
ax_top
ax_bottom
```

This uses the same tuple-unpacking idea I already know.

Previously:

```python
fig, ax = plt.subplots()
```

Now:

```python
fig, (ax_top, ax_bottom) = plt.subplots(2, 1)
```

Each axes can be controlled independently.

```python
ax_top.plot(...)
ax_bottom.plot(...)
```

> **`ax_top` controls the upper chart. `ax_bottom` controls the lower chart.**

---

# `sharex=True`

```python
sharex=True
```

makes the two panels use the **same x-axis range**.

Because both panels represent the same days, their positions line up vertically.

The x-axis labels only need to appear on the **bottom panel**, which keeps the figure cleaner.

---

# Environment Setup

Work script-first again.

At:

```text
foundation %
```

create:

```bash
code two_panel.py
```

Verify the filename:

```bash
ls two_panel.py
```

When the script is complete, run:

```bash
python two_panel.py
```

`plt.show()` will display the figure, and the window may need to be closed before the terminal prompt returns.

---

# First Task — Build the Two-Panel Figure

## Data

```python
days = [1, 2, 3, 4, 5, 6]

prices = [100, 102, 101, 104, 103, 105]

returns = [0.0, 0.02, -0.0098, 0.0297, -0.0096, 0.0194]
```

There are six `days`, six `prices`, and six `returns`.

The first return is:

```python
0.0
```

as a placeholder so the returns list matches the six days.

---

## Script Structure

### 1. Import Matplotlib

```python
import matplotlib.pyplot as plt
```

### 2. Create the three data lists

```python
days = [1, 2, 3, 4, 5, 6]
prices = [100, 102, 101, 104, 103, 105]
returns = [0.0, 0.02, -0.0098, 0.0297, -0.0096, 0.0194]
```

### 3. Create one figure containing two stacked axes

```python
fig, (ax_top, ax_bottom) = plt.subplots(2, 1, sharex=True)
```

### 4. Top Panel — Prices

```python
ax_top.plot(days, prices)
ax_top.set_title("Prices and returns")
ax_top.set_ylabel("Price")
```

The **title** goes on the top panel because it acts as the heading for the complete figure.

---

### 5. Bottom Panel — Returns

```python
ax_bottom.plot(days, returns)
ax_bottom.set_ylabel("Return")
ax_bottom.set_xlabel("Day")
```

The x-axis label goes only on the **bottom panel** because the panels share the x-axis.

Each panel gets its own y-axis label:

```text
Top:    Price
Bottom: Return
```

---

### 6. Save the Complete Figure

```python
fig.savefig("artifacts/two_panel.png")
```

This saves the entire figure containing **both axes**.

---

### 7. Display It

```python
plt.show()
```

---

# My Predictions

## Prediction 1 — How will the panels be arranged?

They should be **stacked vertically**, not side by side.

The reason is:

```python
plt.subplots(2, 1)
```

means:

```text
2 rows × 1 column
```

So I expect:

```text
TOP
Prices
────────────

BOTTOM
Returns
────────────
```

> **Prediction:** prices on top, returns underneath.

---

## Prediction 2 — Where will the Day x-axis labels appear?

Because:

```python
sharex=True
```

makes the two axes share their x-axis, I expect the visible **Day** x-axis labeling to appear only underneath the **bottom panel**.

The top panel does not need a duplicate x-axis label.

> **Prediction:** both charts are aligned to the same days, but the x-axis labeling appears only at the bottom.

===============================================================================================================================

# Day 31 — Build and Run the Two-Panel Figure

Your `two_panel.py` should now be:

```python
import matplotlib.pyplot as plt

days = [1, 2, 3, 4, 5, 6]
prices = [100, 102, 101, 104, 103, 105]
returns = [0.0, 0.02, -0.0098, 0.0297, -0.0096, 0.0194]

fig, (ax_top, ax_bottom) = plt.subplots(2, 1, sharex=True)

ax_top.plot(days, prices)
ax_top.set_title("Prices and returns")
ax_top.set_ylabel("Price")

ax_bottom.plot(days, returns)
ax_bottom.set_ylabel("Return")
ax_bottom.set_xlabel("Day")

fig.savefig("artifacts/two_panel.png")

plt.show()
```

## Run It

From:

```text
foundation %
```

run:

```bash
python two_panel.py
```

Because `plt.show()` blocks in your setup, close the chart window afterward to get the terminal prompt back.

---

## What I Expect to See

### Top axes

```text
Title: Prices and returns
y-axis: Price
```

with the price sequence:

```text
100 → 102 → 101 → 104 → 103 → 105
```

### Bottom axes

```text
y-axis: Return
x-axis: Day
```

with the return sequence:

```text
0.0 → 0.02 → -0.0098 → 0.0297 → -0.0096 → 0.0194
```

### Shared x-axis

Because of:

```python
sharex=True
```

the two panels should line up vertically by day.

In particular:

```text
Day 4
  ↑
price = 104
  │
  │ same x-position
  ↓
return = 0.0297
```

> **This is the key visual payoff:** the same day occupies the same horizontal position in both axes, so related movements can be compared directly by looking vertically.

---

## Verify the Saved Artifact

After closing the window:

```bash
ls -la artifacts/
```

You should now see four PNGs:

```text
prices.png
returns_hist.png
returns_scatter.png
two_panel.png
```

The new one should have a **non-zero file size**.

Show me the rendered two-panel figure and the `ls -la artifacts/` output next, and we can verify the layout before closing **f6d3**.

===============================================================================================================================

# Day 31 — F6D3: Two-Panel Figure with a Shared X-Axis RECAP

## One Figure Can Hold Multiple Axes

Until now, I created one figure with one axes:

```python
fig, ax = plt.subplots()
```

Today I created **one figure containing two axes**:

```python
fig, (ax_top, ax_bottom) = plt.subplots(2, 1, sharex=True)
```

> **Figure = the whole canvas.**
> **Axes = individual plotting areas inside the figure.**

---

## `plt.subplots(2, 1)` — Rows × Columns

```python
plt.subplots(2, 1)
```

means:

```text
2 rows × 1 column
```

So the axes are arranged vertically:

```text
┌──────────────────────┐
│       ax_top         │
│       Prices         │
├──────────────────────┤
│      ax_bottom       │
│       Returns        │
└──────────────────────┘
```

The returned axes are unpacked into:

```python
ax_top
ax_bottom
```

using:

```python
fig, (ax_top, ax_bottom) = plt.subplots(2, 1)
```

This is the same unpacking idea as:

```python
fig, ax = plt.subplots()
```

except now there are **two axes objects instead of one**.

---

## Drawing on Each Axes Independently

The top axes receives the price plot:

```python
ax_top.plot(days, prices)
```

The bottom axes receives the return plot:

```python
ax_bottom.plot(days, returns)
```

Each axes is controlled independently even though both belong to the same figure.

> **`ax_top` controls the upper panel. `ax_bottom` controls the lower panel.**

---

## Sharing the X-Axis

```python
sharex=True
```

makes both panels use the **same x-axis range**.

```python
fig, (ax_top, ax_bottom) = plt.subplots(2, 1, sharex=True)
```

Because both charts use `days`, the same day appears at exactly the same horizontal position in both panels.

For example, at **Day 4**:

```text
Top panel:     price = 104
                    │
                    │ same x-position
                    ↓
Bottom panel: return = 0.0297
```

This lets me compare price behavior and its corresponding return by reading vertically through the figure.

---

## Label Placement Logic

### Top Panel

```python
ax_top.set_title("Prices and returns")
ax_top.set_ylabel("Price")
```

The **title** goes on the top panel so it acts as the heading for the whole figure.

The top panel gets its own y-axis label:

```text
Price
```

### Bottom Panel

```python
ax_bottom.set_ylabel("Return")
ax_bottom.set_xlabel("Day")
```

The bottom panel gets its own y-axis label:

```text
Return
```

The x-axis label:

```text
Day
```

appears only on the bottom panel because the two axes share the same x-axis.

> **Shared x-axis → one x-label at the bottom.**
> **Separate y-data → each panel gets its own y-label.**

---

## Complete Structure

```python
import matplotlib.pyplot as plt

days = [1, 2, 3, 4, 5, 6]
prices = [100, 102, 101, 104, 103, 105]
returns = [0.0, 0.02, -0.0098, 0.0297, -0.0096, 0.0194]

fig, (ax_top, ax_bottom) = plt.subplots(2, 1, sharex=True)

ax_top.plot(days, prices)
ax_top.set_title("Prices and returns")
ax_top.set_ylabel("Price")

ax_bottom.plot(days, returns)
ax_bottom.set_ylabel("Return")
ax_bottom.set_xlabel("Day")

fig.savefig("artifacts/two_panel.png")

plt.show()
```

---

## Why the Explicit Figure/Axes Model Matters

The explicit Matplotlib model makes coordinated multi-panel figures possible:

```text
one Figure
    ↓
multiple Axes
    ↓
independent plots
    ↓
shared coordinate structure
```

> **The two-panel figure is the payoff of learning `fig` and `ax` explicitly: one canvas can contain multiple coordinated plots.**

---

Save this as:

```text
notes_day31.md
```

Then run:

```bash
git status
```

You should expect:

```text
notes_day31.md
two_panel.py
```

to appear as untracked files, while `artifacts/` and `two_panel.png` should **not** appear because `artifacts/` is ignored.

I can't see your local repository's actual `git status`, so paste that output here and I can verify it before you commit.

Then:

```bash
git add notes_day31.md two_panel.py
git commit -m "f6d3: two-panel figure, shared x-axis, prices over returns"
```

Expected commit result: **2 files changed**, with `create mode` for both `notes_day31.md` and `two_panel.py`.



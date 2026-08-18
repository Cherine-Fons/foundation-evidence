# Now the last thing in F6: the cumulative F6 quiz, batched across the whole week, in your own words — same format as the F5 quiz you took 10/10. Answer all ten; I'll mark the batch at the end.

1. fig, ax = plt.subplots() returns two objects. What is fig, what is ax, and what's the relationship between them?

2. You want to label a chart made with the ax approach. What are the three methods for the title, x-axis label, and y-axis label — and what's the naming difference from the quick plt. way?

3. fig.savefig("chart.png") versus plt.show(). What does each do, do they replace each other, and which order do you call them in?

4. In a script (not the REPL), you run a file ending in plt.show() and your terminal prompt doesn't come back. Nothing's broken — what's happening, and how do you get the prompt back?

5. Three chart types: ax.plot(x, y), ax.scatter(x, y), ax.hist(data). What question is each one best for, and how many data arguments does hist take versus plot?

6. plt.subplots(2, 1, sharex=True) — what does the 2, 1 mean, how do you unpack the two axes, and what does sharex=True do?

7. black vs ruff. What does each tool do to your code, which one changes your files, and what does ruff check --fix do that plain ruff check doesn't?

8. You have a function returning a float. Why do you assert it in a test with pytest.approx(expected) instead of == expected? Tie it to something from F5.

9. Type hints — what does def f(x: float) -> float: annotate, and do type hints change what the function does at runtime?

10. Normalization (from the capstone). Why rebase two price series to base 100 before comparing them, and what does the formula p / prices[0] * 100 guarantee about the first value of every normalized series?
===================================================================================================================================================================

1. # plt.subplots() creates two related objects:

fig → Figure object
ax  → Axes object

fig is the entire canvas.
Think of it as the whole sheet of paper or the complete image that Matplotlib will eventually display or save.

It can contain:

one plot
several plots
titles
axes
other graphical elements

ax is the individual plotting area inside the figure.
This is where the actual data is drawn.

What Is Their Relationship?

The Axes lives inside the Figure.

Conceptually:

Figure: fig
┌──────────────────────────────────┐
│                                  │
│       Axes: ax                   │
│       ┌────────────────────┐     │
│       │                    │     │
│       │      the plot      │     │
│       │                    │     │
│       └────────────────────┘     │
│                                  │
└──────────────────────────────────┘

So:

fig
└── contains ax

The figure is the overall container, while the axes is the place inside that container where the chart is drawn.

============

2. # When using the explicit Axes-object approach, the three labeling methods are:

ax.set_title("Chart title")
ax.set_xlabel("X-axis label")
ax.set_ylabel("Y-axis label")

So:

Title   → ax.set_title(...)
X-axis  → ax.set_xlabel(...)
Y-axis  → ax.set_ylabel(...)

# Naming Difference from the Quick plt. Approach

The quick plt. style uses:

plt.title("Chart title")
plt.xlabel("X-axis label")
plt.ylabel("Y-axis label")

# The important difference is the set_ prefix.

Explicit ax approach:       Quick plt approach:


ax.set_title(...)           plt.title(...)
ax.set_xlabel(...)          plt.xlabel(...)
ax.set_ylabel(...)          plt.ylabel(...)

# RULE TO BANK: When calling labeling methods on an ax object, use set_. The quick plt. versions do not use set_.

For example:

fig, ax = plt.subplots()


ax.plot(days, prices)


ax.set_title("Price over 5 days")
ax.set_xlabel("Day")
ax.set_ylabel("Price")

The labels belong specifically to that ax, which becomes especially important when one figure contains multiple axes.

==============

3. # `fig.savefig("chart.png")` vs. `plt.show()`

They do **two different jobs**.

## `fig.savefig("chart.png")`

```python
fig.savefig("chart.png")
```

**Saves the figure to disk** as an image file.

The chart remains available after the program ends because there is now a file such as:

```text
chart.png
```

> **`savefig()` = permanent artifact on disk.**

---

## `plt.show()`

```python
plt.show()
```

**Displays the figure on screen** in a window.

In the terminal setup, that window is temporary, and `plt.show()` may **block** the script until the window is closed.

> **`show()` = display the figure on screen.**

---

## Do They Replace Each Other?

**No.**

You can — and often do — use **both**:

```python
fig.savefig("chart.png")
plt.show()
```

They serve different purposes:

```text
savefig → save it
show    → look at it
```

---

## What Order?

The normal order is:

```python
# build the plot
ax.plot(...)

# add all labels, legends, etc.
ax.set_title(...)
ax.set_xlabel(...)
ax.set_ylabel(...)

# save the completed figure
fig.savefig("chart.png")

# then display it
plt.show()
```

So:

> **Build → label/style → `savefig()` → `show()`**

You want `savefig()` **after the figure is complete**, so the saved image contains all of the labels and other additions.

You generally put it **before `plt.show()`**, especially because `show()` can block or, depending on the backend, close/consume the displayed figure after its window is closed.

### Rule to bank

```text
fig.savefig(...) = writes the completed figure to disk
plt.show()        = displays the figure on screen

They do not replace one another.

Save first, show second.
```
====================

4. # Why Doesn't the Terminal Prompt Come Back After `plt.show()`?

Nothing is broken.

In a normal script, this line:

```python
plt.show()
```

often **blocks execution**.

That means Python opens the chart window and then waits there until you close it.

So the sequence is:

```text
python script.py
↓
script runs
↓
plt.show()
↓
chart window opens
↓
Python waits
↓
terminal prompt does not return yet
```

The terminal is not frozen. The script is still active because the plot window is still open.

## How Do You Get the Prompt Back?

Close the Matplotlib chart window.

Once you close it:

```text
chart window closes
↓
plt.show() finishes
↓
script ends
↓
terminal prompt returns
```

So you should see your prompt again:

```text
foundation %
```

> **RULE TO BANK:**
> In a script, `plt.show()` may block.
> If the prompt does not return, close the plot window.
> The script then finishes and the terminal becomes available again.
======================

5. # `ax.plot(x, y)` vs. `ax.scatter(x, y)` vs. `ax.hist(data)`

Each chart type answers a **different kind of question**.

## `ax.plot(x, y)` — Sequence / Change Over Time

```python
ax.plot(x, y)
```

A line plot is best when the **order of the observations matters**, especially for a time series.

It answers questions like:

> **How does this value change over time or across an ordered sequence?**

Example:

```python
ax.plot(days, prices)
```

The points are connected in order:

```text
Day 1 → Day 2 → Day 3 → Day 4
```

> **`plot` = sequence/trend; connect the points because order matters.**

---

## `ax.scatter(x, y)` — Relationship Between Two Variables

```python
ax.scatter(x, y)
```

A scatter plot is best when asking:

> **Do these two variables appear to move together or have a relationship?**

Example:

```python
ax.scatter(asset_a, asset_b)
```

Each observation becomes one pair:

```text
(x, y)
```

or:

```text
(asset_a[i], asset_b[i])
```

The points are **not connected**, because their order is not the important information. Their positions relative to one another are.

For example:

```text
lower-left → upper-right
```

suggests a positive relationship.

> **`scatter` = relationship/correlation; position matters, not sequence.**

---

## `ax.hist(data)` — Distribution

```python
ax.hist(data)
```

A histogram is best when asking:

> **How are these numerical values distributed?**

For example:

```python
ax.hist(returns)
```

Matplotlib groups the return values into **bins** and counts how many observations fall into each range.

The bar height represents:

```text
frequency = number of observations in that bin
```

A histogram discards the original time order and focuses on the **shape and spread of the values**.

> **`hist` = distribution; bucket values into ranges and count them.**

---

# How Many Data Arguments?

`plot` takes **two main data arguments**:

```python
ax.plot(x, y)
```

```text
x-values
y-values
```

`scatter` also takes **two main data arguments**:

```python
ax.scatter(x, y)
```

But `hist` takes only **one data argument**:

```python
ax.hist(data)
```

Matplotlib constructs the bins and frequencies itself.

---

## Rule to Bank

```text
ax.plot(x, y)
→ sequence / trend
→ 2 data arguments
→ points connected

ax.scatter(x, y)
→ relationship between two variables
→ 2 data arguments
→ points unconnected

ax.hist(data)
→ distribution of one set of values
→ 1 data argument
→ Matplotlib creates the bins
```

> **Plot asks “how did it move?” Scatter asks “do these move together?” Histogram asks “how are these values distributed?”**
=====================

6. # `plt.subplots(2, 1, sharex=True)`

```python
fig, (ax_top, ax_bottom) = plt.subplots(2, 1, sharex=True)
```

This creates **one figure containing two axes**, stacked vertically.

## What Do `2, 1` Mean?

The arguments describe the grid of axes:

```text
2 rows × 1 column
```

So the layout is:

```text
┌──────────────────────┐
│       ax_top         │
├──────────────────────┤
│      ax_bottom       │
└──────────────────────┘
```

Because there are **2 rows** and **1 column**, the two plots are stacked **top and bottom**, not side by side.

> **`plt.subplots(rows, columns)` → here, `2, 1` means two rows and one column.**

---

## How Do You Unpack the Two Axes?

The full line is:

```python
fig, (ax_top, ax_bottom) = plt.subplots(2, 1, sharex=True)
```

`plt.subplots(...)` returns:

1. the **Figure** object
2. a container holding the two **Axes** objects

You unpack them as:

```text
fig
ax_top
ax_bottom
```

Conceptually:

```text
fig
├── ax_top
└── ax_bottom
```

Then you can draw on each axes independently:

```python
ax_top.plot(days, prices)
ax_bottom.plot(days, returns)
```

> **`ax_top` controls the top chart; `ax_bottom` controls the bottom chart.**

---

## What Does `sharex=True` Do?

```python
sharex=True
```

makes both axes use the **same x-axis scale and limits**.

If both plots use `days`, then Day 4 on the top chart sits directly above Day 4 on the bottom chart.

```text
Top:       Day 4 price
               │
               │ same x-position
               ↓
Bottom:    Day 4 return
```

That vertical alignment makes it easy to compare related values at the same point in time.

It also avoids duplicate x-axis labeling: typically the x tick labels appear only on the **bottom axes**.

So the labeling pattern becomes:

```python
ax_top.set_ylabel("Price")

ax_bottom.set_ylabel("Return")
ax_bottom.set_xlabel("Day")
```

The top panel does not need its own duplicate `"Day"` x-label.

---

## Rule to Bank

```text
plt.subplots(2, 1, sharex=True)

2
→ two rows

1
→ one column

(ax_top, ax_bottom)
→ unpack the two axes

sharex=True
→ both axes use the same x-axis
→ x positions align vertically
→ x tick labels are generally shown only on the bottom panel
```

> **One Figure, two stacked Axes, one shared x-axis.**
===================

7. # `black` vs. `ruff`

`black` and `ruff` are both developer tools, but they do **different jobs**.

## `black` — Formatter

```bash
black file.py
```

`black` is a **code formatter**.

It rewrites the file into Black's canonical formatting style.

It can change things such as:

```text
spacing
blank lines
line breaks
operator spacing
comma spacing
trailing newlines
```

For example:

```python
x=1
```

becomes:

```python
x = 1
```

And:

```python
def add( a,b ):
    return a+b
```

becomes:

```python
def add(a, b):
    return a + b
```

> **`black` changes the file itself.**

Its job is primarily:

> **Make the code consistently formatted.**

It should preserve the program's behavior while changing its presentation.

---

## `ruff check` — Linter

```bash
ruff check file.py
```

`ruff` is being used here as a **linter**.

Instead of primarily asking how the code should look, it checks whether the code violates enabled lint rules.

For example, we deliberately wrote:

```python
import os
```

without ever using `os`.

Ruff reported:

```text
F401 [*] `os` imported but unused
```

That code is valid Python and Black would happily format it.

But Ruff notices that the import is unnecessary.

> **`ruff check` inspects and reports problems. It does not normally change the file.**

---

# Which One Changes the File?

Plain:

```bash
black file.py
```

**changes the file** by reformatting it.

Plain:

```bash
ruff check file.py
```

**does not change the file**. It reports violations.

So:

```text
black
→ inspect formatting
→ rewrite file

ruff check
→ inspect lint rules
→ report findings
```

---

# What Does `ruff check --fix` Do?

```bash
ruff check --fix file.py
```

adds automatic fixing.

When Ruff reports an issue marked:

```text
[*]
```

that indicates Ruff knows how to safely auto-fix that violation.

For our unused import:

```python
import os
```

plain Ruff:

```bash
ruff check messy.py
```

reported:

```text
F401 [*] `os` imported but unused
```

but left the file unchanged.

Then:

```bash
ruff check --fix messy.py
```

actually removed the unused import.

It reported:

```text
Found 1 error (1 fixed, 0 remaining).
```

---

## Core Distinction

```text
BLACK
↓
formatter
↓
changes the file
↓
makes formatting canonical


RUFF CHECK
↓
linter
↓
reports lint-rule violations
↓
does not ordinarily modify the file


RUFF CHECK --FIX
↓
linter + fixer
↓
reports violations
↓
automatically fixes eligible [*] issues
```

> **RULE TO BANK:**
> `black` reformats.
> `ruff check` diagnoses.
> `ruff check --fix` diagnoses **and fixes the violations Ruff knows how to fix automatically**.
=====================

8. # Why Use `pytest.approx(expected)` for Floats?

When a function returns a floating-point value, I should usually test it with:

```python
assert actual == pytest.approx(expected)
```

instead of:

```python
assert actual == expected
```

## Why?

Floating-point numbers are stored in **binary**, and many ordinary decimal values cannot be represented exactly.

A classic example is:

```python
0.1 + 0.2
```

Mathematically:

```text
0.1 + 0.2 = 0.3
```

But in floating-point arithmetic, the stored result can be slightly different from exact `0.3`.

So an exact comparison with:

```python
==
```

can fail because of tiny numerical representation error, even when the calculation is mathematically correct.

---

## What `pytest.approx()` Does

```python
pytest.approx(expected)
```

compares the actual value to the expected value **within a small tolerance**.

For example:

```python
def test_mean_return():
    assert mean_return([0.1, 0.2, 0.3]) == pytest.approx(0.2)
```

This means:

> The result should be sufficiently close to `0.2`, allowing for tiny floating-point error.

---

# Connection to F5

This is the same idea we used in F5 with NumPy.

Instead of testing floating-point arrays with exact equality:

```python
Sigma == Sigma.T
```

we learned to use:

```python
np.allclose(Sigma, Sigma.T)
```

because two mathematically equal floating-point computations can differ by tiny numerical amounts.

We also used a tolerance when checking whether eigenvalues were nonnegative:

```python
np.all(eigenvalues >= -1e-12)
```

instead of demanding:

```python
eigenvalues >= 0
```

because a mathematically zero eigenvalue might appear numerically as something tiny like:

```text
-1e-16
```

---

## Same Principle, Different Tool

```text
F5 NumPy:
np.allclose(...)
or an explicit numerical tolerance

F6 pytest:
pytest.approx(...)
```

Both encode the same idea:

> **For floating-point calculations, test mathematical closeness rather than exact bit-for-bit equality.**

### Rule to Bank

```python
assert integer_result == expected
```

is often fine for exact discrete values.

But for floating-point results:

```python
assert float_result == pytest.approx(expected)
```

is safer and expresses the numerical intent more accurately.
=======================

9. # Type Hints

Given:

```python
def f(x: float) -> float:
```

the type hints annotate **two things**:

```text
x: float
```

means:

> The parameter `x` is intended to be a `float`.

And:

```text
-> float
```

means:

> The function is intended to return a `float`.

So the signature documents:

```text
input x   → float
return    → float
```

For example:

```python
def simple_return(old_price: float, new_price: float) -> float:
    return (new_price - old_price) / old_price
```

documents that both inputs are intended to be floats and the returned result is intended to be a float.

## Do Type Hints Change Runtime Behavior?

**No.**

Type hints do **not** change the arithmetic or logic the function performs.

For example:

```python
def f(x: float) -> float:
    return x * 2
```

the `: float` and `-> float` are annotations. Python does not automatically enforce them at runtime.

The actual computation is still:

```python
return x * 2
```

> **Type hints document the intended interface; they do not themselves change what the function computes.**

They are useful because readers, IDEs, linters, and type-checking tools can use them to understand the intended types.

### Rule to Bank

```text
parameter: type
→ intended input type

-> type
→ intended return type

Type hints
→ documentation/tooling information
→ no automatic runtime enforcement
→ no change to the function's computation
```
=====================

10. # Normalization to Base 100

We rebase two price series to **base 100** so we can compare their **relative performance**, rather than their raw dollar prices.

Suppose:

```text
Asset A starts at $100
Asset B starts at $30
```

If we plot the raw prices, Asset A naturally sits much higher simply because its price level is larger.

That does **not** mean Asset A performed better.

Normalization removes that scale difference.

---

## The Formula

```python
p / prices[0] * 100
```

means:

```text
current price
───────────── × 100
starting price
```

So each price is expressed relative to that asset's **own starting price**.

---

## Why Base 100 Helps

After normalization:

```text
100   = no change from the starting price
105   = 5% above the starting price
90    = 10% below the starting price
130   = 30% above the starting price
```

Now two assets with completely different dollar prices can be compared on the same scale.

> **Normalization changes the question from “What price is this asset?” to “How much has this asset moved relative to where it started?”**

---

## What Does the Formula Guarantee About the First Value?

For the first observation:

```python
p = prices[0]
```

so the formula becomes:

```text
prices[0] / prices[0] * 100
= 1 * 100
= 100
```

Therefore:

> **Every series normalized with `p / prices[0] * 100` is guaranteed to begin at exactly `100`, assuming the starting price is nonzero.**

That shared starting point is what makes relative performance visually comparable.

---

## Capstone Example

Asset A:

```text
100 → 103
```

Normalized:

```text
100 → 103
```

So it gained:

```text
3%
```

Asset B:

```text
30 → 34
```

Normalized ending value:

```text
34 / 30 * 100 ≈ 113.33
```

So it gained approximately:

```text
13.33%
```

Even though Asset B's raw price is much lower, normalization reveals that **Asset B was the much larger relative mover**.

> **RULE TO BANK:**
> Normalize to base 100 to remove raw-price scale differences and compare relative growth.
> The first value is always `100` because the starting price is divided by itself.

# Day 29 — matplotlib, the figure/axes model

F6 Start — Matplotlib, Figure/Axes Model, and Environment Setup

## **What we are doing:**
---------------------

> F6 begins with Matplotlib, Python’s plotting library. The goal of this lesson is to learn the figure/axes model and use the explicit plotting style:

fig, ax = plt.subplots()

instead of relying only on the quick:

`plt.plot(...)`

> The explicit fig, ax style is being taught because it scales to more complex figures. One figure can contain multiple axes, which is the pattern that will later support multi-panel figures.


## **What I need:**
----------------

>Matplotlib must be installed inside the project’s active virtual environment.

<Installing Matplotlib added nine new packages/lines to requirements.txt, unlike NumPy, which had added only one. This is because Matplotlib needs additional machinery for things such as fonts, image handling, and dates.

<After installation, requirements.txt was refreshed and the install step was committed.

On the first Matplotlib import, I may see:

>Matplotlib is building the font cache; this may take a moment

This is normal and should be a one-time operation. Matplotlib is scanning the system fonts and caching them.

>What the new library gives me

The plotting module is imported with the standard alias:

`import matplotlib.pyplot as plt`

plt is the conventional alias for matplotlib.pyplot, just as np is the conventional alias for NumPy.


## **The main model for this lesson is:**
---------------------------------------

fig, ax = plt.subplots()

This returns two objects through tuple unpacking.

fig

`fig` is the Figure.

It represents the entire canvas, image, or window.

>Think of it as the whole sheet of paper.

A single figure can contain multiple axes.

`ax`

ax is the Axes.

It represents one plotting area inside the figure.

>Think of it as one chart drawn on the sheet of paper.

With this explicit style, plotting and labeling methods are called on ax:

ax.plot(x, y)
ax.set_title(...)
ax.set_xlabel(...)
ax.set_ylabel(...)

The important difference is that I am working on a specific axes object rather than calling everything directly through plt.


## **How I set up the environment for this lesson:**
----------------------------------------------------

I need to be in the active virtual environment:

(.venv)

From the shell prompt:

foundation %

I launch Python with:

python

not:

python3

Then I should see the Python REPL prompt:

>>>

At >>>, I import Matplotlib:

`import matplotlib.pyplot as plt`

The import should complete silently apart from the possible one-time font-cache message.

Everything in this lesson is being typed at the:

>>>

Python prompt, not at:

foundation %

# First Task

The first plotting data is:

prices = [100, 102, 101, 104, 103]
days = [1, 2, 3, 4, 5]

These are two plain Python lists:

days will be the x-axis
prices will be the y-axis

Then I type:

fig, ax = plt.subplots()

and stop.

<The task is asking me to understand what Matplotlib has created before any data is plotted.
===========================================================================================
My predictions:

1. What is fig?

fig is the Figure object — the whole canvas or complete image/window.

2. What is ax?

ax is the Axes object — the individual plotting area inside that figure.

3. Should a completed chart appear yet?

No completed chart should appear yet because:

fig, ax = plt.subplots()

only creates the figure and axes.

I have not drawn the data yet because I have not called:

ax.plot(days, prices)

Depending on the environment, a blank figure window may appear or nothing visible may appear yet. Either is normal.
===========================================================================================

>One environment note, since it matters for how you'll see results: you're in a plain terminal >>>, not a notebook. In this setup, plots don't auto-display — you have to explicitly call plt.show() to pop the window, and nothing appears until you do. (Colab/Jupyter show inline automatically; the terminal doesn't. Good to know the difference — it's why your F6 work here needs plt.show() where the diagnostic notebook didn't.)

===========================================================================================

# Now draw on the axes. Type this one line and stop:

`ax.plot(days, prices)`

Predict first:

1. This draws the line onto ax — but you're in the terminal, so does the chart appear on screen from this line alone, or do you still need something else?
2. When you run ax.plot(...), the terminal will echo something back (a return value) — a line like [<matplotlib.lines.Line2D object at 0x...>]. That's not an error — what do you think it is? (Think: ax.plot returns the line object it just created, and >>> echoes any return value.)

Run it, give me both predictions, and tell me what the terminal echoed. Then we label the axes and call show() to actually see the chart.

---

### Prediction 1 — Will the chart appear yet?

```python
ax.plot(days, prices)
```

will **draw the line onto `ax`**, but because you're running this in a plain terminal `>>>`, the chart still will **not appear on screen yet**.

You still need:

```python
plt.show()
```

to open the figure window.

> **Terminal rule:** plotting commands build the figure; `plt.show()` actually displays it.

---

### Prediction 2 — What will the terminal echo?

`ax.plot(days, prices)` returns the line object it created, so the REPL will echo something like:

```text
[<matplotlib.lines.Line2D object at 0x...>]
```

That is **not an error**.

It means:

> `ax.plot(...)` created a Matplotlib `Line2D` object and returned it.

The square brackets are there because `ax.plot(...)` returns a **list of line objects**. In this case, you plotted one line, so the list contains one `Line2D` object.

So the expected interaction is:

```python
>>> ax.plot(days, prices)
[<matplotlib.lines.Line2D object at 0x...>]
```

And the chart still stays hidden until:

```python
plt.show()
```

### 🧠 Remember

```markdown
- `ax.plot(...)` = create/draw the line on the axes
- returned `Line2D` object = the line Matplotlib created
- `plt.show()` = display the figure window in a terminal session
```
========================================================================
Now label the axes before showing — this is where the set_ methods come in, and it's the piece that distinguishes the explicit ax approach. Type these three at >>>:

ax.set_title("Price over 5 days")
ax.set_xlabel("Day")
ax.set_ylabel("Price")

Note the pattern, and bank it: on an axes object it's ax.set_title(...), ax.set_xlabel(...), ax.set_ylabel(...) — the set_ prefix. (Contrast the quick way, which uses plt.title(...) with no set_. This is the single most common source of "why doesn't my label work" confusion — mixing the two APIs. On an ax, use ax.set_xlabel.)

Each of those three will also echo a return value (a Text object) — same story as the Line2D, ignore it, not an error.

Then, finally, display it:

plt.show()
======
Predict before you run show():

What happens on screen? (A window should pop up — an actual chart with your line, title, and labels.)
Here's the terminal gotcha, worth knowing: in many terminal setups, plt.show() blocks — the >>> prompt won't come back until you close the chart window. So after the plot appears, you may need to close the window to get your prompt back. (Some backends don't block; you'll find out which you have.)

Run the three set_ lines, then plt.show(), and tell me: did a window pop up with the labeled chart, and did your >>> prompt come back immediately or only after closing the window? (A screenshot of the chart is great if it appears.)
====

### Predictions before `plt.show()`

```python
ax.set_title("Price over 5 days")
ax.set_xlabel("Day")
ax.set_ylabel("Price")
plt.show()
```

### 1. What should happen on screen?

A **separate chart window should open** showing:

* the line through the five price points
* title: **Price over 5 days**
* x-axis label: **Day**
* y-axis label: **Price**

> **`ax.plot(...)` built the line, the `ax.set_...` methods labeled the axes, and `plt.show()` finally displays the completed figure.**

---

### 2. What happens to the `>>>` prompt?

I predict that `plt.show()` will probably **block the terminal** while the chart window is open.

So the sequence may look like:

```text
>>> plt.show()
```

Then the plot window appears, but no new:

```text
>>>
```

prompt yet.

Once you **close the chart window**, the Python prompt should return:

```text
>>>
```

If your Matplotlib backend is non-blocking, the prompt may return immediately instead. Either behavior can occur.

---

### 🧠 Important API distinction

```markdown
> **Explicit axes style**
> - `ax.plot(...)`
> - `ax.set_title(...)`
> - `ax.set_xlabel(...)`
> - `ax.set_ylabel(...)`
>
> **Quick pyplot style**
> - `plt.plot(...)`
> - `plt.title(...)`
> - `plt.xlabel(...)`
> - `plt.ylabel(...)`
```

The important thing is **not to mix up the naming conventions**: when working with the `ax` object, the label methods use the `set_` prefix.
====================================================================================

At foundation % (open a second tab or exit Python first):

code plot_prices.py

Then verify the name landed right (the filename-space trap):

ls plot_prices.py

Once the file's open and correctly named, here's what it needs to contain — write it yourself, in this order:

The import (import matplotlib.pyplot as plt)
The two data lists (prices, days)
fig, ax = plt.subplots()
ax.plot(...) — with the right arguments (which list is x, which is y?)
The three labels — set_title, set_xlabel ("Day"), set_ylabel ("Price") — each once, correct the first time (the whole advantage of a file)
plt.show() at the end

You know every one of these lines now — you just typed them all in the REPL. The difference is writing them clean, once, in order. Predict-as-you-go isn't needed here since you've seen each piece; just assemble the script.

Create the file, write the six parts, save (watch the tab dot), then run it from foundation %:

python plot_prices.py

A fresh figure window should pop with everything correct. 

====================================================================================

## `plot_prices.py`

```python
import matplotlib.pyplot as plt

prices = [100, 102, 101, 104, 103]
days = [1, 2, 3, 4, 5]

fig, ax = plt.subplots()

ax.plot(days, prices)

ax.set_title("Price over 5 days")
ax.set_xlabel("Day")
ax.set_ylabel("Price")

plt.show()
```

### What the script does

```markdown
> **Data direction:** `days` goes on the x-axis and `prices` goes on the y-axis.
```

The sequence is:

```markdown
1. `import matplotlib.pyplot as plt` → loads the plotting library.
2. `prices` and `days` → store the data.
3. `fig, ax = plt.subplots()` → creates a fresh figure and one axes.
4. `ax.plot(days, prices)` → draws Price against Day.
5. `ax.set_...` → adds the title and axis labels.
6. `plt.show()` → displays the finished figure.
```

From `foundation %`, run:

```bash
python plot_prices.py
```

### Prediction

A fresh window should open containing a line connecting:

```text
(1, 100)
(2, 102)
(3, 101)
(4, 104)
(5, 103)
```

with:

```text
Title:  Price over 5 days
x-axis: Day
y-axis: Price
```

> **Why the script is cleaner than the REPL:** every run starts the sequence fresh—create figure → draw → label → show—so there is no leftover figure state from an earlier `plt.show()` cycle.

=================================================================================

# Framing: plt.show() displays the figure in a window (ephemeral). 
# fig.savefig("path") writes it to disk as an image file (permanent). You want both — save it, then show it. And it goes on the fig object (the whole canvas), because you're saving the entire figure, not just one axes.

The card says save to an artifacts/ folder. So first, in your script, add a line to save the figure before plt.show():
`
`fig.savefig("artifacts/prices.png")`

But that folder doesn't exist yet, and savefig won't create it — it'll error if artifacts/ isn't there. So first make the folder. At foundation %:

mkdir -p artifacts

Then add the fig.savefig("artifacts/prices.png") line to your script — place it after the labels but before plt.show() (you want the fully-labeled figure saved). Save the script, re-run:

python plot_prices.py

Then verify the file was created:

ls -la artifacts/

You want to see prices.png with a non-zero size. Predict first: when you run the script now, will a window still pop up (from plt.show()), and will a PNG appear in artifacts/? Or does savefig replace show()?

Add the folder + the savefig line, run it, and paste ls -la artifacts/ plus your prediction. Then we handle one .gitignore decision (do we commit the PNG or ignore it?) and commit f6d1.

====================================================================================

### Prediction

Yes — **both things should happen**.

```python
fig.savefig("artifacts/prices.png")
```

will save the fully labeled figure to disk, and then:

```python
plt.show()
```

will still display the chart window.

So `savefig` does **not** replace `show()`; they do different jobs:

```markdown
> **`fig.savefig(...)`** = save a permanent image file  
> **`plt.show()`** = display the figure on screen
```

The order should be:

```python
ax.set_title("Price over 5 days")
ax.set_xlabel("Day")
ax.set_ylabel("Price")

fig.savefig("artifacts/prices.png")

plt.show()
```

And before running the script, create the folder from `foundation %`:

```bash
mkdir -p artifacts
```

Then run:

```bash
python plot_prices.py
```

and verify with:

```bash
ls -la artifacts/
```

### Expected result

You should still get the chart window **and** see something like:

```text
prices.png
```

inside `artifacts/`, with a non-zero file size.

> **Important:** saving comes after the labels so the PNG contains the complete labeled chart, and before `plt.show()` so the figure is definitely saved during the same fresh build cycle.

=============================================================================================

>Now — the .gitignore decision before we commit. You've got a new generated file, artifacts/prices.png. Question: do we commit the PNG, or ignore it?

Here's the reasoning, and it's a real design choice (predict your answer):

**Argument for ignoring it:** the PNG is a generated artifact — it's produced by running plot_prices.py. Anyone with the script and the data can regenerate it exactly. Committing generated output is often considered clutter: you version the source (the script), not the output (the image), same reason you don't commit .pyc files or __pycache__.

**Argument for committing it:** sometimes you want the rendered figure in the repo — for a report, a portfolio, a README showing results — so a viewer sees the chart without running anything.

For a foundation learning repo, the cleaner convention is usually to ignore generated figures (version the script, regenerate the image on demand). The card's own instinct leans that way — it treats artifacts//figures/ as output folders.

So: what's your call — commit prices.png, or add artifacts/ to .gitignore so generated figures stay out of version control? Give me your answer and reasoning (there's a defensible case either way — I want your read). Then we commit f6d1 accordingly: either committing the script + PNG, or the script + updated .gitignore.
=============================================================================================

### My call: **ignore `artifacts/`**

For this foundation learning repo, I would add:

```gitignore
artifacts/
```

to `.gitignore` and commit the **script**, not the generated PNG.

### Why

> **The script is the source; the PNG is reproducible output.**

`plot_prices.py` contains the actual work and logic:

```text
data → figure → axes → plot → labels → savefig
```

`prices.png` can be regenerated at any time just by running:

```bash
python plot_prices.py
```

So committing the PNG would mean versioning something that is derived from code you already version.

This is the same general principle as ignoring:

```text
__pycache__/
.venv/
```

You keep the files that define the project and ignore machine-generated or reproducible output.

### When I would make the opposite choice

If this were a **portfolio repo, paper repo, report, or README** where the finished chart itself is part of what a reader is supposed to see, then I would commit selected final figures.

But for this repo:

```markdown
> **Decision:** Ignore `artifacts/` because figures are generated outputs that can be recreated from the committed source code.
```

So your clean f6d1 commit should include:

```text
plot_prices.py
.gitignore   ← updated with artifacts/
```

but **not** `artifacts/prices.png`.

=============================================================================================

## TODAY'S FIRST LESSON RECAP

### Figure vs. Axes

```python
fig, ax = plt.subplots()
```

* `fig` = the **Figure** — the entire canvas/window.
* `ax` = the **Axes** — the individual plotting area inside the figure.
* One figure can contain multiple axes.

> **Mental model:** `fig` is the sheet of paper; `ax` is the chart drawn on that paper.

---

### Plotting and labeling with the Axes object

```python
ax.plot(days, prices)

ax.set_title("Price over 5 days")
ax.set_xlabel("Day")
ax.set_ylabel("Price")
```

When using the explicit `fig, ax` style, the labels are methods on `ax` and use the **`set_` prefix**.

> **Important:** Calling a `set_` method again **overwrites** the previous value. For example, a second `ax.set_xlabel(...)` replaces the first x-axis label.

---

### `savefig()` vs. `show()`

```python
fig.savefig("artifacts/prices.png")
plt.show()
```

* `fig.savefig(...)` = writes the figure to disk as a **permanent image file**.
* `plt.show()` = displays the figure in a window **temporarily**.

Both can be used in the same script.

The correct order is:

```python
# build plot
# add labels
fig.savefig("artifacts/prices.png")
plt.show()
```

> **Save after the figure is fully labeled and before showing it.**

---

### `plt.show()` in a terminal/script

In the terminal, plots do **not** automatically display.

```python
plt.show()
```

is required to open the figure window.

In my setup, `plt.show()` **blocks** execution: the terminal prompt does not return until I close the figure window.

---

### Why a script is better than the REPL for plotting

A script gives me one clean, repeatable sequence:

```text
import
→ data
→ create figure/axes
→ plot
→ label
→ save
→ show
```

Running:

```bash
python plot_prices.py
```

builds a fresh figure every time. This avoids leftover figure state, repeated label changes, and REPL scrollback confusion.

---

### Generated artifacts

`artifacts/prices.png` is generated by the script, so the `artifacts/` directory is ignored in `.gitignore`.

```gitignore
artifacts/
```

> **The script is the source; the PNG is reproducible output.**

Then commit exactly the three intended files:

```bash
git add .gitignore plot_prices.py notes_day29.md
git commit -m "f6d1: matplotlib figure/axes model, labeled line plot, savefig"
```

Afterward, `git status` should be clean if everything was committed successfully.

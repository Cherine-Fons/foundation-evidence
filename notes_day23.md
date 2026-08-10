# DAY 23
# warm-up — three from last week, in your own words:

1. Multiplicity-aware degrees: why + e.multiplicity and not +1? What specifically does +1 break?
2. pip freeze > requirements.txt — what does it capture, and why do we regenerate it right after installing a new package (which is exactly what we're about to do)?
3. __str__ vs __repr__ — which one fires on print(obj) versus typing obj bare at >>>, and who's the intended audience for each?


# Answers
1. We use + e.multiplicity because one Edge object can represent several parallel copies of the same edge. Each of those copies contributes to the degree of both endpoints. If I used +1, I would count the Edge object only once instead of counting all the edges it represents, so any edge with multiplicity greater than 1 would make the vertex degrees too small.

2. `pip freeze > requirements.txt` records the packages currently installed in my active virtual environment, including their exact versions, and writes that list into `requirements.txt`. I regenerate it after installing a new package so the file stays synchronized with the environment I am actually using. That way, someone else — or future me on a new machine — can recreate the same setup with the same dependencies instead of guessing what needs to be installed.**

3. 
print(obj) uses __str__. It is meant for human-readable output — concise and pleasant to display.

Typing obj bare at >>> uses __repr__. It is meant for developers/debugging — more complete and precise about what the object actually contains.

Using the Quote example:

print(q)
# AAPL: 150.0/150.2

That is __str__.

But:

>>> q
Quote(ticker='AAPL', bid=150.0, ask=150.2, timestamp='2026-08-08')

That is __repr__.

So the easiest way to remember it is:

__str__ = “How should this look to a person?”
__repr__ = “What is this object exactly?”


# Correction
3/3 — clean across the board.

1. Exactly right, and you named the failure mode precisely: +1 counts the object, not the copies it stands for, so every parallel bundle collapses to one and degrees come out too small. That's the whole reason the solver's instance shape carries multiplicity on the edge.
2. Correct — snapshot of the active venv with pinned versions, regenerated so the file never drifts from reality. Which is why it's step two today, right after the install.
3. Correct, and your mnemonic is the right one. One thing to bank alongside it: __str__ falls back to __repr__ if you don't define it, but never the other way around — so if you only write one, write __repr__.

----------------------------------------------------------------------------------------------------------------
 
# Now the install. First, look at your foundation % prompt and confirm (.venv) is showing — inside the venv, plain pip is the project's pip, and installing into the wrong Python is the one way this goes sideways.

If (.venv) is there, run this at foundation %:

pip install numpy
----------------------------------------------------

Now step two, and predict before you freeze. requirements.txt currently holds the pytest line and its dependencies from Day 20. After this install, pip freeze > requirements.txt will regenerate the whole snapshot.

Predict for me first: how many new lines does numpy add — exactly one, or one plus some dependencies? Commit to an answer before you look.

Then run these at foundation %:

pip freeze > requirements.txt
cat requirements.txt

Tell me your prediction and what cat actually shows.
-----------------------------------------------------
IN SHELL:

(.venv) cherinefons@Mac foundation % pip install numpy
Collecting numpy
  Downloading numpy-2.5.2-cp314-cp314-macosx_14_0_arm64.whl.metadata (6.6 kB)
Downloading numpy-2.5.2-cp314-cp314-macosx_14_0_arm64.whl (5.4 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 5.4/5.4 MB 21.5 MB/s  0:00:00
Installing collected packages: numpy
Successfully installed numpy-2.5.2
(.venv) cherinefons@Mac foundation % successfully installed
zsh: command not found: successfully
(.venv) cherinefons@Mac foundation % pip freeze > requirements.txt
(.venv) cherinefons@Mac foundation % cat requirements.txt
iniconfig==2.3.0
numpy==2.5.2
packaging==26.3
pluggy==1.6.0
Pygments==2.20.0
pytest==9.1.1
(.venv) cherinefons@Mac foundation % 
-----------------------------------------------------
# Q
Now the prediction payoff. numpy added exactly one line — just numpy==2.5.2. The other five (iniconfig, packaging, pluggy, Pygments, pytest) were already there from Day 20.

Here's the drill, and it's a real reasoning question, not something you can read off the screen: back on Day 20, installing pytest added five lines — itself plus iniconfig, pluggy, packaging, Pygments. Today, installing numpy added one. Same pip install, wildly different footprint. Why? What's different about what these two packages need to run?
------------------------------------------------------
# A

Because pip install installs not only the package you asked for, but also any runtime dependencies that package declares it needs.

pytest is built on several separate Python packages. To run, it relies on things like pluggy, iniconfig, packaging, and Pygments, so pip had to install those alongside pytest. That is why one request produced five entries in requirements.txt.

numpy is different. The NumPy wheel you installed is essentially self-contained at runtime for your platform: its core functionality comes packaged inside NumPy itself, including compiled numerical code, so it did not require additional Python packages to be installed with it. Therefore:

pip install pytest
→ pytest + its dependencies

pip install numpy
→ numpy only

The important idea is:

The number of packages pip installs depends on the dependency tree of the package, not on the pip install command itself.

Small technical nuance: NumPy does have machinery and dependencies involved if it must be built from source, but because pip installed a ready-made wheel for your system, those are not additional runtime packages showing up in your pip freeze.

Some packages depend on other packages; some are mostly self-contained. Pip installs the whole dependency chain automatically.

That is why the same command can add a very different number of lines to requirements.txt.
----------------------------------------------------------

# Day 23 — arrays vs lists. This is new material, so framing before any prediction, per how we do new syntax.

You already own Python lists cold. The question NumPy answers is: why would a numerical person ever want something other than a list? Three differences, and they're the spine of everything in F5:

1. Homogeneous vs heterogeneous. A list holds anything — [1, "hello", 3.5, None] is legal. A NumPy array holds one dtype, decided up front and enforced. That sounds like a limitation; it's the source of the power. Because every element is the same type and size, the array sits in one contiguous block of memory, and the compiled C underneath (the same "self-contained numerical engine" from the dependency question earlier) can rip through it without stopping to ask "what type is this element?" at every step.

2. Vectorized operations vs loops. With a list, prices * 2 doesn't double the numbers — think about what it actually does. With an array, arr * 2 doubles every element at once, no loop written. That's vectorization, and it's the single biggest mental shift this week: you stop writing for loops over numbers and start writing whole-array expressions.

3. Shape. A list is one-dimensional and ragged — a list of lists can have rows of different lengths. An array has a rigid shape: a 2×3 array is always 2 rows by 3 columns, and that regularity is what makes matrix operations (your Day 27 w.T @ Sigma @ w) even possible.

# Q Hold those three. Now a prediction, before you type anything — reason it out from what I just said:

You have a plain Python list prices = [100, 102, 101]. You write prices * 2. What does Python give you — and why is it emphatically not [200, 204, 202]?
----------------------------------------------------------
# A

prices * 2 on a list repeats it, giving [100, 102, 101, 100, 102, 101], because * on a list means repetition, not element-wise math — the exact list-vs-array distinction it's teaching

Tell me your answer and your reasoning, then we'll bring NumPy in and watch the array version behave differently.
----------------------------------------------------------

# EVAL

Exactly right, and you named the mechanism: for a list, * is a sequence operator — it means "repeat this sequence N times," same as "ab" * 3 gives "ababab". It has nothing to do with the numbers inside. So prices * 2 is [100, 102, 101, 100, 102, 101] — length 6, not doubled values. That's the wall vectorization is built to knock down.
----------------------------------------------------------
Now bring NumPy in and watch the difference live. This is the first array you create, so we go a piece at a time.

At your >>> prompt (the Python tab, not foundation %):

import numpy as np

# If (.venv) is not showing: reactivate first, then launch:
  source .venv/bin/activate
  python

np is the universal convention — every NumPy codebase, every CPF notebook, every StackOverflow answer writes np. 

Type it, then predict before the next line:
----------------------------------------------------------
You're about to run prices_arr = np.array([100, 102, 101]). Two predictions:

1. When you then type prices_arr bare at >>>, what do you think it prints — and how will it look different from how the plain list [100, 102, 101] prints? (Think back to __repr__ — what's the array telling the developer about itself?)
2. Then, when you run prices_arr * 2, what comes back now?

Give me both predictions with reasoning, then run these two lines and we compare:

prices_arr = np.array([100, 102, 101])
prices_arr
prices_arr * 2
-----------------------------------------------------------
# PREDICTION

1. array([100, 102, 101])

2. array([200, 204, 202])

------------------------------------------------------------

Your two predictions should be:

```python
>>> prices_arr = np.array([100, 102, 101])
>>> prices_arr
array([100, 102, 101])
```

A plain Python list would display as:

```python
[100, 102, 101]
```

The NumPy array’s `__repr__` includes the `array(...)` wrapper, which tells the developer, “this is a NumPy array, not an ordinary Python list.”

Then:

```python
>>> prices_arr * 2
array([200, 204, 202])
```

NumPy multiplies **each element** by `2`.

That is very different from a Python list:

```python
[100, 102, 101] * 2
```

which would repeat the list:

```python
[100, 102, 101, 100, 102, 101]
```

So the big NumPy shift is:

> **Array arithmetic is element-by-element arithmetic.** `prices_arr * 2` doubles the numbers; it does not duplicate the container.
-----------------------------------------------------------------------------
# Conclusion

Both predictions are exactly right — hold onto them, because you predicted before the venv trap interrupted you, and I want you to actually see them land rather than just take the checkmark.

So the sequence now:

exit() out of the wrong interpreter.
Get back into the venv's Python (the two-case fix from my last message — reactivate with source .venv/bin/activate if (.venv) isn't showing, then launch with python, not python3).
Re-run the three lines:
   import numpy as np
   prices_arr = np.array([100, 102, 101])
   prices_arr
   prices_arr * 2

Then check your two predictions against the screen. And notice why your first prediction is the right shape: typing prices_arr bare fires __repr__, and the array's repr is literally array([100, 102, 101]) — the object announcing "I'm a NumPy array, not a list," which is exactly the developer-facing precision you described for __repr__ last week. The list would've just shown [100, 102, 101] with no wrapper.
-----------------------------------------------------------------------------
# Feedback

There it is — both predictions confirmed against the screen, and you fixed the venv trap cleanly (reactivate → launch with python, not python3). That's the whole arc of the moment: right interpreter, package visible, and * now means element-wise math instead of list repetition.

Look at what just happened side by side, because this is the mental model for the entire week:

[100, 102, 101] * 2   →  [100, 102, 101, 100, 102, 101]   (repeat the sequence)
array([100, 102, 101]) * 2   →  array([200, 204, 202])     (multiply every element)

Same syntax, completely different meaning — and the array version is the one that matches how a mathematician thinks about scaling a vector. No loop written, the multiply happened across all three elements at once. 
# That's vectorization, live.
-----------------------------------------------------------------------------

# NEXT

Now let's expose the thing that makes it possible — the enforced single dtype. Predict before running:

You built prices_arr from [100, 102, 101] — all integers. You're about to ask the array what type it decided on, and then hand it a list with a float mixed in. Two predictions:

1. prices_arr.dtype — what does it report? (It's an attribute, no parens — like field vs method from last week.)
2. np.array([100, 102.5, 101]) — one float among two ints. The array can't hold mixed types. So what does it do — reject it, or force everything to one type? If it forces, which type wins, int or float, and why that direction?

Run these at >>>:

prices_arr.dtype
np.array([100, 102.5, 101])

Give me both predictions with reasoning first, then the output.
-----------------------------------------------------------------------------
# ANSWER

My predictions:

```python
>>> prices_arr.dtype
dtype('int64')
```

Reason: you built the array from:

```python
[100, 102, 101]
```

and every value is an integer, so NumPy chooses one integer dtype for the whole array.

For:

```python
>>> np.array([100, 102.5, 101])
```

I predict:

```python
array([100. , 102.5, 101. ])
```

NumPy does **not** reject the mixed input. It promotes everything to one common type, here `float64`.

Why does `float` win? Because converting `102.5` to an integer would lose information:

```text
102.5 → 102   # information lost
```

But converting the integers to floats preserves their values:

```text
100 → 100.0
101 → 101.0
```

So NumPy moves in the safer direction:

> **int + float → float**, because a float can represent those integer values without throwing away the decimal part.

So the expected session is:

```python
>>> prices_arr.dtype
dtype('int64')

>>> np.array([100, 102.5, 101])
array([100. , 102.5, 101. ])
```

And yes: `dtype` has **no parentheses** because it is an attribute describing the array, not a method you are calling.
------------------------------------------------------------------------------------
Both confirmed, and the screen shows the upcast beautifully. Read the float array output closely:

array([100. , 102.5, 101. ])

See the bare 100. and 101. — a decimal point with nothing after it. Those were your integers 100 and 101, dragged to float because one 102.5 forced the whole array to float64. That trailing dot is NumPy telling you "these are floats now." All-one-type or nothing, made visible exactly as predicted.

And dtype('int64') on both prices_arr checks — the 64 is the bit width, and it stayed integer because that array never saw a float. Solid.

One quick bank-it note, no action: you'll sometimes see int64 vs int32 depending on the machine — on your arm64 Mac the default integer is 64-bit. Not important now, just don't be surprised when a dtype carries a number.

So the dtype half of Day 23 is closed. You've got: arrays are single-dtype, * is element-wise not repetition, upcasting goes toward the information-preserving type, and .dtype reports type + bit width. That's a clean unit — let's commit it before the last piece.

# NOTE
1. np.array([100, 102.5, 101]) → prints array([100. , 102.5, 101. ]). This float array is not saved to any name — you created it, NumPy printed it, and it's gone. You never asked it for its dtype.
2. prices_arr.dtype → int64. But prices_arr is still the original array from way back: np.array([100, 102, 101]), all integers. That variable never changed. Making a new float array on one line doesn't reach back and mutate a different variable.
------------------------------------------------------------------------------------

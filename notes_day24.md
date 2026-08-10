# Day 24 it is — indexing, slicing, and boolean masks. This is the "select from an array" piece, and it splits into two halves: positional access (indexing/slicing, which will feel familiar from lists) and boolean masks (which won't — that's the new mental model).

Let me set the working array first so we're operating on something with a bit more to grab. At `>>>` (confirm `(.venv)` and that numpy's still imported from earlier — if you restarted the interpreter, `import numpy as np` again):

```
returns = np.array([0.012, -0.008, 0.0, 0.021, -0.015, 0.006])
```

That's six daily returns — the same series shape you'll see all over CPF.

**Half one: indexing and slicing.** Framing, but light, because this half genuinely does behave like lists:

- Single index: `returns[0]` is the first element, `returns[-1]` the last — same as lists.
- Slice: `returns[1:4]` is start-inclusive, stop-exclusive — positions 1, 2, 3, *not* 4. Same half-open rule you already know from list slicing and from the strict-`>` boundary work in F4.
-----------------------------------------------------------------------------------------
Predict before running — this should be fast since it's list muscle memory:

1. `returns[0]` → ?
2. `returns[-1]` → ?
3. `returns[1:4]` → which three values? (name them, and say why position 4's value is excluded)
-----------------------------------------------------------------------------------------
# PREDICTIONS

1. `returns[0]` → first element : 0.012
2. `returns[-1]` → last element : 0.006
3. `returns[1:4]` → positions 1, 2 and 3 : -0.008, 0.0, 0.021

-----------------------------------------------------------------------------------------
Run at `>>>`:

>>> exit()
(.venv) cherinefons@Mac foundation % python3
Python 3.14.6 (v3.14.6:c63aec69bd5, Jun 10 2026, 08:07:54) [Clang 21.0.0 (clang-2100.1.1.101)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import numpy as np
>>> returns = np.array([0.012, -0.008, 0.0, 0.021, -0.015, 0.006])
>>> 
>>> returns[0]
np.float64(0.012)
>>> returns[-1]
np.float64(0.006)
>>> returns[1:4]
array([-0.008,  0.   ,  0.021])
>>> 
-----------------------------------------------------------------------------------------
# FEEDBACK

All three predictions correct — indexing and slicing behave exactly like list muscle memory, half-open slice and all. But two things to catch before we move, one of them a landmine you walked past.

The landmine — you launched with python3 again. Look:

(.venv) cherinefons@Mac foundation % python3

It worked this time — numpy imported fine — but that's luck, not correctness, and here's why it's dangerous. When (.venv) is active, python3 sometimes resolves to the venv's Python and sometimes to the system one, depending on how the shell caches the path. Earlier today python3 gave you the system Python with no numpy (the ModuleNotFoundError). This time it happened to hit the venv. Same command, two different outcomes on the same day — that's exactly the kind of nondeterminism you don't want. The rule that removes the coin-flip: inside the venv, launch with plain python. Not python3. Bank that hard, because a "works sometimes" bug is worse than a "fails always" one.

# The teaching detail — read what returns[0] actually returned:

np.float64(0.012)

Not bare 0.012 — it's wrapped: np.float64(...). That wrapper is telling you something precise: when you pull a single element out of a NumPy array, you don't get a plain Python float, you get a NumPy scalar (np.float64) — NumPy's own number type, carrying that float64 dtype from the array it came from. It behaves like a float for arithmetic, but it's the array's type system reaching all the way down to the individual element. Contrast that with the slice returns[1:4], which came back as array([...]) — a slice gives you a smaller array, a single index gives you a scalar. That distinction (index → scalar, slice → array) matters later.
-----------------------------------------------------------------------------------------
Now — the actual new material of Day 24: boolean masks. This is the part with no list equivalent, so full framing.

Watch what happens when you use a comparison operator on a whole array. Predict first:

You run returns > 0. On a single number that'd give True or False. But returns is six numbers. So what do you think comes back — a single True/False, or something shaped like the array? Reason from vectorization: you've seen * 2 apply to every element at once. What does > 0 do to every element at once?

Run at >>> (you're already there):

returns > 0

Give me your prediction with reasoning, then the output. This is the foundation the whole mask idea is built on, so let's get the prediction on record before you see it.
-----------------------------------------------------------------------------------------

# Prediction:

```python
returns > 0
```

will return a **boolean array with the same shape as `returns`**, not one single `True` or `False`.

Reason: just like:

```python
returns * 2
```

applies `* 2` to every element, the comparison:

```python
returns > 0
```

asks each element, one by one:

```text
0.012  > 0   → True
-0.008 > 0   → False
0.0    > 0   → False
0.021  > 0   → True
-0.015 > 0   → False
0.006  > 0   → True
```

# So I predict:

```python
array([ True, False, False,  True, False,  True])
```

That boolean array is the **mask**: one `True`/`False` decision for each original element.
----------------------------------------------------------------------------------------------
# FEEDBACK

Exactly right — and name what just happened, because it's the entire engine behind masks: `> 0` **vectorized**, same as `* 2` did. It compared every element against 0 independently and handed back a **boolean array** of the same shape — `True` at each position where the return was positive, `False` elsewhere. Six inputs, six True/False out, position-matched.

That boolean array is called a **mask**. On its own it's just a list of yes/no flags. The power move is what you do *with* it: you can feed a mask back into the array as an index, and NumPy returns **only the elements where the mask is `True`**. This is *boolean indexing*, and it's the thing you'll reach for constantly — "give me the returns that are positive," "select the days below the drawdown threshold."
----------------------------------------------------------------------------------------------
# NEXT

Framing the mechanic before you predict: `returns[some_boolean_array]` keeps position 0's value if the mask is `True` at position 0, drops it if `False`, walks the whole array that way, and collects the survivors into a new (usually shorter) array.

Two predictions:

1. `returns[returns > 0]` — reason it through. The mask is `[True, False, False, True, False, True]`. Which values survive, and what array comes back? (Name the actual numbers.)
2. This is the payoff, so predict the *shape* logic too: will the result be the same length as `returns` (6), or shorter? Why?

Run at `>>>`:

```
returns > 0
returns[returns > 0]
```

(Re-running `returns > 0` first just so you see the mask and the selection stacked together.)

Give me both predictions with reasoning, then the output.
----------------------------------------------------------------------------------------------
Prediction:

```python
returns[returns > 0]
```

keeps only the entries where the mask is `True`.

The mask is:

```python
[True, False, False, True, False, True]
```

So the survivors are:

```text
position 0 → 0.012   keep
position 1 → -0.008  drop
position 2 → 0.0     drop
position 3 → 0.021   keep
position 4 → -0.015  drop
position 5 → 0.006   keep
```

# So I predict:

```python
array([0.012, 0.021, 0.006])
```

And the result is **shorter than the original**: length `3` instead of `6`, because boolean indexing does not preserve the False positions as blanks—it removes them and collects only the values whose mask entries are `True`.

So stacked together:

```python
>>> returns > 0
array([ True, False, False,  True, False,  True])

>>> returns[returns > 0]
array([0.012, 0.021, 0.006])
```

# The key idea is:

> The comparison builds the mask; using that mask inside `returns[...]` filters the array down to only the matching values.
----------------------------------------------------------------------
# CONCLUSION

And the shape logic is the key insight: the result is length 3, not 6. A boolean mask selects, so the output shrinks to however many Trues there were. You can't predict a masked result's length from the input's length — it depends on how many elements pass the test. That's different from * 2 or > 0, which always return something the same shape as the input. Selection changes size; elementwise ops don't.
----------------------------------------------------------------------

# So you now have the two halves of Day 24:

positional access — returns[0] (scalar), returns[1:4] (slice → array), half-open like lists
boolean masking — a comparison vectorizes into a mask, and array[mask] keeps only the True positions, returning a shorter array
----------------------------------------------------------------------
# One more piece to make this finance-real, then we commit. The Day-24 card (Ch 8 Simple Ex 3) is literally "select returns under a drawdown threshold" — so let's do the negative side, the losing days. Predict:

returns[returns < 0] — which values come back, and what length? Reason from the mask.

Run at >>>:

returns[returns < 0]

Prediction with reasoning, then output — and after that we write notes and commit f5d2.
----------------------------------------------------------------------

# ANSWER

Prediction:

```python
returns[returns < 0]
```

first creates a mask asking, for each value, “is this less than zero?”

```text
0.012   < 0 → False
-0.008  < 0 → True
0.0     < 0 → False
0.021   < 0 → False
-0.015  < 0 → True
0.006   < 0 → False
```

So the mask is:

```python
[False, True, False, False, True, False]
```

Only the two `True` positions survive, so I predict:

```python
array([-0.008, -0.015])
```

The result has **length 2**, because there are exactly two negative-return days.

Expected output:

```python
>>> returns[returns < 0]
array([-0.008, -0.015])
```

So the finance interpretation is: **the boolean mask filters the return series down to only the losing days.**
-------------------------------------------------------------------------
# EVAL

Correct — [-0.008, -0.015], length 2. The mask returns < 0 is [False, True, False, False, True, False], two Trues, two survivors. That's your drawdown-selection pattern: "give me only the losing days." Same move you'll use in CPF for every "filter the series by a condition" task.

# Worth banking the pair side by side — the positives were length 3, the negatives length 2, and 3 + 2 = 5, not 6. The missing one is the 0.0 day, which is neither > 0 nor < 0. That's a real gotcha: strict comparisons exclude the boundary. If you actually wanted "non-losing days" you'd need >= 0 to catch the zero — the exact strict-vs-inclusive boundary distinction from your F4 pytest work, showing up again in mask form. Same lesson, new surface.
--------------------------------------------------------------------------

# DAY 24 SUMMARY

Day 24 is complete. Ledger:

1. indexing → scalar (np.float64 wrapper), slicing → array, half-open like lists
2. launch venv Python with python, not python3 (removes the coin-flip)
3. comparison on an array vectorizes into a boolean mask
4. array[mask] keeps only True positions → shorter array; selection changes length, elementwise ops don't
5. strict </> exclude the boundary (the 0.0 day); >=/<= include it
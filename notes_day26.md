Day 26 — broadcasting and the start of linear algebra (f5d4). Two connected pieces: first the *rules* behind something you've already seen work, then your first real matrix operations. This leans directly on yesterday's axis reasoning.

Environment check: `>>>` prompt, numpy imported (relaunch with `python` not `python3` if you restarted). Everything at `>>>`.

**Framing — broadcasting.** You've already used it without the name. `prices_arr * 2` on Day 23 multiplied every element by a single scalar — a shape `(3,)` array met a shape `()` scalar and it just worked. That's **broadcasting**: NumPy's rules for making arrays of *different* shapes work together by stretching the smaller one across the larger, without you writing a loop or copying data.

The contrast that defines it — you've seen both ends:
- `prices_arr * 2` → worked (scalar broadcast across the array)
- `prices_arr * np.array([2, 3])` → `ValueError: could not be broadcast together with shapes (3,) (2,)` → **failed**

So some shape mismatches broadcast and some don't. Today you learn the rule that separates them.

**The rule (simplified for what you need this week):** two shapes are compatible when, comparing them dimension by dimension, each pair is either **equal** or **one of them is 1**. A scalar (or a size-1 dimension) gets stretched to match. `(3,)` vs `()` → the scalar stretches → fine. `(3,)` vs `(2,)` → 3≠2 and neither is 1 → refused.

Let me make the useful case concrete before you predict — the one you'll actually use: subtracting a per-column mean from a table (mean-centering, the first step of covariance).

Rebuild the fixture at `>>>`:

```
data = np.array([[0.01, 0.02],
                 [0.03, 0.04],
                 [0.05, 0.06]])
col_means = data.mean(axis=0)
```

`data` is shape `(3, 2)`. `col_means` — predict its shape first, from yesterday's axis rule: `mean(axis=0)` kills which dimension, leaving what length?

Then the broadcast: `data - col_means` subtracts a `(3, 2)` table and a `(2,)` row. Predict:

1. `col_means.shape` → ? (axis-0 kills the rows → length ?)
2. Does `data - col_means` broadcast or error? Reason with the rule — line up `(3, 2)` against `(2,)`: compare the *last* dimensions first (2 vs 2), then what happens to the leftover 3? (The row of 2 means gets stretched down across all 3 rows — is that allowed?)

Run at `>>>`:

```
col_means.shape
data - col_means
```

Both predictions with reasoning, then output. This is the pattern the covariance work is built on, so let's get it on record.
-------------------------------------------------------------------------------------------------------

# EXPLANATION

# Predictions:


input at >>> is:

data = np.array([[0.01, 0.02],
                 [0.03, 0.04],
                 [0.05, 0.06]])
col_means = data.mean(axis=0)




```python
col_means = data.mean(axis=0)
```

Yesterday’s rule says **the named axis disappears**. `data` has shape:

```python
(3, 2)
```

and `axis=0` collapses the `3` rows, leaving one mean per column:

```python
col_means = array([0.03, 0.04])     (since >>> data.mean(axis=0) gives aarray([0.03, 0.04]) from yesterday)
```

So:

```python
>>> col_means.shape
(2,)
```

For:

```python
data - col_means
```

# I predict it **broadcasts successfully**.

The shapes are:

```text
data:       (3, 2)
col_means:     (2,)
```

NumPy lines them up from the right:

```text
(3, 2)
(   2)
     ↑
   2 = 2 ✓
```

The `(2,)` array is treated like one row of two values and stretched down across all three rows:

```text
data                     subtract       col_means
0.01   0.02                             0.03   0.04
0.03   0.04              −              0.03   0.04
0.05   0.06                             0.03   0.04
```

So row by row:

```text
0.01 - 0.03 = -0.02     0.02 - 0.04 = -0.02
0.03 - 0.03 =  0.00     0.04 - 0.04 =  0.00
0.05 - 0.03 =  0.02     0.06 - 0.04 =  0.02
```

Expected output:

```python
>>> col_means.shape
(2,)

>>> data - col_means
array([[-0.02, -0.02],
       [ 0.  ,  0.  ],
       [ 0.02,  0.02]])
```

# So the key idea is:

> **The two column means are broadcast down the three rows, so each asset column has its own mean subtracted from every day.**
-----------------------------------------------------------------------------------------------------------

Both exactly right, and this is a genuinely important pattern — let me make sure the why is locked, not just the output.

col_means.shape → (2,): axis-0 killed the rows (the 3), leaving one mean per asset, length 2. ✓

data - col_means broadcast successfully because of the rule: line up (3, 2) against (2,), compare from the right:

last dims: 2 vs 2 → equal ✓
data has a leftover dimension on the left (the 3); col_means has nothing there, which NumPy treats as "stretch me" → the row of two means gets copied down across all 3 rows

So each row of data had the same per-asset means subtracted. Read your result as mean-centering: asset A's mean is 0.03, so the column [0.01, 0.03, 0.05] became [-0.02, 0.00, 0.02] — deviations from the mean. Every column now centered on zero. That's exactly the first step of computing a covariance matrix, and you did it with one -, no loop, the (2,) means broadcast across the (3,2) table.
-----------------------------------------------------------------------------------------------------------
# Bank the mechanic: broadcasting compares shapes right-to-left; a dimension of 1 (or a missing dimension) stretches to match. That single sentence covers the scalar case (* 2), this mean-centering case, and the failures.

Now — one quick prediction to prove you can call broadcast success vs failure before running, since Day 29's quiz is exactly this. Don't run yet, just reason:

For each pair, say broadcasts or ValueError, using the right-to-left rule:

(3, 2) and (2,) — [you just did this one, state the verdict]
(3, 2) and (3,) — line them up right-to-left: 2 vs 3. Verdict?
(3, 2) and (3, 1) — 2 vs 1, then 3 vs 3. Verdict?

Give me all three verdicts with one-line reasoning each. Then we run one to confirm and move to the matrix piece.
-----------------------------------------------------------------------------------------------------------
# ANSWER

1. **`(3, 2)` and `(2,)` → broadcasts**

Right-to-left:

```text
2 vs 2 → equal ✓
```

The `(2,)` row stretches across the 3 rows.

2. **`(3, 2)` and `(3,)` → `ValueError`**

Right-to-left:

```text
2 vs 3 → not equal, and neither is 1 ✗
```

So NumPy cannot broadcast them together.

3. **`(3, 2)` and `(3, 1)` → broadcasts**

Right-to-left:

```text
2 vs 1 → 1 can stretch to 2 ✓
3 vs 3 → equal ✓
```

So `(3,1)` stretches across the 2 columns.

The compact rule:

> **Compare shapes from the right. Each pair of dimensions must either match or have a `1` on one side.**
---------------------------------------------------------------------------------------------------------

# EVAL

All three correct, and the reasoning is exactly the rule:

1. (3, 2) vs (2,) → broadcasts (2=2, the 3 stretches). ✓
2. (3, 2) vs (3,) → ValueError — right-to-left, 2 vs 3, neither equal nor 1. ✓ This is the classic beginner trap: you have 3 rows and a length-3 array and feel like they should align, but broadcasting compares from the right, so the 3 lands against the 2 (columns) and fails. If you actually wanted to subtract a per-row value, you'd need shape (3, 1) — which is exactly case 3.
3. (3, 2) vs (3, 1) → broadcasts — 2 vs 1 (the 1 stretches across columns), 3 vs 3 (equal). ✓

That case-2-vs-case-3 distinction — (3,) fails but (3, 1) works — is the broadcasting gotcha, and you called both correctly cold. That's the Day 29 quiz question in your pocket.

Quick confirm of case 2, then we move — run the failure so you see the exact error text once more:

data - np.array([1, 2, 3])

Read the shapes it names in the ValueError. Then tell me: does the message report (3,2) and (3,), matching your prediction?


>>> data - np.array([1, 2, 3])
Traceback (most recent call last):
  File "<python-input-21>", line 1, in <module>
    data - np.array([1, 2, 3])
    ~~~~~^~~~~~~~~~~~~~~~~~~~~
ValueError: operands could not be broadcast together with shapes (3,2) (3,) 
>>> 
-----------------------------------------------------------------------------------------------------------
# Now the second half of Day 26 — the start of linear algebra, your home turf conceptually. The one thing that's not obvious is which operator does what, because NumPy has a trap here:

Framing: on arrays, * is elementwise (you know this cold). But matrix multiplication — the real linear-algebra dot-product operation — is a different operator: @. This catches every mathematician: 
# A * B is not matrix multiplication, A @ B is. Confusing them is a silent bug when the shapes happen to allow both.

Predict, reasoning from your linear algebra:

Take w = np.array([0.6, 0.4]) (portfolio weights) and r = np.array([0.03, 0.05]) (asset returns). The portfolio return is the weighted sum: 0.6×0.03 + 0.4×0.05.

w * r — elementwise. What array comes back? (length 2, not summed yet)
w @ r — the dot product. What single number? (this is w * r then summed)

Run at >>>:

data - np.array([1, 2, 3])
w = np.array([0.6, 0.4])
r = np.array([0.03, 0.05])
w * r
w @ r

Give me the case-2 error confirmation, both * vs @ predictions with numbers, then output.
----------------------------------------------------------------------------------------------------------
# ANSWER

First, the broadcast failure:

```python
data - np.array([1, 2, 3])
```

`data` has shape `(3, 2)` and the new array has shape `(3,)`. NumPy compares from the right:

```text
(3, 2)
(   3)
     ↑
   2 vs 3  ✗
```

They are unequal and neither dimension is `1`, so I predict:

```text
ValueError: operands could not be broadcast together with shapes (3,2) (3,)
```

Now:

```python
w = np.array([0.6, 0.4])
r = np.array([0.03, 0.05])
```

# For `w * r`, `*` means **elementwise multiplication**:

```text
0.6 × 0.03 = 0.018
0.4 × 0.05 = 0.020
```

So:

```python
>>> w * r
array([0.018, 0.02 ])
```

Nothing has been summed yet.

# For `w @ r`, `@` means the **dot product**:

```text
(0.6 × 0.03) + (0.4 × 0.05)
= 0.018 + 0.020
= 0.038
```

So:

```python
>>> w @ r
0.038
```

# Your expected session is therefore roughly:

```python
>>> data - np.array([1, 2, 3])
Traceback (most recent call last):
    ...
ValueError: operands could not be broadcast together with shapes (3,2) (3,)

>>> w = np.array([0.6, 0.4])
>>> r = np.array([0.03, 0.05])

>>> w * r
array([0.018, 0.02 ])

>>> w @ r
0.038
```

# The distinction to lock in is:

> **`*` multiplies matching elements and keeps them separate. `@` performs the linear-algebra product, so for two 1D vectors it multiplies corresponding entries and sums them into one scalar.**
=========================================================================================================
# CORRECTION AND FEEDBACK

Both correct — and the contrast is the whole lesson:

w * r → array([0.018, 0.02]) — elementwise, two separate products, still an array. 0.6×0.03=0.018, 0.4×0.05=0.02. The pieces, uncollapsed.

w @ r → np.float64(0.038...) — the dot product, those same two products summed: 0.018 + 0.02 = 0.038. A single scalar. That 0.038 is the portfolio return — the weighted average of the asset returns.


Same two inputs, one operator returns an array, the other collapses to a number. That's the * vs @ distinction that will bite if you ever reach for * expecting matrix behavior. Rule to bank: * is elementwise (Hadamard), @ is the dot/matrix product. For a mathematician the operation is second nature — it's the NumPy spelling that's the trap.

One thing to notice, no action needed: w @ r printed 0.038000000000000006, not a clean 0.038. That's ordinary floating-point representation — 0.6, 0.4, 0.05 aren't exactly representable in binary, so the arithmetic carries a tiny tail. This is why finance code compares floats with a tolerance, never ==. You'll meet it formally on Day 27 when you verify a covariance matrix is symmetric "up to tolerance" — this is that tolerance's reason for existing. Bank it, move on.

=========================================================================================================
# SUMMARY

Day 26 ledger:

1. broadcasting compares shapes right-to-left; each pair must be equal or one is 1; the 1 (or missing dim) stretches
2. (3,) fails against (3,2) but (3,1) works — the core gotcha
3. mean-centering: data - data.mean(axis=0) broadcasts a (2,) row across a (3,2) table (first step of covariance)
4. * = elementwise, @ = dot/matrix product — the operator trap
5. floats carry representation tails → compare with tolerance, never ==
=========================================================================================================




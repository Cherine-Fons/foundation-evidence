# Cumulative F5 quiz, full week's NumPy (Days 23–28), in your own words. Answer all ten; I'll mark the whole batch at the end. Take them in order, no rush.

**1.** A plain Python list `p = [10, 20, 30]` versus `a = np.array([10, 20, 30])`. What does `p * 2` produce, and what does `a * 2` produce? Name the *mechanism* behind each — why are they different?

**2.** You build `np.array([1, 2, 3.5])` — two ints and a float. What dtype results, and why that one and not the other? State the rule that governs the direction.

**3.** The "named axis disappears" rule. For a `(4, 3)` array (4 days, 3 assets), you call `.mean(axis=0)`. What length is the result, does it give you per-day or per-asset means, and which dimension vanished?

**4.** Broadcasting, right-to-left. For each pair, say **broadcasts** or **ValueError**, one-line reason each:
   (a) `(5, 3)` and `(3,)`
   (b) `(5, 3)` and `(5,)`
   (c) `(5, 3)` and `(5, 1)`

**5.** `*` versus `@` on two arrays. What does each compute? Given `w = [0.6, 0.4]` and `r = [0.02, 0.05]`, which one gives you the portfolio return as a single number, and what's the other one give you?

**6. (mandatory — shape-mismatch debugging.)** You run some array math and get:
```
ValueError: operands could not be broadcast together with shapes (6,) (5,)
```
Walk me through your debugging: what does this error tell you the problem is, what do you go look at, and what do you *not* waste time on?

**7.** Why is `==` the wrong way to check if two float arrays are equal, and what do you use instead? Tie it to something concrete you saw this week.

**8.** `np.std(returns)` versus `np.std(returns, ddof=1)`. Which is larger, which does finance want for a return series, and what does `ddof=1` change in the calculation?

**9.** You have a symmetric adjacency matrix `M` where `M[i][j]` is the number of edges between vertices `i` and `j`. How do you get the degree of every vertex in one line, and which axis? If `M[0][2] = 2`, how does that show up in vertex 0's degree, and what week-one rule is that?

**10.** Indexing versus slicing. `a = np.array([5, 6, 7, 8])`. What *type* comes back from `a[0]` versus `a[1:3]` — scalar or array for each? And separately: `a[a > 6]` — what does this return and what's it called?

Answer all ten in your own words. Fire away.
==================================================================================================================

1. ```python
p = [10, 20, 30]
p * 2
```

produces:

```python
[10, 20, 30, 10, 20, 30]
```

because Python lists use `*` as **sequence repetition**. It repeats the whole list twice; it does not multiply the numbers inside it.

But:

```python
a = np.array([10, 20, 30])
a * 2
```

produces:

```python
array([20, 40, 60])
```

because NumPy arrays use `*` as **elementwise multiplication**. The scalar `2` is broadcast across the array, and each element is multiplied by it:

```text
10 × 2 = 20
20 × 2 = 40
30 × 2 = 60
```

So the mechanism is:

> **Python list `*` = repetition of the container.**
> **NumPy array `*` = vectorized elementwise arithmetic, with the scalar broadcast to every element.**


2. `np.array([1, 2, 3.5])` will use a **floating-point dtype**, typically:

```python
dtype('float64')
```

and the array will look like:

```python
array([1. , 2. , 3.5])
```

Why float wins: NumPy requires one common dtype for the whole array. Converting the integers `1` and `2` to floats preserves their values exactly, but converting `3.5` to an integer would lose the `.5`.

So the rule is:

> **NumPy promotes values toward a common type that can represent all of them without losing information.**

For this case:

```text
int + float → float
```

because float is the safer, more expressive type here.

3. For a shape:

```python
(4, 3)
```

you have **4 days (rows)** and **3 assets (columns)**.

Calling:

```python
.mean(axis=0)
```

means **axis 0 disappears** — the `4` row/day dimension is collapsed.

So the result has length:

```python
3
```

and gives you **one mean per asset**, averaged across the 4 days.

In short:

> `(4, 3)` with `axis=0` → kill the `4`, keep the `3` → **3 per-asset means**.


4. (a) **`(5, 3)` and `(3,)` → broadcasts.**
Right-to-left: `3` vs `3` matches, so the `(3,)` row stretches across all 5 rows.

(b) **`(5, 3)` and `(5,)` → `ValueError`.**
Right-to-left: `3` vs `5` do not match, and neither is `1`, so broadcasting fails.

(c) **`(5, 3)` and `(5, 1)` → broadcasts.**
Right-to-left: `3` vs `1` works because `1` can stretch to `3`; then `5` vs `5` matches.

Rule:

> **Compare shapes from right to left: each dimension pair must either be equal or one of them must be `1`.**

5. `*` does **elementwise multiplication**:

```python
w * r
```

with:

```python
w = np.array([0.6, 0.4])
r = np.array([0.02, 0.05])
```

gives:

```python
array([0.012, 0.020])
```

because:

```text
0.6 × 0.02 = 0.012
0.4 × 0.05 = 0.020
```

`@` does the **dot product** for these two 1D arrays:

```python
w @ r
```

which computes:

```text
(0.6 × 0.02) + (0.4 × 0.05)
= 0.012 + 0.020
= 0.032
```

So:

```python
w @ r
# 0.032
```

**`@` gives the portfolio return as one scalar** because portfolio return is the weighted sum of the asset returns.

> **`*` → multiply each pair, keep the results separate.**
> **`@` → multiply the pairs and sum them into the dot product.**


6. That error tells me the problem is **shape compatibility**, not the arithmetic itself:

```text
ValueError: operands could not be broadcast together with shapes (6,) (5,)
```

I read it as: “I am trying to combine a length-6 array with a length-5 array, and NumPy has no valid broadcasting rule for that.”

Right-to-left, the only dimensions are:

```text
6 vs 5
```

They are not equal, and neither is `1`, so broadcasting fails.

My debugging process would be:

```python
a.shape
b.shape
```

Then I would go back to **where those two arrays were created** and ask why one has 6 elements and the other has 5. Did I slice one differently? Drop a value? Build them from unequal data? Filter one with a boolean mask but not the other? The bug is usually upstream in how the shapes were produced.

For example:

```python
returns.shape   # (6,)
weights.shape   # (5,)
```

immediately tells me those two objects cannot be paired element-by-element.

What I **wouldn't** waste time on first: changing the numerical values, checking `dtype`, reinstalling NumPy, rewriting the multiplication/subtraction formula, or staring at individual numbers. NumPy has already told me the immediate failure: **the dimensions don't line up**.

So the rule I’d write in my notes is:

> **When I get a broadcasting `ValueError`, I inspect `.shape` first, then trace backward to find why the arrays ended up with incompatible dimensions. I debug the structure before the values.**

7. `==` is the wrong tool for float arrays because it demands **exact bit-for-bit equality** at every position. Floating-point arithmetic can introduce tiny rounding differences, so two values that are mathematically the same can end up as things like:

```python
0.038
0.038000000000000006
```

and `==` may treat them as different.

This week we saw the same issue in the covariance-matrix work: even when `Sigma` is mathematically symmetric, relying on exact float equality is brittle. The robust check is:

```python
np.allclose(Sigma, Sigma.T)
```

`np.allclose` asks whether corresponding entries are equal **within a small numerical tolerance**, and it gives one overall `True`/`False` verdict.

So the rule is:

> **For float arrays, use tolerance-aware comparison such as `np.allclose`, not exact `==`, because floating-point calculations can differ in the last few bits even when the mathematics says the values are equal.**

8. `np.std(returns, ddof=1)` is **larger** than plain `np.std(returns)`.

Why:

```python
np.std(returns)          # ddof=0 → divides variance by N
np.std(returns, ddof=1)  # divides variance by N - 1
```

With `ddof=1`, the denominator is smaller, so the estimated variance—and therefore the standard deviation—is slightly larger.

For the return-series work we did, we use:

```python
np.std(returns, ddof=1)
```

because we are treating the observed returns as a **sample** and want the **sample standard deviation**.

So in my own words:

> **`ddof=1` changes the variance denominator from (N) to (N-1). That makes the standard deviation slightly larger and gives me the sample standard deviation, which is the version I use for my return series.**

9. You get all vertex degrees in one line with:

```python
M.sum(axis=1)
```

I use **`axis=1`** because I want to collapse the **columns across each row**, leaving one sum per row/vertex.

If:

```python
M[0][2] = 2
```

that means there are **two parallel edges** between vertices `0` and `2`, so that entry contributes **2** to vertex `0`’s row sum, not 1.

That is exactly the week-one multigraph rule:

> **Multiplicity counts in the degree, so add the edge multiplicity, not just +1.**

Matrix version:

```text
row sum
= total number of incident edge copies
= degree
```

So `M[0][2] = 2` is the adjacency-matrix form of `+ e.multiplicity`.

10. 

For:

```python
a = np.array([5, 6, 7, 8])
```

`a[0]` is **single indexing**, so it selects one element and returns a **NumPy scalar**:

```python
a[0]
# np.int64(5)   # exact integer dtype may depend on platform
```

`a[1:3]` is **slicing**, so it selects a range of elements and returns a **NumPy array**:

```python
a[1:3]
# array([6, 7])
```

Remember the slice is start-inclusive and stop-exclusive: indices `1` and `2` survive; index `3` does not.

Separately:

```python
a[a > 6]
```

first creates the boolean mask:

```python
a > 6
# array([False, False, True, True])
```

and then uses that mask to keep only the `True` positions:

```python
a[a > 6]
# array([7, 8])
```

This is called **boolean indexing** or **boolean masking**.

So the distinction is:

> **Single index → scalar. Slice → array. Boolean mask → filtered array containing only values where the mask is `True`.**

=============================================================================================================
# KEY

**10/10 — clean sweep.** Every answer correct, and several went beyond the minimum. On a cumulative week-spanning quiz, the morning after six dense cards, that's the real evidence the material consolidated — not just recognized, but reconstructed in your own words.

Quick confirmation down the line:

1. ✓ Sequence-repetition vs elementwise, scalar broadcast named. Exact.
2. ✓ float64, upcast toward information-preserving type, `int + float → float`. Exact.
3. ✓ Kill the 4, keep the 3, per-asset across days. Exact.
4. ✓✓✓ (a) broadcasts, (b) ValueError, (c) broadcasts — all three with correct right-to-left reasoning, including the `(5,)`-fails-but-`(5,1)`-works gotcha. That's the one most people get backwards.
5. ✓ `*` → `[0.012, 0.020]`, `@` → `0.032` scalar portfolio return. Arithmetic correct.
6. ✓ **Mandatory, and your strongest answer.** You nailed the whole debugging discipline: read it as a *structure* problem not a value problem, inspect `.shape` first, trace *backward* to where the arrays were built ("did I slice one differently, drop a value, mask one but not the other"), and explicitly listed what *not* to touch (values, dtype, reinstalling, rewriting the formula). That "debug the structure before the values" instinct is exactly what the card was built to install, and it'll save you real hours in CPF.
7. ✓ Bit-for-bit vs tolerance, `np.allclose`, tied to the symmetry check. Correct.
8. ✓ `ddof=1` larger, sample std, N−1 vs N, correct for returns. Exact.
9. ✓ `M.sum(axis=1)`, multiplicity carried in the entry = week-one `+ e.multiplicity`. You closed the loop back to your very first warm-up this session — that's the transfer working.
10. ✓ Index → scalar, slice → array, half-open, `a[a > 6]` → boolean masking. Exact, and you even flagged the int64/platform nuance.

No corrections to log — the quiz file stands as-is. Commit it:

```
git add quiz_day23_28.md
git commit -m "f5d6: cumulative F5 quiz, days 23-28, 10/10"
```

Confirm `1 file changed`.

**That closes F5's teaching and retention.** Six lessons + a perfect cumulative quiz. Where F5 stands now:

- **Lessons (Days 23–28):** ✓ complete
- **Cumulative quiz:** ✓ 10/10
- **Still open in F5:** the *exit standard* (a light cold-check — vectorize a loop cold, predict three broadcast shapes, boolean-mask unaided, ≥24 commits — done as you roll into F6, not a big event), and the **CPF diagnostic block** (≤2–3h, separate `cpf-ramp-up-2026` repo, whenever it fits this week).

After those, **F6** opens: Matplotlib (figures/axes), black + ruff, and the test suite grows. Different texture from F5 — less new-paradigm, more tooling-and-polish.


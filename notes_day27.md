# Day 27 — the linear-algebra card (f5d5): a covariance matrix, verifying it's symmetric and PSD, and portfolio variance `wᵀΣw`. This is where today's whole stack — broadcasting, `@`, axis, float tolerance — gets put to work. Your home turf on the math; the patience goes on the NumPy spelling.

Environment: `>>>`, numpy imported. Relaunch with `python` (not `python3`) if you restarted, then `import numpy as np`. All at `>>>`.
============================================================
**Framing.** A covariance matrix has two defining properties you know cold: it's **symmetric**, and it's **positive semi-definite (PSD)**. Today we manufacture one, then *verify* both properties in NumPy — and the verification is where the float-tolerance idea from yesterday earns its keep.
============================================================

# First, new API — a reproducible random matrix. Two lines to introduce (this is new syntax, so I'm handing you the calls; type them at `>>>`):

```
rng = np.random.default_rng(0)
A = rng.standard_normal((3, 3))
```

- `default_rng(0)` builds a random-number generator seeded with 0 — the seed makes it **reproducible** (same seed → same numbers, the reproducibility habit from `requirements.txt`, now for randomness).
- `standard_normal((3, 3))` draws a 3×3 array of standard-normal values (mean 0, can be negative).

Run those two, then type `A` bare to see your matrix.
===========================================================
# RUNNING IN >>>

>>> exit()
(.venv) cherinefons@Mac foundation % python3
Python 3.14.6 (v3.14.6:c63aec69bd5, Jun 10 2026, 08:07:54) [Clang 21.0.0 (clang-2100.1.1.101)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import numpy as np
>>> rng = np.random.default_rng(0)
>>> A = rng.standard_normal((3, 3))
>>> 
>>> A
array([[ 0.12573022, -0.13210486,  0.64042265],
       [ 0.10490012, -0.53566937,  0.36159505],
       [ 1.30400005,  0.94708096, -0.70373524]])
>>> 
=============================================================
# NEXT 

Now the construction — and this part is *yours*, not mine to hand you. From your linear algebra:

You have a random, almost-certainly-*non*-symmetric `A`. You need a matrix `Sigma` that is **guaranteed** symmetric and PSD. There's a one-line construction from `A` that gives you both for free. 

1. What matrix do you form? (Name it in matrix notation first — what combination of `A` and its transpose?)
2. Spell it in NumPy using `.T` (transpose) and `@` (matmul). Write the line yourself.
3. Predict: what **shape** is `Sigma`, and give me the one-line reason it's symmetric.

Write your `Sigma = ...` line, run it, and give me the shape + symmetry reasoning. Don't verify anything yet — just build it and predict. Verification is the next piece.
=============================================================
# RESPONSE

Use the standard Gram-matrix construction:

[
\Sigma = A A^\top
]

In NumPy:

```python
Sigma = A @ A.T
```

That is the line I would write.

Since `A` has shape:

```python
(3, 3)
```

and `A.T` also has shape:

```python
(3, 3)
```

the matrix product has shape:

```python
Sigma.shape
# (3, 3)
```

# Why is it symmetric? Because:

(AA^⊤)^⊤ = (A^⊤)^⊤A^⊤ = AA^⊤

so transposing `Sigma` gives `Sigma` back.

# So the prediction is:

```python
Sigma = A @ A.T
Sigma.shape
# (3, 3)
```

# and the one-line symmetry reason is:

> **`Sigma = A @ A.T` is symmetric because transposing `A Aᵀ` gives `A Aᵀ` again.**

# It is also PSD because for any vector (x),

x^⊤Σx = x^⊤AA^⊤x = ∥A^⊤x∥^2 ≥ 0,

which is the property you’ll verify next.
=============================================================
# PROOF

For $\Sigma = AA^\top$, the property we want is **positive semidefiniteness**.

A symmetric matrix $\Sigma$ is positive semidefinite (PSD) if, for every vector $x$,

$$
x^\top \Sigma x \ge 0.
$$

Now substitute $\Sigma = AA^\top$:

$$
x^\top \Sigma x = x^\top AA^\top x.
$$

Regroup the multiplication:

$$
x^\top AA^\top x
=
(A^\top x)^\top(A^\top x).
$$

Let

$$
y = A^\top x.
$$

Then the expression becomes

$$
y^\top y.
$$

But $y^\top y$ is simply the dot product of a vector with itself:

$$
y^\top y
=
y_1^2 + y_2^2 + \cdots + y_n^2
=
\|y\|^2.
$$

Every squared real number is nonnegative, so

$$
\|y\|^2 \ge 0.
$$

Therefore,

$$
\boxed{
x^\top AA^\top x \ge 0
\quad \text{for every } x
}
$$

and hence

$$
\boxed{
AA^\top \text{ is positive semidefinite.}
}
$$

=============================================================

# That's the construction — `Sigma = A @ A.T`, shape `(3, 3)`. ✓ And you know both properties come for free, but let me make you *say* them because verifying them is the whole card:

**Why symmetric:** `Sigma.T = (A @ A.T).T = (A.T).T @ A.T = A @ A.T = Sigma`. Transpose of a product reverses order and transposes each factor, and it lands back on itself. So `AAᵀ` is symmetric by construction. ✓

**Why PSD:** for any vector `x`, `xᵀ(AAᵀ)x = (Aᵀx)ᵀ(Aᵀx) = ‖Aᵀx‖² ≥ 0`. A squared norm can't be negative, so `Sigma` is PSD. ✓ (You'll verify this numerically via eigenvalues in a moment.)
=============================================================
Now the NumPy half — *verifying* what you just proved, which is where the float tail from yesterday bites.

**Symmetry check.** Predict before running. You want to confirm `Sigma == Sigma.T`. Two predictions:

1. `Sigma == Sigma.T` — what does this return? Not `True`/`False` — think about what `==` does on two arrays (it's a comparison, like `> 0` was). What shape and dtype comes back?
2. Here's the trap: even though `Sigma` is *mathematically* symmetric, will **every** entry of `Sigma == Sigma.T` be `True`? Reason from yesterday's `0.038000000000000006`: the off-diagonal pairs are computed by *different* sums of products — do two different floating-point computations of the "same" value always land on the identical bit pattern?

Run at `>>>`:

```
Sigma == Sigma.T
```

Both predictions, then output. This sets up *why* we need `np.allclose` instead of `==` — the punchline of the card.
=================================================================================================================

>>> exit()
(.venv) cherinefons@Mac foundation % python3
Python 3.14.6 (v3.14.6:c63aec69bd5, Jun 10 2026, 08:07:54) [Clang 21.0.0 (clang-2100.1.1.101)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import numpy as np
>>> rng = np.random.default_rng(0)
>>> A = rng.standard_normal((3, 3))
>>> 
>>> A
array([[ 0.12573022, -0.13210486,  0.64042265],
       [ 0.10490012, -0.53566937,  0.36159505],
       [ 1.30400005,  0.94708096, -0.70373524]])
>>> Sigma = A @ A.T
>>> Sigma.shape
(3, 3)
>>> Sigma == Sigma.T
array([[ True,  True,  True],
       [ True,  True,  True],
       [ True,  True,  True]])
>>> 
=================================================================================================================

# MORE DETAILS

For the first prediction:

```python
Sigma == Sigma.T
```

does **not** return one Boolean. NumPy compares the matrices entry-by-entry, so it returns a **3×3 Boolean array**:

```python
shape: (3, 3)
dtype: bool
```

Conceptually, each entry asks:

```text
Is Sigma[i,j] exactly equal to Sigma.T[i,j]?
```

which is the same as asking whether `Sigma[i,j]` exactly equals `Sigma[j,i]`.

For your particular construction,

```python
Sigma = A @ A.T
```

I would actually predict **all `True`** for this run:

```python
array([[ True,  True,  True],
       [ True,  True,  True],
       [ True,  True,  True]])
```

There is an important nuance here. Floating-point arithmetic absolutely can make mathematically equal quantities differ by tiny amounts, which is why `np.allclose()` is the right general tool for checking numerical symmetry. But `A @ A.T` commonly comes out exactly symmetric entry-for-entry in NumPy, so this particular example may not produce the hoped-for `False` entries.

So I’d expect:

```python
>>> Sigma == Sigma.T
array([[ True,  True,  True],
       [ True,  True,  True],
       [ True,  True,  True]])
```

# The lesson you still want to keep is:

> **`==` asks for exact floating-point equality element by element; `np.allclose()` asks whether the matrices are equal within a small numerical tolerance.**

So for robust numerical code, the symmetry check should be:

```python
np.allclose(Sigma, Sigma.T)
```

which returns one Boolean:

```python
True
```
==================================================
# VERIFICATION

>>> Sigma = A @ A.T
>>> Sigma.shape
(3, 3)
>>> Sigma == Sigma.T
array([[ True,  True,  True],
       [ True,  True,  True],
       [ True,  True,  True]])
>>> np.allclose(Sigma, Sigma.T)
True
>>> 
==================================================
# IMPORTANT ANALYSIS

Interesting result — and it's worth pausing on, because it came out *cleaner* than the setup predicted, and understanding why is the real lesson.

`Sigma == Sigma.T` returned **all `True`** here. Your prediction of the shape/dtype was right — it's a `(3,3)` boolean array, `==` vectorized elementwise just like `> 0`. But the trap I set up (expecting some `False` from float tails) **didn't fire this time**. Why?

Because of *how* `Sigma.T` is computed. Transpose doesn't recompute anything — it just re-indexes the same underlying numbers, so `Sigma.T[i,j]` is the literal same float object as `Sigma[j,i]`. The off-diagonal pairs in `A @ A.T` happened to be computed once and mirrored, so `==` finds identical bit patterns. So `==` *can* pass here.

But — and this is the point — **you cannot rely on that.** Change the construction slightly (e.g. `(A + A.T)/2`, or accumulate the matrix a different way) and the two sides get computed by genuinely different float operations, and `==` starts returning stray `False`s on entries that are equal to fourteen decimal places. The rule survives regardless: **never test float equality with `==`; test with tolerance.** Which is exactly what you did on the next line —

`np.allclose(Sigma, Sigma.T)` → `True`. That's the correct, robust check: "are these two arrays equal *within a small tolerance*?" It returns a single `True`/`False` for the whole array, and it's immune to float tails whether or not they happen to appear. `allclose` is the tool; `==` on floats is the bug waiting to happen.

Bank the pair: `==` on floats gives you an elementwise boolean array and lies at the last decimal; `np.allclose` gives you one tolerance-aware verdict and is what finance/numerical code actually uses.

Now the **PSD verification** — the second property, checked numerically. Framing: a symmetric matrix is PSD iff all its **eigenvalues are ≥ 0**. NumPy computes eigenvalues of a symmetric matrix with `np.linalg.eigvalsh` (the `h` = Hermitian/symmetric, the right tool for `Sigma`).
======================================================================================
Predict before running:

1. `np.linalg.eigvalsh(Sigma)` returns what — a scalar, a vector, or a matrix? What length? (Think: how many eigenvalues does a 3×3 matrix have?)
2. What sign should they all be, and why — and here's the tolerance wrinkle: PSD allows eigenvalue `= 0`, and float error can push a true-zero eigenvalue to something like `-1e-16`. So when you *check* "all ≥ 0," should you test `>= 0` strictly, or `>= -tiny_tolerance`? Reason it out.

Run at `>>>`:

```
eigenvalues = np.linalg.eigvalsh(Sigma)
eigenvalues
```

Both predictions with reasoning, then output. After this we do portfolio variance and commit.
======================================================================================


1. `np.linalg.eigvalsh(Sigma)` returns a **1D vector of eigenvalues**. Since `Sigma` is (3\times 3), it has **3 eigenvalues**, so the result has shape:

```python
(3,)
```

With your seeded matrix, I expect something approximately like:

```python
array([0.10865198, 0.5463923 , 3.30967512])
```

2. They should all be **nonnegative** because

[
\Sigma = AA^\top
]

is PSD, and a symmetric matrix is PSD exactly when all of its eigenvalues are (\ge 0).

For the numerical check, though, I would **not** use a strict:

```python
eigenvalues >= 0
```

as the general rule. If the mathematics says an eigenvalue is exactly (0), floating-point arithmetic might return something tiny like:

```text
-1e-16
```

That is numerical noise, not evidence that the matrix is genuinely non-PSD.

So the robust check is something like:

```python
eigenvalues >= -1e-12
```

or:

```python
np.all(eigenvalues >= -1e-12)
```

# The logic is:

> **Mathematically PSD means eigenvalues (\ge 0); numerically, allow a tiny negative tolerance so floating-point noise near zero does not create a false failure.**

For this particular seeded example, all three eigenvalues are comfortably positive anyway, so even a strict check would pass.
==============================================================================
# NOTE

-1e-12 is just scientific notation for a very tiny negative number:

-1e-12 = -0.000000000001

The e means “times ten to a power”.

So when we write:

eigenvalues >= -1e-12

we are saying:

“Treat anything larger than about negative one-trillionth as effectively zero.”
==================================================================================

>>> eigenvalues = np.linalg.eigvalsh(Sigma)
>>> eigenvalues
array([0.10865198, 0.5463923 , 3.30967512])
>>> 

==================================================================================
# MISSED PART

Output's there, but you skipped the predictions again — and the reasoning is the part that matters more than the numbers here, so let me pull it back out of you rather than just confirming.

What the output shows: three eigenvalues, `[0.109, 0.546, 3.310]` — a **vector of length 3** (a 3×3 matrix has 3 eigenvalues), and all three **strictly positive**. So `Sigma` isn't just PSD, it's positive *definite* (all eigenvalues > 0, not just ≥ 0) — which makes sense: `A @ A.T` is PD whenever `A` is full-rank, and a random 3×3 almost always is. Your PSD proof from earlier is confirmed numerically.

But answer the reasoning question I set, because it's a Day-29-quiz-grade idea and I want it in your words, not skipped:

# **When you write the actual PSD *check* in code — "are all eigenvalues ≥ 0?" — do you test `eigenvalues >= 0` strictly, or `eigenvalues >= -tiny_tolerance`? And why?** Think about a matrix that's PSD-but-not-PD (a true-zero eigenvalue): float error can compute that exact zero as `-1e-16`. What does a strict `>= 0` do to that case, and is that the right answer or a false alarm?

Give me that reasoning in a sentence or two — it's the same "never trust the last bit" lesson as `allclose`, applied to the sign test.
=================================================================================

# ANSWER

For the PSD check, I would use a tiny tolerance rather than strict zero:

```python
np.all(eigenvalues >= -1e-12)
```

The reason is that a matrix can be mathematically PSD with a true eigenvalue of exactly `0`, but floating-point arithmetic might compute that as something tiny like `-1e-16`. A strict `>= 0` would incorrectly flag the matrix as non-PSD. Allowing a very small negative tolerance avoids that false alarm.


================================================================

# LAST PART

Then let's land the payoff of the card — portfolio variance, wᵀΣw, the formula this whole matrix exists to serve. **Framing: given weights w and covariance Sigma, the portfolio variance is the scalar w @ Sigma @ w. (For a 1-D w, w.T and w are identical to NumPy, so you can write it either way — w @ Sigma @ w reads cleanest.)**

# Predict before running:

w = np.array([0.5, 0.3, 0.2])
w @ Sigma @ w 


— what kind of result: array or scalar? Reason from the chain of shapes: (3,) @ (3,3) gives what shape, then @ (3,) collapses to what?
Should the result be positive? Tie it to PSD — wᵀΣw for a PSD Sigma and any real w is guaranteed to be what sign?
Run at >>>:

w = np.array([0.5, 0.3, 0.2])
w @ Sigma @ w


Give me the eigenvalue-tolerance reasoning, both portfolio-variance predictions, then the output.


=============================================================================================
# FINAL RESPONSES


For the portfolio variance:

```python
w = np.array([0.5, 0.3, 0.2])
w @ Sigma @ w
```

the result should be a **scalar**. Shape-wise:

```text
(3,) @ (3,3) → (3,)
(3,) @ (3,)  → scalar
```

And it should be **nonnegative** because `Sigma` is PSD, so for every real vector (w),

w^⊤Σw ≥ 0

In this particular case `Sigma` is actually positive definite and `w` is nonzero, so the variance should be strictly positive.

With the seeded `A` you built, the output is:

```python
>>> w @ Sigma @ w
np.float64(0.21042608641555083)
```

Numerically:

```text
portfolio variance ≈ 0.2104261
```

So the two ideas to bank are:

> **PSD check:** tolerate microscopic negative eigenvalues caused by floating-point error.
> **Portfolio variance:** (w^⊤Σw) is a scalar and cannot be negative when (\Sigma) is PSD.
=========================================================================================

# RESULTS SUMMARY

You should get a single positive np.float64(...). The shape logic is exactly as you wrote it: (3,) @ (3,3) produces (3,), then @ (3,) contracts the last matching dimension to a scalar — the two @s chain left to right, and the vector-matrix-vector sandwich always collapses to one number. And it's strictly positive because Sigma is PD and w ≠ 0, so wᵀΣw > 0. That number is the portfolio variance — the single most-used quantity in mean-variance optimization, which is (not coincidentally) the leading candidate for your CPF capstone.

That closes the Day-27 content.

Day 27 ledger:

1. reproducible RNG: np.random.default_rng(seed) → .standard_normal(shape)
2. Sigma = A @ A.T is symmetric (transpose lands on itself) and PSD (xᵀAAᵀx = ‖Aᵀx‖² ≥ 0) by construction
3. symmetry check: np.allclose(Sigma, Sigma.T), never == on floats
4. PSD check: np.linalg.eigvalsh (symmetric-matrix eigenvalues), all ≥ -tiny_tolerance — not strict >= 0
5. portfolio variance: w @ Sigma @ w, vector-matrix-vector → scalar, > 0 for PD Sigma

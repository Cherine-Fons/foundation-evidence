# Mock Exit 1 — Hand-Derived Oracle

## Problem

The fixed crew-assignment instance has workers

\[
W(G)=\{a,b,c,d\}
\]

with shifts

- `s0 = (a,b)`
- `s1 = (a,b)` — parallel copy
- `s2 = (b,c)`
- `s3 = (c,d)`

and skill values

- `skill(a) = 1`
- `skill(b) = 1`
- `skill(c) = 2`
- `skill(d) = 2`

For a crew \(W\):

- `i(W)` is the number of shift copies with both workers in \(W\),
- `∂(W)` is the set of shift copies with exactly one worker in \(W\),
- `skill(W)` is the sum of worker skill values.

A pair `(W, S)` is admissible iff:

1. \(W\) is nonempty and \(W\subseteq WORKERS\),
2. \(S\subseteq\partial(W)\),
3. \(skill(W)+|S|\) is even,
4. \(skill(W)+|S|\ge4\).

For admissible pairs,

\[
value(W,S)
=
\frac{2i(W)+|S|}
     {skill(W)+|S|-2}.
\]

The objective must be interpreted exactly as written: only the internal-shift count is multiplied by 2. The numerator is \(2i(W)+|S|\), not \(2(i(W)+|S|)\).

---

## Candidate maximizer

Consider

\[
W^*=\{a,b,c\}.
\]

The internal shifts are

- `s0 = (a,b)`
- `s1 = (a,b)`
- `s2 = (b,c)`

so

\[
i(W^*)=3.
\]

The only fringe shift is

\[
\partial(W^*)=\{s3\}.
\]

The crew skill is

\[
skill(W^*)=1+1+2=4.
\]

The two possible subsets of the fringe are therefore

\[
S=\varnothing
\]

and

\[
S=\{s3\}.
\]

For \(S=\varnothing\),

\[
skill(W^*)+|S|=4,
\]

which is even and at least 4, so the pair is admissible.

Its value is

\[
value(W^*,\varnothing)
=
\frac{2(3)+0}{4+0-2}
=
\frac{6}{2}
=
3.
\]

For \(S=\{s3\}\),

\[
skill(W^*)+|S|=5,
\]

which is odd, so that pair is inadmissible.

Thus the only admissible pair for this crew has value 3.

---

## Competitor audit

For a fixed crew \(W\), the objective depends on a selected fringe set \(S\) only through its cardinality

\[
x=|S|.
\]

Therefore I can audit each crew by determining:

- `skill(W)`,
- `i(W)`,
- `∂(W)`,
- the possible admissible values of \(x\).

There are \(2^4-1=15\) nonempty worker subsets.

| Crew \(W\) | skill(W) | i(W) | fringe | admissible \(|S|\) | best value |
|---|---:|---:|---|---|---:|
| `{a}` | 1 | 0 | `{s0,s1}` | none | — |
| `{b}` | 1 | 0 | `{s0,s1,s2}` | 3 | \(3/2\) |
| `{c}` | 2 | 0 | `{s2,s3}` | 2 | \(1\) |
| `{d}` | 2 | 0 | `{s3}` | none | — |
| `{a,b}` | 2 | 2 | `{s2}` | none | — |
| `{a,c}` | 3 | 0 | `{s0,s1,s2,s3}` | 1, 3 | \(3/4\) |
| `{a,d}` | 3 | 0 | `{s0,s1,s3}` | 1, 3 | \(3/4\) |
| `{b,c}` | 3 | 1 | `{s0,s1,s3}` | 1, 3 | \(3/2\) |
| `{b,d}` | 3 | 0 | `{s0,s1,s2,s3}` | 1, 3 | \(3/4\) |
| `{c,d}` | 4 | 1 | `{s2}` | 0 | \(1\) |
| `{a,b,c}` | 4 | 3 | `{s3}` | 0 | **\(3\)** |
| `{a,b,d}` | 4 | 2 | `{s2,s3}` | 0, 2 | \(2\) |
| `{a,c,d}` | 5 | 1 | `{s0,s1,s2}` | 1, 3 | \(5/6\) |
| `{b,c,d}` | 5 | 2 | `{s0,s1}` | 1 | \(5/4\) |
| `{a,b,c,d}` | 6 | 4 | `∅` | 0 | \(2\) |

The largest value outside the proposed winner is 2.

For example,

\[
W=\{a,b,d\},\qquad S=\varnothing
\]

has

\[
i(W)=2,\qquad skill(W)=4,
\]

so

\[
value(W,S)
=
\frac{2(2)}{4-2}
=
2.
\]

The whole worker set also has value 2:

\[
\frac{2(4)}{6-2}
=
2.
\]

Neither ties the candidate value 3.

---

## Oracle lock

The hand-derived maximum is therefore

\[
\boxed{3}.
\]

The maximizing pair is uniquely

\[
\boxed{
W^*=\{a,b,c\},
\qquad
S^*=\varnothing.
}
\]

The future brute-force checker must therefore return exactly:

- `value = Fraction(3, 1)`
- `W = frozenset({"a", "b", "c"})`
- `S = frozenset()`

No checker code was used to obtain this oracle.
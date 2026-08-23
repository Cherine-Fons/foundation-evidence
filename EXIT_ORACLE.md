```markdown
# EXIT TEST — Hand-Derived Ledger Optimization Oracle

## Source Data

This oracle is derived only from the good trades produced by Part A.

The five good trades are:

| Trade | Trader | Quantity | Price | Volume |
|---|---|---:|---:|---:|
| `t1` | alice | 10 | 3 | 30 |
| `t2` | bob | 5 | 2 | 10 |
| `t5` | dana | 12 | 1 | 12 |
| `t6` | bob | 7 | 7 | 49 |
| `t8` | carol | 9 | 3 | 27 |

The three malformed rows are excluded from this oracle.

---

## Trader Contributions

For Part C:

\[
vol(T)
\]

is the total `quantity * price` over good trades whose trader belongs to \(T\), and:

\[
count(T)
\]

is the number of good trades whose trader belongs to \(T\).

Thus the trader-level contributions are:

| Trader | Trade count | Volume |
|---|---:|---:|
| alice | 1 | 30 |
| bob | 2 | 59 |
| carol | 1 | 27 |
| dana | 1 | 12 |

---

## Eligibility and Objective

A trader subset \(T\) is eligible iff:

1. \(T\neq\varnothing\);
2. \(count(T)\) is odd;
3. \(vol(T)\ge20\).

For an eligible subset:

\[
score(T)
=
\frac{vol(T)}
{2count(T)-1}.
\]

All scores below are exact rational values.

---

## Complete Audit of All 15 Nonempty Trader Subsets

| # | T | count(T) | vol(T) | Eligible? | Exact score / reason |
|---:|---|---:|---:|---|---|
| 1 | `{alice}` | 1 | 30 | yes | \(30\) |
| 2 | `{bob}` | 2 | 59 | no | count is even |
| 3 | `{carol}` | 1 | 27 | yes | \(27\) |
| 4 | `{dana}` | 1 | 12 | no | volume \(12<20\) |
| 5 | `{alice,bob}` | 3 | 89 | yes | \(89/5\) |
| 6 | `{alice,carol}` | 2 | 57 | no | count is even |
| 7 | `{alice,dana}` | 2 | 42 | no | count is even |
| 8 | `{bob,carol}` | 3 | 86 | yes | \(86/5\) |
| 9 | `{bob,dana}` | 3 | 71 | yes | \(71/5\) |
| 10 | `{carol,dana}` | 2 | 39 | no | count is even |
| 11 | `{alice,bob,carol}` | 4 | 116 | no | count is even |
| 12 | `{alice,bob,dana}` | 4 | 101 | no | count is even |
| 13 | `{alice,carol,dana}` | 3 | 69 | yes | \(69/5\) |
| 14 | `{bob,carol,dana}` | 4 | 98 | no | count is even |
| 15 | `{alice,bob,carol,dana}` | 5 | 128 | yes | \(128/9\) |

There are exactly:

\[
7
\]

eligible subsets.

They are:

\[
\{\text{alice}\},
\]

\[
\{\text{carol}\},
\]

\[
\{\text{alice},\text{bob}\},
\]

\[
\{\text{bob},\text{carol}\},
\]

\[
\{\text{bob},\text{dana}\},
\]

\[
\{\text{alice},\text{carol},\text{dana}\},
\]

and:

\[
\{\text{alice},\text{bob},\text{carol},\text{dana}\}.
\]

Their exact scores are respectively:

\[
30,
\quad
27,
\quad
\frac{89}{5},
\quad
\frac{86}{5},
\quad
\frac{71}{5},
\quad
\frac{69}{5},
\quad
\frac{128}{9}.
\]

---

## Exact Maximization

For the denominator-5 candidates:

\[
30=\frac{150}{5},
\]

and:

\[
150>89,\quad
150>86,\quad
150>71,\quad
150>69.
\]

Therefore:

\[
30>
\frac{89}{5},
\frac{86}{5},
\frac{71}{5},
\frac{69}{5}.
\]

Also:

\[
30>27.
\]

For the denominator-9 candidate:

\[
30=\frac{270}{9},
\]

and:

\[
270>128.
\]

Therefore:

\[
30>\frac{128}{9}.
\]

Hence the unique maximizing trader subset is:

\[
\boxed{
T^*=\{\text{alice}\}
}
\]

with exact score:

\[
\boxed{
score(T^*)=30
}
\]

---

## Tie Rule for the Future Search

Trader enumeration will be deterministic, beginning from:

```text
["alice", "bob", "carol", "dana"]
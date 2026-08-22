# Mock Exit 1 — Build Notes

## Purpose

This mock is a guided build of an exact brute-force checker for the Crew-Assignment Density problem.

The workflow is deliberately:

1. understand the specification,
2. derive the oracle by hand,
3. commit the oracle before checker code exists,
4. design representations and contracts,
5. implement the instance and validation,
6. implement mathematical primitives,
7. implement admissibility,
8. implement exact evaluation,
9. implement exhaustive search,
10. build guard-isolated and known-answer tests,
11. lint, test, and commit.

The important discipline is that the expected mathematical answer exists before the program that will be tested against it.

---

## File Convention

All mock files live flat inside the existing `foundation` repository.

Mock implementation files use names that do not collide with the F7 capstone, for example:

- `mock_instance.py`
- `mock_primitives.py`
- `mock_admissibility.py`
- `mock_evaluator.py`
- `mock_search.py`
- `test_mock.py`

The formal hand-derived oracle is:

- `MOCK_ORACLE.md`

These learning notes are:

- `mock_notes_1.md`

Mock commits use the prefix:

```text
mock1:

=============================================================


The distinction between your two Markdown files is:

```text
mock_notes_1.md
    = EVERYTHING YOU ARE LEARNING
      explanations, comparisons, commands, design decisions,
      reasoning, examples, rules, mistakes, test ideas

MOCK_ORACLE.md
    = ONLY THE FORMAL HAND-DERIVED ANSWER
      the mathematical winner and proof/audit establishing it
```

So the explanation below belongs in **`mock_notes_1.md`**, not the oracle.

---

# Part 1 — What Problem Are We Actually Solving?

The specification dresses the problem up as a staffing system, but mathematically it is another **small multigraph optimization problem**.

That is the first translation you should make.

You are given:

```text
workers  → vertices
shifts   → edges
```

So the workers

```text
a, b, c, d
```

form the vertex set:

[
V={a,b,c,d}.
]

The shifts are:

```text
s0 = (a,b)
s1 = (a,b)
s2 = (b,c)
s3 = (c,d)
```

Each shift connects the two workers who staff it.

So as a graph:

```text
       s0
    ┌───────┐
a ──┤       ├── b ──s2── c ──s3── d
    └───────┘
       s1
```

Or more compactly:

```text
a ══ b ── c ── d
```

The double line between `a` and `b` represents **two distinct edges**.

That makes this a **multigraph**.

---

# Part 2 — Why Are `s0` and `s1` Different if They Connect the Same Workers?

This is extremely important.

We have:

```python
("s0", "a", "b")
("s1", "a", "b")
```

Both connect `a` and `b`, but they represent **two different shifts**.

Think of it operationally as:

```text
s0 = Monday morning shift staffed by a and b
s1 = Tuesday morning shift staffed by a and b
```

The worker pair is identical, but the actual work assignments are different objects.

Mathematically:

[
s0\neq s1.
]

Therefore, if we count shifts internal to a crew containing `a` and `b`, both count:

[
2,
]

not:

[
1.
]

This is exactly analogous to the parallel edges in your capstone toy graph:

```text
e0 = (0,1)
e1 = (0,1)
```

The endpoints do **not** uniquely identify an edge copy.

The **ID** identifies the edge copy.

That is why we will eventually represent each shift as:

```python
(shift_id, worker1, worker2)
```

rather than merely:

```python
(worker1, worker2)
```

If we discarded the IDs, `s0` and `s1` could collapse into one apparent edge, and the mathematics would be wrong.

---

# Part 3 — What Is a Crew `W`?

A crew is simply a **subset of the workers**.

For example:

[
W={a,b}
]

means:

> For this candidate, I am examining the subgroup consisting of workers `a` and `b`.

Another possible crew is:

[
W={b,c,d}.
]

And another is:

[
W={a}.
]

Eventually the exhaustive search will examine **every nonempty subset of workers**.

There are four workers.

A four-element set has:

[
2^4=16
]

subsets total.

One is the empty set.

So there are:

[
2^4-1=15
]

nonempty crews for the search to consider.

This is exactly analogous to your capstone's (U).

There you had:

[
U\subseteq V(G).
]

Here you have:

[
W\subseteq WORKERS.
]

So mentally:

```text
capstone U  ↔  mock W
```

Different letter, same structural role.

---

# Part 4 — What Does `skill(W)` Mean?

Each worker has a positive integer skill value:

```text
a → 1
b → 1
c → 2
d → 2
```

For any crew (W),

[
skill(W)
]

means:

> Add the skill values of all workers belonging to W.

For example, if:

[
W={a,b},
]

then:

[
skill(W)=skill(a)+skill(b)
]

so:

[
skill({a,b})=1+1=2.
]

For:

[
W={a,b,c},
]

we get:

[
skill({a,b,c})=1+1+2=4.
]

For the entire worker set:

[
skill({a,b,c,d})=1+1+2+2=6.
]

This is structurally the same role that (f(U)) played in your capstone.

Capstone:

[
f(U)=\sum_{v\in U}f(v).
]

Mock:

[
skill(W)=\sum_{w\in W}skill(w).
]

So:

```text
capstone f(v)  ↔  mock skill(worker)

capstone f(U)  ↔  mock skill(W)
```

The name has changed, but the basic aggregation operation has not.

---

# Part 5 — What Is an Internal Shift?

Now suppose:

[
W={a,b}.
]

Look at each shift:

```text
s0 = (a,b)
s1 = (a,b)
s2 = (b,c)
s3 = (c,d)
```

A shift is **internal to (W)** when **both endpoints belong to (W)**.

For `s0`:

```text
a ∈ W
b ∈ W
```

Both are inside.

So `s0` is internal.

For `s1`:

```text
a ∈ W
b ∈ W
```

Again both are inside.

So `s1` is internal too.

For `s2 = (b,c)`:

```text
b ∈ W
c ∉ W
```

Only one endpoint is inside.

So `s2` is **not internal**.

For `s3 = (c,d)`:

```text
c ∉ W
d ∉ W
```

Neither endpoint is inside.

So it is not internal.

Therefore:

[
i({a,b})=2.
]

The notation:

[
i(W)
]

simply means:

> number of physical shift copies completely contained inside crew (W).

This corresponds directly to the capstone's:

[
e(U)=|E(G[U])|.
]

So:

```text
capstone e(U)  ↔  mock i(W)
```

Both count internal edge copies.

---

# Part 6 — What Is the Fringe `∂(W)`?

Now we introduce the other kind of edge.

A shift is on the **fringe** of (W) if it has **exactly one endpoint inside (W)**.

This is the same graph-theoretic boundary concept you used in the capstone.

Take again:

[
W={a,b}.
]

We already classified:

```text
s0 = (a,b) → both inside
s1 = (a,b) → both inside
s2 = (b,c) → one inside, one outside
s3 = (c,d) → both outside
```

Therefore:

[
\partial(W)={s2}.
]

Why?

Because `s2` is the only shift that **crosses from the crew to the outside world**:

```text
inside        outside

   b  ──s2──  c
```

This is the same XOR idea you learned earlier.

For any edge `(u,v)`:

```python
(u in W) != (v in W)
```

means:

```text
True != False  → True
False != True  → True

True != True   → False
False != False → False
```

So it is true exactly when one endpoint lies inside and one lies outside.

That is the fringe.

Structurally:

```text
capstone ∂G(U)  ↔  mock ∂(W)
```

They are the same kind of object.

---

# Part 7 — Internal and Fringe Are Not the Same Thing

This distinction is crucial.

For:

[
W={a,b},
]

we have:

```text
internal shifts:
{s0, s1}

fringe shifts:
{s2}
```

They play different roles in the objective.

The internal shifts contribute through:

[
i(W).
]

The selected fringe shifts contribute through a separate object:

[
S.
]

Do not combine them.

A useful picture is:

```text
                  outside W
                      c
                      |
                     s2     ← fringe
                      |
      ┌────────────────────┐
      │        W           │
      │                    │
      │  a ══ b            │
      │   s0,s1            │
      │  internal          │
      └────────────────────┘
```

An internal shift is completely inside the crew.

A fringe shift crosses its boundary.

---

# Part 8 — What Is `S`?

This is probably the most important conceptual distinction in the whole specification.

A **candidate is not just a crew (W)**.

It is a pair:

[
(W,S).
]

Here:

[
W
]

is a set of workers.

But:

[
S
]

is a set of **shift IDs**.

And importantly:

[
S\subseteq\partial(W).
]

So once we choose a crew, we may choose **some subset of its fringe shifts**.

We do **not** have to choose all of them.

Suppose:

[
W={b}.
]

Which shifts touch `b`?

```text
s0 = (a,b)
s1 = (a,b)
s2 = (b,c)
```

Since `b` is inside (W), while `a` and `c` are outside, all three are fringe shifts:

[
\partial({b})={s0,s1,s2}.
]

Then possible (S)'s include:

[
\varnothing,
]

[
{s0},
]

[
{s1},
]

[
{s2},
]

[
{s0,s1},
]

and so on, up through:

[
{s0,s1,s2}.
]

There are:

[
2^3=8
]

possible subsets of a three-element fringe.

The search will eventually consider all of them.

This is directly analogous to your capstone:

```text
capstone candidate: (U,F)
mock candidate:     (W,S)
```

with:

```text
capstone F ⊆ ∂G(U)
mock S ⊆ ∂(W)
```

---

# Part 9 — Why Does `S` Contain IDs Rather Than Endpoint Pairs?

Suppose the fringe contains both parallel shifts:

```text
s0 = (a,b)
s1 = (a,b)
```

If we represented shifts merely by:

```python
("a", "b")
```

then the two physical copies would look identical.

A set would collapse them.

But:

```python
{"s0", "s1"}
```

keeps both physical copies distinct.

That matters because:

[
|S|
]

means the number of selected **actual shifts**.

Selecting `s0` and `s1` means:

[
|S|=2,
]

not (1).

This is exactly the representation invariant you discovered while hardening the capstone.

That is why the mock explicitly requires **unique shift IDs** in instance validation.

---

# Part 10 — What Does “Admissible” Mean?

The search is going to generate lots of possible pairs ((W,S)).

But not every generated pair is allowed to compete.

“Admissible” means:

> This candidate satisfies all of the mathematical eligibility conditions and is therefore allowed into the optimization.

There are four gates.

### Condition 1

[
W\neq\varnothing
]

and:

[
W\subseteq WORKERS.
]

So the crew must contain at least one worker, and every worker named in it must actually exist.

---

### Condition 2

[
S\subseteq\partial(W).
]

You can select only genuine fringe shifts for that crew.

You cannot arbitrarily put an internal shift into (S).

You cannot put an unrelated shift into (S).

---

### Condition 3

[
skill(W)+|S|
]

must be **even**.

For example:

```text
skill(W) = 4
|S| = 0

total = 4
```

Even → passes.

But:

```text
skill(W) = 4
|S| = 1

total = 5
```

Odd → fails.

This is one deliberate reversal from your capstone, where the corresponding total had to be **odd**.

---

### Condition 4

[
skill(W)+|S|\ge4.
]

So evenness alone is not enough.

For example:

[
skill(W)+|S|=2
]

is even, but:

[
2<4.
]

So the candidate still fails.

This is another deliberate change from the capstone, whose threshold was (3).

---

# Part 11 — Why Does Condition 4 Matter to the Formula?

The denominator is:

[
skill(W)+|S|-2.
]

Condition 4 says:

[
skill(W)+|S|\ge4.
]

Subtract (2) from both sides:

[
skill(W)+|S|-2\ge2.
]

Therefore every admissible candidate has denominator at least:

[
2.
]

That guarantees:

```text
no zero denominator
no negative denominator
```

So the evaluator can safely construct an exact rational value once admissibility has already been established.

This is the same architectural idea you used in the capstone:

```text
admissibility establishes eligibility
↓
evaluator trusts admissibility
↓
evaluator performs arithmetic
```

---

# Part 12 — What Is the Objective Actually Measuring?

For an admissible pair:

[
value(W,S)
==========

\frac{2i(W)+|S|}
{skill(W)+|S|-2}.
]

Think of it as a **density ratio**.

The numerator measures the shift-side contribution:

[
2i(W)+|S|.
]

Every internal shift contributes:

[
2.
]

Every selected fringe shift contributes:

[
1.
]

The denominator is:

[
skill(W)+|S|-2.
]

So it grows with:

* the total skill inside the crew;
* the number of selected fringe shifts.

The search is asking:

> Among every admissible crew/fringe-selection pair, which one makes this ratio as large as possible?

I would not read a deeper real-world staffing interpretation into it than the specification provides. This is mainly a graph optimization exercise wearing staffing terminology.

Mathematically, it rewards a crew for containing many internal shift copies relative to the denominator contributed by its worker skills and selected fringe shifts.

---

# Part 13 — The Most Dangerous Formula Difference From the Capstone

Your capstone objective had:

[
2(e(U)+|F|).
]

Expand that:

[
2e(U)+2|F|.
]

So a selected boundary edge effectively contributed **2** to the capstone numerator.

The mock says:

[
2i(W)+|S|.
]

Here a selected fringe shift contributes only **1**.

Compare:

```text
CAPSTONE
2(e(U) + |F|)
=
2e(U) + 2|F|

MOCK
2i(W) + |S|
```

Suppose:

```text
internal count = 3
selected fringe count = 1
```

Capstone-style numerator would be:

[
2(3+1)=8.
]

Mock numerator is:

[
2(3)+1=7.
]

That is a real mathematical difference.

Pattern-replaying the capstone code would silently produce the wrong answer.

---

# Part 14 — Complete Translation Dictionary

Here is the conceptual bridge between the project you just completed and this mock:

| Capstone          | Mock              | Meaning                                 |      |   |   |             |
| ----------------- | ----------------- | --------------------------------------- | ---- | - | - | ----------- |
| vertex (v)        | worker            | basic graph object                      |      |   |   |             |
| edge copy (e)     | shift             | connection between two vertices/workers |      |   |   |             |
| edge ID `e0`      | shift ID `s0`     | identity of a physical parallel copy    |      |   |   |             |
| (U)               | (W)               | chosen vertex/worker subset             |      |   |   |             |
| (f(v))            | `skill(worker)`   | positive integer attached to a vertex   |      |   |   |             |
| (f(U))            | `skill(W)`        | sum over the chosen subset              |      |   |   |             |
| (e(U))            | (i(W))            | number of internal edge/shift copies    |      |   |   |             |
| (\partial_G(U))   | (\partial(W))     | crossing edge/shift copies              |      |   |   |             |
| (F)               | (S)               | selected subset of boundary/fringe IDs  |      |   |   |             |
| `(U,F)`           | `(W,S)`           | candidate pair                          |      |   |   |             |
| odd parity        | even parity       | **changed**                             |      |   |   |             |
| total ≥ 3         | total ≥ 4         | **changed**                             |      |   |   |             |
| denominator `-1`  | denominator `-2`  | **changed**                             |      |   |   |             |
| `2(e+             | F                 | )`                                      | `2i+ | S | ` | **changed** |
| `Fraction`        | `Fraction`        | exact arithmetic remains                |      |   |   |             |
| exhaustive search | exhaustive search | architecture remains                    |      |   |   |             |

This mock is therefore testing something very specific:

> Can you preserve the **software architecture** you learned while changing the **mathematics** wherever the new specification requires it?

That is much more important than memorizing the old implementation.

---

# Part 15 — Let's Work One Crew Completely

Before we touch the full oracle, let's use:

[
W={a,b}.
]

We will compute everything from zero.

### Step A: `skill(W)`

Workers in (W):

```text
a
b
```

Their skills:

```text
a → 1
b → 1
```

Therefore:

[
skill(W)=1+1=2.
]

### Step B: `i(W)`

Check every shift:

```text
s0 = (a,b)
both inside → internal

s1 = (a,b)
both inside → internal

s2 = (b,c)
b inside, c outside → not internal

s3 = (c,d)
both outside → not internal
```

Therefore:

[
i(W)=2.
]

### Step C: `∂(W)`

We want exactly one endpoint inside.

```text
s0:
both inside → not fringe

s1:
both inside → not fringe

s2:
b inside, c outside → fringe

s3:
both outside → not fringe
```

Therefore:

[
\partial(W)={s2}.
]

### Step D: possible `S`

Because:

[
S\subseteq{s2},
]

there are only two possibilities:

[
S=\varnothing
]

and:

[
S={s2}.
]

Now admissibility filters them.

For:

[
S=\varnothing,
]

we have:

[
skill(W)+|S|=2+0=2.
]

Condition 3:

[
2\text{ is even}.
]

Pass.

Condition 4:

[
2\ge4?
]

No.

So:

[
({a,b},\varnothing)
]

is **inadmissible**.

Now take:

[
S={s2}.
]

Then:

[
skill(W)+|S|=2+1=3.
]

Condition 3 requires even.

But (3) is odd.

So this candidate is also inadmissible.

Therefore:

[
W={a,b}
]

has **no admissible (S)** at all.

That means the attractive parallel pair does not even enter the optimization.

This is exactly why the architecture is:

```text
enumerate candidate
↓
test admissibility
↓
ONLY THEN evaluate objective
```

We never evaluate a pair just because it looks dense.

---

# Part 16 — Why This Is Different From “Find the Densest Subgraph”

This is not simply:

> Pick the crew containing the most internal shifts.

If that were the problem, `{a,b}` would look extremely attractive because two workers contain two parallel shifts.

But admissibility can eliminate an entire crew.

And the denominator contains the crew's skills.

And selecting fringe shifts can change both admissibility **and** the objective.

So the actual problem is:

[
\max_{(W,S)\text{ admissible}}
\frac{2i(W)+|S|}
{skill(W)+|S|-2}.
]

The search variable is the **pair** ((W,S)), not merely (W).

---

# COPY INTO `mock_notes_1.md`

Everything below is a clean notes version of what we just established. Paste it into your notes file.

````markdown
# Mock Exit 1 — First-Principles Problem Model

## What the problem is

The Crew-Assignment Density problem is a small multigraph optimization problem written in staffing language.

The translation is:

```text
workers -> vertices
shifts  -> edges
````

The worker set is:

```text
WORKERS = {a, b, c, d}
```

The shifts are:

```text
s0 = (a, b)
s1 = (a, b)
s2 = (b, c)
s3 = (c, d)
```

A useful picture is:

```text
a == b -- c -- d
```

where the double connection between `a` and `b` means there are two distinct physical shift copies.

---

## Why this is a multigraph

`s0` and `s1` connect the same worker pair:

```text
s0 = (a, b)
s1 = (a, b)
```

but they are distinct shifts.

Therefore:

```text
s0 != s1
```

and both must count separately.

The endpoints do not uniquely identify a physical shift copy. The shift ID does.

This is why unique shift IDs will become an instance invariant.

---

## The crew W

A crew `W` is a subset of the workers.

Examples:

```text
{a}
{a, b}
{b, c, d}
{a, b, c, d}
```

The empty crew is not admissible.

Because there are four workers, there are:

```text
2^4 = 16
```

worker subsets total and:

```text
2^4 - 1 = 15
```

nonempty crews.

The later exhaustive search will consider all 15.

---

## skill(W)

Worker skill values are:

```text
a -> 1
b -> 1
c -> 2
d -> 2
```

`skill(W)` means:

> Add the skill value of every worker in W.

Examples:

```text
skill({a,b}) = 1 + 1 = 2

skill({a,b,c}) = 1 + 1 + 2 = 4

skill({a,b,c,d}) = 1 + 1 + 2 + 2 = 6
```

This plays the same structural role as `f(U)` in the F7 capstone.

---

## Internal shifts i(W)

A shift is internal to `W` when BOTH workers staffing it belong to `W`.

`i(W)` counts all such physical shift copies.

For:

```text
W = {a,b}
```

the shifts are classified as:

```text
s0 = (a,b) -> both inside -> internal
s1 = (a,b) -> both inside -> internal
s2 = (b,c) -> only b inside -> not internal
s3 = (c,d) -> neither inside -> not internal
```

Therefore:

```text
i({a,b}) = 2
```

Parallel copies count separately.

This corresponds to `e(U)` in the capstone.

---

## Fringe ∂(W)

A shift belongs to the fringe of `W` when EXACTLY ONE endpoint belongs to `W`.

This is the boundary-crossing condition.

For:

```text
W = {a,b}
```

we have:

```text
s0 -> both inside -> not fringe
s1 -> both inside -> not fringe
s2 -> b inside, c outside -> fringe
s3 -> both outside -> not fringe
```

Therefore:

```text
∂({a,b}) = {s2}
```

In Python, the eventual membership test has the XOR shape:

```python
(u in W) != (v in W)
```

It is true exactly when one endpoint is inside and one is outside.

---

## Internal versus fringe

These are different collections.

For:

```text
W = {a,b}
```

we have:

```text
internal shifts = {s0, s1}
fringe shifts   = {s2}
```

Internal shifts contribute through `i(W)`.

Fringe shifts are the source from which `S` may be selected.

---

## What S is

A candidate is not just a crew.

A candidate is:

```text
(W, S)
```

where:

```text
W = set of workers
S = set of shift IDs
```

and:

```text
S ⊆ ∂(W)
```

`S` does not have to contain every fringe shift.

For example, if:

```text
∂(W) = {s0, s1, s2}
```

then possible `S` values include:

```text
∅
{s0}
{s1}
{s2}
{s0,s1}
{s0,s2}
{s1,s2}
{s0,s1,s2}
```

There are:

```text
2^3 = 8
```

subsets.

Shift IDs must remain distinct because `|S|` counts actual physical shift copies.

---

## The four admissibility conditions

A candidate `(W,S)` is admissible exactly when all four conditions hold, in this order.

### Condition 1

```text
W is nonempty
and
W ⊆ WORKERS
```

### Condition 2

```text
S ⊆ ∂(W)
```

Every selected shift must actually cross the boundary of the chosen crew.

### Condition 3

```text
skill(W) + |S| is even
```

### Condition 4

```text
skill(W) + |S| >= 4
```

Condition 4 guarantees:

```text
skill(W) + |S| - 2 >= 2
```

so every admissible pair has a positive, nonzero objective denominator.

---

## The objective

For an admissible pair:

```text
value(W,S)
=
(2*i(W) + |S|)
/
(skill(W) + |S| - 2)
```

This is an exact rational density.

The numerator is:

```text
2*i(W) + |S|
```

NOT:

```text
2*(i(W) + |S|)
```

Internal shifts receive coefficient 2.

Selected fringe shifts receive coefficient 1.

The denominator depends on:

```text
crew skill + selected fringe count - 2
```

The search asks:

> Among every admissible pair `(W,S)`, which pair maximizes this exact ratio?

---

## Worked crew: W = {a,b}

First:

```text
skill({a,b}) = 1 + 1 = 2
```

Internal shifts:

```text
s0 = (a,b)
s1 = (a,b)
```

so:

```text
i({a,b}) = 2
```

Fringe:

```text
∂({a,b}) = {s2}
```

Therefore the only possible S values are:

```text
S = ∅
S = {s2}
```

For:

```text
S = ∅
```

the total is:

```text
skill(W) + |S|
= 2 + 0
= 2
```

Condition 3 passes because 2 is even.

Condition 4 fails because:

```text
2 < 4
```

So the pair is inadmissible.

For:

```text
S = {s2}
```

the total is:

```text
2 + 1 = 3
```

Condition 3 fails because 3 is odd.

Therefore the crew `{a,b}` has no admissible choice of `S`.

This demonstrates why the program must:

```text
enumerate candidate
        ↓
test admissibility
        ↓
evaluate only if admissible
```

A crew can contain many internal shifts and still have no admissible pair.

---

## Comparison with the F7 capstone

The structural correspondence is:

| F7 capstone       | Mock              |
| ----------------- | ----------------- |
| vertex            | worker            |
| edge copy         | shift             |
| edge ID           | shift ID          |
| U                 | W                 |
| f(v)              | skill(worker)     |
| f(U)              | skill(W)          |
| e(U)              | i(W)              |
| boundary ∂G(U)    | fringe ∂(W)       |
| F                 | S                 |
| candidate (U,F)   | candidate (W,S)   |
| exact Fraction    | exact Fraction    |
| exhaustive search | exhaustive search |

But the mathematics deliberately changes.

### Capstone

```text
parity:
f(U) + |F| is odd

lower bound:
f(U) + |F| >= 3

numerator:
2*(e(U) + |F|)
= 2e(U) + 2|F|

denominator:
f(U) + |F| - 1
```

### Mock

```text
parity:
skill(W) + |S| is even

lower bound:
skill(W) + |S| >= 4

numerator:
2*i(W) + |S|

denominator:
skill(W) + |S| - 2
```

There is also NO skill-versus-degree assumption in the mock.

The mock therefore tests whether I can preserve the software architecture while changing the mathematics according to a new specification rather than pattern-replaying the previous checker.

```

## What happens next

Do **not** create any Python files yet.

The next thing we will do together is derive the oracle, but we are going to do it in a way that teaches you how to reason through the search space rather than handing you a mysterious completed table.

We will start with the four **singleton crews**:

\[
\{a\},\{b\},\{c\},\{d\},
\]

and for each one I will walk you through, in order:

\[
skill(W)
\rightarrow
i(W)
\rightarrow
\partial(W)
\rightarrow
\text{possible }S
\rightarrow
\text{admissibility}
\rightarrow
\text{value if admissible}.
\]

Then we do the six 2-worker crews, then the four 3-worker crews, then the whole graph. By the time we finish, the oracle table will not be something you copied; every column will have a meaning you understand.

> **RULE TO BANK:** The mock is not asking for “the densest crew.” It optimizes over **pairs \((W,S)\)**. First choose a crew, identify its internal and fringe shifts, choose a subset of the fringe, test all four admissibility conditions, and only then evaluate the exact density.
```
====================================================================================================================================================

Good. We are still entirely in the **hand-analysis phase**. No Python checker files yet.

The next objective is to understand how to analyze a candidate crew systematically. We’ll start with the **four singleton crews**:

[
{a},{b},{c},{d}.
]

By the end of this step, you should be able to look at any fixed (W) and know exactly what questions to ask.

---

# Step 1 — The Analysis Template for Any Crew

For every crew (W), we always proceed in this order:

```text
1. What workers are in W?
        ↓
2. What is skill(W)?
        ↓
3. Which shifts have BOTH endpoints in W?
        ↓
   Count them → i(W)
        ↓
4. Which shifts have EXACTLY ONE endpoint in W?
        ↓
   Those form ∂(W)
        ↓
5. What subsets S ⊆ ∂(W) are possible?
        ↓
6. Which S satisfy:
       skill(W) + |S| even
       skill(W) + |S| >= 4
        ↓
7. ONLY for those admissible pairs:
       evaluate the exact objective
```

That sequence is going to become the architecture of the program later.

For now, we do it manually.

---

# A Useful Compression: Let (x=|S|)

There is an important observation that will save us a lot of hand arithmetic.

For a fixed crew (W), both admissibility conditions 3–4 and the objective depend on (S) through:

[
|S|
]

rather than through the actual names of its shifts.

So during the **hand analysis**, we can temporarily write:

[
x=|S|.
]

Then the parity condition becomes:

[
skill(W)+x\text{ is even},
]

the lower bound becomes:

[
skill(W)+x\ge4,
]

and the objective becomes:

[
\frac{2i(W)+x}{skill(W)+x-2}.
]

This does **not** mean shift identities stop mattering.

They absolutely matter for the actual candidate pair and later code.

It means only that:

> For a fixed (W), two fringe subsets of the same size have the same objective value.

For example, if:

```text
∂(W) = {s0, s1, s2}
```

then:

```text
S = {s0}
S = {s1}
S = {s2}
```

all have:

[
|S|=1.
]

Therefore, for that same (W), all three produce the same arithmetic value.

That observation lets us analyze **possible sizes first**, while preserving actual IDs for the final oracle and later search.

---

# Singleton 1 — (W={a})

Start with:

[
W={a}.
]

## A. Compute `skill(W)`

Worker `a` has:

[
skill(a)=1.
]

Therefore:

[
skill({a})=1.
]

---

## B. Compute the internal count (i(W))

Now inspect every shift.

### `s0 = (a,b)`

`a` is inside.

`b` is outside.

So `s0` is **not internal**.

### `s1 = (a,b)`

Same situation:

```text
a inside
b outside
```

Not internal.

### `s2 = (b,c)`

Neither endpoint is `a`.

Both are outside.

Not internal.

### `s3 = (c,d)`

Again both outside.

Not internal.

Therefore:

[
i({a})=0.
]

---

## C. Compute the fringe (\partial(W))

Now change the question.

We no longer ask:

> Are both endpoints inside?

We ask:

> Is exactly one endpoint inside?

For `s0`:

```text
a inside
b outside
```

Yes.

So:

[
s0\in\partial({a}).
]

For `s1`:

same reasoning.

So:

[
s1\in\partial({a}).
]

For `s2=(b,c)`:

both endpoints are outside.

No.

For `s3=(c,d)`:

both outside.

No.

Therefore:

[
\partial({a})={s0,s1}.
]

Notice something important already:

**both parallel copies survive**.

The fringe has size:

[
|\partial({a})|=2.
]

---

# D. What can (S) be?

Because:

[
S\subseteq{s0,s1},
]

there are:

[
2^2=4
]

possible subsets:

[
\varnothing,
]

[
{s0},
]

[
{s1},
]

[
{s0,s1}.
]

Their possible sizes are:

[
x=0,1,2.
]

Now we use admissibility to eliminate them.

---

## E. Parity

We need:

[
skill(W)+x
]

to be even.

Here:

[
skill(W)=1.
]

So:

[
1+x
]

must be even.

When is odd (+\ x) even?

Only when (x) is odd.

Among:

[
0,1,2,
]

the only odd possibility is:

[
x=1.
]

So parity eliminates (x=0) and (x=2).

---

## F. Lower bound

For:

[
x=1,
]

we get:

[
skill(W)+x
==========

# 1+1

2.

]

But Condition 4 requires:

[
skill(W)+x\ge4.
]

And:

[
2<4.
]

So even the parity-compatible choice fails.

Therefore:

[
\boxed{{a}\text{ has no admissible }S.}
]

We never evaluate the objective.

That is important.

An inadmissible pair has **no optimization value for the search**.

---

# Singleton 2 — (W={b})

Now:

[
W={b}.
]

## A. Skill

[
skill(b)=1.
]

Therefore:

[
skill({b})=1.
]

---

## B. Internal shifts

Check each:

```text
s0 = (a,b)
one inside → not internal

s1 = (a,b)
one inside → not internal

s2 = (b,c)
one inside → not internal

s3 = (c,d)
both outside → not internal
```

Therefore:

[
i({b})=0.
]

---

## C. Fringe

Now exactly one endpoint inside.

```text
s0 = (a,b)
b inside, a outside → fringe

s1 = (a,b)
b inside, a outside → fringe

s2 = (b,c)
b inside, c outside → fringe

s3 = (c,d)
both outside → not fringe
```

Therefore:

[
\partial({b})
=============

{s0,s1,s2}.
]

So:

[
|\partial({b})|=3.
]

Possible (S)-sizes:

[
x=0,1,2,3.
]

---

## D. Parity

Again:

[
skill(W)=1.
]

So:

[
1+x
]

must be even.

Therefore (x) must be odd.

Possible:

[
x=1
]

or:

[
x=3.
]

---

## E. Lower bound

For (x=1):

[
1+1=2<4.
]

Fails Condition 4.

For (x=3):

[
1+3=4.
]

This is:

```text
even ✓
at least 4 ✓
```

So (x=3) is admissible.

Because there are exactly three fringe shifts, the only size-3 subset is the entire fringe:

[
S={s0,s1,s2}.
]

Thus we have our first admissible pair:

[
({b},{s0,s1,s2}).
]

---

## F. Evaluate it

Recall:

[
i(W)=0,
]

[
skill(W)=1,
]

[
|S|=3.
]

The numerator is:

[
2i(W)+|S|.
]

Substitute:

[
2(0)+3=3.
]

The denominator is:

[
skill(W)+|S|-2.
]

Substitute:

[
1+3-2=2.
]

Therefore:

[
value
=====

\frac32.
]

So:

[
\boxed{
value({b},{s0,s1,s2})=\frac32
}
]

This is our first actual competitor value.

---

# Singleton 3 — (W={c})

Now:

[
W={c}.
]

## A. Skill

Worker `c` has skill 2.

Therefore:

[
skill({c})=2.
]

---

## B. Internal shifts

A singleton cannot contain an internal shift in this problem because there are **no self-pairing shifts**.

Every shift connects two different workers.

Explicitly:

```text
s0 = (a,b) → both outside
s1 = (a,b) → both outside
s2 = (b,c) → one inside
s3 = (c,d) → one inside
```

So:

[
i({c})=0.
]

---

## C. Fringe

Exactly one endpoint inside:

```text
s0 → no
s1 → no

s2 = (b,c)
c inside, b outside → yes

s3 = (c,d)
c inside, d outside → yes
```

Therefore:

[
\partial({c})
=============

{s2,s3}.
]

Possible sizes:

[
x=0,1,2.
]

---

## D. Parity

Now:

[
skill(W)=2.
]

We need:

[
2+x
]

even.

Because 2 is already even, (x) must be even.

Possible:

[
x=0
]

or:

[
x=2.
]

---

## E. Lower bound

For (x=0):

[
2+0=2<4.
]

Fails.

For (x=2):

[
2+2=4.
]

Passes.

So:

[
S={s2,s3}
]

is admissible.

---

## F. Objective

We have:

[
i(W)=0,
]

[
skill(W)=2,
]

[
|S|=2.
]

Numerator:

[
2(0)+2=2.
]

Denominator:

[
2+2-2=2.
]

Therefore:

[
value
=====

# \frac22

1.

]

So:

[
\boxed{
value({c},{s2,s3})=1
}
]

---

# Singleton 4 — (W={d})

Now:

[
W={d}.
]

## A. Skill

[
skill(d)=2.
]

Therefore:

[
skill({d})=2.
]

---

## B. Internal shifts

Again there are no loops, so:

[
i({d})=0.
]

---

## C. Fringe

Only one shift touches `d`:

```text
s3 = (c,d)
```

Here:

```text
d inside
c outside
```

so:

[
\partial({d})={s3}.
]

Possible sizes:

[
x=0,1.
]

---

## D. Parity

We need:

[
2+x
]

even.

Thus (x) must be even.

Among:

[
0,1,
]

only:

[
x=0.
]

passes parity.

---

## E. Lower bound

For (x=0):

[
2+0=2.
]

But:

[
2<4.
]

So it fails Condition 4.

Could (x=1) help with the bound?

It gives:

[
2+1=3,
]

which is still below 4 **and** odd.

So no.

Therefore:

[
\boxed{{d}\text{ has no admissible }S.}
]

---

# What We Learned From the Four Singletons

Let's compress everything:

| (W)   | `skill(W)` | `i(W)` | `∂(W)`       | admissible `S` | value |
| ----- | ---------: | -----: | ------------ | -------------- | ----: |
| `{a}` |          1 |      0 | `{s0,s1}`    | none           |     — |
| `{b}` |          1 |      0 | `{s0,s1,s2}` | `{s0,s1,s2}`   | (3/2) |
| `{c}` |          2 |      0 | `{s2,s3}`    | `{s2,s3}`      |   (1) |
| `{d}` |          2 |      0 | `{s3}`       | none           |     — |

So after analyzing all one-worker crews, the best value we have seen is:

[
\frac32.
]

Current leader:

[
W={b},
\qquad
S={s0,s1,s2},
\qquad
value=\frac32.
]

But this is **not the oracle yet** because we still have:

```text
6 two-worker crews
4 three-worker crews
1 four-worker crew
```

left to audit.

---

# A Useful Parity Shortcut You Just Learned

There is already a reusable deduction.

Condition 3 requires:

[
skill(W)+|S|
]

even.

Therefore:

```text
if skill(W) is even
→ |S| must be even

if skill(W) is odd
→ |S| must be odd
```

Why?

Because:

```text
even + even = even
odd  + odd  = even
```

while:

```text
even + odd = odd
odd + even = odd
```

This lets us eliminate half the candidate subset sizes immediately.

But we still have to check the lower bound afterward.

Parity passing does **not** imply admissibility.

We saw that with:

[
W={a},\quad |S|=1.
]

The total:

[
1+1=2
]

was even, but still below 4.

---

# COPY INTO `mock_notes_1.md`

Add this next.

````markdown
## Hand Analysis Method

For every fixed crew `W`, analyze it in this order:

```text
1. Compute skill(W).

2. Determine which physical shift copies have both endpoints in W.
   Count them to obtain i(W).

3. Determine which physical shift copies have exactly one endpoint in W.
   These form ∂(W).

4. Enumerate possible S ⊆ ∂(W).

5. Filter candidate S by:
       skill(W) + |S| even
       skill(W) + |S| >= 4

6. Only after the pair is admissible, evaluate:

       (2*i(W) + |S|)
       -----------------------
       skill(W) + |S| - 2
````

The order matters. Inadmissible pairs do not participate in the optimization and should not be evaluated as competitors.

---

## Cardinality Compression for Hand Analysis

For a fixed crew `W`, admissibility conditions 3–4 and the objective depend on a fringe subset `S` through its cardinality:

```text
x = |S|
```

So the formulas become:

```text
parity:
skill(W) + x must be even

lower bound:
skill(W) + x >= 4

objective:
(2*i(W) + x) / (skill(W) + x - 2)
```

This makes the hand analysis shorter.

However, shift identity still matters mathematically and computationally because `S` is a set of actual shift copies. Different physical shifts must retain different IDs.

Two different `S` sets with the same size have the same objective value for a fixed `W`, but they are still different candidate pairs.

---

## Parity Shortcut

Because:

```text
skill(W) + |S|
```

must be even:

```text
if skill(W) is even:
    |S| must be even

if skill(W) is odd:
    |S| must be odd
```

Passing parity does not guarantee admissibility. The lower bound must still be checked separately.

---

## Singleton Crews

### W = {a}

```text
skill(W) = 1
i(W) = 0
∂(W) = {s0, s1}
possible |S| = 0, 1, 2
```

Because skill is odd, `|S|` must be odd.

Only:

```text
|S| = 1
```

passes parity.

But:

```text
skill(W) + |S|
= 1 + 1
= 2
< 4
```

so Condition 4 fails.

Therefore `{a}` has no admissible `S`.

---

### W = {b}

```text
skill(W) = 1
i(W) = 0
∂(W) = {s0, s1, s2}
possible |S| = 0, 1, 2, 3
```

Skill is odd, so `|S|` must be odd.

Possible parity-compatible sizes:

```text
1, 3
```

For `|S| = 1`:

```text
1 + 1 = 2 < 4
```

so the lower bound fails.

For `|S| = 3`:

```text
1 + 3 = 4
```

which is even and at least 4.

Since the fringe itself has exactly three shifts, the admissible set is:

```text
S = {s0, s1, s2}
```

Objective:

```text
numerator
= 2*i(W) + |S|
= 2*0 + 3
= 3

denominator
= skill(W) + |S| - 2
= 1 + 3 - 2
= 2

value
= 3/2
```

So:

```text
value({b}, {s0,s1,s2}) = 3/2
```

---

### W = {c}

```text
skill(W) = 2
i(W) = 0
∂(W) = {s2, s3}
possible |S| = 0, 1, 2
```

Skill is even, so `|S|` must be even.

Possible:

```text
0, 2
```

For `|S| = 0`:

```text
2 + 0 = 2 < 4
```

so the lower bound fails.

For `|S| = 2`:

```text
2 + 2 = 4
```

so the pair is admissible.

Thus:

```text
S = {s2, s3}
```

and:

```text
numerator
= 2*0 + 2
= 2

denominator
= 2 + 2 - 2
= 2

value
= 1
```

---

### W = {d}

```text
skill(W) = 2
i(W) = 0
∂(W) = {s3}
possible |S| = 0, 1
```

Skill is even, so `|S|` must be even.

Only `|S| = 0` passes parity.

But:

```text
2 + 0 = 2 < 4
```

so Condition 4 fails.

Therefore `{d}` has no admissible `S`.

---

## Singleton Summary

| Crew  | skill(W) | i(W) | fringe       | admissible S | value |
| ----- | -------: | ---: | ------------ | ------------ | ----: |
| `{a}` |        1 |    0 | `{s0,s1}`    | none         |     — |
| `{b}` |        1 |    0 | `{s0,s1,s2}` | `{s0,s1,s2}` | `3/2` |
| `{c}` |        2 |    0 | `{s2,s3}`    | `{s2,s3}`    |   `1` |
| `{d}` |        2 |    0 | `{s3}`       | none         |     — |

After all singleton crews, the current best admissible value is:

```text
3/2
```

attained by:

```text
W = {b}
S = {s0, s1, s2}
```

This is only the current leader. The remaining two-worker, three-worker, and four-worker crews must still be audited before the oracle can be locked.

````

---

# COPY INTO `MOCK_ORACLE.md`

Now we can begin the formal oracle itself. If your oracle file is still empty, put this at the top:

```markdown
# Mock Exit 1 — Hand-Derived Oracle

## Fixed Instance

The worker set is

\[
\{a,b,c,d\}.
\]

The shift copies are

- `s0 = (a,b)`
- `s1 = (a,b)`
- `s2 = (b,c)`
- `s3 = (c,d)`

with skill values

\[
skill(a)=1,\qquad
skill(b)=1,\qquad
skill(c)=2,\qquad
skill(d)=2.
\]

For a crew \(W\), let:

- \(skill(W)\) be the sum of its workers' skill values,
- \(i(W)\) be the number of shift copies having both endpoints in \(W\),
- \(\partial(W)\) be the shift copies having exactly one endpoint in \(W\).

For \(S\subseteq\partial(W)\), the pair \((W,S)\) is admissible exactly when:

1. \(W\neq\varnothing\) and \(W\subseteq WORKERS\),
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

The objective is interpreted exactly as written: only \(i(W)\) is multiplied by 2.

## Singleton Crews

For \(W=\{a\}\),

\[
skill(W)=1,\qquad
i(W)=0,\qquad
\partial(W)=\{s0,s1\}.
\]

Parity requires \(|S|\) odd, so the only possible size is \(1\). Then

\[
skill(W)+|S|=2<4.
\]

Hence there is no admissible pair with \(W=\{a\}\).

For \(W=\{b\}\),

\[
skill(W)=1,\qquad
i(W)=0,\qquad
\partial(W)=\{s0,s1,s2\}.
\]

The only admissible fringe size is \(|S|=3\), giving

\[
S=\{s0,s1,s2\}.
\]

Its value is

\[
\frac{2(0)+3}{1+3-2}
=
\frac32.
\]

For \(W=\{c\}\),

\[
skill(W)=2,\qquad
i(W)=0,\qquad
\partial(W)=\{s2,s3\}.
\]

The only admissible fringe size is \(|S|=2\), giving

\[
S=\{s2,s3\}.
\]

Its value is

\[
\frac{2(0)+2}{2+2-2}
=
1.
\]

For \(W=\{d\}\),

\[
skill(W)=2,\qquad
i(W)=0,\qquad
\partial(W)=\{s3\}.
\]

Parity permits only \(|S|=0\), but then

\[
skill(W)+|S|=2<4.
\]

Hence there is no admissible pair with \(W=\{d\}\).

After the singleton cases, the current maximum is

\[
\frac32,
\]

attained by

\[
W=\{b\},
\qquad
S=\{s0,s1,s2\}.
\]

This is not yet the final oracle; all larger crews remain to be checked.
````

Do **not commit yet**. We are building the entire hand oracle first, and only once the full competitor audit is complete will we make the required pre-code `mock1:` oracle commit.

Next we will do the **six two-worker crews**. That is where the graph starts getting much more interesting because internal shifts appear, and you’ll see why the tempting parallel pair `{a,b}` still cannot compete while another two-worker crew becomes a legitimate density candidate.
===============================================================================================================================================================

Good. We now move to the **six two-worker crews**, still entirely by hand. No Python files yet.

This is where the mock starts testing whether you actually understand the graph rather than just the formulas, because a two-worker crew may contain internal shifts, fringe shifts, both, or neither.

There are

[
\binom{4}{2}=6
]

two-worker crews:

[
{a,b},{a,c},{a,d},{b,c},{b,d},{c,d}.
]

We will use exactly the same analysis pipeline for every one:

```text
crew W
↓
skill(W)
↓
internal shifts → i(W)
↓
fringe shifts → ∂(W)
↓
possible |S|
↓
parity
↓
lower bound
↓
objective only if admissible
```

---

# 1. (W={a,b})

We already worked this one once, but now it belongs in the systematic oracle audit.

## Skill

```text
a → 1
b → 1
```

Therefore:

[
skill({a,b})=1+1=2.
]

## Internal shifts

Check all four physical shift copies:

```text
s0 = (a,b)
a inside, b inside
→ internal

s1 = (a,b)
a inside, b inside
→ internal

s2 = (b,c)
b inside, c outside
→ not internal

s3 = (c,d)
both outside
→ not internal
```

Therefore:

[
i({a,b})=2.
]

Notice again that the two parallel copies count separately.

## Fringe

Fringe means **exactly one endpoint inside**.

```text
s0 → both inside → no
s1 → both inside → no
s2 → b inside, c outside → yes
s3 → both outside → no
```

So:

[
\partial({a,b})={s2}.
]

Thus:

[
|S|\in{0,1}.
]

## Admissibility

The crew skill is even:

[
skill(W)=2.
]

Therefore parity requires (|S|) even.

Among `0, 1`, only:

[
|S|=0
]

passes Condition 3.

But then:

[
skill(W)+|S|=2+0=2<4.
]

So Condition 4 fails.

If (|S|=1), then:

[
2+1=3,
]

which fails parity anyway.

Therefore:

[
\boxed{{a,b}\text{ has no admissible pair.}}
]

This is important because `{a,b}` contains **two internal shifts** and superficially looks dense. But the optimization never gets to evaluate it.

---

# 2. (W={a,c})

Now choose workers `a` and `c`.

## Skill

```text
a → 1
c → 2
```

Therefore:

[
skill({a,c})=1+2=3.
]

## Internal shifts

Look for a shift whose **both endpoints** lie in `{a,c}`.

```text
s0 = (a,b)
b outside
→ not internal

s1 = (a,b)
b outside
→ not internal

s2 = (b,c)
b outside
→ not internal

s3 = (c,d)
d outside
→ not internal
```

There is no `(a,c)` shift.

Therefore:

[
i({a,c})=0.
]

## Fringe

Now ask whether exactly one endpoint is inside.

```text
s0 = (a,b)
a inside, b outside
→ fringe

s1 = (a,b)
a inside, b outside
→ fringe

s2 = (b,c)
b outside, c inside
→ fringe

s3 = (c,d)
c inside, d outside
→ fringe
```

Every shift crosses the crew boundary.

Therefore:

[
\partial({a,c})
===============

{s0,s1,s2,s3}.
]

So the fringe has size 4.

Possible cardinalities are:

[
|S|=0,1,2,3,4.
]

## Parity

The skill is odd:

[
skill(W)=3.
]

To make:

[
3+|S|
]

even, (|S|) must be odd.

Thus only:

[
|S|=1
]

or:

[
|S|=3
]

can be admissible.

## Lower bound

For (|S|=1):

[
3+1=4.
]

Pass.

For (|S|=3):

[
3+3=6.
]

Pass.

So **both cardinalities are admissible**.

---

## Objective when (|S|=1)

We have:

[
i(W)=0.
]

Numerator:

[
2(0)+1=1.
]

Denominator:

[
3+1-2=2.
]

Therefore:

[
value=\frac12.
]

There are four different one-shift choices:

[
{s0},{s1},{s2},{s3}.
]

Each is a different candidate pair, but each has the same value:

[
\frac12.
]

---

## Objective when (|S|=3)

Numerator:

[
2(0)+3=3.
]

Denominator:

[
3+3-2=4.
]

Therefore:

[
value=\frac34.
]

There are:

[
\binom43=4
]

different three-shift subsets, and all four have value:

[
\frac34.
]

So the best value for this crew is:

[
\boxed{\frac34}.
]

Notice something subtle:

[
\frac34>\frac12.
]

For this particular crew, selecting more fringe shifts raises the ratio.

But we should **never generalize that into a rule** without proof. The effect of increasing (|S|) depends on both numerator and denominator.

---

# 3. (W={a,d})

## Skill

[
skill({a,d})=1+2=3.
]

## Internal shifts

There is no shift between `a` and `d`.

Check explicitly:

```text
s0 = (a,b) → b outside
s1 = (a,b) → b outside
s2 = (b,c) → both outside
s3 = (c,d) → c outside
```

Therefore:

[
i({a,d})=0.
]

## Fringe

```text
s0 = (a,b)
a inside, b outside
→ fringe

s1 = (a,b)
a inside, b outside
→ fringe

s2 = (b,c)
both outside
→ not fringe

s3 = (c,d)
c outside, d inside
→ fringe
```

Therefore:

[
\partial({a,d})
===============

{s0,s1,s3}.
]

Possible sizes:

[
|S|=0,1,2,3.
]

## Parity

Skill is 3, which is odd.

So (|S|) must be odd:

[
|S|=1
]

or:

[
|S|=3.
]

Both satisfy the lower bound:

[
3+1=4
]

and:

[
3+3=6.
]

---

## Value at (|S|=1)

[
\frac{2(0)+1}{3+1-2}
====================

\frac12.
]

## Value at (|S|=3)

[
\frac{2(0)+3}{3+3-2}
====================

\frac34.
]

Therefore:

[
\boxed{\text{best for }{a,d}=\frac34}.
]

---

# 4. (W={b,c})

This one is more interesting because now we get an internal shift **and** three fringe shifts.

## Skill

```text
b → 1
c → 2
```

Therefore:

[
skill({b,c})=1+2=3.
]

## Internal shifts

```text
s0 = (a,b)
a outside
→ not internal

s1 = (a,b)
a outside
→ not internal

s2 = (b,c)
both b and c inside
→ internal

s3 = (c,d)
d outside
→ not internal
```

Therefore:

[
i({b,c})=1.
]

## Fringe

```text
s0:
a outside, b inside
→ fringe

s1:
a outside, b inside
→ fringe

s2:
both inside
→ not fringe

s3:
c inside, d outside
→ fringe
```

Therefore:

[
\partial({b,c})
===============

{s0,s1,s3}.
]

Possible sizes:

[
|S|=0,1,2,3.
]

## Parity

Skill is odd:

[
3.
]

So (|S|) must be odd:

[
|S|=1
]

or:

[
|S|=3.
]

Both pass the lower bound.

---

## Value at (|S|=1)

Now be careful with the mock numerator.

It is:

[
2i(W)+|S|.
]

Since:

[
i(W)=1,
]

we get:

[
2(1)+1=3.
]

Denominator:

[
3+1-2=2.
]

Thus:

[
value=\frac32.
]

And because there are three fringe shifts, there are three different size-1 choices:

[
S={s0},
]

[
S={s1},
]

or:

[
S={s3}.
]

Each gives:

[
\frac32.
]

---

## Value at (|S|=3)

Now:

[
S={s0,s1,s3}.
]

Numerator:

[
2(1)+3=5.
]

Denominator:

[
3+3-2=4.
]

Therefore:

[
value=\frac54.
]

Compare:

[
\frac32=1.5
]

versus:

[
\frac54=1.25.
]

So here **adding more fringe shifts makes the ratio smaller**.

That is worth noticing because it is the opposite behavior from the `{a,c}` crew.

Why?

Because the internal contribution is already helping the numerator strongly. Adding fringe shifts increases numerator and denominator by the same amount, but the ratio can move either direction depending on the starting values.

Therefore the best for this crew is:

[
\boxed{\frac32}.
]

This **ties** our current singleton leader `{b}`.

So at this stage, before larger crews are considered, the current maximum is not unique.

---

# 5. (W={b,d})

## Skill

[
skill({b,d})=1+2=3.
]

## Internal shifts

There is no shift connecting `b` to `d`.

```text
s0 = (a,b) → one inside
s1 = (a,b) → one inside
s2 = (b,c) → one inside
s3 = (c,d) → one inside
```

Therefore:

[
i({b,d})=0.
]

## Fringe

The interesting thing here is that **every single shift has exactly one endpoint in the crew**.

```text
s0: b inside, a outside
s1: b inside, a outside
s2: b inside, c outside
s3: d inside, c outside
```

So:

[
\partial({b,d})
===============

{s0,s1,s2,s3}.
]

Possible (|S|):

[
0,1,2,3,4.
]

Skill is odd, so admissible parity requires:

[
|S|=1
]

or:

[
|S|=3.
]

Both satisfy the lower bound.

Because (i(W)=0), this has exactly the same arithmetic pattern as `{a,c}`:

For (|S|=1):

[
value=\frac12.
]

For (|S|=3):

[
value=\frac34.
]

Therefore:

[
\boxed{\text{best for }{b,d}=\frac34}.
]

---

# 6. (W={c,d})

## Skill

```text
c → 2
d → 2
```

Therefore:

[
skill({c,d})=2+2=4.
]

## Internal shifts

```text
s0 = (a,b)
both outside
→ no

s1 = (a,b)
both outside
→ no

s2 = (b,c)
b outside
→ no

s3 = (c,d)
both inside
→ internal
```

Therefore:

[
i({c,d})=1.
]

## Fringe

```text
s0 → both outside → no
s1 → both outside → no

s2 = (b,c)
b outside, c inside
→ fringe

s3 = (c,d)
both inside
→ no
```

Thus:

[
\partial({c,d})={s2}.
]

Possible sizes:

[
|S|=0,1.
]

## Parity

Skill is even:

[
4.
]

Therefore (|S|) must be even.

Only:

[
|S|=0
]

works.

Lower bound:

[
4+0=4.
]

Pass.

So:

[
S=\varnothing
]

is admissible.

## Objective

Numerator:

[
2(1)+0=2.
]

Denominator:

[
4+0-2=2.
]

Therefore:

[
value=1.
]

So:

[
\boxed{
value({c,d},\varnothing)=1
}.
]

---

# Two-Worker Summary

We can now extend our audit:

| Crew (W) | skill | (i(W)) | fringe | admissible (|S|) | best value |
|---|---:|---:|---|---|---:|
| `{a,b}` | 2 | 2 | `{s2}` | none | — |
| `{a,c}` | 3 | 0 | `{s0,s1,s2,s3}` | 1, 3 | (3/4) |
| `{a,d}` | 3 | 0 | `{s0,s1,s3}` | 1, 3 | (3/4) |
| `{b,c}` | 3 | 1 | `{s0,s1,s3}` | 1, 3 | **(3/2)** |
| `{b,d}` | 3 | 0 | `{s0,s1,s2,s3}` | 1, 3 | (3/4) |
| `{c,d}` | 4 | 1 | `{s2}` | 0 | (1) |

After all one-worker **and** two-worker crews, the current best value is still:

[
\frac32.
]

But now it is attained in several ways.

One is:

[
W={b},
\qquad
S={s0,s1,s2}.
]

And for:

[
W={b,c},
]

each of these is also worth (\frac32):

[
S={s0},
]

[
S={s1},
]

[
S={s3}.
]

So the current maximum has a tie.

This matters because our oracle must not casually claim uniqueness until we have checked the entire search space.

---

# A Deeper Lesson From `{a,c}` Versus `{b,c}`

This pair of examples teaches something important about ratios.

For `{a,c}`, where:

[
i(W)=0,
]

increasing (|S|) from 1 to 3 changes:

[
\frac12
]

to:

[
\frac34.
]

The ratio **increases**.

But for `{b,c}`, where:

[
i(W)=1,
]

increasing (|S|) from 1 to 3 changes:

[
\frac32
]

to:

[
\frac54.
]

The ratio **decreases**.

So we cannot use a heuristic such as:

> “More selected fringe shifts always improves density.”

Nor can we say:

> “Use as few fringe shifts as possible.”

Neither is generally true.

The correct search must enumerate every admissible (S), calculate its exact value, and compare.

That is precisely why brute force is useful for a toy oracle/checker.

---

# COPY INTO `mock_notes_1.md`

Paste this next:

````markdown
## Two-Worker Crews

There are

\[
\binom{4}{2}=6
\]

two-worker crews:

```text
{a,b}
{a,c}
{a,d}
{b,c}
{b,d}
{c,d}
````

Each is analyzed using the same sequence:

```text
skill(W)
→ internal shifts i(W)
→ fringe ∂(W)
→ possible |S|
→ parity
→ lower bound
→ objective
```

---

### W = {a,b}

```text
skill(W) = 1 + 1 = 2
```

Internal shifts:

```text
s0 = (a,b) → internal
s1 = (a,b) → internal
```

so:

```text
i(W) = 2
```

Fringe:

```text
s2 = (b,c)
```

so:

```text
∂(W) = {s2}
```

Possible sizes:

```text
|S| = 0 or 1
```

Because skill is even, parity requires `|S|` even.

Thus only:

```text
|S| = 0
```

passes parity.

But then:

```text
skill(W) + |S|
= 2
< 4
```

so Condition 4 fails.

Therefore `{a,b}` has no admissible pair.

This is important because the crew contains two internal parallel shifts but is still completely excluded by admissibility.

---

### W = {a,c}

```text
skill(W) = 1 + 2 = 3
i(W) = 0
```

Every shift has exactly one endpoint in the crew:

```text
∂(W) = {s0,s1,s2,s3}
```

Possible sizes are:

```text
0, 1, 2, 3, 4
```

Because skill is odd, `|S|` must be odd:

```text
|S| = 1 or 3
```

Both satisfy the lower bound.

For `|S| = 1`:

```text
numerator
= 2*0 + 1
= 1

denominator
= 3 + 1 - 2
= 2

value
= 1/2
```

For `|S| = 3`:

```text
numerator
= 2*0 + 3
= 3

denominator
= 3 + 3 - 2
= 4

value
= 3/4
```

Therefore the best value for `{a,c}` is:

```text
3/4
```

There are four distinct size-3 choices of `S`, all with the same value.

---

### W = {a,d}

```text
skill(W) = 1 + 2 = 3
i(W) = 0
∂(W) = {s0,s1,s3}
```

Skill is odd, so:

```text
|S| = 1 or 3
```

For `|S| = 1`:

```text
value = 1/2
```

For `|S| = 3`:

```text
value = 3/4
```

Therefore the best value for `{a,d}` is:

```text
3/4
```

---

### W = {b,c}

```text
skill(W) = 1 + 2 = 3
```

Internal shift:

```text
s2 = (b,c)
```

so:

```text
i(W) = 1
```

Fringe:

```text
s0 = (a,b)
s1 = (a,b)
s3 = (c,d)
```

therefore:

```text
∂(W) = {s0,s1,s3}
```

Skill is odd, so admissible parity requires:

```text
|S| = 1 or 3
```

For `|S| = 1`:

```text
numerator
= 2*1 + 1
= 3

denominator
= 3 + 1 - 2
= 2

value
= 3/2
```

There are three distinct size-1 candidates:

```text
S = {s0}
S = {s1}
S = {s3}
```

and each has value:

```text
3/2
```

For `|S| = 3`:

```text
numerator
= 2*1 + 3
= 5

denominator
= 3 + 3 - 2
= 4

value
= 5/4
```

So the best value for `{b,c}` is:

```text
3/2
```

---

### W = {b,d}

```text
skill(W) = 1 + 2 = 3
i(W) = 0
```

Every shift crosses the crew boundary:

```text
∂(W) = {s0,s1,s2,s3}
```

Parity permits:

```text
|S| = 1 or 3
```

The corresponding values are:

```text
|S| = 1 → 1/2
|S| = 3 → 3/4
```

Therefore the best value is:

```text
3/4
```

---

### W = {c,d}

```text
skill(W) = 2 + 2 = 4
```

Internal shift:

```text
s3 = (c,d)
```

so:

```text
i(W) = 1
```

Fringe:

```text
∂(W) = {s2}
```

Since skill is even, `|S|` must be even.

The only possible even size is:

```text
|S| = 0
```

and:

```text
skill(W) + |S|
= 4
```

passes the lower bound.

Thus:

```text
S = ∅
```

is admissible.

Its value is:

```text
numerator
= 2*1 + 0
= 2

denominator
= 4 + 0 - 2
= 2

value
= 1
```

---

## Two-Worker Summary

| Crew    | skill(W) | i(W) | fringe          | admissible | best value |       |       |
| ------- | -------: | ---: | --------------- | ---------- | ---------: | ----- | ----- |
| `{a,b}` |        2 |    2 | `{s2}`          | none       |          — |       |       |
| `{a,c}` |        3 |    0 | `{s0,s1,s2,s3}` | `          |          S | =1,3` | `3/4` |
| `{a,d}` |        3 |    0 | `{s0,s1,s3}`    | `          |          S | =1,3` | `3/4` |
| `{b,c}` |        3 |    1 | `{s0,s1,s3}`    | `          |          S | =1,3` | `3/2` |
| `{b,d}` |        3 |    0 | `{s0,s1,s2,s3}` | `          |          S | =1,3` | `3/4` |
| `{c,d}` |        4 |    1 | `{s2}`          | `S=∅`      |        `1` |       |       |

After the singleton and two-worker cases, the current maximum is:

```text
3/2
```

It is not currently unique.

One maximizing pair so far is:

```text
W = {b}
S = {s0,s1,s2}
```

For `W = {b,c}`, each of these also has value `3/2`:

```text
S = {s0}
S = {s1}
S = {s3}
```

Larger crews must still be audited before making any uniqueness claim.

---

## Important Ratio Lesson

Adding more selected fringe shifts does not have a universal effect on the objective.

For `{a,c}`:

```text
|S| = 1 → value = 1/2
|S| = 3 → value = 3/4
```

so the ratio increases.

For `{b,c}`:

```text
|S| = 1 → value = 3/2
|S| = 3 → value = 5/4
```

so the ratio decreases.

Therefore the search cannot use a shortcut such as:

```text
always choose the largest S
```

or:

```text
always choose the smallest S
```

Every admissible candidate must be evaluated exactly.

````

---

# COPY INTO `MOCK_ORACLE.md`

Append this after the singleton section:

```markdown
## Two-Worker Crews

There are six two-worker crews.

For \(W=\{a,b\}\),

\[
skill(W)=2,\qquad
i(W)=2,\qquad
\partial(W)=\{s2\}.
\]

The only parity-compatible fringe size is \(|S|=0\), but then

\[
skill(W)+|S|=2<4.
\]

Hence there is no admissible pair with this crew.

For \(W=\{a,c\}\),

\[
skill(W)=3,\qquad
i(W)=0,\qquad
\partial(W)=\{s0,s1,s2,s3\}.
\]

Admissibility permits \(|S|=1\) or \(3\). Their values are

\[
\frac{1}{2}
\]

and

\[
\frac{3}{4},
\]

respectively. Thus the best value for this crew is \(3/4\).

For \(W=\{a,d\}\),

\[
skill(W)=3,\qquad
i(W)=0,\qquad
\partial(W)=\{s0,s1,s3\}.
\]

Again \(|S|=1\) or \(3\), giving values \(1/2\) and \(3/4\). Thus the best value is \(3/4\).

For \(W=\{b,c\}\),

\[
skill(W)=3,\qquad
i(W)=1,\qquad
\partial(W)=\{s0,s1,s3\}.
\]

For \(|S|=1\),

\[
value
=
\frac{2(1)+1}{3+1-2}
=
\frac32.
\]

Each of

\[
S=\{s0\},\qquad
S=\{s1\},\qquad
S=\{s3\}
\]

gives this value.

For \(|S|=3\),

\[
value
=
\frac{2(1)+3}{3+3-2}
=
\frac54.
\]

Thus the best value for this crew is \(3/2\).

For \(W=\{b,d\}\),

\[
skill(W)=3,\qquad
i(W)=0,\qquad
\partial(W)=\{s0,s1,s2,s3\}.
\]

Admissible sizes \(1\) and \(3\) give values \(1/2\) and \(3/4\), respectively. Thus the best value is \(3/4\).

For \(W=\{c,d\}\),

\[
skill(W)=4,\qquad
i(W)=1,\qquad
\partial(W)=\{s2\}.
\]

The admissible choice is \(S=\varnothing\), giving

\[
value
=
\frac{2(1)}{4-2}
=
1.
\]

After all singleton and two-worker cases, the largest value seen is

\[
\frac32.
\]

At this stage the maximum is not unique: it is attained by the singleton crew \(\{b\}\) with its full fringe and by several pairs based on \(W=\{b,c\}\).

The three-worker and four-worker crews remain to be checked.
````

Still **do not commit** and still **do not create Python files**.

Next we do the **four three-worker crews**:

[
{a,b,c},\quad
{a,b,d},\quad
{a,c,d},\quad
{b,c,d}.
]

This is the decisive step: one of these produces value (3), and we will derive exactly why it beats the current (3/2) leader rather than merely declaring it the winner.

===============================================================================================================================================================

Now we reach the **four three-worker crews**. This is the decisive part of the oracle because one of these crews jumps from our current best value

[
\frac32
]

to

[
3.
]

We are still doing **mathematics only**. No Python files yet.

The four three-worker subsets are:

[
{a,b,c},\quad
{a,b,d},\quad
{a,c,d},\quad
{b,c,d}.
]

There are exactly four because:

[
\binom43=4.
]

The analysis procedure does not change:

```text
1. skill(W)
2. internal shifts → i(W)
3. fringe shifts → ∂(W)
4. possible S ⊆ ∂(W)
5. parity
6. lower bound
7. exact objective
```

---

# 1. (W={a,b,c})

This crew contains the first three workers:

```text
a ══ b ── c      d
               |
              s3
```

More precisely, `d` is the only worker outside the crew.

## A. Compute `skill(W)`

The workers in the crew have skills:

```text
a → 1
b → 1
c → 2
```

Therefore:

[
skill({a,b,c})
==============

# 1+1+2

4.

]

So:

[
\boxed{skill(W)=4}.
]

---

## B. Compute the internal shifts

Remember:

> Internal means **both endpoints are inside (W)**.

Check every physical shift copy.

### `s0 = (a,b)`

Both `a` and `b` are in (W).

So:

[
s0\text{ is internal}.
]

### `s1 = (a,b)`

Again, both endpoints are in (W).

So:

[
s1\text{ is internal}.
]

And yes, it counts separately from `s0`.

### `s2 = (b,c)`

Both `b` and `c` are inside.

So:

[
s2\text{ is internal}.
]

### `s3 = (c,d)`

`c` is inside.

`d` is outside.

So `s3` is **not internal**.

Therefore the internal shifts are:

[
{s0,s1,s2}.
]

Hence:

[
\boxed{i(W)=3}.
]

This is already interesting: we have found a crew containing **three internal shift copies**.

---

# C. Compute the fringe

Now change the question from:

> both endpoints inside?

to:

> exactly one endpoint inside?

We already know:

```text
s0 → both inside → not fringe
s1 → both inside → not fringe
s2 → both inside → not fringe
```

For:

```text
s3 = (c,d)
```

we have:

```text
c inside
d outside
```

Exactly one endpoint is inside.

Therefore:

[
\boxed{\partial(W)={s3}}.
]

The fringe has only one shift.

---

# D. What can (S) be?

Since:

[
S\subseteq{s3},
]

there are exactly:

[
2^1=2
]

possible choices:

[
S=\varnothing
]

or:

[
S={s3}.
]

Equivalently:

[
|S|=0
]

or:

[
|S|=1.
]

---

# E. Apply parity

We have:

[
skill(W)=4.
]

Four is even.

Condition 3 requires:

[
skill(W)+|S|
]

to remain even.

Therefore (|S|) must be even.

Of the two possibilities:

```text
|S| = 0 → even
|S| = 1 → odd
```

only:

[
\boxed{|S|=0}
]

passes parity.

So immediately:

[
S={s3}
]

is inadmissible.

The only candidate surviving parity is:

[
S=\varnothing.
]

---

# F. Apply the lower bound

For the empty (S):

[
skill(W)+|S|
============

# 4+0

4.

]

Condition 4 requires:

[
4\ge4.
]

Yes.

Therefore:

[
\boxed{({a,b,c},\varnothing)\text{ is admissible}.}
]

---

# G. Evaluate the objective

Now, and only now, do we use:

[
value(W,S)
==========

\frac{2i(W)+|S|}
{skill(W)+|S|-2}.
]

We know:

[
i(W)=3,
]

[
|S|=0,
]

[
skill(W)=4.
]

### Numerator

[
2i(W)+|S|
=========

# 2(3)+0

6.

]

### Denominator

[
skill(W)+|S|-2
==============

# 4+0-2

2.

]

Therefore:

[
value(W,S)
==========

# \frac62

3.

]

So we have:

[
\boxed{
value({a,b,c},\varnothing)=3
}
]

🎯 This is our new leader.

Our previous best was:

[
\frac32.
]

Now we have:

[
3.
]

And:

[
3>\frac32.
]

So everything we saw among the singleton and two-worker crews has just been beaten.

But **we still cannot declare victory**.

There are three other three-worker crews plus the whole worker set.

---

# 2. (W={a,b,d})

Now the crew contains:

```text
a, b, d
```

and leaves only:

```text
c
```

outside.

## A. Skill

```text
a → 1
b → 1
d → 2
```

Therefore:

[
skill(W)
========

# 1+1+2

4.

]

So:

[
\boxed{skill(W)=4}.
]

---

# B. Internal shifts

Inspect every shift.

### `s0 = (a,b)`

Both inside.

Internal.

### `s1 = (a,b)`

Both inside.

Internal.

### `s2 = (b,c)`

`b` inside, `c` outside.

Not internal.

### `s3 = (c,d)`

`c` outside, `d` inside.

Not internal.

Thus:

[
\boxed{i(W)=2}.
]

The internal shifts are:

[
{s0,s1}.
]

---

# C. Fringe

Now look for exactly one endpoint inside.

```text
s0 → both inside → not fringe
s1 → both inside → not fringe

s2 = (b,c)
b inside, c outside
→ fringe

s3 = (c,d)
c outside, d inside
→ fringe
```

Therefore:

[
\boxed{
\partial(W)={s2,s3}
}.
]

Possible sizes:

[
|S|=0,1,2.
]

---

# D. Parity

Skill is:

[
4,
]

which is even.

So (|S|) must also be even.

Therefore:

[
|S|=0
]

or:

[
|S|=2.
]

The size-1 candidates are eliminated by parity.

---

# E. Lower bound

For (|S|=0):

[
4+0=4.
]

Pass.

For (|S|=2):

[
4+2=6.
]

Pass.

So there are two admissible cardinalities.

Because the fringe contains exactly two shifts, these correspond to:

[
S=\varnothing
]

and:

[
S={s2,s3}.
]

---

# F. Evaluate (S=\varnothing)

We have:

[
i(W)=2.
]

Numerator:

[
2(2)+0=4.
]

Denominator:

[
4+0-2=2.
]

Therefore:

[
value
=====

# \frac42

2.

]

So:

[
\boxed{
value({a,b,d},\varnothing)=2
}
]

This is a good competitor, but:

[
2<3.
]

It does not beat `{a,b,c}`.

---

# G. Evaluate (S={s2,s3})

Now:

[
|S|=2.
]

Numerator:

[
2(2)+2
======

6.

]

Denominator:

[
4+2-2
=====

4.

]

Therefore:

[
value
=====

# \frac64

\frac32.
]

So selecting both fringe shifts actually reduces the value from:

[
2
]

to:

[
\frac32.
]

Thus the best value for this crew is:

[
\boxed{2}.
]

Current leader remains:

[
3.
]

---

# 3. (W={a,c,d})

This crew contains:

```text
a, c, d
```

and leaves:

```text
b
```

outside.

## A. Skill

```text
a → 1
c → 2
d → 2
```

Therefore:

[
skill(W)
========

# 1+2+2

5.

]

So:

[
\boxed{skill(W)=5}.
]

---

# B. Internal shifts

Check all four.

### `s0 = (a,b)`

`a` inside, `b` outside.

Not internal.

### `s1 = (a,b)`

Same.

Not internal.

### `s2 = (b,c)`

`b` outside, `c` inside.

Not internal.

### `s3 = (c,d)`

Both `c` and `d` inside.

Internal.

Therefore:

[
\boxed{i(W)=1}.
]

The only internal shift is:

[
s3.
]

---

# C. Fringe

Now exactly one endpoint inside:

```text
s0 = (a,b)
a inside, b outside
→ fringe

s1 = (a,b)
a inside, b outside
→ fringe

s2 = (b,c)
b outside, c inside
→ fringe

s3 = (c,d)
both inside
→ not fringe
```

Therefore:

[
\boxed{
\partial(W)={s0,s1,s2}
}.
]

Possible sizes:

[
|S|=0,1,2,3.
]

---

# D. Parity

The skill is:

[
5,
]

which is odd.

So (|S|) must be odd to make the total even.

Thus:

[
|S|=1
]

or:

[
|S|=3.
]

---

# E. Lower bound

For (|S|=1):

[
5+1=6\ge4.
]

Pass.

For (|S|=3):

[
5+3=8\ge4.
]

Pass.

Both are admissible.

---

# F. Value when (|S|=1)

Numerator:

[
2(1)+1
======

3.

]

Denominator:

[
5+1-2
=====

4.

]

Therefore:

[
value
=====

\frac34.
]

---

# G. Value when (|S|=3)

Numerator:

[
2(1)+3
======

5.

]

Denominator:

[
5+3-2
=====

6.

]

Therefore:

[
value
=====

\frac56.
]

Compare:

[
\frac56>\frac34.
]

So the best value for this crew is:

[
\boxed{\frac56}.
]

Still far below:

[
3.
]

---

# 4. (W={b,c,d})

This crew contains:

```text
b, c, d
```

and leaves:

```text
a
```

outside.

## A. Skill

```text
b → 1
c → 2
d → 2
```

Therefore:

[
skill(W)
========

# 1+2+2

5.

]

So:

[
\boxed{skill(W)=5}.
]

---

# B. Internal shifts

### `s0 = (a,b)`

`a` outside, `b` inside.

Not internal.

### `s1 = (a,b)`

Same.

Not internal.

### `s2 = (b,c)`

Both inside.

Internal.

### `s3 = (c,d)`

Both inside.

Internal.

Therefore:

[
\boxed{i(W)=2}.
]

Internal shifts:

[
{s2,s3}.
]

---

# C. Fringe

```text
s0 = (a,b)
a outside, b inside
→ fringe

s1 = (a,b)
a outside, b inside
→ fringe

s2
both inside
→ not fringe

s3
both inside
→ not fringe
```

Thus:

[
\boxed{
\partial(W)={s0,s1}
}.
]

Possible sizes:

[
|S|=0,1,2.
]

---

# D. Parity

Skill is odd:

[
5.
]

Therefore (|S|) must be odd.

Among:

[
0,1,2,
]

only:

[
|S|=1
]

works.

The lower bound is automatic here:

[
5+1=6\ge4.
]

So any single fringe shift produces an admissible pair.

There are two such pairs:

[
S={s0}
]

or:

[
S={s1}.
]

Again, parallel copies produce two distinct candidate pairs.

---

# E. Objective

With:

[
i(W)=2,
]

and:

[
|S|=1,
]

the numerator is:

[
2(2)+1
======

5.

]

The denominator is:

[
5+1-2
=====

4.

]

Therefore:

[
value
=====

\frac54.
]

So:

[
\boxed{
\text{best value for }{b,c,d}=\frac54
}.
]

---

# Three-Worker Summary

Now we have:

| Crew (W) | skill | (i(W)) | fringe | admissible (|S|) | best value |
|---|---:|---:|---|---|---:|
| `{a,b,c}` | 4 | 3 | `{s3}` | 0 | **3** |
| `{a,b,d}` | 4 | 2 | `{s2,s3}` | 0, 2 | 2 |
| `{a,c,d}` | 5 | 1 | `{s0,s1,s2}` | 1, 3 | (5/6) |
| `{b,c,d}` | 5 | 2 | `{s0,s1}` | 1 | (5/4) |

Our leader is now:

[
\boxed{3}
]

at:

[
\boxed{
W={a,b,c},
\qquad
S=\varnothing
}.
]

And something significant happened:

The best value among all other three-worker crews is only:

[
2.
]

So within this size class, `{a,b,c}` is uniquely best.

---

# Why `{a,b,c}` Is So Strong

Let's compare the two strongest three-worker crews.

## `{a,b,c}`

```text
skill = 4
internal count = 3
S = ∅
```

So:

[
\frac{2(3)}{4-2}
================

# \frac62

3.

]

## `{a,b,d}`

```text
skill = 4
internal count = 2
S = ∅
```

So:

[
\frac{2(2)}{4-2}
================

# \frac42

2.

]

They have the **same skill denominator contribution**.

But `{a,b,c}` contains one additional internal shift:

```text
s2 = (b,c)
```

That extra internal copy contributes:

[
+2
]

to the numerator while leaving the denominator unchanged.

That is exactly why the value jumps from:

[
2
]

to:

[
3.
]

This is a structural explanation, not just arithmetic.

---

# Why the Empty `S` Is Allowed

This is worth making explicit because sometimes people mentally interpret “choose some fringe shifts” as “choose at least one.”

But mathematically:

[
S\subseteq\partial(W)
]

includes the empty subset.

For:

[
\partial(W)={s3},
]

the subsets are:

[
\varnothing
]

and:

[
{s3}.
]

So:

[
S=\varnothing
]

is absolutely legal under Condition 2.

It then survives Conditions 3 and 4 for `{a,b,c}`, which is why it becomes our current maximizing candidate.

This same fact will matter later when we use:

```python
range(len(fringe_edges) + 1)
```

because starting at subset size zero is what makes sure the empty subset is not omitted.

---

# COPY INTO `mock_notes_1.md`

Append this:

````markdown
## Three-Worker Crews

There are

\[
\binom{4}{3}=4
\]

three-worker crews:

```text
{a,b,c}
{a,b,d}
{a,c,d}
{b,c,d}
````

These cases are decisive because `{a,b,c}` produces a value larger than every singleton and two-worker candidate seen so far.

---

### W = {a,b,c}

```text
skill(W)
= 1 + 1 + 2
= 4
```

Internal shifts:

```text
s0 = (a,b) → internal
s1 = (a,b) → internal
s2 = (b,c) → internal
s3 = (c,d) → not internal
```

Therefore:

```text
i(W) = 3
```

The fringe is:

```text
∂(W) = {s3}
```

so:

```text
|S| = 0 or 1
```

Because `skill(W) = 4` is even, parity requires `|S|` even.

Thus only:

```text
|S| = 0
```

survives.

The total is:

```text
skill(W) + |S|
= 4
```

so the lower bound also passes.

Therefore:

```text
W = {a,b,c}
S = ∅
```

is admissible.

Its exact objective value is:

```text
numerator
= 2*i(W) + |S|
= 2*3 + 0
= 6

denominator
= skill(W) + |S| - 2
= 4 + 0 - 2
= 2

value
= 6/2
= 3
```

This becomes the new current maximum.

The other fringe choice:

```text
S = {s3}
```

gives total:

```text
4 + 1 = 5
```

which is odd, so it is inadmissible.

---

### W = {a,b,d}

```text
skill(W)
= 1 + 1 + 2
= 4
```

Internal shifts:

```text
s0 = (a,b)
s1 = (a,b)
```

so:

```text
i(W) = 2
```

Fringe:

```text
∂(W) = {s2,s3}
```

Since skill is even, `|S|` must be even:

```text
|S| = 0 or 2
```

Both satisfy the lower bound.

For `S = ∅`:

```text
numerator = 2*2 = 4
denominator = 4 - 2 = 2
value = 2
```

For `S = {s2,s3}`:

```text
numerator = 2*2 + 2 = 6
denominator = 4 + 2 - 2 = 4
value = 6/4 = 3/2
```

Therefore the best value for `{a,b,d}` is:

```text
2
```

---

### W = {a,c,d}

```text
skill(W)
= 1 + 2 + 2
= 5
```

Only:

```text
s3 = (c,d)
```

is internal, so:

```text
i(W) = 1
```

The fringe is:

```text
∂(W) = {s0,s1,s2}
```

Because skill is odd, `|S|` must be odd:

```text
|S| = 1 or 3
```

For `|S| = 1`:

```text
numerator = 2*1 + 1 = 3
denominator = 5 + 1 - 2 = 4
value = 3/4
```

For `|S| = 3`:

```text
numerator = 2*1 + 3 = 5
denominator = 5 + 3 - 2 = 6
value = 5/6
```

Therefore the best value for this crew is:

```text
5/6
```

---

### W = {b,c,d}

```text
skill(W)
= 1 + 2 + 2
= 5
```

Internal shifts:

```text
s2 = (b,c)
s3 = (c,d)
```

so:

```text
i(W) = 2
```

Fringe:

```text
∂(W) = {s0,s1}
```

Skill is odd, so `|S|` must be odd.

The only possible odd size is:

```text
|S| = 1
```

and:

```text
5 + 1 = 6 >= 4
```

so it is admissible.

Either:

```text
S = {s0}
```

or:

```text
S = {s1}
```

has:

```text
numerator
= 2*2 + 1
= 5

denominator
= 5 + 1 - 2
= 4

value
= 5/4
```

Therefore the best value for this crew is:

```text
5/4
```

---

## Three-Worker Summary

| Crew      | skill(W) | i(W) | fringe       | admissible | best value |       |       |
| --------- | -------: | ---: | ------------ | ---------- | ---------: | ----- | ----- |
| `{a,b,c}` |        4 |    3 | `{s3}`       | `S=∅`      |      **3** |       |       |
| `{a,b,d}` |        4 |    2 | `{s2,s3}`    | `          |          S | =0,2` | `2`   |
| `{a,c,d}` |        5 |    1 | `{s0,s1,s2}` | `          |          S | =1,3` | `5/6` |
| `{b,c,d}` |        5 |    2 | `{s0,s1}`    | `          |          S | =1`   | `5/4` |

The current maximum is now:

```text
3
```

at:

```text
W = {a,b,c}
S = ∅
```

The previous maximum of `3/2` has been strictly beaten.

---

## Why {a,b,c} is strong

Compare:

```text
{a,b,c}
skill = 4
internal shifts = 3
```

with:

```text
{a,b,d}
skill = 4
internal shifts = 2
```

With `S = ∅`, both have denominator:

```text
4 - 2 = 2
```

but `{a,b,c}` has one additional internal shift.

Because each internal shift contributes `2` to the numerator, that extra internal copy changes:

```text
4/2 = 2
```

into:

```text
6/2 = 3
```

The advantage comes from additional internal structure without additional skill cost.

---

## The Empty S Matters

Condition 2 requires:

```text
S ⊆ ∂(W)
```

A subset may be empty.

Therefore:

```text
S = ∅
```

is a legitimate candidate whenever the remaining admissibility conditions hold.

For `{a,b,c}`, the empty S is not merely allowed; it is the only parity-compatible fringe choice and produces the current maximum.

The later power-set enumeration must therefore include subset size zero.

````

---

# COPY INTO `MOCK_ORACLE.md`

Append:

```markdown
## Three-Worker Crews

For \(W=\{a,b,c\}\),

\[
skill(W)=4,\qquad
i(W)=3,\qquad
\partial(W)=\{s3\}.
\]

Since the crew skill is even, admissibility requires \(|S|\) even. The only possible even size is \(|S|=0\), so

\[
S=\varnothing.
\]

The lower bound is satisfied because

\[
skill(W)+|S|=4.
\]

Its exact value is

\[
value
=
\frac{2(3)+0}{4+0-2}
=
\frac62
=
3.
\]

Thus the current maximum becomes \(3\).

For \(W=\{a,b,d\}\),

\[
skill(W)=4,\qquad
i(W)=2,\qquad
\partial(W)=\{s2,s3\}.
\]

The admissible sizes are \(|S|=0\) and \(2\).

For \(S=\varnothing\),

\[
value
=
\frac{2(2)}{4-2}
=
2.
\]

For \(S=\{s2,s3\}\),

\[
value
=
\frac{2(2)+2}{4+2-2}
=
\frac64
=
\frac32.
\]

Thus the best value for this crew is \(2\).

For \(W=\{a,c,d\}\),

\[
skill(W)=5,\qquad
i(W)=1,\qquad
\partial(W)=\{s0,s1,s2\}.
\]

Admissibility permits \(|S|=1\) or \(3\). Their values are

\[
\frac{2(1)+1}{5+1-2}
=
\frac34
\]

and

\[
\frac{2(1)+3}{5+3-2}
=
\frac56.
\]

Thus the best value for this crew is \(5/6\).

For \(W=\{b,c,d\}\),

\[
skill(W)=5,\qquad
i(W)=2,\qquad
\partial(W)=\{s0,s1\}.
\]

The only admissible fringe size is \(|S|=1\), giving

\[
value
=
\frac{2(2)+1}{5+1-2}
=
\frac54.
\]

After all three-worker crews, the largest value is

\[
3,
\]

attained by

\[
W=\{a,b,c\},
\qquad
S=\varnothing.
\]

The full four-worker crew remains to be checked before the oracle can be locked.
````

Do **not commit yet**.

There is now only **one crew left**:

[
W={a,b,c,d}.
]

That case will finish the exhaustive hand audit. Then we will compare all 15 crews, establish whether the value-3 maximizer is unique, write the final **Oracle Lock**, and make the critical pre-code `mock1:` commit.

===============================================================================================================================================================

Now we finish the **hand oracle**. This is the last mathematical case before any checker code is allowed to exist.

There is only one crew left:

[
W={a,b,c,d}.
]

This is the entire worker set, and that fact makes the case especially useful because it tests whether you understand what happens to the fringe when there is **no outside**.

---

# Part 1 — Analyze the Full Crew

We take:

[
W={a,b,c,d}.
]

This is every worker in the graph.

The graph is:

```text
a ══ b ── c ── d
```

with physical shift copies:

```text
s0 = (a,b)
s1 = (a,b)
s2 = (b,c)
s3 = (c,d)
```

---

## Step A — Compute `skill(W)`

The worker skills are:

```text
a → 1
b → 1
c → 2
d → 2
```

Since **all four workers** are in (W):

[
skill(W)
========

# 1+1+2+2

6.

]

So:

[
\boxed{skill(W)=6}.
]

---

# Step B — Compute the internal count (i(W))

Remember the definition:

> A shift is internal when **both** of its workers belong to (W).

But (W) contains **every worker**.

Therefore every endpoint of every shift lies inside (W).

Let's still inspect them explicitly:

```text
s0 = (a,b)
a inside, b inside
→ internal

s1 = (a,b)
a inside, b inside
→ internal

s2 = (b,c)
b inside, c inside
→ internal

s3 = (c,d)
c inside, d inside
→ internal
```

So all four physical shift copies are internal:

[
{s0,s1,s2,s3}.
]

Therefore:

[
\boxed{i(W)=4}.
]

Again, `s0` and `s1` count separately.

---

# Step C — Compute the fringe (\partial(W))

Now ask the fringe question:

> Does the shift have **exactly one endpoint inside (W)**?

But there is no worker outside (W).

Every worker belongs to:

[
{a,b,c,d}.
]

Therefore every shift has:

```text
both endpoints inside
```

and **none** has one endpoint outside.

Thus:

[
\boxed{\partial(W)=\varnothing}.
]

This is a very useful boundary fact:

> If (W) is the entire vertex/worker set, its fringe is empty because there is nowhere outside the set for an edge to cross.

Compare this with your F7 capstone, where:

[
\partial_G(V(G))=\varnothing.
]

Same graph concept.

---

# Step D — What choices of (S) exist?

Condition 2 requires:

[
S\subseteq\partial(W).
]

But:

[
\partial(W)=\varnothing.
]

What subsets does the empty set have?

Exactly one:

[
\varnothing.
]

So:

[
\boxed{S=\varnothing}
]

is not merely one possibility. It is the **only** possibility.

And:

[
|S|=0.
]

---

# Step E — Check Condition 3: parity

We have:

[
skill(W)=6
]

and:

[
|S|=0.
]

Therefore:

[
skill(W)+|S|
============

# 6+0

6.

]

Six is even.

So Condition 3 passes:

[
\boxed{\text{parity passes}}.
]

---

# Step F — Check Condition 4: lower bound

Condition 4 requires:

[
skill(W)+|S|\ge4.
]

We have:

[
6\ge4.
]

So Condition 4 passes too.

Therefore:

[
\boxed{
({a,b,c,d},\varnothing)
\text{ is admissible}
}.
]

---

# Step G — Evaluate the objective

Now we are allowed to evaluate:

[
value(W,S)
==========

\frac{2i(W)+|S|}
{skill(W)+|S|-2}.
]

Substitute:

[
i(W)=4,
]

[
|S|=0,
]

[
skill(W)=6.
]

## Numerator

[
2i(W)+|S|
=========

# 2(4)+0

8.

]

## Denominator

[
skill(W)+|S|-2
==============

# 6+0-2

4.

]

Therefore:

[
value
=====

# \frac84

2.

]

So:

[
\boxed{
value({a,b,c,d},\varnothing)=2
}.
]

---

# Part 2 — Compare It to the Current Leader

Our current leader is:

[
W={a,b,c},
\qquad
S=\varnothing,
]

with:

[
value=3.
]

The whole crew gives:

[
2.
]

Therefore:

[
2<3.
]

The final remaining crew does **not** beat or tie the leader.

And now something important has happened:

> We have exhausted every nonempty (W\subseteq WORKERS).

There were:

[
2^4-1=15
]

such crews.

We have checked all 15.

Now we are finally entitled to lock the oracle.

---

# Part 3 — Review All 15 Crews

Here is the full audit in one place.

| Crew (W) | skill(W) | (i(W)) | fringe | admissible (|S|) | best value |
|---|---:|---:|---|---|---:|
| `{a}` | 1 | 0 | `{s0,s1}` | none | — |
| `{b}` | 1 | 0 | `{s0,s1,s2}` | 3 | (3/2) |
| `{c}` | 2 | 0 | `{s2,s3}` | 2 | (1) |
| `{d}` | 2 | 0 | `{s3}` | none | — |
| `{a,b}` | 2 | 2 | `{s2}` | none | — |
| `{a,c}` | 3 | 0 | `{s0,s1,s2,s3}` | 1, 3 | (3/4) |
| `{a,d}` | 3 | 0 | `{s0,s1,s3}` | 1, 3 | (3/4) |
| `{b,c}` | 3 | 1 | `{s0,s1,s3}` | 1, 3 | (3/2) |
| `{b,d}` | 3 | 0 | `{s0,s1,s2,s3}` | 1, 3 | (3/4) |
| `{c,d}` | 4 | 1 | `{s2}` | 0 | (1) |
| `{a,b,c}` | 4 | 3 | `{s3}` | 0 | **(3)** |
| `{a,b,d}` | 4 | 2 | `{s2,s3}` | 0, 2 | (2) |
| `{a,c,d}` | 5 | 1 | `{s0,s1,s2}` | 1, 3 | (5/6) |
| `{b,c,d}` | 5 | 2 | `{s0,s1}` | 1 | (5/4) |
| `{a,b,c,d}` | 6 | 4 | `∅` | 0 | (2) |

The largest value is:

[
3.
]

The next-highest value is:

[
2.
]

So there is a strict gap:

[
3>2.
]

That proves no other crew can tie the winner.

---

# Part 4 — Why the Winner Is Unique

The proposed winner is:

[
W^*={a,b,c}.
]

For that crew:

[
\partial(W^*)={s3}.
]

There are only two possible (S)'s:

[
\varnothing
]

and:

[
{s3}.
]

But:

[
skill(W^*)=4.
]

With:

[
S={s3},
]

we get:

[
4+1=5,
]

which is odd.

Therefore that pair is inadmissible.

So the **only admissible pair based on the winning crew** is:

[
({a,b,c},\varnothing).
]

And every other crew has best value at most:

[
2.
]

Therefore the maximizing **pair**, not merely the maximizing crew, is unique:

[
\boxed{
W^*={a,b,c},
\qquad
S^*=\varnothing
}
]

with:

[
\boxed{value=3}.
]

That is our locked known answer.

---

# Part 5 — What the Future Python Test Must Eventually Assert

We are **not writing this test yet**.

But this is the translation from our mathematics into the future Python representation.

We expect:

```python
result.value == Fraction(3, 1)
```

because:

[
3=\frac31.
]

We expect:

```python
result.W == frozenset({"a", "b", "c"})
```

because the maximizing crew is:

[
{a,b,c}.
]

And:

```python
result.S == frozenset()
```

because:

[
S^*=\varnothing.
]

That future test will not invent the expected answer.

It will simply encode what we just established independently.

---

# COPY INTO `mock_notes_1.md`

Paste this into your notes:

````markdown
## Full Worker Set

The final nonempty crew is:

```text
W = {a,b,c,d}
````

This is the entire worker set.

### Skill

```text
skill(W)
= 1 + 1 + 2 + 2
= 6
```

### Internal shifts

Every worker is inside `W`, so both endpoints of every shift are inside.

Therefore all four physical shift copies are internal:

```text
s0
s1
s2
s3
```

and:

```text
i(W) = 4
```

### Fringe

A fringe shift must have exactly one endpoint inside `W`.

Because `W` contains every worker, there is no outside worker.

Therefore:

```text
∂(W) = ∅
```

The empty set has exactly one subset:

```text
S = ∅
```

so:

```text
|S| = 0
```

### Admissibility

```text
skill(W) + |S|
= 6 + 0
= 6
```

Six is even, so Condition 3 passes.

Also:

```text
6 >= 4
```

so Condition 4 passes.

Thus:

```text
({a,b,c,d}, ∅)
```

is admissible.

### Objective

```text
numerator
= 2*i(W) + |S|
= 2*4 + 0
= 8

denominator
= skill(W) + |S| - 2
= 6 + 0 - 2
= 4

value
= 8/4
= 2
```

So the whole worker set has exact value:

```text
2
```

It does not beat the current leader `3`.

---

## Complete Hand Audit

There are:

```text
2^4 - 1 = 15
```

nonempty crews, and all 15 have now been examined.

| Crew W      | skill(W) | i(W) | fringe          | admissible | best value |       |       |
| ----------- | -------: | ---: | --------------- | ---------- | ---------: | ----- | ----- |
| `{a}`       |        1 |    0 | `{s0,s1}`       | none       |          — |       |       |
| `{b}`       |        1 |    0 | `{s0,s1,s2}`    | `          |          S | =3`   | `3/2` |
| `{c}`       |        2 |    0 | `{s2,s3}`       | `          |          S | =2`   | `1`   |
| `{d}`       |        2 |    0 | `{s3}`          | none       |          — |       |       |
| `{a,b}`     |        2 |    2 | `{s2}`          | none       |          — |       |       |
| `{a,c}`     |        3 |    0 | `{s0,s1,s2,s3}` | `          |          S | =1,3` | `3/4` |
| `{a,d}`     |        3 |    0 | `{s0,s1,s3}`    | `          |          S | =1,3` | `3/4` |
| `{b,c}`     |        3 |    1 | `{s0,s1,s3}`    | `          |          S | =1,3` | `3/2` |
| `{b,d}`     |        3 |    0 | `{s0,s1,s2,s3}` | `          |          S | =1,3` | `3/4` |
| `{c,d}`     |        4 |    1 | `{s2}`          | `S=∅`      |        `1` |       |       |
| `{a,b,c}`   |        4 |    3 | `{s3}`          | `S=∅`      |    **`3`** |       |       |
| `{a,b,d}`   |        4 |    2 | `{s2,s3}`       | `          |          S | =0,2` | `2`   |
| `{a,c,d}`   |        5 |    1 | `{s0,s1,s2}`    | `          |          S | =1,3` | `5/6` |
| `{b,c,d}`   |        5 |    2 | `{s0,s1}`       | `          |          S | =1`   | `5/4` |
| `{a,b,c,d}` |        6 |    4 | `∅`             | `S=∅`      |        `2` |       |       |

The largest competitor value outside the winner is:

```text
2
```

while the winning value is:

```text
3
```

Therefore the winner is strictly better than every competitor.

---

## Oracle Lock

The unique maximizing pair is:

```text
W* = {a,b,c}
S* = ∅
```

with exact value:

```text
3
```

The winning arithmetic is:

```text
skill(W*) = 4
i(W*) = 3
∂(W*) = {s3}
S* = ∅

numerator
= 2*3 + 0
= 6

denominator
= 4 + 0 - 2
= 2

value
= 6/2
= 3
```

The only other possible fringe choice for this crew is:

```text
S = {s3}
```

but then:

```text
skill(W*) + |S|
= 4 + 1
= 5
```

which is odd, so that pair is inadmissible.

Every other crew has best value at most `2`.

Therefore the maximizing pair itself is unique.

The future checker must return exactly:

```text
value = Fraction(3, 1)
W = frozenset({"a", "b", "c"})
S = frozenset()
```

This expected answer was derived before any checker code existed.

````

---

# COPY INTO `MOCK_ORACLE.md`

Append this final section:

```markdown
## Full Worker Set

For

\[
W=\{a,b,c,d\},
\]

all workers are included, so

\[
skill(W)=1+1+2+2=6.
\]

Every shift copy is internal:

\[
i(W)=4.
\]

Since there is no worker outside \(W\),

\[
\partial(W)=\varnothing.
\]

Thus the only possible choice is

\[
S=\varnothing.
\]

The pair is admissible because

\[
skill(W)+|S|=6
\]

is even and at least 4.

Its value is

\[
value
=
\frac{2(4)+0}{6+0-2}
=
\frac84
=
2.
\]

This does not beat the value \(3\) obtained by \(W=\{a,b,c\}\).

---

## Complete Competitor Audit

The best value obtainable for each nonempty crew is:

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

Every nonwinning crew has best value at most

\[
2.
\]

The proposed winner has value

\[
3.
\]

Hence no other crew can tie or exceed it.

---

## Oracle Lock

The unique maximizing pair is

\[
\boxed{
W^*=\{a,b,c\},
\qquad
S^*=\varnothing
}
\]

with exact value

\[
\boxed{3}.
\]

Indeed,

\[
skill(W^*)=4,
\qquad
i(W^*)=3,
\qquad
\partial(W^*)=\{s3\}.
\]

The empty fringe selection is admissible and gives

\[
value(W^*,S^*)
=
\frac{2(3)+0}{4+0-2}
=
3.
\]

The only other possible fringe selection is \(S=\{s3\}\), but then

\[
skill(W^*)+|S|
=
5,
\]

which is odd and therefore inadmissible.

Thus the maximizing pair itself is unique.

The future brute-force checker must return exactly:

- `value = Fraction(3, 1)`
- `W = frozenset({"a", "b", "c"})`
- `S = frozenset()`

This oracle was derived before any checker code was created.
````

---

# Now We Reach the Protocol Gate

Before doing anything else, **save both Markdown files**.

Then run:

```bash
git status
```

At this stage you should have something resembling:

```text
untracked: MOCK_ORACLE.md
untracked: mock_notes_1.md
```

There should still be **no**:

```text
mock_instance.py
mock_primitives.py
mock_admissibility.py
mock_evaluator.py
mock_search.py
test_mock.py
```

That is exactly what we want.

---

# Commit 1 — The Oracle Must Go First

Stage **only** the oracle:

```bash
git add MOCK_ORACLE.md
```

Now inspect:

```bash
git status
```

Prediction:

```text
Changes to be committed:
    new file: MOCK_ORACLE.md

Untracked files:
    mock_notes_1.md
```

That is good.

The notes may exist, but only the formal oracle is entering the first commit.

Now commit:

```bash
git commit -m "mock1: lock hand-derived crew-assignment oracle"
```

Then verify the timestamped boundary:

```bash
git log -1 --oneline
```

You should see something like:

```text
abc1234 mock1: lock hand-derived crew-assignment oracle
```

That commit is now the record that the mathematical answer existed **before checker code**.

---

# Commit 2 — Your Learning Notes

Before writing any Python, let's also commit your notes separately.

Run:

```bash
git add mock_notes_1.md
```

Then:

```bash
git commit -m "mock1: document problem model and hand-analysis process"
```

Then:

```bash
git status
```

Prediction:

```text
nothing to commit, working tree clean
```

Finally:

```bash
git log -2 --oneline
```

You should see, newest first, approximately:

```text
<hash> mock1: document problem model and hand-analysis process
<hash> mock1: lock hand-derived crew-assignment oracle
```

That ordering is fine because **both precede implementation**, while the oracle itself has its own earlier commit.

---

> **RULE TO BANK:** Exhaustive hand derivation means the eventual checker does not get to define reality. We independently examined all (2^4-1=15) nonempty crews, proved the unique optimum is (({a,b,c},\varnothing)) with value (3), and only now are we permitted to write implementation code.

Once those two commits are complete and `git status` is clean, tell me **“oracle committed.”** Then we start `mock_instance.py` from absolute zero: first representation choices, then data, then each validator invariant, with predictions and break tests just like we did for the capstone.
================================================================================================================================================================

We are now allowed to write the **first Python implementation file** because the oracle exists first in Git. From this point onward, we are translating already-established mathematics into software.

# Step 2 — Build `mock_instance.py`

The instance module has two jobs:

1. **Store the fixed problem data.**
2. **Reject malformed instance data before anything downstream trusts it.**

It does **not** compute admissibility, density, or search results. Those belong to later layers.

---

## 1. Preflight

First confirm you are starting this implementation step from a clean repository:

```bash
git status
```

We want:

```text
nothing to commit, working tree clean
```

Now create the first Python file:

```bash
code mock_instance.py
```

Confirm:

```bash
ls mock_instance.py
```

Expected:

```text
mock_instance.py
```

---

# 2. Translate the Mathematical Objects Into Python

We have three pieces of instance data:

```text
workers
shifts
skill values
```

We need a representation for each.

---

## `WORKERS` — use a `frozenset`

Mathematically:

[
WORKERS={a,b,c,d}.
]

In Python:

```python
WORKERS = frozenset({"a", "b", "c", "d"})
```

Why `frozenset`?

Because the workers form a mathematical set:

* order is not mathematically significant;
* duplicates make no sense;
* membership tests such as `"a" in WORKERS` are natural;
* the fixed instance should not accidentally mutate the worker set.

This is the same representation idea you used for the capstone vertex set.

---

# 3. `SHIFTS` — use a list of triples

Each physical shift is:

```text
(shift_id, worker1, worker2)
```

so:

```python
SHIFTS = [
    ("s0", "a", "b"),
    ("s1", "a", "b"),
    ("s2", "b", "c"),
    ("s3", "c", "d"),
]
```

Why a list?

Because the **physical copies must remain separate**.

These are distinct:

```python
("s0", "a", "b")
("s1", "a", "b")
```

even though the endpoints match.

A later loop should encounter both copies.

The list also preserves a stable order:

```text
s0
s1
s2
s3
```

That will eventually help make exhaustive enumeration deterministic.

---

# 4. `SKILL_VALUES` — use a dictionary

The mathematical function is:

```text
a → 1
b → 1
c → 2
d → 2
```

Python dictionaries are designed for exactly this kind of mapping:

```python
SKILL_VALUES = {
    "a": 1,
    "b": 1,
    "c": 2,
    "d": 2,
}
```

Then later:

```python
SKILL_VALUES["c"]
```

returns:

```text
2
```

This is directly analogous to your capstone's `F_VALUES`.

---

# 5. What Does `validate_instance()` Actually Protect?

The validator protects the **fixed input data**, not candidate queries.

This distinction matters:

```text
validate_instance()
    asks whether the graph itself is structurally trustworthy

is_admissible(W, S)
    will later ask whether one candidate pair is allowed
```

Those are different contracts.

The mock specification gives five minimum instance invariants.

We will implement exactly those five.

---

# Check 1 — `WORKERS` Must Be Nonempty

The problem requires actual workers.

So:

```python
if not WORKERS:
    raise ValueError("WORKERS must be nonempty")
```

If the worker set were empty, the entire fixed problem would be malformed.

This is an **instance error**, so we raise.

It is not an ordinary negative search result.

---

# Check 2 — No Shift May Pair a Worker With Themselves

A shift such as:

```python
("s3", "c", "c")
```

would be a loop.

But the specification explicitly says:

> No shift pairs a worker with themselves.

So every shift must satisfy:

[
worker1\neq worker2.
]

In Python:

```python
if worker1 == worker2:
```

then raise a named error.

I propose:

```text
shift s3 self-pairs worker 'c'
```

The exact exception line would be:

```text
ValueError: shift s3 self-pairs worker 'c'
```

The `!r` representation gives us the quotes around `"c"`.

---

# Check 3 — Every Shift Endpoint Must Be a Known Worker

Suppose somebody accidentally writes:

```python
("s3", "c", "x")
```

where `"x"` is not in:

```python
WORKERS
```

We do **not** want that malformed graph to survive until some later function fails mysteriously.

So for every shift:

```python
worker1 in WORKERS
worker2 in WORKERS
```

must both hold.

If not, we raise and name:

* the shift ID;
* the offending endpoint.

For example:

```text
ValueError: shift s3 has unknown worker 'x'
```

This follows the hardening lesson from the capstone:

> Catch the semantic contract violation rather than waiting for a mechanical `KeyError`.

---

# Check 4 — Every Shift ID Must Be Unique

This is one of the most important representation invariants.

Valid parallel shifts:

```python
("s0", "a", "b")
("s1", "a", "b")
```

Same endpoints.

Different IDs.

Invalid:

```python
("s0", "a", "b")
("s0", "a", "b")
```

Why dangerous?

Later, fringe sets and candidate (S) values will be represented using **shift IDs**.

If two physical shifts share `"s0"`, then:

```python
frozenset({"s0", "s0"})
```

collapses to:

```python
frozenset({"s0"})
```

and:

[
|S|
]

would silently undercount the physical shift copies.

That could produce mathematically wrong values without causing a crash.

So we use the same `seen`-set pattern you learned:

```python
seen_shift_ids = set()

for shift_id, ... in SHIFTS:
    if shift_id in seen_shift_ids:
        raise ValueError(...)
    seen_shift_ids.add(shift_id)
```

The logic is:

```text
first s0
→ unseen
→ record s0

s1
→ unseen
→ record s1

...

another s0
→ already seen
→ reject
```

---

# Check 5 — Every Worker Must Have a Positive Integer Skill

For each worker:

```python
worker in WORKERS
```

we first require a mapping entry:

```python
worker in SKILL_VALUES
```

If not:

```text
ValueError: missing skill value for worker 'c'
```

Then we require its value to be a **positive integer**.

So:

```text
1  ✓
2  ✓
5  ✓

0     ✗
-2    ✗
1.5   ✗
"2"   ✗
True  ✗
```

You might ask why `True` is listed as invalid when:

```python
isinstance(True, int)
```

is actually `True` in Python.

Python's `bool` type is a subclass of `int`.

So we deliberately use:

```python
type(skill_value) is not int
```

rather than:

```python
not isinstance(skill_value, int)
```

That expresses the contract:

> actual integer, not Boolean masquerading as one.

---

# 6. Notice What Is NOT In This Validator

There is **no** condition like:

[
skill(w)\le degree(w).
]

That existed in your capstone's active regime.

It does **not** exist in this mock specification.

So we must not pattern-replay:

```python
if SKILL_VALUES[worker] > degree[worker]:
    ...
```

That code would be mathematically unjustified here.

This is one of the main things the mock is testing:

> Reuse architecture; do not import assumptions.

---

# 7. Why This Module Should Be Silent

When another module eventually writes:

```python
from mock_instance import WORKERS, SHIFTS, SKILL_VALUES
```

we do not want importing the data module to unexpectedly print messages or execute a search.

So there will be **no top-level print** and no top-level call to:

```python
validate_instance()
```

The file consists only of:

```text
data
function definitions
```

That makes it a clean importable module.

---

# 8. Prediction Before Running Anything

With the correct locked instance, every validation condition passes:

```text
Check 1
WORKERS nonempty
→ pass

Check 2
no self-pairing
→ pass

Check 3
all shift endpoints known
→ pass

Check 4
shift IDs s0, s1, s2, s3 unique
→ pass

Check 5
all four workers have positive integer skills
→ pass
```

Therefore:

```python
validate_instance()
```

should return normally without printing anything.

Rather than temporarily altering the module to call itself, we can test it from the terminal:

```bash
python -c "from mock_instance import validate_instance; validate_instance(); print('mock instance valid')"
```

Prediction:

```text
mock instance valid
```

The function itself prints nothing.

The explicit terminal `print(...)` runs only if validation reaches the end without raising.

---

# 9. Do This Now

Paste the complete `mock_instance.py` below into VS Code and save it.

Then run:

```bash
python -c "from mock_instance import validate_instance; validate_instance(); print('mock instance valid')"
```

Expected:

```text
mock instance valid
```

Then run:

```bash
python mock_instance.py
```

Expected:

**nothing at all.**

That proves the module itself remains silent when loaded as a script because it only defines data and functions.

Do **not commit yet**. We will prove at least the two highest-risk guards reject malformed data before committing the instance module.

---

# COPY INTO `mock_notes_1.md`

````markdown
## Step 2 — Instance Representation and Validation

The first implementation layer is `mock_instance.py`.

Its responsibilities are deliberately narrow:

1. store the fixed problem data;
2. validate the graph-level invariants.

It does not:

- evaluate candidate admissibility,
- compute density,
- enumerate subsets,
- search for a maximizer.

Those responsibilities belong to later modules.

---

### Representing WORKERS

The mathematical worker set is:

```text
{a,b,c,d}
````

The Python representation is:

```python
WORKERS = frozenset({"a", "b", "c", "d"})
```

A `frozenset` is appropriate because:

* workers form a mathematical set;
* order is not mathematically meaningful;
* duplicates are impossible;
* membership testing is natural;
* the fixed worker set should not mutate accidentally.

---

### Representing SHIFTS

Each physical shift copy has the structure:

```text
(shift_id, worker1, worker2)
```

The fixed shifts are:

```python
SHIFTS = [
    ("s0", "a", "b"),
    ("s1", "a", "b"),
    ("s2", "b", "c"),
    ("s3", "c", "d"),
]
```

A list is useful because:

* every physical copy remains present;
* parallel copies remain distinct;
* stable input order is preserved;
* later deterministic enumeration can inherit that order.

The two shifts:

```text
s0 = (a,b)
s1 = (a,b)
```

have identical endpoints but different identities.

Parallelism means:

```text
same endpoints
different IDs
```

---

### Representing Skill Values

Worker skill is a mapping:

```text
worker -> positive integer skill
```

so a dictionary is appropriate:

```python
SKILL_VALUES = {
    "a": 1,
    "b": 1,
    "c": 2,
    "d": 2,
}
```

---

## Instance Validation Contract

`validate_instance()` protects the fixed graph data.

An invalid instance is not an ordinary search outcome. It means downstream mathematics cannot be trusted.

Therefore:

```text
bad instance
→ raise ValueError
```

The validator is fail-fast: the first discovered violation stops execution.

Messages should identify the offending worker or shift.

---

### Check 1 — Nonempty Worker Set

Require:

```text
WORKERS != ∅
```

If the worker set is empty:

```text
ValueError: WORKERS must be nonempty
```

---

### Check 2 — No Self-Pairing

Every shift:

```text
(shift_id, worker1, worker2)
```

must satisfy:

```text
worker1 != worker2
```

A shift such as:

```text
("s3", "c", "c")
```

violates the problem specification.

The validator should name the shift and worker.

---

### Check 3 — Every Shift Endpoint Is Known

For every shift:

```text
worker1 in WORKERS
worker2 in WORKERS
```

must hold.

For example:

```text
("s3", "c", "x")
```

must be rejected because `"x"` is not a known worker.

This check converts a potentially confusing downstream mechanical failure into a named semantic contract violation.

The lesson carried from F7 hardening is:

> Validate the prerequisites of later computations before those computations can fail for the wrong reason.

---

### Check 4 — Unique Shift IDs

Every physical shift copy must have a unique ID.

Valid:

```text
("s0", "a", "b")
("s1", "a", "b")
```

Invalid:

```text
("s0", "a", "b")
("s0", "a", "b")
```

The check uses a `seen_shift_ids` set:

```text
start seen = ∅

first ID:
    if unseen → record it

later ID:
    if already seen → reject
```

This is not cosmetic metadata validation.

Later:

```text
fringe(W)
```

will return shift IDs and candidate `S` will be represented as a `frozenset` of IDs.

If two physical shifts shared one ID, converting selected IDs to a `frozenset` could collapse the copies:

```text
{"s0", "s0"} → {"s0"}
```

Then:

```text
|S|
```

would silently undercount physical shifts.

That would corrupt the mathematical search space without necessarily causing an exception.

---

### Check 5 — Positive Integer Skills

Every worker in `WORKERS` must have a skill value.

Each skill must satisfy:

```text
type(skill) is int
skill > 0
```

Using:

```python
type(skill_value) is int
```

rather than merely:

```python
isinstance(skill_value, int)
```

also rejects Boolean values, since Python treats `bool` as a subclass of `int`.

---

## What Is Deliberately NOT Validated

The F7 capstone contained an active-regime assumption:

```text
f(v) <= d(v)
```

No corresponding assumption exists in the Crew-Assignment Density specification.

Therefore `mock_instance.py` must not invent:

```text
skill(worker) <= degree(worker)
```

or any related check.

This mock tests the distinction:

> Reuse software patterns only when the new mathematical specification supports them.

Architecture may transfer.

Assumptions do not transfer automatically.

---

## Module Silence

`mock_instance.py` contains only:

* fixed data,
* function definitions.

It contains no top-level print and no top-level validation call.

This keeps it silent when imported by future modules.

The valid instance can be exercised externally with:

```bash
python -c "from mock_instance import validate_instance; validate_instance(); print('mock instance valid')"
```

Expected:

```text
mock instance valid
```

Running:

```bash
python mock_instance.py
```

should produce no output.

---

> **RULE TO BANK:** The instance layer establishes whether the fixed input data is trustworthy. Validate representation invariants there, especially invariants whose violation could silently change the mathematical object represented by the code.

````

# COPY INTO `mock_instance.py`

```python
# ==================================================================================================
# MOCK EXIT 1 — CREW-ASSIGNMENT INSTANCE
# ==================================================================================================
#
# PURPOSE:
#
# Store the fixed Crew-Assignment Density instance and validate the
# graph-level assumptions required by every later checker component.
#
#
# THIS MODULE CONTAINS:
#
# 1. WORKERS
# 2. SHIFTS
# 3. SKILL_VALUES
# 4. validate_instance()
#
#
# RESPONSIBILITY BOUNDARY:
#
# This module validates the INSTANCE.
#
# It does NOT:
#
#     - judge candidate admissibility,
#     - evaluate the objective,
#     - enumerate candidate pairs,
#     - search for a maximizer.
#
# Those belong to later modules.
#
#
# MODULE BEHAVIOR:
#
# This file is intentionally silent.
#
# Importing it should define data and functions without printing or
# automatically running validation.
#
# ==================================================================================================


# ==================================================================================================
# WORKERS
# ==================================================================================================
#
# The fixed worker set is:
#
#     {a, b, c, d}
#
# A frozenset is used because:
#
#     - workers form a mathematical set,
#     - order is not mathematically significant,
#     - duplicates should not exist,
#     - membership checks are natural,
#     - the fixed instance should not accidentally mutate this set.
#
# ==================================================================================================


WORKERS = frozenset({"a", "b", "c", "d"})


# ==================================================================================================
# SHIFTS
# ==================================================================================================
#
# Every physical shift copy has the form:
#
#     (shift_id, worker1, worker2)
#
# The fixed instance contains:
#
#     s0 = (a, b)
#     s1 = (a, b)    parallel copy of s0
#     s2 = (b, c)
#     s3 = (c, d)
#
# A list preserves:
#
#     - every physical shift copy,
#     - the distinction between parallel copies,
#     - stable input order.
#
# IMPORTANT:
#
#     s0 and s1 have the same endpoints,
#
# but:
#
#     s0 != s1
#
# because they are distinct physical shifts.
#
# Shift IDs therefore function as the identities of physical copies.
#
# ==================================================================================================


SHIFTS = [
    ("s0", "a", "b"),
    ("s1", "a", "b"),
    ("s2", "b", "c"),
    ("s3", "c", "d"),
]


# ==================================================================================================
# SKILL VALUES
# ==================================================================================================
#
# Skill is a positive-integer function on workers:
#
#     a -> 1
#     b -> 1
#     c -> 2
#     d -> 2
#
# A dictionary represents:
#
#     worker -> skill value
#
# ==================================================================================================


SKILL_VALUES = {
    "a": 1,
    "b": 1,
    "c": 2,
    "d": 2,
}


# ==================================================================================================
# VALIDATE INSTANCE
# ==================================================================================================
#
# PURPOSE:
#
# Reject malformed fixed-instance data before any downstream computation
# is trusted.
#
#
# FAILURE CONTRACT:
#
#     invalid instance -> raise ValueError immediately
#
# The validator is fail-fast:
#
#     the first discovered violation stops execution.
#
# Each error message should name the offending worker or shift whenever
# there is a specific culprit.
#
#
# CHECK 1 — NONEMPTY WORKER SET
#
# Require:
#
#     WORKERS != empty
#
#
# CHECK 2 — NO SELF-PAIRING
#
# Every shift:
#
#     (shift_id, worker1, worker2)
#
# must satisfy:
#
#     worker1 != worker2
#
# Example invalid shift:
#
#     ("s3", "c", "c")
#
#
# CHECK 3 — KNOWN SHIFT ENDPOINTS
#
# Every endpoint appearing in SHIFTS must belong to WORKERS.
#
# Require:
#
#     worker1 in WORKERS
#     worker2 in WORKERS
#
# Example invalid shift:
#
#     ("s3", "c", "x")
#
# where:
#
#     "x" not in WORKERS
#
#
# CHECK 4 — UNIQUE SHIFT IDs
#
# Every physical shift copy must have its own unique ID.
#
# Parallel shifts are allowed to have:
#
#     the same endpoints
#
# but must have:
#
#     different IDs.
#
# The uniqueness check uses a seen-set walk:
#
#     seen_shift_ids = set()
#
# For each shift ID:
#
#     if already seen:
#         raise ValueError
#
#     otherwise:
#         add it to seen_shift_ids
#
# This invariant is essential because later fringe sets and candidate S
# values will represent physical shifts by ID.
#
# Duplicate IDs could otherwise collapse distinct physical copies when
# converted to a frozenset and silently corrupt |S|.
#
#
# CHECK 5 — POSITIVE INTEGER SKILL VALUES
#
# Every worker must have a skill value.
#
# Every skill value must satisfy:
#
#     type(skill_value) is int
#
# and:
#
#     skill_value > 0
#
# Using exact type comparison deliberately rejects Boolean values.
#
#
# IMPORTANT NON-CHECK:
#
# There is NO skill-versus-degree condition in this problem.
#
# The F7 capstone's condition:
#
#     f(v) <= d(v)
#
# must NOT be pattern-replayed here.
#
# ==================================================================================================


def validate_instance():
    # Check 1 — the worker set must be nonempty.
    if not WORKERS:
        raise ValueError("WORKERS must be nonempty")

    # Check 2 — no shift may pair a worker with themselves.
    for shift_id, worker1, worker2 in SHIFTS:
        if worker1 == worker2:
            raise ValueError(
                f"shift {shift_id} self-pairs worker {worker1!r}"
            )

    # Check 3 — every shift endpoint must be a known worker.
    for shift_id, worker1, worker2 in SHIFTS:
        if worker1 not in WORKERS:
            raise ValueError(
                f"shift {shift_id} has unknown worker {worker1!r}"
            )

        if worker2 not in WORKERS:
            raise ValueError(
                f"shift {shift_id} has unknown worker {worker2!r}"
            )

    # Check 4 — every physical shift copy must have a unique shift ID.
    seen_shift_ids = set()

    for shift_id, _worker1, _worker2 in SHIFTS:
        if shift_id in seen_shift_ids:
            raise ValueError(f"duplicate shift ID {shift_id!r}")

        seen_shift_ids.add(shift_id)

    # Check 5 — every worker must have a positive integer skill value.
    for worker in WORKERS:
        if worker not in SKILL_VALUES:
            raise ValueError(f"missing skill value for worker {worker!r}")

        skill_value = SKILL_VALUES[worker]

        if type(skill_value) is not int or skill_value <= 0:
            raise ValueError(
                f"skill({worker}) must be a positive integer, "
                f"got {skill_value!r}"
            )
````

Now save `mock_instance.py` and run:

```bash
python -c "from mock_instance import validate_instance; validate_instance(); print('mock instance valid')"
```

Prediction:

```text
mock instance valid
```

Then:

```bash
python mock_instance.py
```

Prediction: **silent**.

Bring me those two outputs next. Then we will deliberately break the **duplicate-ID guard** and **unknown-worker guard**, predict their exact messages, prove them rejecting, restore the instance, and only then make the `mock1:` instance commit.
==================================================================================================================================================================

Excellent. Both predictions matched exactly:

```text
python -c "... validate_instance() ..."
→ mock instance valid
```

and:

```text
python mock_instance.py
→ silent
```

That establishes two different facts:

1. **The correct instance passes all five guards.**
2. **`mock_instance.py` is a clean module**: merely executing/importing it does not automatically validate or print anything.

Now we prove the guards reject malformed data. We will do **one corruption at a time**, because the validator is fail-fast.

# Step 2A — Break the Unique-Shift-ID Invariant

We start with the more dangerous invariant: duplicate shift IDs.

The valid first two shifts are:

```python
("s0", "a", "b"),
("s1", "a", "b"),
```

They are parallel copies:

```text
same endpoints
different IDs
```

We will temporarily corrupt the second one to:

```python
("s0", "a", "b"),
```

giving:

```python
("s0", "a", "b"),
("s0", "a", "b"),
```

There are still physically two entries in the `SHIFTS` list, but they now claim the same identity.

---

## Predict Before Running

Look at the validator's order:

```text
Check 1 — WORKERS nonempty
Check 2 — no self-pairing
Check 3 — every endpoint known
Check 4 — unique shift IDs
Check 5 — positive integer skills
```

With our deliberate corruption:

### Check 1

`WORKERS` is still:

```python
frozenset({"a", "b", "c", "d"})
```

so:

```text
PASS
```

### Check 2

Both corrupted shifts are still:

```text
(a,b)
```

with:

```text
a != b
```

so:

```text
PASS
```

### Check 3

Both `a` and `b` still belong to `WORKERS`.

So:

```text
PASS
```

### Check 4

Now the seen-set walk begins.

Initially:

```python
seen_shift_ids = set()
```

which means:

```text
seen_shift_ids = {}
conceptually empty
```

First shift:

```text
shift_id = "s0"
```

Question:

```python
"s0" in seen_shift_ids
```

Answer:

```text
False
```

So we execute:

```python
seen_shift_ids.add("s0")
```

Now:

```text
seen_shift_ids = {"s0"}
```

Second shift:

```text
shift_id = "s0"
```

Question:

```python
"s0" in seen_shift_ids
```

Answer:

```text
True
```

So this fires:

```python
raise ValueError(f"duplicate shift ID {shift_id!r}")
```

Because:

```python
shift_id == "s0"
```

and `!r` uses the representation of the string, the exact message is:

```text
duplicate shift ID 's0'
```

Therefore the final traceback line should be **exactly**:

```text
ValueError: duplicate shift ID 's0'
```

Check 5 should never run because the validator stops immediately at Check 4.

---

# Why This Test Matters More Than Just Seeing an Exception

We are proving the exact failure mode that would otherwise be dangerous.

Without this guard, later we could have:

```text
physical shift 1 → "s0"
physical shift 2 → "s0"
```

and a fringe list could conceptually contain:

```python
["s0", "s0"]
```

But later candidate (S) will become a `frozenset`:

```python
frozenset(["s0", "s0"])
```

which becomes:

```python
frozenset({"s0"})
```

Its length is:

```python
1
```

even though two physical shifts were selected.

That changes:

[
|S|
]

and therefore can change:

* admissibility,
* numerator,
* denominator,
* objective,
* search result.

Worse, it could happen **silently**.

So the validator is preventing representation corruption, not merely enforcing pretty IDs.

---

# What to Do Now

Replace `mock_instance.py` temporarily with the complete version below.

Then run:

```bash
python -c "from mock_instance import validate_instance; validate_instance()"
```

Do **not** add a `print("valid")` this time.

We expect the function to fail.

### Exact predicted last line

```text
ValueError: duplicate shift ID 's0'
```

Paste the traceback's last line when you get it.

Do **not commit this broken version**.

After we see the duplicate-ID guard fire, we will restore `s1`, then deliberately break an endpoint and prove the unknown-worker guard fires.

---

# COPY INTO `mock_notes_1.md`

````markdown
## Step 2A — Proving the Unique-Shift-ID Guard Rejects

The valid instance first passed all five instance guards:

```bash
python -c "from mock_instance import validate_instance; validate_instance(); print('mock instance valid')"
````

produced:

```text
mock instance valid
```

Running the module directly:

```bash
python mock_instance.py
```

produced no output.

This establishes two separate properties:

1. the valid instance passes validation;
2. `mock_instance.py` remains silent and import-safe.

---

### Why rejection must also be tested

A validator that has only been observed accepting valid data is not fully exercised.

The F1/F7 guard doctrine is:

> Prove that a guard rejects the malformed input it was designed to reject, not merely that valid input passes.

Because `validate_instance()` is fail-fast, corrupt only one invariant at a time.

---

### Deliberate duplicate-ID corruption

The correct parallel shifts are:

```python
("s0", "a", "b")
("s1", "a", "b")
```

Parallel copies are allowed to have the same endpoints, but they must have different IDs.

For the rejection test, temporarily change the second copy to:

```python
("s0", "a", "b")
```

so the first two entries become:

```python
("s0", "a", "b")
("s0", "a", "b")
```

The graph still contains two physical list entries, but the representation now gives both copies the same identity.

---

### Expected control flow

The validator checks, in order:

```text
Check 1 — WORKERS nonempty
Check 2 — no self-pairing
Check 3 — endpoints known
Check 4 — shift IDs unique
Check 5 — positive integer skill values
```

The deliberate duplicate passes Checks 1–3.

Check 4 uses:

```python
seen_shift_ids = set()
```

The walk is:

```text
first "s0":
    not in seen_shift_ids
    add it

seen_shift_ids = {"s0"}

second "s0":
    already in seen_shift_ids
    raise ValueError
```

The exception is constructed by:

```python
raise ValueError(f"duplicate shift ID {shift_id!r}")
```

Since:

```text
shift_id = "s0"
```

the exact expected traceback line is:

```text
ValueError: duplicate shift ID 's0'
```

The `!r` conversion displays the string representation, including quotes.

---

### Why duplicate IDs are dangerous

Later, fringe shifts are represented by shift IDs and candidate `S` values become `frozenset`s.

If two physical shift copies shared one ID, something conceptually like:

```python
["s0", "s0"]
```

would become:

```python
frozenset({"s0"})
```

The two physical copies would collapse into one set element.

Then:

```text
|S|
```

would silently undercount selected physical shifts.

Because `|S|` appears in:

```text
admissibility parity
lower-bound condition
objective numerator
objective denominator
```

the entire mathematical search could be corrupted without an obvious crash.

Therefore:

> Unique shift IDs are a representation invariant, not cosmetic metadata.

---

### Predicted rejection command

```bash
python -c "from mock_instance import validate_instance; validate_instance()"
```

Expected final traceback line:

```text
ValueError: duplicate shift ID 's0'
```

The broken instance must never be committed.

````

# COPY INTO `mock_instance.py`

```python
# ==================================================================================================
# MOCK EXIT 1 — CREW-ASSIGNMENT INSTANCE
# ==================================================================================================
#
# PURPOSE:
#
# Store the fixed Crew-Assignment Density instance and validate the
# graph-level assumptions required by every later checker component.
#
#
# THIS MODULE CONTAINS:
#
# 1. WORKERS
# 2. SHIFTS
# 3. SKILL_VALUES
# 4. validate_instance()
#
#
# RESPONSIBILITY BOUNDARY:
#
# This module validates the INSTANCE.
#
# It does NOT:
#
#     - judge candidate admissibility,
#     - evaluate the objective,
#     - enumerate candidate pairs,
#     - search for a maximizer.
#
# Those belong to later modules.
#
#
# MODULE BEHAVIOR:
#
# This file is intentionally silent.
#
# Importing it should define data and functions without printing or
# automatically running validation.
#
# ==================================================================================================


# ==================================================================================================
# WORKERS
# ==================================================================================================
#
# The fixed worker set is:
#
#     {a, b, c, d}
#
# A frozenset is used because:
#
#     - workers form a mathematical set,
#     - order is not mathematically significant,
#     - duplicates should not exist,
#     - membership checks are natural,
#     - the fixed instance should not accidentally mutate this set.
#
# ==================================================================================================


WORKERS = frozenset({"a", "b", "c", "d"})


# ==================================================================================================
# SHIFTS
# ==================================================================================================
#
# Every physical shift copy has the form:
#
#     (shift_id, worker1, worker2)
#
# IMPORTANT:
#
# This version is TEMPORARILY CORRUPTED to exercise the unique-ID guard.
#
# The correct parallel copies are:
#
#     ("s0", "a", "b")
#     ("s1", "a", "b")
#
# For this rejection test, both are temporarily assigned:
#
#     "s0"
#
# The validator should reject the second occurrence.
#
# This broken version must not be committed.
#
# ==================================================================================================


SHIFTS = [
    ("s0", "a", "b"),
    ("s0", "a", "b"),  # TEMPORARY BREAK — correct ID is "s1"
    ("s2", "b", "c"),
    ("s3", "c", "d"),
]


# ==================================================================================================
# SKILL VALUES
# ==================================================================================================
#
# Skill is a positive-integer function on workers:
#
#     a -> 1
#     b -> 1
#     c -> 2
#     d -> 2
#
# ==================================================================================================


SKILL_VALUES = {
    "a": 1,
    "b": 1,
    "c": 2,
    "d": 2,
}


# ==================================================================================================
# VALIDATE INSTANCE
# ==================================================================================================
#
# FAILURE CONTRACT:
#
#     invalid instance -> raise ValueError immediately
#
# The validator is fail-fast.
#
#
# CHECK 1 — NONEMPTY WORKER SET
#
#     WORKERS must be nonempty.
#
#
# CHECK 2 — NO SELF-PAIRING
#
#     Every shift must satisfy:
#
#         worker1 != worker2
#
#
# CHECK 3 — KNOWN SHIFT ENDPOINTS
#
#     Every endpoint must belong to WORKERS.
#
#
# CHECK 4 — UNIQUE SHIFT IDs
#
#     Every physical shift copy must have its own ID.
#
# The check uses:
#
#     seen_shift_ids = set()
#
# and scans the shifts in stable list order.
#
# For this temporary broken instance:
#
#     first "s0"  -> unseen -> add
#     second "s0" -> already seen -> raise
#
# Exact predicted error:
#
#     ValueError: duplicate shift ID 's0'
#
#
# CHECK 5 — POSITIVE INTEGER SKILL VALUES
#
#     Every worker must have a skill value.
#
#     Every skill must satisfy:
#
#         type(skill_value) is int
#         skill_value > 0
#
#
# IMPORTANT:
#
# There is no skill-versus-degree condition in this problem.
#
# ==================================================================================================


def validate_instance():
    # Check 1 — the worker set must be nonempty.
    if not WORKERS:
        raise ValueError("WORKERS must be nonempty")

    # Check 2 — no shift may pair a worker with themselves.
    for shift_id, worker1, worker2 in SHIFTS:
        if worker1 == worker2:
            raise ValueError(
                f"shift {shift_id} self-pairs worker {worker1!r}"
            )

    # Check 3 — every shift endpoint must be a known worker.
    for shift_id, worker1, worker2 in SHIFTS:
        if worker1 not in WORKERS:
            raise ValueError(
                f"shift {shift_id} has unknown worker {worker1!r}"
            )

        if worker2 not in WORKERS:
            raise ValueError(
                f"shift {shift_id} has unknown worker {worker2!r}"
            )

    # Check 4 — every physical shift copy must have a unique shift ID.
    seen_shift_ids = set()

    for shift_id, _worker1, _worker2 in SHIFTS:
        if shift_id in seen_shift_ids:
            raise ValueError(f"duplicate shift ID {shift_id!r}")

        seen_shift_ids.add(shift_id)

    # Check 5 — every worker must have a positive integer skill value.
    for worker in WORKERS:
        if worker not in SKILL_VALUES:
            raise ValueError(f"missing skill value for worker {worker!r}")

        skill_value = SKILL_VALUES[worker]

        if type(skill_value) is not int or skill_value <= 0:
            raise ValueError(
                f"skill({worker}) must be a positive integer, "
                f"got {skill_value!r}"
            )
````

Run:

```bash
python -c "from mock_instance import validate_instance; validate_instance()"
```

Expected last line:

```text
ValueError: duplicate shift ID 's0'
```

Once you paste that result, we restore the correct `"s1"` and move directly to the **unknown-worker endpoint break**.

==================================================================================================================================================================

Perfect. ✅ The duplicate-ID guard has now been **proven rejecting**, not merely written.

The exact predicted line appeared:

```text
ValueError: duplicate shift ID 's0'
```

That establishes that the `seen_shift_ids` walk works as intended.

Now we move to the second high-risk structural invariant: **every shift endpoint must be a known worker**.

# Step 2B — Prove the Unknown-Worker Guard Rejects

First, restore the duplicate-ID corruption.

Change:

```python
("s0", "a", "b"),
("s0", "a", "b"),
```

back to:

```python
("s0", "a", "b"),
("s1", "a", "b"),
```

Now deliberately corrupt `s3`.

The correct shift is:

```python
("s3", "c", "d"),
```

Temporarily change it to:

```python
("s3", "c", "x"),
```

where:

```text
"x" not in WORKERS
```

Our worker set is only:

```python
frozenset({"a", "b", "c", "d"})
```

---

## Predict the Control Flow Before Running

The validator is ordered:

```text
Check 1 — WORKERS nonempty
Check 2 — no self-pairing
Check 3 — every endpoint known
Check 4 — unique shift IDs
Check 5 — positive integer skills
```

For the deliberately malformed shift:

```python
("s3", "c", "x")
```

### Check 1

`WORKERS` is still nonempty.

```text
PASS
```

### Check 2

The endpoints are:

```text
"c"
"x"
```

and:

```python
"c" != "x"
```

so it is not a self-pairing loop.

```text
PASS
```

### Check 3

The validator first asks:

```python
worker1 not in WORKERS
```

Here:

```python
worker1 == "c"
```

and `"c"` is known.

So that part passes.

Then it asks:

```python
worker2 not in WORKERS
```

Here:

```python
worker2 == "x"
```

and:

```text
"x" not in {"a", "b", "c", "d"}
```

So this guard fires:

```python
raise ValueError(
    f"shift {shift_id} has unknown worker {worker2!r}"
)
```

Substitute:

```text
shift_id = "s3"
worker2 = "x"
```

The exact constructed message is:

```text
shift s3 has unknown worker 'x'
```

Therefore the traceback's final line should be exactly:

```text
ValueError: shift s3 has unknown worker 'x'
```

Checks 4 and 5 are never reached because the validator is fail-fast.

---

# Why We Put This Check Before Anything Derived From the Edges

Suppose we did **not** validate endpoint membership.

Later code may reasonably assume:

> Every endpoint appearing in `SHIFTS` is actually a worker in this graph.

A malformed endpoint could then produce a mechanical failure somewhere else—or worse, contaminate a graph computation.

The validator gives us the semantic diagnosis immediately:

```text
shift s3 has unknown worker 'x'
```

rather than making us reverse-engineer some later failure.

This is the same hardening principle you learned in the capstone:

> Validate the prerequisites of a computation before performing that computation.

---

# Run the Break Test

After pasting the temporary broken file below, run:

```bash
python -c "from mock_instance import validate_instance; validate_instance()"
```

### Prediction

The traceback should end:

```text
ValueError: shift s3 has unknown worker 'x'
```

Do **not** commit this version.

Once we see that exact line, we will:

1. restore `s3` to `("s3", "c", "d")`;
2. run the passing validation again;
3. run `python mock_instance.py` and confirm silence;
4. lint `mock_instance.py`;
5. commit the completed instance module.

---

# COPY INTO `mock_notes_1.md`

````markdown
## Step 2B — Proving the Unknown-Worker Guard Rejects

The duplicate-shift-ID guard was exercised first.

The temporary corruption:

```python
("s0", "a", "b")
("s0", "a", "b")
````

produced the exact expected failure:

```text
ValueError: duplicate shift ID 's0'
```

This proves the unique-ID guard actually rejects duplicated physical-shift identities.

The instance must now be restored before testing a different guard, because `validate_instance()` is fail-fast. If the duplicate ID remained present, it could mask a later violation.

---

### Deliberate Unknown-Worker Corruption

Restore the correct parallel IDs:

```python
("s0", "a", "b")
("s1", "a", "b")
```

Then temporarily change:

```python
("s3", "c", "d")
```

to:

```python
("s3", "c", "x")
```

The fixed worker set is:

```text
{a,b,c,d}
```

so:

```text
"x" not in WORKERS
```

---

### Predicted Control Flow

The validator order is:

```text
Check 1 — nonempty WORKERS
Check 2 — no self-pairing
Check 3 — known endpoints
Check 4 — unique shift IDs
Check 5 — positive integer skills
```

For:

```python
("s3", "c", "x")
```

Check 1 passes because the worker set is nonempty.

Check 2 passes because:

```text
"c" != "x"
```

Check 3 then examines the endpoints.

The first endpoint:

```text
"c"
```

belongs to `WORKERS`.

The second endpoint:

```text
"x"
```

does not.

Therefore the validator executes:

```python
raise ValueError(
    f"shift {shift_id} has unknown worker {worker2!r}"
)
```

With:

```text
shift_id = "s3"
worker2 = "x"
```

the exact expected traceback line is:

```text
ValueError: shift s3 has unknown worker 'x'
```

Because validation is fail-fast, Checks 4 and 5 are not executed after this failure.

---

### Why This Guard Matters

A structural data layer should reject malformed graph objects at the point where their actual contract is known.

An unknown endpoint is not merely a later dictionary or membership problem.

The actual violation is:

> A shift refers to a worker that does not belong to the graph.

Naming that violation directly makes failures easier to diagnose and prevents downstream code from operating under a false assumption.

The broader rule is:

> Validate the prerequisites of a computation before performing the computation.

---

### Break-Test Command

Run:

```bash
python -c "from mock_instance import validate_instance; validate_instance()"
```

Predicted final traceback line:

```text
ValueError: shift s3 has unknown worker 'x'
```

This deliberately corrupted version must not be committed.

After the rejection is observed, restore:

```python
("s3", "c", "d")
```

before making the instance-module commit.

````

# COPY INTO `mock_instance.py`

```python
# ==================================================================================================
# MOCK EXIT 1 — CREW-ASSIGNMENT INSTANCE
# ==================================================================================================
#
# PURPOSE:
#
# Store the fixed Crew-Assignment Density instance and validate the
# graph-level assumptions required by every later checker component.
#
#
# THIS MODULE CONTAINS:
#
# 1. WORKERS
# 2. SHIFTS
# 3. SKILL_VALUES
# 4. validate_instance()
#
#
# RESPONSIBILITY BOUNDARY:
#
# This module validates the INSTANCE.
#
# It does NOT:
#
#     - judge candidate admissibility,
#     - evaluate the objective,
#     - enumerate candidate pairs,
#     - search for a maximizer.
#
# Those belong to later modules.
#
#
# MODULE BEHAVIOR:
#
# This file is intentionally silent.
#
# Importing it should define data and functions without printing or
# automatically running validation.
#
# ==================================================================================================


# ==================================================================================================
# WORKERS
# ==================================================================================================
#
# The fixed worker set is:
#
#     {a, b, c, d}
#
# A frozenset is used because:
#
#     - workers form a mathematical set,
#     - order is not mathematically significant,
#     - duplicates should not exist,
#     - membership checks are natural,
#     - the fixed instance should not accidentally mutate this set.
#
# ==================================================================================================


WORKERS = frozenset({"a", "b", "c", "d"})


# ==================================================================================================
# SHIFTS
# ==================================================================================================
#
# Every physical shift copy has the form:
#
#     (shift_id, worker1, worker2)
#
# The correct fixed instance is:
#
#     s0 = (a, b)
#     s1 = (a, b)    parallel copy
#     s2 = (b, c)
#     s3 = (c, d)
#
#
# IMPORTANT:
#
# This version is TEMPORARILY CORRUPTED to exercise the
# known-endpoint guard.
#
# The correct final shift:
#
#     ("s3", "c", "d")
#
# is temporarily replaced by:
#
#     ("s3", "c", "x")
#
# Since:
#
#     "x" not in WORKERS
#
# validate_instance() must reject it before later code can trust the graph.
#
# This broken version must not be committed.
#
# ==================================================================================================


SHIFTS = [
    ("s0", "a", "b"),
    ("s1", "a", "b"),
    ("s2", "b", "c"),
    ("s3", "c", "x"),  # TEMPORARY BREAK — correct endpoint is "d"
]


# ==================================================================================================
# SKILL VALUES
# ==================================================================================================
#
# Skill is a positive-integer function on workers:
#
#     a -> 1
#     b -> 1
#     c -> 2
#     d -> 2
#
# A dictionary represents:
#
#     worker -> skill value
#
# ==================================================================================================


SKILL_VALUES = {
    "a": 1,
    "b": 1,
    "c": 2,
    "d": 2,
}


# ==================================================================================================
# VALIDATE INSTANCE
# ==================================================================================================
#
# PURPOSE:
#
# Reject malformed fixed-instance data before any downstream computation
# is trusted.
#
#
# FAILURE CONTRACT:
#
#     invalid instance -> raise ValueError immediately
#
# The validator is fail-fast.
#
#
# CHECK 1 — NONEMPTY WORKER SET
#
# Require:
#
#     WORKERS != empty
#
#
# CHECK 2 — NO SELF-PAIRING
#
# Every shift:
#
#     (shift_id, worker1, worker2)
#
# must satisfy:
#
#     worker1 != worker2
#
#
# CHECK 3 — KNOWN SHIFT ENDPOINTS
#
# Every endpoint appearing in SHIFTS must belong to WORKERS.
#
# Require:
#
#     worker1 in WORKERS
#     worker2 in WORKERS
#
# For the temporary broken shift:
#
#     ("s3", "c", "x")
#
# the first endpoint is known:
#
#     "c" in WORKERS
#
# but the second is not:
#
#     "x" not in WORKERS
#
# Exact predicted failure:
#
#     ValueError: shift s3 has unknown worker 'x'
#
#
# CHECK 4 — UNIQUE SHIFT IDs
#
# Every physical shift copy must have its own unique ID.
#
# Parallel shifts may share endpoints but may not share IDs.
#
# The uniqueness check uses a seen-set walk:
#
#     seen_shift_ids = set()
#
#
# CHECK 5 — POSITIVE INTEGER SKILL VALUES
#
# Every worker must have a skill value.
#
# Every skill value must satisfy:
#
#     type(skill_value) is int
#     skill_value > 0
#
#
# IMPORTANT NON-CHECK:
#
# There is no skill-versus-degree condition in this problem.
#
# ==================================================================================================


def validate_instance():
    # Check 1 — the worker set must be nonempty.
    if not WORKERS:
        raise ValueError("WORKERS must be nonempty")

    # Check 2 — no shift may pair a worker with themselves.
    for shift_id, worker1, worker2 in SHIFTS:
        if worker1 == worker2:
            raise ValueError(
                f"shift {shift_id} self-pairs worker {worker1!r}"
            )

    # Check 3 — every shift endpoint must be a known worker.
    for shift_id, worker1, worker2 in SHIFTS:
        if worker1 not in WORKERS:
            raise ValueError(
                f"shift {shift_id} has unknown worker {worker1!r}"
            )

        if worker2 not in WORKERS:
            raise ValueError(
                f"shift {shift_id} has unknown worker {worker2!r}"
            )

    # Check 4 — every physical shift copy must have a unique shift ID.
    seen_shift_ids = set()

    for shift_id, _worker1, _worker2 in SHIFTS:
        if shift_id in seen_shift_ids:
            raise ValueError(f"duplicate shift ID {shift_id!r}")

        seen_shift_ids.add(shift_id)

    # Check 5 — every worker must have a positive integer skill value.
    for worker in WORKERS:
        if worker not in SKILL_VALUES:
            raise ValueError(f"missing skill value for worker {worker!r}")

        skill_value = SKILL_VALUES[worker]

        if type(skill_value) is not int or skill_value <= 0:
            raise ValueError(
                f"skill({worker}) must be a positive integer, "
                f"got {skill_value!r}"
            )
````

Now run:

```bash
python -c "from mock_instance import validate_instance; validate_instance()"
```

and paste the **last traceback line**. We are expecting:

```text
ValueError: shift s3 has unknown worker 'x'
```

> **RULE TO BANK:** With a fail-fast validator, restore the previous deliberate corruption before testing the next invariant. Otherwise an earlier guard can mask the one you intended to prove.

==================================================================================================================================================================

Excellent. The second structural guard also fired **exactly as predicted**:

```text
ValueError: shift s3 has unknown worker 'x'
```

So we have now proved both of the highest-risk representation invariants reject bad data:

```text
duplicate shift ID      → rejected ✓
unknown shift endpoint  → rejected ✓
```

Now we restore the instance, prove the valid state again, lint only this mock file, and commit Step 2.

# Step 2C — Restore and Close the Instance Module

## 1. Restore `s3`

Change the temporary broken shift:

```python
("s3", "c", "x"),
```

back to:

```python
("s3", "c", "d"),
```

The final `SHIFTS` list must therefore be:

```python
SHIFTS = [
    ("s0", "a", "b"),
    ("s1", "a", "b"),
    ("s2", "b", "c"),
    ("s3", "c", "d"),
]
```

We also want the comments in `mock_instance.py` restored to describe the **real instance**, not a temporary break test. The complete clean file is at the end of this response.

---

# 2. Re-prove the Passing Case

After saving the restored file, run:

```bash
python -c "from mock_instance import validate_instance; validate_instance(); print('mock instance valid')"
```

## Prediction

All five checks should pass:

```text
Check 1 — WORKERS nonempty             ✓
Check 2 — no self-pairing              ✓
Check 3 — all endpoints known          ✓
Check 4 — all shift IDs unique         ✓
Check 5 — all skills positive integers ✓
```

Then the explicit terminal print executes.

Expected output:

```text
mock instance valid
```

This matters because after deliberately corrupting data, we always verify that we restored the canonical instance correctly.

---

# 3. Confirm the Module Is Silent Again

Run:

```bash
python mock_instance.py
```

Prediction:

```text
no output
```

Why?

Because the file contains only:

```text
constants
function definitions
```

It has no top-level:

```python
validate_instance()
```

and no top-level `print()`.

This is the same module discipline you learned earlier:

> Importing a module should not unexpectedly execute demonstrations or validation unless that behavior is deliberately part of the module contract.

---

# 4. Run a Scoped Ruff Check

We do **not** want:

```bash
ruff check .
```

because that would drag historical files into this mock step.

Instead:

```bash
ruff check mock_instance.py
```

Prediction:

```text
All checks passed!
```

If Ruff reports something in `mock_instance.py`, paste it before changing anything.

---

# 5. Inspect Git Before Staging

Run:

```bash
git status
```

You will likely see `mock_instance.py` as a new file and `mock_notes_1.md` as modified if you have been adding the notes blocks.

That is fine.

We are going to keep implementation and learning notes as separate commits.

---

# 6. Commit the Instance Module

Stage **only** the implementation:

```bash
git add mock_instance.py
```

Check:

```bash
git status
```

You want `mock_instance.py` under:

```text
Changes to be committed:
```

and `mock_notes_1.md`, if modified, should remain unstaged.

Now commit:

```bash
git commit -m "mock1: add validated crew-assignment instance"
```

Then verify:

```bash
git log -1 --oneline
```

You should see the new `mock1:` commit.

---

# 7. Commit the Notes for This Phase

Then stage the accumulated notes:

```bash
git add mock_notes_1.md
```

Commit:

```bash
git commit -m "mock1: document instance design and validation proofs"
```

Finally:

```bash
git status
```

Prediction:

```text
nothing to commit, working tree clean
```

At that point our repository history tells a very clean story:

```text
oracle mathematically derived
        ↓
oracle committed
        ↓
problem-analysis notes committed
        ↓
instance representation implemented
        ↓
guards deliberately broken and proven
        ↓
valid instance restored
        ↓
instance implementation committed
        ↓
validation learning notes committed
```

Only after that do we move to the three mathematical primitives.

---

# What We Have Built So Far

Notice the layering:

```text
MOCK_ORACLE.md
    tells us what is mathematically true

mock_instance.py
    tells the program what the fixed data is
    and proves the data satisfies its structural contract
```

We have **not** yet taught Python what:

```text
skill(W)
i(W)
∂(W)
```

mean.

Those will be the next module:

```text
mock_primitives.py
```

And the oracle already gives us hand-computed values we can use to predict those functions before running them.

For example, we already know:

```text
skill({a,b,c}) = 4

i({a,b}) = 2

i({a,b,c}) = 3

∂({a,b}) = {s2}

∂({b}) = {s0,s1,s2}

∂(WORKERS) = ∅
```

That is the next important transition:

> We derived the quantities mathematically first; now we will encode them as small reusable functions.

---

# COPY INTO `mock_notes_1.md`

````markdown
## Step 2C — Instance Validation Complete

The second deliberate rejection test targeted an unknown shift endpoint.

The temporary malformed shift was:

```python
("s3", "c", "x")
````

while the worker set was:

```text
{a,b,c,d}
```

Therefore:

```text
"x" not in WORKERS
```

The validator correctly reached the known-endpoint guard and raised exactly:

```text
ValueError: shift s3 has unknown worker 'x'
```

This proves that malformed shift endpoints are rejected at the instance boundary rather than being allowed to reach downstream computations.

---

### Structural Guards Proven So Far

Two high-risk representation invariants were deliberately broken and observed rejecting:

#### Duplicate shift identity

Temporary corruption:

```python
("s0", "a", "b")
("s0", "a", "b")
```

Observed failure:

```text
ValueError: duplicate shift ID 's0'
```

This prevents distinct physical shift copies from silently collapsing when represented later as shift-ID sets.

#### Unknown shift endpoint

Temporary corruption:

```python
("s3", "c", "x")
```

Observed failure:

```text
ValueError: shift s3 has unknown worker 'x'
```

This ensures every endpoint appearing in the graph actually belongs to the worker set.

---

## Why Break Tests Are Restored One at a Time

`validate_instance()` is fail-fast.

That means:

```text
first violation found
→ raise
→ stop execution
```

Therefore each deliberate corruption must be restored before testing another guard.

Otherwise an earlier violation can mask the later guard that the test is supposed to exercise.

The workflow is:

```text
valid instance
    ↓
introduce exactly one corruption
    ↓
predict exact failure
    ↓
run validator
    ↓
observe intended guard
    ↓
restore canonical data
    ↓
move to next corruption
```

---

## Canonical Instance Restored

After the break tests, the shift data is restored to:

```python
SHIFTS = [
    ("s0", "a", "b"),
    ("s1", "a", "b"),
    ("s2", "b", "c"),
    ("s3", "c", "d"),
]
```

The valid instance should again satisfy all five guards:

```text
1. WORKERS is nonempty.
2. No shift self-pairs a worker.
3. Every shift endpoint belongs to WORKERS.
4. Every physical shift copy has a unique shift ID.
5. Every worker has a positive integer skill value.
```

The passing validation command is:

```bash
python -c "from mock_instance import validate_instance; validate_instance(); print('mock instance valid')"
```

Expected output:

```text
mock instance valid
```

Running:

```bash
python mock_instance.py
```

should remain silent because the module contains only data and function definitions.

---

## Scoped Tooling

The mock should be checked without dragging unrelated historical exercises into the tooling pass.

Use:

```bash
ruff check mock_instance.py
```

rather than:

```bash
ruff check .
```

The scope of a tooling command is part of the command's behavior.

A repository-wide command means repository-wide consequences.

---

## Instance Layer Complete

The software architecture now has two established layers:

```text
MOCK_ORACLE.md
    independent mathematical truth
            ↓
mock_instance.py
    fixed data + structural validation
```

The next layer will encode the three mathematical quantities repeatedly used in the oracle:

```text
skill(W)
i(W)
∂(W)
```

These belong in:

```text
mock_primitives.py
```

The oracle already provides known values that can be used as predictions before the functions are executed.

Examples include:

```text
skill({a,b,c}) = 4

i({a,b}) = 2

i({a,b,c}) = 3

∂({a,b}) = {s2}

∂({b}) = {s0,s1,s2}

∂(WORKERS) = ∅
```

The implementation should reproduce these independently hand-derived quantities.

> **RULE TO BANK:** Restore the canonical input after every deliberate break test and re-prove the passing state before committing. A rejection test proves the guard; the final passing run proves the repository was not left corrupted.

````

# COPY INTO `mock_instance.py`

```python
# ==================================================================================================
# MOCK EXIT 1 — CREW-ASSIGNMENT INSTANCE
# ==================================================================================================
#
# PURPOSE:
#
# Store the fixed Crew-Assignment Density instance and validate the
# graph-level assumptions required by every later checker component.
#
#
# THIS MODULE CONTAINS:
#
# 1. WORKERS
# 2. SHIFTS
# 3. SKILL_VALUES
# 4. validate_instance()
#
#
# RESPONSIBILITY BOUNDARY:
#
# This module validates the INSTANCE.
#
# It does NOT:
#
#     - judge candidate admissibility,
#     - evaluate the objective,
#     - enumerate candidate pairs,
#     - search for a maximizer.
#
# Those responsibilities belong to later modules.
#
#
# MODULE BEHAVIOR:
#
# This file is intentionally silent.
#
# Importing or directly executing it defines data and functions without
# printing or automatically running validation.
#
# ==================================================================================================


# ==================================================================================================
# WORKERS
# ==================================================================================================
#
# The fixed worker set is:
#
#     {a, b, c, d}
#
# A frozenset is used because:
#
#     - workers form a mathematical set,
#     - order is not mathematically significant,
#     - duplicates should not exist,
#     - membership checks are natural,
#     - the fixed instance should not accidentally mutate this set.
#
# ==================================================================================================


WORKERS = frozenset({"a", "b", "c", "d"})


# ==================================================================================================
# SHIFTS
# ==================================================================================================
#
# Every physical shift copy has the form:
#
#     (shift_id, worker1, worker2)
#
# The fixed instance contains:
#
#     s0 = (a, b)
#     s1 = (a, b)    parallel copy of s0
#     s2 = (b, c)
#     s3 = (c, d)
#
# A list is used because:
#
#     - every physical shift copy remains present,
#     - parallel copies remain distinct,
#     - stable input order is preserved.
#
# IMPORTANT:
#
#     s0 and s1 have the same endpoints,
#
# but:
#
#     s0 != s1
#
# because they are distinct physical shifts.
#
# Parallel copies therefore have:
#
#     same endpoints
#     different IDs
#
# ==================================================================================================


SHIFTS = [
    ("s0", "a", "b"),
    ("s1", "a", "b"),
    ("s2", "b", "c"),
    ("s3", "c", "d"),
]


# ==================================================================================================
# SKILL VALUES
# ==================================================================================================
#
# Skill is a positive-integer function on workers:
#
#     a -> 1
#     b -> 1
#     c -> 2
#     d -> 2
#
# A dictionary represents:
#
#     worker -> skill value
#
# ==================================================================================================


SKILL_VALUES = {
    "a": 1,
    "b": 1,
    "c": 2,
    "d": 2,
}


# ==================================================================================================
# VALIDATE INSTANCE
# ==================================================================================================
#
# PURPOSE:
#
# Reject malformed fixed-instance data before any downstream computation
# is trusted.
#
#
# FAILURE CONTRACT:
#
#     invalid instance -> raise ValueError immediately
#
# The validator is fail-fast:
#
#     the first discovered violation stops execution.
#
# Each failure message names the offending shift or worker whenever there
# is a specific culprit.
#
#
# CHECK 1 — NONEMPTY WORKER SET
#
# Require:
#
#     WORKERS != empty
#
#
# CHECK 2 — NO SELF-PAIRING
#
# Every shift:
#
#     (shift_id, worker1, worker2)
#
# must satisfy:
#
#     worker1 != worker2
#
# Example invalid shift:
#
#     ("s3", "c", "c")
#
#
# CHECK 3 — KNOWN SHIFT ENDPOINTS
#
# Every endpoint appearing in SHIFTS must belong to WORKERS.
#
# Require:
#
#     worker1 in WORKERS
#     worker2 in WORKERS
#
# Example invalid shift:
#
#     ("s3", "c", "x")
#
# where:
#
#     "x" not in WORKERS
#
#
# CHECK 4 — UNIQUE SHIFT IDs
#
# Every physical shift copy must have its own unique ID.
#
# Parallel shifts may have:
#
#     the same endpoints
#
# but must have:
#
#     different IDs.
#
# The uniqueness check uses a seen-set walk:
#
#     seen_shift_ids = set()
#
# For every shift ID:
#
#     if the ID has already been seen:
#         raise ValueError
#
#     otherwise:
#         add the ID to seen_shift_ids
#
# This is a representation invariant.
#
# Later, fringe shifts and candidate S values will represent physical
# shift copies by ID.
#
# Duplicate IDs could therefore cause two distinct physical shifts to
# collapse into one element of a frozenset, silently corrupting |S|.
#
#
# CHECK 5 — POSITIVE INTEGER SKILL VALUES
#
# Every worker must have a skill value.
#
# Every skill value must satisfy:
#
#     type(skill_value) is int
#
# and:
#
#     skill_value > 0
#
# Exact type comparison deliberately rejects Boolean values.
#
#
# IMPORTANT NON-CHECK:
#
# There is NO skill-versus-degree condition in the Crew-Assignment
# Density specification.
#
# The F7 capstone assumption:
#
#     f(v) <= d(v)
#
# must not be imported into this problem.
#
# ==================================================================================================


def validate_instance():
    # Check 1 — the worker set must be nonempty.
    if not WORKERS:
        raise ValueError("WORKERS must be nonempty")

    # Check 2 — no shift may pair a worker with themselves.
    for shift_id, worker1, worker2 in SHIFTS:
        if worker1 == worker2:
            raise ValueError(
                f"shift {shift_id} self-pairs worker {worker1!r}"
            )

    # Check 3 — every shift endpoint must be a known worker.
    for shift_id, worker1, worker2 in SHIFTS:
        if worker1 not in WORKERS:
            raise ValueError(
                f"shift {shift_id} has unknown worker {worker1!r}"
            )

        if worker2 not in WORKERS:
            raise ValueError(
                f"shift {shift_id} has unknown worker {worker2!r}"
            )

    # Check 4 — every physical shift copy must have a unique shift ID.
    seen_shift_ids = set()

    for shift_id, _worker1, _worker2 in SHIFTS:
        if shift_id in seen_shift_ids:
            raise ValueError(f"duplicate shift ID {shift_id!r}")

        seen_shift_ids.add(shift_id)

    # Check 5 — every worker must have a positive integer skill value.
    for worker in WORKERS:
        if worker not in SKILL_VALUES:
            raise ValueError(f"missing skill value for worker {worker!r}")

        skill_value = SKILL_VALUES[worker]

        if type(skill_value) is not int or skill_value <= 0:
            raise ValueError(
                f"skill({worker}) must be a positive integer, "
                f"got {skill_value!r}"
            )
````

Now restore/save this final version and run, in order:

```bash
python -c "from mock_instance import validate_instance; validate_instance(); print('mock instance valid')"
python mock_instance.py
ruff check mock_instance.py
git status
```

If those results match the predictions, make the two commits:

```bash
git add mock_instance.py
git commit -m "mock1: add validated crew-assignment instance"

git add mock_notes_1.md
git commit -m "mock1: document instance design and validation proofs"

git status
```

Then we begin **`mock_primitives.py`**, and I’ll teach all three functions from their mathematical definitions before we write a line of executable code.

==================================================================================================================================================================

Good. We now begin the **second implementation layer**: the mathematical primitives.

The instance layer answered:

> What is the fixed graph, and is its data structurally valid?

The primitives layer answers:

> Given a particular crew (W), what are the basic mathematical quantities associated with it?

We are going to build these **one at a time**, not all three at once:

```text
1. skill_of(W)
2. internal_shift_count(W)
3. fringe(W)
```

We will not commit `mock_primitives.py` until all three are built, predicted against the oracle, and exercised.

# Step 3A — Create `mock_primitives.py`

First make sure the previous step is clean:

```bash
git status
```

Ideally:

```text
nothing to commit, working tree clean
```

Now create:

```bash
code mock_primitives.py
```

Confirm:

```bash
ls mock_primitives.py
```

Expected:

```text
mock_primitives.py
```

---

# 1. What Is a “Primitive”?

Here, “primitive” does not mean a Python primitive type like `int`.

It means:

> A small, foundational computation that more complicated checker logic will build on.

Our later admissibility function will need:

[
skill(W)
]

The evaluator will need:

[
skill(W)
]

and:

[
i(W).
]

The search will need:

[
\partial(W)
]

in order to know which possible (S)'s exist.

So the dependency structure is:

```text
fixed instance
      ↓
mathematical primitives
      ↓
admissibility + evaluator
      ↓
search
```

If the primitives are wrong, everything above them can be perfectly written and still return mathematically wrong answers.

That is why these tiny functions matter so much.

---

# 2. Primitive 1 — `skill_of(W)`

Mathematically, the definition is:

[
skill(W)=\sum_{w\in W}skill(w).
]

That means:

> Look at every worker in the crew and add that worker's stored skill value.

For example:

[
W={a,b,c}.
]

The skills are:

```text
a → 1
b → 1
c → 2
```

Therefore:

[
skill({a,b,c})
==============

# 1+1+2

4.

]

There is no graph-edge reasoning involved in this function.

It does not care about:

```text
s0
s1
s2
s3
```

at all.

It only needs:

```text
WORKERS
SKILL_VALUES
```

That is why our initial import should be:

```python
from mock_instance import SKILL_VALUES, WORKERS
```

We should **not** import `SHIFTS` yet merely because this module will eventually need it. At this moment, no executable function uses `SHIFTS`.

That keeps the file free of unused imports and makes each dependency explicit.

---

# 3. What Should Happen If `W` Contains an Unknown Worker?

Suppose someone calls:

```python
skill_of({"a", "x"})
```

where:

```text
"x" not in WORKERS
```

There are two possible philosophies.

We could let this line:

```python
SKILL_VALUES[worker]
```

eventually raise:

```text
KeyError: 'x'
```

Or we can establish a clear query contract and raise something semantic:

```text
ValueError: W contains unknown worker 'x'
```

I prefer the second.

Why?

`validate_instance()` proves that the **stored instance** is internally valid.

But it does not prove that every future caller will submit a valid **query crew**.

These are different things:

```text
instance validation
    "Is the graph itself valid?"

query validation
    "Does this requested W actually refer to workers in this graph?"
```

So `skill_of(W)` should explicitly reject an unknown worker.

This mirrors a lesson from your capstone's `f_of(U)`.

---

# 4. Why `skill_of(∅)` Should Return 0

There is another contract question.

What if:

```python
W = frozenset()
```

?

The eventual admissibility rule says:

[
W\neq\varnothing.
]

Does that mean `skill_of()` should reject the empty set?

No.

The mathematical sum over an empty set is:

[
\sum_{w\in\varnothing}skill(w)=0.
]

So:

```python
skill_of(frozenset())
```

should naturally return:

```text
0
```

That preserves separation of responsibilities:

```text
skill_of(W)
    computes the mathematical quantity

is_admissible(W, S)
    later decides whether empty W is allowed to compete
```

We do not want to smuggle an admissibility condition into a basic primitive.

This was exactly the architectural distinction you learned with `f_of(∅)=0`.

---

# 5. Comments-First Algorithm

Before executable code, the reasoning is:

```text
INPUT:
    a collection W of workers

1. Start:
       total = 0

2. For each worker in W:

       first verify:
           worker ∈ WORKERS

       if not:
           raise ValueError naming that worker

       otherwise:
           look up SKILL_VALUES[worker]

       add that value to total

3. Return total
```

This is an **accumulator pattern**, which you learned much earlier.

Start with the additive identity:

```python
total = 0
```

then repeatedly do:

```python
total += value
```

---

# 6. Predictions Before Running

We already know the answers from the hand oracle.

That is important: **the program is not supplying our expected values.**

## Prediction 1

```python
skill_of(frozenset({"a", "b", "c"}))
```

The hand calculation is:

[
1+1+2=4.
]

Prediction:

```text
4
```

---

## Prediction 2

```python
skill_of(frozenset({"b", "d"}))
```

The hand calculation is:

[
1+2=3.
]

Prediction:

```text
3
```

---

## Prediction 3

```python
skill_of(WORKERS)
```

Since:

[
WORKERS={a,b,c,d},
]

we get:

[
1+1+2+2=6.
]

Prediction:

```text
6
```

---

## Prediction 4 — Empty Crew

```python
skill_of(frozenset())
```

The loop runs zero times.

`total` starts at zero and never changes.

Prediction:

```text
0
```

Again, this does **not** mean an empty crew is admissible.

It means the mathematical primitive is well-defined on the empty set.

---

# 7. What the Function Actually Looks Like

Executable logic:

```python
def skill_of(W):
    total = 0

    for worker in W:
        if worker not in WORKERS:
            raise ValueError(f"W contains unknown worker {worker!r}")

        total += SKILL_VALUES[worker]

    return total
```

Walk through:

```python
skill_of({"a", "b", "c"})
```

Start:

```text
total = 0
```

Suppose iteration visits `"a"`:

```text
"a" is known
total = 0 + 1 = 1
```

Then `"b"`:

```text
"b" is known
total = 1 + 1 = 2
```

Then `"c"`:

```text
"c" is known
total = 2 + 2 = 4
```

Return:

```text
4
```

Because a set's iteration order should not be relied upon, Python might visit the workers in another order.

But addition is order-independent here:

[
1+1+2=2+1+1=4.
]

So deterministic worker iteration is not required for this primitive.

Later, deterministic **search enumeration** will be a different issue.

---

# 8. Put the File in Place

Paste the complete file at the end of this response into:

```text
mock_primitives.py
```

Save it.

Then run these four checks individually:

```bash
python -c 'from mock_primitives import skill_of; print(skill_of(frozenset({"a", "b", "c"})))'
```

Prediction:

```text
4
```

Then:

```bash
python -c 'from mock_primitives import skill_of; print(skill_of(frozenset({"b", "d"})))'
```

Prediction:

```text
3
```

Then:

```bash
python -c 'from mock_instance import WORKERS; from mock_primitives import skill_of; print(skill_of(WORKERS))'
```

Prediction:

```text
6
```

Then:

```bash
python -c 'from mock_primitives import skill_of; print(skill_of(frozenset()))'
```

Prediction:

```text
0
```

---

# 9. Prove the Query Guard Too

Then deliberately call:

```bash
python -c 'from mock_primitives import skill_of; skill_of(frozenset({"a", "x"}))'
```

Prediction:

```text
ValueError: W contains unknown worker 'x'
```

Notice that we do **not** corrupt `mock_instance.py` for this test.

The instance is perfectly valid.

We are testing a bad **query**, not bad stored data.

That is a new distinction worth noticing:

```text
bad stored graph
→ validate_instance() raises

bad crew submitted to primitive
→ skill_of() raises
```

Both use exceptions because both represent violations of a function's input contract.

Later:

```text
validly formed but mathematically inadmissible candidate
→ is_admissible() returns False
```

That will be different again.

---

# 10. Do Not Commit Yet

After these checks, leave `mock_primitives.py` uncommitted.

We still need to add:

```text
internal_shift_count(W)
fringe(W)
```

Then we will run all primitive predictions together, lint the complete module, and commit it as one coherent unit.

---

# COPY INTO `mock_notes_1.md`

````markdown
## Step 3 — Mathematical Primitives

The second implementation layer is:

```text
mock_primitives.py
````

A primitive here means a small foundational mathematical computation used by higher-level checker logic.

The dependency structure is:

```text
mock_instance.py
    fixed validated data
            ↓
mock_primitives.py
    skill(W)
    i(W)
    ∂(W)
            ↓
admissibility and evaluation
            ↓
exhaustive search
```

If a primitive computes the wrong mathematical quantity, every higher layer can be internally correct and still produce a wrong result.

The primitives are therefore tested against values already established independently in `MOCK_ORACLE.md`.

---

### Primitive 1 — `skill_of(W)`

The mathematical definition is:

[
skill(W)
========

\sum_{w\in W}skill(w).
]

The function simply adds the skill value associated with each worker in `W`.

For example:

```text
W = {a,b,c}
```

has:

```text
skill(a) = 1
skill(b) = 1
skill(c) = 2
```

therefore:

[
skill({a,b,c})
==============

# 1+1+2

4.

]

---

### Required Instance Data

`skill_of(W)` needs:

```text
WORKERS
SKILL_VALUES
```

It does not yet need `SHIFTS`.

Therefore the initial module import is:

```python
from mock_instance import SKILL_VALUES, WORKERS
```

Avoid importing future dependencies before executable code actually needs them.

---

### Query Contract

`validate_instance()` establishes that the stored fixed instance is valid.

It does not establish that every later caller supplies a valid crew.

Therefore `skill_of(W)` explicitly checks:

```text
worker ∈ WORKERS
```

for every worker supplied in `W`.

A query such as:

```python
skill_of(frozenset({"a", "x"}))
```

should raise:

```text
ValueError: W contains unknown worker 'x'
```

rather than leaking a generic dictionary `KeyError`.

This separates two kinds of validation:

```text
instance validation:
    Is the stored graph itself valid?

query validation:
    Does this requested W refer only to workers belonging to this graph?
```

---

### Empty Crew Behavior

`skill_of()` should not reject:

```text
W = ∅
```

The mathematical empty sum is:

[
skill(\varnothing)=0.
]

The implementation starts:

```python
total = 0
```

and an empty crew causes the loop to execute zero times, leaving:

```text
total = 0
```

The later admissibility layer is responsible for enforcing:

[
W\neq\varnothing.
]

This preserves separation of concerns:

```text
primitive
→ compute the mathematical quantity

admissibility
→ decide whether a candidate may compete
```

---

### Accumulator Pattern

The function uses the accumulator pattern:

```text
start total at 0

for every worker in W:
    validate worker
    add worker's skill to total

return total
```

Executable shape:

```python
def skill_of(W):
    total = 0

    for worker in W:
        if worker not in WORKERS:
            raise ValueError(f"W contains unknown worker {worker!r}")

        total += SKILL_VALUES[worker]

    return total
```

---

### Hand-Derived Predictions

The oracle gives the expected values before execution.

#### Prediction 1

```python
skill_of(frozenset({"a", "b", "c"}))
```

Hand arithmetic:

[
1+1+2=4.
]

Expected:

```text
4
```

#### Prediction 2

```python
skill_of(frozenset({"b", "d"}))
```

Hand arithmetic:

[
1+2=3.
]

Expected:

```text
3
```

#### Prediction 3

```python
skill_of(WORKERS)
```

Hand arithmetic:

[
1+1+2+2=6.
]

Expected:

```text
6
```

#### Prediction 4

```python
skill_of(frozenset())
```

Expected:

```text
0
```

because the sum over the empty set is zero.

---

### Unknown-Worker Prediction

For:

```python
skill_of(frozenset({"a", "x"}))
```

the instance itself remains valid, but the query violates the primitive's contract.

Expected final traceback line:

```text
ValueError: W contains unknown worker 'x'
```

This is a query-validation test, not an instance-corruption test.

---

> **RULE TO BANK:** A primitive should faithfully compute its mathematical quantity while rejecting inputs for which that quantity is being requested on objects outside the instance. Higher-level feasibility conditions belong to the higher-level predicate, not inside the primitive.

````

# COPY INTO `mock_primitives.py`

```python
# ==================================================================================================
# MOCK EXIT 1 — MATHEMATICAL PRIMITIVES
# ==================================================================================================
#
# PURPOSE:
#
# Implement the small mathematical quantities that later checker layers
# will depend on.
#
#
# THE THREE PRIMITIVES WILL BE:
#
#     1. skill_of(W)
#     2. internal_shift_count(W)
#     3. fringe(W)
#
# They are being built and verified one at a time.
#
#
# RESPONSIBILITY BOUNDARY:
#
# These functions compute mathematical quantities associated with a crew W.
#
# They do NOT decide whether a candidate pair (W, S) is admissible.
#
# For example:
#
#     skill_of(empty crew)
#
# is mathematically well-defined and equals 0, even though the later
# admissibility rules reject an empty crew.
#
#
# QUERY VALIDATION:
#
# validate_instance() protects the STORED instance.
#
# These primitives must still reject a query that refers to a worker
# outside WORKERS.
#
# ==================================================================================================


from mock_instance import SKILL_VALUES, WORKERS


# ==================================================================================================
# PRIMITIVE 1 — skill_of(W)
# ==================================================================================================
#
# MATHEMATICAL DEFINITION:
#
#     skill(W) = sum of skill(w) over every worker w in W
#
#
# INPUT:
#
#     W
#
# A collection of workers.
#
# Examples:
#
#     frozenset({"a", "b"})
#     frozenset({"a", "b", "c"})
#     frozenset()
#
#
# OUTPUT:
#
#     an integer equal to skill(W)
#
#
# QUERY CONTRACT:
#
# Every worker supplied in W must belong to:
#
#     WORKERS
#
# Example invalid query:
#
#     W = {"a", "x"}
#
# Since:
#
#     "x" not in WORKERS
#
# raise:
#
#     ValueError: W contains unknown worker 'x'
#
#
# EMPTY-CREW BEHAVIOR:
#
#     skill(empty set) = 0
#
# This primitive therefore does not reject an empty W.
#
# The later admissibility predicate will enforce:
#
#     W != empty
#
#
# COMMENTS-FIRST ALGORITHM:
#
# 1. Start:
#
#        total = 0
#
# 2. For every worker in W:
#
#        verify worker belongs to WORKERS
#
#        if not:
#            raise ValueError naming that worker
#
#        otherwise:
#            add SKILL_VALUES[worker] to total
#
# 3. Return total.
#
#
# HAND-DERIVED PREDICTIONS:
#
#     skill_of({"a", "b", "c"})
#
#         = 1 + 1 + 2
#         = 4
#
#
#     skill_of({"b", "d"})
#
#         = 1 + 2
#         = 3
#
#
#     skill_of(WORKERS)
#
#         = 1 + 1 + 2 + 2
#         = 6
#
#
#     skill_of(empty set)
#
#         = 0
#
# ==================================================================================================


def skill_of(W):
    total = 0

    for worker in W:
        if worker not in WORKERS:
            raise ValueError(f"W contains unknown worker {worker!r}")

        total += SKILL_VALUES[worker]

    return total
````

Run the four passing predictions and the one rejection prediction now. Then paste the outputs, and we will add **Primitive 2: `internal_shift_count(W)`** to the complete file.
==================================================================================================================================================================
Perfect. Every prediction matched:

```text
skill({a,b,c}) = 4      ✓
skill({b,d})   = 3      ✓
skill(WORKERS) = 6      ✓
skill(∅)       = 0      ✓
unknown "x"    → ValueError ✓
```

That proves `skill_of(W)` is doing two things correctly: it computes the mathematical sum, and it enforces its query contract.

We now add **Primitive 2: `internal_shift_count(W)`**.

# Step 3B — `internal_shift_count(W)`

## 1. What quantity are we computing?

The mathematical definition is:

[
i(W)=\text{number of physical shifts whose two workers are both in }W.
]

The key phrase is **both endpoints**.

For a shift:

```text
(shift_id, worker1, worker2)
```

it is internal precisely when:

```python
worker1 in W and worker2 in W
```

This is an **AND** condition.

Compare that with the fringe primitive we will build next:

```text
internal:
both endpoints inside

fringe:
exactly one endpoint inside
```

Those must never be confused.

---

# 2. Why We Now Need `SHIFTS`

`skill_of(W)` only needed:

```text
WORKERS
SKILL_VALUES
```

But `internal_shift_count(W)` has to inspect the graph's actual shift copies.

So the import at the top changes from:

```python
from mock_instance import SKILL_VALUES, WORKERS
```

to:

```python
from mock_instance import SHIFTS, SKILL_VALUES, WORKERS
```

This is a genuine dependency now, so it belongs in the module.

---

# 3. What Does the Function Actually Count?

Take:

[
W={a,b}.
]

Our stored list is:

```text
s0 = (a,b)
s1 = (a,b)
s2 = (b,c)
s3 = (c,d)
```

Now evaluate the condition:

```python
worker1 in W and worker2 in W
```

for every physical shift.

### `s0`

```text
a in W → True
b in W → True

True and True → True
```

Count it.

### `s1`

Exactly the same endpoints, but this is another physical list entry:

```text
a in W → True
b in W → True
```

Count it too.

Now:

```text
count = 2
```

### `s2`

```text
b in W → True
c in W → False

True and False → False
```

Do not count it.

### `s3`

```text
c in W → False
d in W → False
```

Do not count it.

Therefore:

[
i({a,b})=2.
]

---

# 4. Why Parallel Copies Are Automatically Counted Correctly

This is one reason our instance representation matters.

`SHIFTS` contains:

```python
("s0", "a", "b"),
("s1", "a", "b"),
```

as **two separate list entries**.

Our function walks through `SHIFTS` entry by entry.

So it does:

```text
see s0 → internal → +1
see s1 → internal → +1
```

It never tries to deduplicate endpoint pairs.

Therefore parallel multiplicity is preserved naturally.

If instead we had represented the graph carelessly as:

```python
{("a", "b"), ("b", "c"), ("c", "d")}
```

the parallel copy would already have disappeared before this function ever ran.

So there is an important architecture principle here:

> A correct algorithm cannot recover distinctions that the data representation already destroyed.

Our representation preserves physical copies, so the primitive can count them correctly.

---

# 5. Does This Function Need the Shift ID?

When we loop through:

```python
for shift_id, worker1, worker2 in SHIFTS:
```

the internal-count test only needs:

```text
worker1
worker2
```

It does not need the ID.

So we can write:

```python
for _shift_id, worker1, worker2 in SHIFTS:
```

The leading underscore means:

> I know this value exists in the tuple, but this particular function intentionally does not use it.

That is clearer than pretending the field does not exist.

---

# 6. Query Contract

The same issue from `skill_of(W)` applies.

Suppose somebody asks:

```python
internal_shift_count({"a", "x"})
```

The graph instance is valid, but the query crew is not.

Should the function silently calculate something using the valid part `{a}`?

Absolutely not.

That would be dangerous because the result might look plausible.

So before counting shifts, we validate every worker in (W):

```python
for worker in W:
    if worker not in WORKERS:
        raise ValueError(...)
```

with the same contract message:

```text
ValueError: W contains unknown worker 'x'
```

Consistency across primitives is useful.

---

# 7. What About the Empty Crew?

Again:

```python
W = frozenset()
```

is mathematically meaningful for this primitive.

Can any loopless shift have **both endpoints inside the empty set**?

No.

Therefore:

[
i(\varnothing)=0.
]

So we do **not** reject the empty crew here.

Later:

```text
is_admissible(W,S)
```

will reject empty (W).

This is the same separation we established for `skill_of()`.

---

# 8. Comments-First Algorithm

Before code, the function is:

```text
INPUT:
    crew W

1. Verify every worker in W belongs to WORKERS.

2. Start:
       count = 0

3. Scan every physical shift copy in SHIFTS.

4. For each:
       (shift_id, worker1, worker2)

   ask:

       worker1 in W AND worker2 in W ?

5. If yes:
       count += 1

6. If no:
       do nothing

7. Return count.
```

The important distinction:

```text
internal → AND
```

We will contrast this with:

```text
fringe → XOR
```

in the next step.

---

# 9. Predictions From the Oracle

We do not guess these from the function. We already derived them by hand.

## Prediction 1 — Parallel pair

```python
internal_shift_count(frozenset({"a", "b"}))
```

Internal:

```text
s0
s1
```

Therefore:

[
i({a,b})=2.
]

Expected:

```text
2
```

---

## Prediction 2 — Winning crew

```python
internal_shift_count(frozenset({"a", "b", "c"}))
```

Internal:

```text
s0 = (a,b)
s1 = (a,b)
s2 = (b,c)
```

`s3` crosses to `d`.

Therefore:

[
i({a,b,c})=3.
]

Expected:

```text
3
```

---

## Prediction 3 — `{b,c}`

```python
internal_shift_count(frozenset({"b", "c"}))
```

Only:

```text
s2 = (b,c)
```

has both endpoints inside.

Therefore:

[
i({b,c})=1.
]

Expected:

```text
1
```

---

## Prediction 4 — Disconnected crew `{a,c}`

```python
internal_shift_count(frozenset({"a", "c"}))
```

Check:

```text
s0 = (a,b) → b outside
s1 = (a,b) → b outside
s2 = (b,c) → b outside
s3 = (c,d) → d outside
```

No shift has both endpoints in `{a,c}`.

Therefore:

[
i({a,c})=0.
]

Expected:

```text
0
```

---

## Prediction 5 — Whole worker set

```python
internal_shift_count(WORKERS)
```

Every endpoint of every shift lies inside the full worker set.

There are four physical copies:

```text
s0
s1
s2
s3
```

Therefore:

[
i(WORKERS)=4.
]

Expected:

```text
4
```

---

## Prediction 6 — Empty crew

```python
internal_shift_count(frozenset())
```

No edge can have both endpoints in the empty set.

Expected:

```text
0
```

---

# 10. Run These After Updating the File

After pasting the complete file below, save it.

Run:

```bash
python -c 'from mock_primitives import internal_shift_count; print(internal_shift_count(frozenset({"a", "b"})))'
```

Prediction:

```text
2
```

Then:

```bash
python -c 'from mock_primitives import internal_shift_count; print(internal_shift_count(frozenset({"a", "b", "c"})))'
```

Prediction:

```text
3
```

Then:

```bash
python -c 'from mock_primitives import internal_shift_count; print(internal_shift_count(frozenset({"b", "c"})))'
```

Prediction:

```text
1
```

Then:

```bash
python -c 'from mock_primitives import internal_shift_count; print(internal_shift_count(frozenset({"a", "c"})))'
```

Prediction:

```text
0
```

Then:

```bash
python -c 'from mock_instance import WORKERS; from mock_primitives import internal_shift_count; print(internal_shift_count(WORKERS))'
```

Prediction:

```text
4
```

Finally:

```bash
python -c 'from mock_primitives import internal_shift_count; print(internal_shift_count(frozenset()))'
```

Prediction:

```text
0
```

And prove the query guard:

```bash
python -c 'from mock_primitives import internal_shift_count; internal_shift_count(frozenset({"b", "x"}))'
```

Expected final line:

```text
ValueError: W contains unknown worker 'x'
```

Still **do not commit**. Primitive 3 remains.

---

# COPY INTO `mock_notes_1.md`

````markdown
## Step 3B — Primitive 2: `internal_shift_count(W)`

The second mathematical primitive computes:

\[
i(W),
\]

the number of physical shift copies whose two workers both belong to crew \(W\).

The defining logical condition is:

```text
worker1 in W AND worker2 in W
````

In Python:

```python
if worker1 in W and worker2 in W:
```

This is the internal-edge condition.

It must not be confused with the fringe condition, which will require exactly one endpoint inside.

---

### New Module Dependency

`skill_of(W)` needed only:

```text
WORKERS
SKILL_VALUES
```

`internal_shift_count(W)` must inspect actual physical shift copies.

Therefore `mock_primitives.py` now imports:

```python
from mock_instance import SHIFTS, SKILL_VALUES, WORKERS
```

`SHIFTS` is imported only once executable code genuinely requires it.

---

### Parallel Copies

The fixed graph contains:

```text
s0 = (a,b)
s1 = (a,b)
```

These have identical endpoints but are distinct physical shift copies.

For:

```text
W = {a,b}
```

both are internal.

The function scans the list:

```text
s0 → both endpoints inside → count +1
s1 → both endpoints inside → count +1
```

so:

[
i({a,b})=2.
]

Multiplicity is handled correctly because `SHIFTS` preserved the two physical copies as separate list entries.

The function does not need special parallel-edge logic.

The correct representation already preserved the distinction.

This gives a broader software principle:

> An algorithm cannot recover distinctions that its data representation has already destroyed.

---

### Why the Shift ID Is Unused Here

A shift tuple has:

```text
(shift_id, worker1, worker2)
```

but internal membership depends only on the endpoints.

Therefore the loop can use:

```python
for _shift_id, worker1, worker2 in SHIFTS:
```

The leading underscore communicates that the shift ID is intentionally unpacked but unused by this function.

Identity still exists in the representation even when a particular computation does not need it.

---

### Query Validation

As with `skill_of(W)`, every worker supplied in `W` must belong to `WORKERS`.

A query such as:

```python
internal_shift_count(frozenset({"b", "x"}))
```

should raise:

```text
ValueError: W contains unknown worker 'x'
```

The graph itself may be valid while a caller supplies an invalid query.

Instance validation and query validation therefore remain separate contracts.

---

### Empty Crew

The primitive does not reject:

```text
W = ∅
```

No physical shift can have both endpoints in the empty set, so:

[
i(\varnothing)=0.
]

The later admissibility predicate, not the primitive, will reject an empty crew from the optimization.

---

### Comments-First Algorithm

```text
1. Verify every worker in W belongs to WORKERS.

2. Start:
       count = 0

3. Scan every physical shift copy:
       (shift_id, worker1, worker2)

4. Test:
       worker1 in W AND worker2 in W

5. If both endpoints are inside:
       count += 1

6. Return count.
```

The durable logical distinction is:

```text
internal shift
→ BOTH endpoints inside
→ AND
```

The next primitive will use:

```text
fringe shift
→ EXACTLY ONE endpoint inside
→ XOR
```

---

### Hand-Derived Predictions

#### Parallel pair

```python
internal_shift_count(frozenset({"a", "b"}))
```

Internal shifts:

```text
s0
s1
```

Expected:

```text
2
```

#### Winning crew

```python
internal_shift_count(frozenset({"a", "b", "c"}))
```

Internal shifts:

```text
s0
s1
s2
```

Expected:

```text
3
```

#### Crew `{b,c}`

Only:

```text
s2
```

is internal.

Expected:

```text
1
```

#### Crew `{a,c}`

No physical shift has both endpoints in the crew.

Expected:

```text
0
```

#### Full worker set

All four physical shifts are internal.

Expected:

```text
4
```

#### Empty crew

Expected:

```text
0
```

because no shift can lie entirely inside the empty set.

---

> **RULE TO BANK:** Internal membership is an `AND` condition: count a physical shift exactly when both endpoints belong to the crew. Parallel copies count separately because they remain separate objects in the stored shift list.

````

# COPY INTO `mock_primitives.py`

```python
# ==================================================================================================
# MOCK EXIT 1 — MATHEMATICAL PRIMITIVES
# ==================================================================================================
#
# PURPOSE:
#
# Implement the small mathematical quantities that later checker layers
# will depend on.
#
#
# THE THREE PRIMITIVES ARE:
#
#     1. skill_of(W)
#     2. internal_shift_count(W)
#     3. fringe(W)
#
# The module is being built and verified one primitive at a time.
#
#
# RESPONSIBILITY BOUNDARY:
#
# These functions compute mathematical quantities associated with a crew W.
#
# They do NOT decide whether a candidate pair (W, S) is admissible.
#
# For example:
#
#     skill_of(empty crew) = 0
#     internal_shift_count(empty crew) = 0
#
# even though the later admissibility predicate rejects an empty crew.
#
#
# QUERY VALIDATION:
#
# validate_instance() protects the STORED instance.
#
# These primitives separately reject query crews containing workers
# outside WORKERS.
#
# ==================================================================================================


from mock_instance import SHIFTS, SKILL_VALUES, WORKERS


# ==================================================================================================
# PRIMITIVE 1 — skill_of(W)
# ==================================================================================================
#
# MATHEMATICAL DEFINITION:
#
#     skill(W) = sum of skill(w) over every worker w in W
#
#
# INPUT:
#
#     W
#
# A collection of workers.
#
#
# OUTPUT:
#
#     an integer equal to skill(W)
#
#
# QUERY CONTRACT:
#
# Every worker supplied in W must belong to:
#
#     WORKERS
#
# Example invalid query:
#
#     W = {"a", "x"}
#
# should raise:
#
#     ValueError: W contains unknown worker 'x'
#
#
# EMPTY-CREW BEHAVIOR:
#
#     skill(empty set) = 0
#
# The primitive does not enforce the later admissibility requirement
# that W be nonempty.
#
#
# COMMENTS-FIRST ALGORITHM:
#
# 1. Start:
#
#        total = 0
#
# 2. For every worker in W:
#
#        verify worker belongs to WORKERS
#
#        if not:
#            raise ValueError naming that worker
#
#        otherwise:
#            add SKILL_VALUES[worker] to total
#
# 3. Return total.
#
#
# HAND-DERIVED PREDICTIONS:
#
#     skill_of({"a", "b", "c"}) = 4
#
#     skill_of({"b", "d"}) = 3
#
#     skill_of(WORKERS) = 6
#
#     skill_of(empty set) = 0
#
# ==================================================================================================


def skill_of(W):
    total = 0

    for worker in W:
        if worker not in WORKERS:
            raise ValueError(f"W contains unknown worker {worker!r}")

        total += SKILL_VALUES[worker]

    return total


# ==================================================================================================
# PRIMITIVE 2 — internal_shift_count(W)
# ==================================================================================================
#
# MATHEMATICAL DEFINITION:
#
#     i(W)
#
# is the number of PHYSICAL SHIFT COPIES whose two endpoints both belong
# to W.
#
#
# INTERNAL-SHIFT CONDITION:
#
# For a physical shift:
#
#     (shift_id, worker1, worker2)
#
# the shift is internal exactly when:
#
#     worker1 in W
#
# AND:
#
#     worker2 in W
#
# In Python:
#
#     worker1 in W and worker2 in W
#
#
# MULTIGRAPH / PARALLEL-COPY RULE:
#
# Parallel shifts count separately.
#
# The fixed instance contains:
#
#     s0 = (a, b)
#     s1 = (a, b)
#
# For:
#
#     W = {a, b}
#
# both physical copies are internal.
#
# Therefore:
#
#     i({a,b}) = 2
#
# This happens naturally because SHIFTS stores s0 and s1 as separate
# list entries and this function scans every entry.
#
#
# SHIFT-ID FIELD:
#
# Internal membership depends on the endpoints rather than the shift ID.
#
# The loop therefore names the first tuple field:
#
#     _shift_id
#
# The leading underscore communicates:
#
#     this field exists and is intentionally unused in this function.
#
#
# QUERY CONTRACT:
#
# Every worker supplied in W must belong to WORKERS.
#
# Example:
#
#     W = {"b", "x"}
#
# should raise:
#
#     ValueError: W contains unknown worker 'x'
#
#
# EMPTY-CREW BEHAVIOR:
#
# No shift can have both endpoints in the empty set.
#
# Therefore:
#
#     i(empty set) = 0
#
# The later admissibility predicate is responsible for rejecting an
# empty crew from the optimization problem.
#
#
# COMMENTS-FIRST ALGORITHM:
#
# 1. Verify every worker in W belongs to WORKERS.
#
# 2. Start:
#
#        count = 0
#
# 3. Scan every physical shift copy:
#
#        (shift_id, worker1, worker2)
#
# 4. Ask:
#
#        worker1 in W AND worker2 in W ?
#
# 5. If yes:
#
#        count += 1
#
# 6. Otherwise:
#
#        do nothing
#
# 7. Return count.
#
#
# HAND-DERIVED PREDICTIONS:
#
#     internal_shift_count({"a", "b"})
#
#         s0 and s1 are internal
#
#         = 2
#
#
#     internal_shift_count({"a", "b", "c"})
#
#         s0, s1, and s2 are internal
#
#         = 3
#
#
#     internal_shift_count({"b", "c"})
#
#         only s2 is internal
#
#         = 1
#
#
#     internal_shift_count({"a", "c"})
#
#         no physical shift has both endpoints inside
#
#         = 0
#
#
#     internal_shift_count(WORKERS)
#
#         all four physical shifts are internal
#
#         = 4
#
#
#     internal_shift_count(empty set)
#
#         = 0
#
# ==================================================================================================


def internal_shift_count(W):
    for worker in W:
        if worker not in WORKERS:
            raise ValueError(f"W contains unknown worker {worker!r}")

    count = 0

    for _shift_id, worker1, worker2 in SHIFTS:
        if worker1 in W and worker2 in W:
            count += 1

    return count
````

Run the predictions now and paste the outputs. Then we will add **Primitive 3: `fringe(W)`**, where the key logical move changes from **AND** to **XOR** and where the return representation becomes a design decision because the future `S` enumeration inherits it.

==================================================================================================================================================================

Perfect. Every prediction for `internal_shift_count(W)` matched, including the bad-query rejection:

```text
i({a,b})       = 2   ✓
i({a,b,c})     = 3   ✓
i({b,c})       = 1   ✓
i({a,c})       = 0   ✓
i(WORKERS)     = 4   ✓
i(∅)           = 0   ✓
unknown "x"    → ValueError ✓
```

So Primitive 2 is behaving exactly like the hand oracle.

Now we build **Primitive 3: `fringe(W)`**. This completes `mock_primitives.py`.

# Step 3C — `fringe(W)`

## 1. What quantity are we computing?

For a crew (W), the fringe

[
\partial(W)
]

is the collection of **physical shift copies with exactly one worker inside (W)**.

That phrase **exactly one** is the entire definition.

Take a physical shift:

```text
(shift_id, worker1, worker2)
```

There are four possible membership patterns:

```text
worker1 in W    worker2 in W

True            True
False           False
True            False
False           True
```

Only the last two are fringe cases:

```text
True  / False
False / True
```

because exactly one endpoint belongs to the crew.

---

# 2. Contrast Internal With Fringe

This is worth locking firmly because these two primitives scan the **same shifts** but ask different logical questions.

For an internal shift:

```python
worker1 in W and worker2 in W
```

That is:

> both endpoints are inside.

For a fringe shift:

```python
(worker1 in W) != (worker2 in W)
```

That is:

> the two membership results differ.

Boolean inequality is functioning as **exclusive OR**, or XOR.

So:

```text
INTERNAL
both inside
True AND True
→ count it

FRINGE
exactly one inside
True XOR False
or
False XOR True
→ collect it
```

---

# 3. Why `(worker1 in W) != (worker2 in W)` Works

Suppose:

```python
worker1_inside = worker1 in W
worker2_inside = worker2 in W
```

Then Python Boolean inequality gives:

```text
True  != True   → False
False != False  → False

True  != False  → True
False != True   → True
```

Translate that back into graph language:

```text
both inside
→ False
→ not fringe

both outside
→ False
→ not fringe

first inside, second outside
→ True
→ fringe

first outside, second inside
→ True
→ fringe
```

That is exactly the mathematical definition.

So the clean implementation is:

```python
if (worker1 in W) != (worker2 in W):
```

---

# 4. The Important Design Question — What Does `fringe(W)` Return?

Unlike:

```python
skill_of(W)
```

which returns one integer, and:

```python
internal_shift_count(W)
```

which returns one integer, `fringe(W)` returns a **collection of shifts**.

We need to choose its representation carefully because downstream code will inherit that choice.

The two important consumers are:

```text
is_admissible(W, S)
```

and:

```text
find_max_density()
```

The search will need to generate every subset:

[
S\subseteq\partial(W).
]

Our final result contract expects:

```python
result.S
```

to look like:

```python
frozenset({"s0", "s1"})
```

or, for the winner:

```python
frozenset()
```

So I would have `fringe(W)` return:

```python
list[str]
```

conceptually—a **list of shift IDs**.

For example:

```python
["s0", "s1", "s2"]
```

---

# 5. Why Return IDs Instead of Full Shift Tuples?

We could return:

```python
[
    ("s0", "a", "b"),
    ("s1", "a", "b"),
    ("s2", "b", "c"),
]
```

That would preserve identity.

But the future candidate (S) is defined in our code as a collection of **shift IDs**.

The evaluator only needs:

[
|S|,
]

not the endpoints of the selected fringe shifts.

The admissibility predicate needs to ask:

> Is every ID in `S` one of the IDs returned by `fringe(W)`?

So returning IDs aligns directly with the downstream representation.

The full shift triples are needed only **inside `fringe()` to decide whether an edge crosses**.

Once that decision is made, the ID is sufficient.

---

# 6. Why Return a List Instead of a Set?

This is a subtle but important search-design decision.

Mathematically, the fringe is a set.

So why not return:

```python
{"s0", "s1", "s2"}
```

?

Because our later exhaustive search needs **deterministic enumeration**.

`SHIFTS` has a stable list order:

```text
s0
s1
s2
s3
```

If `fringe(W)` walks `SHIFTS` in that order and appends matching IDs to a list, then the result preserves that stable order.

Example:

```python
fringe({"b"})
```

will return:

```python
["s0", "s1", "s2"]
```

in that order.

Later:

```python
itertools.combinations(fringe_edges, r)
```

preserves its input order.

That gives us deterministic subset enumeration.

This matters because the search contract says:

> If two candidates tie, the first encountered wins.

"First" only has a reliable meaning if the enumeration order is deterministic.

So the chain is:

```text
SHIFTS stored in stable list order
        ↓
fringe(W) returns IDs in that same list order
        ↓
itertools.combinations respects input order
        ↓
S enumeration deterministic
        ↓
"first maximizer wins" has a stable meaning
```

This is exactly the kind of design consequence we want to notice **before** writing the search.

---

# 7. Parallel Copies Still Survive

Consider:

[
W={b}.
]

The shifts are:

```text
s0 = (a,b)
s1 = (a,b)
s2 = (b,c)
s3 = (c,d)
```

For `s0`:

```text
a outside
b inside
→ fringe
```

For `s1`:

```text
a outside
b inside
→ fringe
```

Even though those endpoints are identical, the IDs are different.

So the returned list contains both:

```python
["s0", "s1", "s2"]
```

not:

```python
["s0", "s2"]
```

and not:

```python
[("a", "b"), ("b", "c")]
```

This is why we validated unique shift IDs in `mock_instance.py`.

The representation contract now fits together:

```text
physical copy
→ unique shift ID
→ fringe returns ID
→ S stores ID
→ |S| counts physical selected shifts correctly
```

---

# 8. Query Contract

Same as the other primitives.

If somebody calls:

```python
fringe(frozenset({"a", "x"}))
```

we should not silently treat `"x"` as an irrelevant outside worker.

That would be mathematically misleading.

The requested crew itself is invalid because it contains something outside:

```python
WORKERS
```

So:

```text
ValueError: W contains unknown worker 'x'
```

Again:

```text
bad stored graph
→ validate_instance()

bad primitive query
→ primitive raises

well-formed but inadmissible candidate
→ later predicate returns False
```

Those are three different contracts.

---

# 9. Empty Crew Behavior

What is:

[
\partial(\varnothing)?
]

For a shift to be fringe, exactly one endpoint would have to lie in the empty set.

But **nothing** lies in the empty set.

For every physical shift:

```text
worker1 in ∅ → False
worker2 in ∅ → False

False != False → False
```

Therefore:

[
\partial(\varnothing)=\varnothing.
]

In our Python representation:

```python
fringe(frozenset())
```

should return:

```python
[]
```

Again, the primitive computes a legitimate mathematical quantity even though empty (W) will later fail admissibility Condition 1.

---

# 10. Predictions From the Oracle

Now the important part: predict before running.

## Prediction 1 — `{a,b}`

```python
fringe(frozenset({"a", "b"}))
```

Inspect:

```text
s0 = (a,b)
both inside
→ not fringe

s1 = (a,b)
both inside
→ not fringe

s2 = (b,c)
b inside, c outside
→ fringe

s3 = (c,d)
both outside
→ not fringe
```

Prediction:

```python
["s2"]
```

---

## Prediction 2 — `{b}`

```python
fringe(frozenset({"b"}))
```

Inspect:

```text
s0 = (a,b)
one inside
→ fringe

s1 = (a,b)
one inside
→ fringe

s2 = (b,c)
one inside
→ fringe

s3 = (c,d)
both outside
→ not fringe
```

Prediction:

```python
["s0", "s1", "s2"]
```

This is a key parallel-copy test.

---

## Prediction 3 — `{a,c}`

```python
fringe(frozenset({"a", "c"}))
```

Check all four:

```text
s0 = (a,b)
a inside, b outside
→ fringe

s1 = (a,b)
a inside, b outside
→ fringe

s2 = (b,c)
b outside, c inside
→ fringe

s3 = (c,d)
c inside, d outside
→ fringe
```

Every shift crosses.

Prediction:

```python
["s0", "s1", "s2", "s3"]
```

---

## Prediction 4 — Winning Crew `{a,b,c}`

```python
fringe(frozenset({"a", "b", "c"}))
```

We derived:

```text
s0 → internal
s1 → internal
s2 → internal
s3 → crosses from c to d
```

Prediction:

```python
["s3"]
```

This will later force the winning crew's only two possible `S` candidates to be:

```python
frozenset()
```

and:

```python
frozenset({"s3"})
```

---

## Prediction 5 — `{b,c,d}`

```python
fringe(frozenset({"b", "c", "d"}))
```

Here `a` is the only outside worker.

Both parallel `a-b` shifts cross:

```text
s0 → fringe
s1 → fringe
```

while:

```text
s2 = (b,c) → both inside
s3 = (c,d) → both inside
```

Prediction:

```python
["s0", "s1"]
```

---

## Prediction 6 — Full Worker Set

```python
fringe(WORKERS)
```

Every worker is inside.

Therefore every shift has both endpoints inside.

Prediction:

```python
[]
```

or mathematically:

[
\partial(WORKERS)=\varnothing.
]

---

## Prediction 7 — Empty Crew

```python
fringe(frozenset())
```

Neither endpoint of any shift belongs to the empty crew.

Prediction:

```python
[]
```

Notice:

```text
fringe(∅) = []
fringe(WORKERS) = []
```

but for completely different reasons:

```text
empty crew:
both endpoints outside every time

whole crew:
both endpoints inside every time
```

In neither case does **exactly one** endpoint lie inside.

---

# 11. Comments-First Algorithm

The function is:

```text
INPUT:
    crew W

1. Verify every worker in W belongs to WORKERS.

2. Start:
       crossing_shift_ids = []

3. Scan SHIFTS in stable order.

4. For each:
       (shift_id, worker1, worker2)

   evaluate:
       (worker1 in W) != (worker2 in W)

5. If True:
       append shift_id

6. If False:
       do nothing

7. Return crossing_shift_ids.
```

That is all the executable logic.

But because of our representation decisions, that little function also establishes the stable edge-ID sequence from which later (S)-subsets will be generated.

---

# 12. Run These After Updating `mock_primitives.py`

Paste the complete updated file below and save it.

Then run:

```bash
python -c 'from mock_primitives import fringe; print(fringe(frozenset({"a", "b"})))'
```

Expected:

```text
['s2']
```

Then:

```bash
python -c 'from mock_primitives import fringe; print(fringe(frozenset({"b"})))'
```

Expected:

```text
['s0', 's1', 's2']
```

Then:

```bash
python -c 'from mock_primitives import fringe; print(fringe(frozenset({"a", "c"})))'
```

Expected:

```text
['s0', 's1', 's2', 's3']
```

Then:

```bash
python -c 'from mock_primitives import fringe; print(fringe(frozenset({"a", "b", "c"})))'
```

Expected:

```text
['s3']
```

Then:

```bash
python -c 'from mock_primitives import fringe; print(fringe(frozenset({"b", "c", "d"})))'
```

Expected:

```text
['s0', 's1']
```

Then:

```bash
python -c 'from mock_instance import WORKERS; from mock_primitives import fringe; print(fringe(WORKERS))'
```

Expected:

```text
[]
```

Then:

```bash
python -c 'from mock_primitives import fringe; print(fringe(frozenset()))'
```

Expected:

```text
[]
```

Finally test the query contract:

```bash
python -c 'from mock_primitives import fringe; fringe(frozenset({"c", "x"}))'
```

Expected final line:

```text
ValueError: W contains unknown worker 'x'
```

---

# 13. After the Predictions Pass

Once those all match, we will close the primitive module with:

```bash
python mock_primitives.py
```

Prediction: silent.

Then:

```bash
ruff check mock_primitives.py
```

Prediction:

```text
All checks passed!
```

Then we will commit:

```bash
git add mock_primitives.py
git commit -m "mock1: add crew-assignment mathematical primitives"
```

and separately commit your accumulated notes:

```bash
git add mock_notes_1.md
git commit -m "mock1: document primitive design and oracle checks"
```

But **do not commit yet**. First run the fringe predictions and bring me the outputs.

---

# COPY INTO `mock_notes_1.md`

````markdown
## Step 3C — Primitive 3: `fringe(W)`

The third mathematical primitive computes:

\[
\partial(W),
\]

the collection of physical shift copies having **exactly one endpoint inside crew \(W\)**.

This completes the three primitive quantities used throughout the Crew-Assignment Density problem:

```text
skill(W)
i(W)
∂(W)
````

---

### Internal Versus Fringe Logic

The internal-shift condition is:

```text
both endpoints inside
```

which corresponds to:

```python
worker1 in W and worker2 in W
```

The fringe condition is different:

```text
exactly one endpoint inside
```

which corresponds to:

```python
(worker1 in W) != (worker2 in W)
```

Boolean inequality acts as XOR.

The truth table is:

```text
worker1 in W    worker2 in W    != result    classification

True            True            False        both inside
False           False           False        both outside
True            False           True         fringe
False           True            True         fringe
```

Therefore:

```text
internal shift
→ AND

fringe shift
→ XOR
```

---

### Return Representation

`fringe(W)` returns a **list of shift IDs**.

Example:

```python
["s0", "s1", "s2"]
```

rather than full tuples such as:

```python
[
    ("s0", "a", "b"),
    ("s1", "a", "b"),
    ("s2", "b", "c"),
]
```

The full tuples are needed inside `fringe()` to determine whether each shift crosses the crew boundary.

After that decision, downstream code needs the physical shift identity, which is already supplied by the shift ID.

This representation aligns with the future candidate:

```text
S = set of shift IDs
```

and with the final search result field:

```python
result.S
```

---

### Why the Return Type Is a List

Mathematically the fringe is a set, but the implementation returns its shift IDs in a list because the stored `SHIFTS` list has stable order.

The chain is:

```text
SHIFTS stable list order
        ↓
fringe(W) scans in that order
        ↓
matching IDs are appended in that order
        ↓
itertools.combinations later preserves input order
        ↓
S-subset enumeration is deterministic
```

This matters because the search contract says:

> When several candidates tie, the first encountered maximizer wins.

A deterministic tie rule requires deterministic enumeration.

Thus the list representation is not arbitrary. It preserves a useful ordering contract for the future exhaustive search.

---

### Parallel Shift Copies Remain Distinct

For:

[
W={b},
]

the fringe contains:

```text
s0 = (a,b)
s1 = (a,b)
s2 = (b,c)
```

so:

```python
fringe(frozenset({"b"}))
```

must return:

```python
["s0", "s1", "s2"]
```

Both parallel copies survive because their IDs are distinct.

This connects directly to the unique-shift-ID invariant in `mock_instance.py`.

The representation chain is:

```text
physical shift copy
→ unique shift ID
→ fringe returns ID
→ candidate S stores ID
→ len(S) correctly counts selected physical copies
```

---

### Query Contract

As with the other primitives, every worker supplied in `W` must belong to `WORKERS`.

For example:

```python
fringe(frozenset({"c", "x"}))
```

should raise:

```text
ValueError: W contains unknown worker 'x'
```

The fixed graph may be valid while a caller submits an invalid crew.

---

### Empty-Crew Behavior

For:

[
W=\varnothing,
]

no endpoint of any shift is inside.

Thus every shift has the membership pattern:

```text
False, False
```

and:

```text
False != False
→ False
```

Therefore:

[
\partial(\varnothing)=\varnothing.
]

The Python result should be:

```python
[]
```

This does not make the empty crew admissible.

The primitive computes the mathematical fringe; the later admissibility predicate rejects empty crews.

---

### Full-Crew Behavior

For:

[
W=WORKERS,
]

every endpoint of every shift is inside.

Thus every shift has:

```text
True, True
```

and:

```text
True != True
→ False
```

Therefore:

[
\partial(WORKERS)=\varnothing.
]

Again the Python result is:

```python
[]
```

The empty and full crews therefore both have empty fringe, but for opposite structural reasons:

```text
W = ∅
→ every shift has both endpoints outside

W = WORKERS
→ every shift has both endpoints inside
```

In neither situation does exactly one endpoint lie inside.

---

### Comments-First Algorithm

```text
1. Verify every worker in W belongs to WORKERS.

2. Start:
       crossing_shift_ids = []

3. Scan every physical shift copy in SHIFTS.

4. For each shift, test:

       (worker1 in W) != (worker2 in W)

5. If True:
       append shift_id

6. Return crossing_shift_ids.
```

---

### Hand-Derived Predictions

#### Crew `{a,b}`

Only `s2` crosses:

```python
fringe(frozenset({"a", "b"}))
```

Expected:

```python
["s2"]
```

#### Singleton `{b}`

The parallel `a-b` shifts and `b-c` all cross:

```python
fringe(frozenset({"b"}))
```

Expected:

```python
["s0", "s1", "s2"]
```

#### Crew `{a,c}`

Every physical shift crosses:

```python
fringe(frozenset({"a", "c"}))
```

Expected:

```python
["s0", "s1", "s2", "s3"]
```

#### Winning crew `{a,b,c}`

Only `s3 = (c,d)` crosses:

```python
fringe(frozenset({"a", "b", "c"}))
```

Expected:

```python
["s3"]
```

#### Crew `{b,c,d}`

Only the parallel `a-b` copies cross:

```python
fringe(frozenset({"b", "c", "d"}))
```

Expected:

```python
["s0", "s1"]
```

#### Full worker set

```python
fringe(WORKERS)
```

Expected:

```python
[]
```

#### Empty crew

```python
fringe(frozenset())
```

Expected:

```python
[]
```

---

> **RULE TO BANK:** Fringe membership is an XOR condition: exactly one endpoint lies in the crew. Return physical shift IDs in stable list order so parallel identity survives and later subset enumeration remains deterministic.

````

# COPY INTO `mock_primitives.py`

```python
# ==================================================================================================
# MOCK EXIT 1 — MATHEMATICAL PRIMITIVES
# ==================================================================================================
#
# PURPOSE:
#
# Implement the small mathematical quantities that later checker layers
# depend on.
#
#
# THE THREE PRIMITIVES ARE:
#
#     1. skill_of(W)
#     2. internal_shift_count(W)
#     3. fringe(W)
#
#
# RESPONSIBILITY BOUNDARY:
#
# These functions compute mathematical quantities associated with a crew W.
#
# They do NOT decide whether a candidate pair (W, S) is admissible.
#
# For example:
#
#     skill_of(empty crew) = 0
#     internal_shift_count(empty crew) = 0
#     fringe(empty crew) = []
#
# even though the later admissibility predicate rejects an empty crew.
#
#
# QUERY VALIDATION:
#
# validate_instance() protects the STORED instance.
#
# These primitives separately reject query crews containing workers
# outside WORKERS.
#
# ==================================================================================================


from mock_instance import SHIFTS, SKILL_VALUES, WORKERS


# ==================================================================================================
# PRIMITIVE 1 — skill_of(W)
# ==================================================================================================
#
# MATHEMATICAL DEFINITION:
#
#     skill(W) = sum of skill(w) over every worker w in W
#
#
# INPUT:
#
#     W
#
# A collection of workers.
#
#
# OUTPUT:
#
#     an integer equal to skill(W)
#
#
# QUERY CONTRACT:
#
# Every worker supplied in W must belong to WORKERS.
#
# Example invalid query:
#
#     W = {"a", "x"}
#
# should raise:
#
#     ValueError: W contains unknown worker 'x'
#
#
# EMPTY-CREW BEHAVIOR:
#
#     skill(empty set) = 0
#
# The primitive does not enforce the later admissibility requirement
# that W be nonempty.
#
#
# COMMENTS-FIRST ALGORITHM:
#
# 1. Start:
#
#        total = 0
#
# 2. For every worker in W:
#
#        verify worker belongs to WORKERS
#
#        if not:
#            raise ValueError naming that worker
#
#        otherwise:
#            add SKILL_VALUES[worker] to total
#
# 3. Return total.
#
#
# HAND-DERIVED PREDICTIONS:
#
#     skill_of({"a", "b", "c"}) = 4
#
#     skill_of({"b", "d"}) = 3
#
#     skill_of(WORKERS) = 6
#
#     skill_of(empty set) = 0
#
# ==================================================================================================


def skill_of(W):
    total = 0

    for worker in W:
        if worker not in WORKERS:
            raise ValueError(f"W contains unknown worker {worker!r}")

        total += SKILL_VALUES[worker]

    return total


# ==================================================================================================
# PRIMITIVE 2 — internal_shift_count(W)
# ==================================================================================================
#
# MATHEMATICAL DEFINITION:
#
#     i(W)
#
# is the number of PHYSICAL SHIFT COPIES whose two endpoints both belong
# to W.
#
#
# INTERNAL-SHIFT CONDITION:
#
# For a physical shift:
#
#     (shift_id, worker1, worker2)
#
# the shift is internal exactly when:
#
#     worker1 in W
#
# AND:
#
#     worker2 in W
#
# In Python:
#
#     worker1 in W and worker2 in W
#
#
# MULTIGRAPH / PARALLEL-COPY RULE:
#
# Parallel shifts count separately.
#
# The fixed instance contains:
#
#     s0 = (a, b)
#     s1 = (a, b)
#
# For:
#
#     W = {a, b}
#
# both physical copies are internal.
#
# Therefore:
#
#     i({a,b}) = 2
#
# This happens naturally because SHIFTS stores s0 and s1 as separate
# list entries and this function scans every entry.
#
#
# SHIFT-ID FIELD:
#
# Internal membership depends on the endpoints rather than the shift ID.
#
# The loop therefore names the first tuple field:
#
#     _shift_id
#
# The leading underscore communicates that the field exists but is
# intentionally unused in this computation.
#
#
# QUERY CONTRACT:
#
# Every worker supplied in W must belong to WORKERS.
#
#
# EMPTY-CREW BEHAVIOR:
#
# No shift can have both endpoints in the empty set.
#
# Therefore:
#
#     i(empty set) = 0
#
#
# COMMENTS-FIRST ALGORITHM:
#
# 1. Verify every worker in W belongs to WORKERS.
#
# 2. Start:
#
#        count = 0
#
# 3. Scan every physical shift copy:
#
#        (shift_id, worker1, worker2)
#
# 4. Ask:
#
#        worker1 in W AND worker2 in W ?
#
# 5. If yes:
#
#        count += 1
#
# 6. Return count.
#
#
# HAND-DERIVED PREDICTIONS:
#
#     internal_shift_count({"a", "b"}) = 2
#
#     internal_shift_count({"a", "b", "c"}) = 3
#
#     internal_shift_count({"b", "c"}) = 1
#
#     internal_shift_count({"a", "c"}) = 0
#
#     internal_shift_count(WORKERS) = 4
#
#     internal_shift_count(empty set) = 0
#
# ==================================================================================================


def internal_shift_count(W):
    for worker in W:
        if worker not in WORKERS:
            raise ValueError(f"W contains unknown worker {worker!r}")

    count = 0

    for _shift_id, worker1, worker2 in SHIFTS:
        if worker1 in W and worker2 in W:
            count += 1

    return count


# ==================================================================================================
# PRIMITIVE 3 — fringe(W)
# ==================================================================================================
#
# MATHEMATICAL DEFINITION:
#
#     ∂(W)
#
# is the collection of PHYSICAL SHIFT COPIES having exactly one endpoint
# inside W.
#
#
# FRINGE CONDITION:
#
# For:
#
#     (shift_id, worker1, worker2)
#
# define the two membership statements:
#
#     worker1 in W
#     worker2 in W
#
# A shift is on the fringe exactly when those two Boolean values differ.
#
# In Python:
#
#     (worker1 in W) != (worker2 in W)
#
#
# BOOLEAN / XOR INTERPRETATION:
#
#     True  != True   -> False
#     False != False  -> False
#     True  != False  -> True
#     False != True   -> True
#
# Therefore:
#
#     both inside   -> not fringe
#     both outside  -> not fringe
#     exactly one inside -> fringe
#
#
# INTERNAL VERSUS FRINGE:
#
#     internal:
#         both endpoints inside
#         AND condition
#
#     fringe:
#         exactly one endpoint inside
#         XOR condition
#
#
# RETURN REPRESENTATION:
#
# fringe(W) returns a LIST OF SHIFT IDs.
#
# Example:
#
#     ["s0", "s1", "s2"]
#
# rather than full:
#
#     (shift_id, worker1, worker2)
#
# triples.
#
#
# WHY SHIFT IDs:
#
# The later candidate S is represented as a set of physical shift IDs.
#
# The future evaluator uses:
#
#     |S|
#
# rather than the selected shifts' endpoints.
#
# Returning IDs therefore aligns the primitive directly with the
# downstream candidate representation.
#
#
# WHY A LIST:
#
# SHIFTS has stable list order:
#
#     s0, s1, s2, s3
#
# fringe(W) scans that list in order and appends matching IDs.
#
# Therefore the returned fringe list inherits deterministic order.
#
# Later:
#
#     itertools.combinations(...)
#
# will preserve that input order while enumerating every subset S.
#
# This gives a deterministic search order, which is necessary for the
# contract:
#
#     first encountered maximizer wins ties.
#
#
# PARALLEL SHIFT COPIES:
#
# For:
#
#     W = {b}
#
# both:
#
#     s0 = (a,b)
#     s1 = (a,b)
#
# are fringe shifts.
#
# Since their IDs are different, the result contains both:
#
#     ["s0", "s1", "s2"]
#
# Physical parallel-copy identity is therefore preserved.
#
#
# QUERY CONTRACT:
#
# Every worker supplied in W must belong to WORKERS.
#
# Example invalid query:
#
#     W = {"c", "x"}
#
# should raise:
#
#     ValueError: W contains unknown worker 'x'
#
#
# EMPTY-CREW BEHAVIOR:
#
# For the empty crew, every shift has both endpoints outside.
#
# Therefore:
#
#     fringe(empty set) = []
#
#
# FULL-CREW BEHAVIOR:
#
# For W = WORKERS, every shift has both endpoints inside.
#
# Therefore:
#
#     fringe(WORKERS) = []
#
#
# COMMENTS-FIRST ALGORITHM:
#
# 1. Verify every worker in W belongs to WORKERS.
#
# 2. Start:
#
#        crossing_shift_ids = []
#
# 3. Scan every physical shift copy in SHIFTS.
#
# 4. For each:
#
#        (shift_id, worker1, worker2)
#
#    evaluate:
#
#        (worker1 in W) != (worker2 in W)
#
# 5. If True:
#
#        append shift_id
#
# 6. Return crossing_shift_ids.
#
#
# HAND-DERIVED PREDICTIONS:
#
#     fringe({"a", "b"})
#
#         = ["s2"]
#
#
#     fringe({"b"})
#
#         = ["s0", "s1", "s2"]
#
#
#     fringe({"a", "c"})
#
#         = ["s0", "s1", "s2", "s3"]
#
#
#     fringe({"a", "b", "c"})
#
#         = ["s3"]
#
#
#     fringe({"b", "c", "d"})
#
#         = ["s0", "s1"]
#
#
#     fringe(WORKERS)
#
#         = []
#
#
#     fringe(empty set)
#
#         = []
#
# ==================================================================================================


def fringe(W):
    for worker in W:
        if worker not in WORKERS:
            raise ValueError(f"W contains unknown worker {worker!r}")

    crossing_shift_ids = []

    for shift_id, worker1, worker2 in SHIFTS:
        if (worker1 in W) != (worker2 in W):
            crossing_shift_ids.append(shift_id)

    return crossing_shift_ids
````

Run the seven passing predictions plus the bad-query case now. Then paste the outputs, and we’ll close and commit the primitive layer.

==================================================================================================================================================================






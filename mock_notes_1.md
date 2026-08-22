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


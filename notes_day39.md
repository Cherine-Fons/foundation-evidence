# Task — Build the Locked Toy Instance in `instance.py`

## What the Task Is Asking

Create a standalone instance module containing the three pieces of data that define the hand-verified toy multigraph:

```text
VERTICES
EDGES
F_VALUES
```

This file records the **graph-level instance**. It does not yet enumerate candidate pairs or test pair admissibility.

The manuscript’s model is a finite, nonempty, loopless multigraph; parallel edge copies are counted separately, and (f) is a positive integer-valued function on the vertices. 

---

## Create and Verify the File

From the feature branch at:

```text
(.venv) foundation %
```

run:

```bash
code instance.py
```

Then verify:

```bash
ls instance.py
```

### Prediction

```text
instance.py
```

---

# Type Decision 1 — `VERTICES`

## Choice

Use a:

```python
frozenset
```

## Why

The vertex collection is:

* fixed after the instance is defined
* unordered
* used frequently for membership checks
* not something the checker should accidentally modify

A `frozenset` gives set-style membership while making the collection immutable.

```python
VERTICES = frozenset({0, 1, 2, 3, 4})
```

> `frozenset` means: fixed, unordered, unique collection.

One later precision: if deterministic iteration order is needed, use:

```python
sorted(VERTICES)
```

rather than relying on the iteration order of the `frozenset`.

---

# Type Decision 2 — `EDGES`

## Choice

Use a:

```python
list
```

Each edge copy is represented as:

```python
(edge_id, u, v)
```

The six locked copies are:

```python
EDGES = [
    ("e0", 0, 1),
    ("e1", 0, 1),
    ("e2", 1, 2),
    ("e3", 2, 3),
    ("e4", 3, 4),
    ("e5", 2, 4),
]
```

## Why the Edges Must Stay a List

This is a **multigraph**, so edges are actual copies, not merely adjacent vertex pairs.

```text
e0 = (0, 1)
e1 = (0, 1)
```

have the same endpoints but are two distinct edges. Their IDs preserve that identity.

A list is the correct contract because it:

* retains every explicit edge copy
* preserves a deterministic input order
* allows parallel copies without treating the edge collection as a uniqueness-only object
* makes later enumeration by edge ID straightforward

With the IDs included, a Python set of the full three-part tuples would technically keep `e0` and `e1` distinct. But a set is still the wrong abstraction: it discards order and encourages treating the edge collection as a collection of unique endpoint relations. If edge IDs were omitted and only `(u, v)` pairs were stored, a set would collapse the parallel copies immediately.

The manuscript explicitly requires parallel edges to be counted separately. 

> **Do not represent this multigraph as a set of endpoint pairs.**

---

# Type Decision 3 — `F_VALUES`

## Choice

Use a:

```python
dict
```

A dictionary maps each vertex to its assigned (f)-value:

```python
F_VALUES = {
    0: 1,
    1: 1,
    2: 2,
    3: 2,
    4: 2,
}
```

This directly represents:

[
f:V(G)\to\mathbb Z_{>0}.
]

For example:

```python
F_VALUES[2]
```

returns:

```text
2
```

and later:

```python
sum(F_VALUES[v] for v in U)
```

will compute (f(U)).

---

# Complete `instance.py`

```python
# The fixed vertex set of the toy multigraph.
#
# A frozenset is appropriate because:
# - vertex order does not matter,
# - membership checks will be frequent,
# - the instance's vertex set should not be mutated.
VERTICES = frozenset({0, 1, 2, 3, 4})


# The explicit edge copies of the loopless multigraph.
#
# Each edge is stored as:
#
#     (edge_id, endpoint_u, endpoint_v)
#
# e0 and e1 are distinct parallel edge copies even though they have
# the same endpoints.
#
# EDGES must remain a list so every explicit edge copy and its stable
# input order are preserved.
EDGES = [
    ("e0", 0, 1),
    ("e1", 0, 1),
    ("e2", 1, 2),
    ("e3", 2, 3),
    ("e4", 3, 4),
    ("e5", 2, 4),
]


# The locked positive integer vertex function:
#
#     f = (1, 1, 2, 2, 2)
#
# The dictionary maps:
#
#     vertex -> f-value
F_VALUES = {
    0: 1,
    1: 1,
    2: 2,
    3: 2,
    4: 2,
}
```

---

## Expected Instance Facts

```text
number of vertices = 5
number of edge copies = 6
number of f-values = 5
```

Parallel pair:

```text
e0 = (0, 1)
e1 = (0, 1)
```

Bridge:

```text
e2 = (1, 2)
```

Triangle:

```text
e3 = (2, 3)
e4 = (3, 4)
e5 = (2, 4)
```

Locked (f)-assignment:

```text
f = (1, 1, 2, 2, 2)
```

---

> **RULE TO BANK:**
> Use a `frozenset` for a fixed unordered vertex domain, a `list` for explicit multigraph edge copies, and a `dict` for the vertex-to-(f)-value mapping.

======================================================================================================================================================================

# Task — Compute Vertex Degrees from the Explicit Edge Copies

## What the Task Is Asking

The instance-level validator eventually needs to check

[
f(v)\le d_G(v)
]

for every vertex. So before validating that condition, the program needs to compute the degree of every vertex from `EDGES`.

The manuscript defines (d_G(v)) with **parallel edges counted separately**, and explicitly notes that the degrees can be computed by a single preprocessing scan of the edge list.  

---

## What Structure Accumulates the Counts?

Use a **dictionary**:

```python
degrees = {
    vertex: degree
}
```

More specifically, initialize every vertex at degree `0`:

```python
degrees = {v: 0 for v in VERTICES}
```

That gives:

```text
0 → 0
1 → 0
2 → 0
3 → 0
4 → 0
```

before any edges have been scanned.

### Why initialize every vertex?

Because the returned dictionary should describe the **entire vertex set**, not only vertices that happened to appear in an edge.

That will also make later instance validation straightforward.

---

# Comments-First Pseudocode

Before writing the live function, the reasoning is:

```python
# Start every vertex with degree 0.
#
# Walk through EDGES exactly once.
#
# Each edge has the form:
#
#     (edge_id, u, v)
#
# For every edge copy:
#
#     add 1 to the degree of u
#     add 1 to the degree of v
#
# Return the completed vertex -> degree dictionary.
#
# IMPORTANT:
# parallel edge copies are separate entries in EDGES,
# so each copy contributes separately to both endpoint degrees.
```

---

## Why Each Edge Adds `1` to Both Endpoints

For an ordinary loopless edge:

```text
(u, v)
```

the edge is incident with both:

```text
u
v
```

so it contributes:

```text
+1 to d(u)
+1 to d(v)
```

This agrees with the manuscript's multigraph convention: every parallel copy counts separately in vertex degrees. 

For example:

```text
e0 = (0, 1)
e1 = (0, 1)
```

are two separate copies.

Therefore together they contribute:

```text
vertex 0 → +2
vertex 1 → +2
```

They must **not** collapse into a single contribution.

---

# Write `compute_degrees()`

Add this below the locked data in `instance.py`:

```python
def compute_degrees():
    degrees = {v: 0 for v in VERTICES}

    for edge_id, u, v in EDGES:
        degrees[u] += 1
        degrees[v] += 1

    return degrees
```

### One small syntax point

In this version:

```python
for edge_id, u, v in EDGES:
```

`edge_id` is unpacked even though the degree calculation does not need it.

That is fine: the edge ID matters to the graph representation even when this particular computation only needs the endpoints.

You could also write:

```python
for _, u, v in EDGES:
```

to signal explicitly that this function does not use the ID. Either is valid; for the learning build, I would use:

```python
for edge_id, u, v in EDGES:
```

because it keeps the full edge structure visible while you are first building the checker.

---

# Prediction — Expected Degree Dictionary

Using:

```python
EDGES = [
    ("e0", 0, 1),
    ("e1", 0, 1),
    ("e2", 1, 2),
    ("e3", 2, 3),
    ("e4", 3, 4),
    ("e5", 2, 4),
]
```

we predict:

```text
vertex 0:
e0, e1
→ degree 2

vertex 1:
e0, e1, e2
→ degree 3

vertex 2:
e2, e3, e5
→ degree 3

vertex 3:
e3, e4
→ degree 2

vertex 4:
e4, e5
→ degree 2
```

So:

```python
{
    0: 2,
    1: 3,
    2: 3,
    3: 2,
    4: 2,
}
```

---

# Sanity Check

The degree sum should be:

```text
2 + 3 + 3 + 2 + 2
= 12
```

There are six edge copies:

```text
|E| = 6
```

For a loopless graph:

```text
sum of degrees = 2 × number of edges
```

so:

```text
12 = 2 × 6
```

✓ consistent.

---

> **RULE TO BANK:**
> To compute degrees in an explicit loopless multigraph, initialize one count per vertex and scan the edge-copy list once. **Every edge copy contributes `+1` to each endpoint, so parallel copies automatically contribute multiplicity.**

======================================================================================================================================================================

# Task — Run `compute_degrees()` Against the Hand-Derived Audit

## What the Task Is Asking

You have written:

```python
def compute_degrees():
    degrees = {v: 0 for v in VERTICES}

    for edge_id, u, v in EDGES:
        degrees[u] += 1
        degrees[v] += 1

    return degrees
```

Before trusting the function, predict its result from the graph **independently**, then temporarily print the function's output and compare it with the known degree audit.

---

## Prediction — Degree of Every Vertex

The locked edge list is:

```python
EDGES = [
    ("e0", 0, 1),
    ("e1", 0, 1),
    ("e2", 1, 2),
    ("e3", 2, 3),
    ("e4", 3, 4),
    ("e5", 2, 4),
]
```

### Vertex `0`

Incident edge copies:

```text
e0
e1
```

Therefore:

```text
d(0) = 2
```

### Vertex `1`

Incident edge copies:

```text
e0
e1
e2
```

Therefore:

```text
d(1) = 3
```

### Vertex `2`

Incident edge copies:

```text
e2
e3
e5
```

Therefore:

```text
d(2) = 3
```

### Vertex `3`

Incident edge copies:

```text
e3
e4
```

Therefore:

```text
d(3) = 2
```

### Vertex `4`

Incident edge copies:

```text
e4
e5
```

Therefore:

```text
d(4) = 2
```

So the expected mapping is:

```python
{
    0: 2,
    1: 3,
    2: 3,
    3: 2,
    4: 2,
}
```

---

## Why the Parallel Pair Matters

These are two separate entries:

```python
("e0", 0, 1)
("e1", 0, 1)
```

so the loop processes them on **two separate passes**.

Each pass contributes:

```text
+1 to vertex 0
+1 to vertex 1
```

Together:

```text
vertex 0 gets +2
vertex 1 gets +2
```

No special “multiplicity code” is required because multiplicity is already represented by separate edge copies.

---

## Temporary Check

At the very bottom of `instance.py`, temporarily add:

```python
print(compute_degrees())
```

Then run:

```bash
python instance.py
```

### Expected Output

The mapping should contain exactly:

```text
0 → 2
1 → 3
2 → 3
3 → 2
4 → 2
```

It may print as:

```text
{0: 2, 1: 3, 2: 3, 3: 2, 4: 2}
```

### Small Precision

Because `VERTICES` is a `frozenset`, you should care about the **mapping**, not rely on a particular printed key order.

The correctness claim is:

```python
compute_degrees() == {
    0: 2,
    1: 3,
    2: 3,
    3: 2,
    4: 2,
}
```

not “the keys must visually print in this exact sequence.”

---

## After It Matches

Delete the temporary line:

```python
print(compute_degrees())
```

The module should return to being **silent when imported**.

That keeps the same module discipline you've already established:

```text
module
→ defines data and reusable functions
→ does not perform demonstration prints at top level
```

---

> **RULE TO BANK:**
> Derive the expected graph quantity by hand first, then use a temporary print or test only to confirm the implementation. **The code verifies against the oracle; the code does not create the oracle.**

======================================================================================================================================================================

# Task — Write `validate_instance()` and Make Invalid Instances Fail Loudly

## Design Decision — What Should Happen When Validation Fails?

**Choice: 1 — raise an exception.**

> An invalid graph instance is not a recoverable “maybe” result; it violates assumptions the checker is about to trust. The validator should **stop execution immediately and identify the violated condition**, rather than quietly returning `False` and relying on a caller to remember to inspect it.

For these input-contract violations, I would use:

```python
ValueError
```

rather than merely printing a warning.

---

# What `validate_instance()` Must Check

The validator runs once at the **instance level** and checks these four conditions:

```text
1. VERTICES is nonempty
2. the graph is loopless
3. every f(v) is a positive integer
4. f(v) ≤ d_G(v) for every vertex
```

These are separate from the later admissibility conditions on individual `(U, F)` pairs.

---

# Comments-First Design

Add this reasoning above the function in `instance.py`:

```python
# --------------------------------------------------------------------------------------------------
# VALIDATE THE GRAPH INSTANCE
# --------------------------------------------------------------------------------------------------
#
# These are INSTANCE-LEVEL checks.
#
# They run once on the graph before the checker trusts the instance.
#
# If any condition fails, raise ValueError immediately.
# Do not quietly return False, because a caller could forget to check it.
#
# Check 1:
#     VERTICES must be nonempty.
#
# Check 2:
#     the graph must be loopless.
#     For every edge (edge_id, u, v), require u != v.
#
# Check 3:
#     every f(v) must be a positive integer.
#
# Check 4:
#     compute the degrees, counting parallel edge copies separately,
#     and require:
#
#         f(v) <= d_G(v)
#
#     for every vertex v.
#
# If all four checks pass, the function finishes normally.
```

---

# Code to Add

Below `compute_degrees()`, add:

```python
def validate_instance():
    # Check 1 — the vertex set must be nonempty.
    if not VERTICES:
        raise ValueError("VERTICES must be nonempty")

    # Check 2 — the multigraph must be loopless.
    for edge_id, u, v in EDGES:
        if u == v:
            raise ValueError(f"loop detected on edge {edge_id}: ({u}, {v})")

    # Check 3 — every f-value must be a positive integer.
    for v in VERTICES:
        f_value = F_VALUES[v]

        if type(f_value) is not int or f_value <= 0:
            raise ValueError(
                f"f({v}) must be a positive integer, got {f_value!r}"
            )

    # Check 4 — active-regime condition f(v) <= d_G(v).
    degrees = compute_degrees()

    for v in VERTICES:
        if F_VALUES[v] > degrees[v]:
            raise ValueError(
                f"active-regime violation at vertex {v}: "
                f"f({v})={F_VALUES[v]} > d_G({v})={degrees[v]}"
            )
```

---

# Why `type(f_value) is not int`?

You might expect:

```python
isinstance(f_value, int)
```

but Python has a subtlety:

```python
isinstance(True, int)
```

is `True`.

For a mathematical function

```text
f : V → positive integers
```

I do **not** want:

```python
True
False
```

silently accepted as legitimate integer capacities.

So:

```python
type(f_value) is int
```

expresses the stricter contract we actually intend here.

---

# Prediction for the Locked Instance

Your current data satisfy all four checks.

### Check 1

```text
VERTICES = {0,1,2,3,4}
```

Nonempty → **pass**

### Check 2

Every edge has different endpoints:

```text
e0 = 0–1
e1 = 0–1
e2 = 1–2
e3 = 2–3
e4 = 3–4
e5 = 2–4
```

No loops → **pass**

### Check 3

```text
f = (1,1,2,2,2)
```

Every value is a positive integer → **pass**

### Check 4

```text
f = (1,1,2,2,2)
d = (2,3,3,2,2)
```

Vertex by vertex:

```text
1 ≤ 2
1 ≤ 3
2 ≤ 3
2 ≤ 2
2 ≤ 2
```

Active-regime condition → **pass**

Therefore, calling:

```python
validate_instance()
```

should produce **no error**.

That silence means:

> all required instance assumptions passed.

---

# One Important Distinction

A validator that succeeds does not need to print:

```text
"valid!"
```

Its contract can simply be:

```text
valid instance
→ return normally

invalid instance
→ raise ValueError immediately
```

Later, pytest can explicitly test both behaviors.

---

> **RULE TO BANK:**
> **Validation guards invariants. Invalid foundational input should fail loudly.**
> For this checker, `validate_instance()` returns normally when the graph satisfies its contract and raises a specific exception the moment an instance-level assumption is violated.
===============================================================================================================================================================

# Task — Write `validate_instance()`

## What the Task Is Asking

`validate_instance()` is the **instance-level gatekeeper**. It runs before the checker trusts the graph.

It must verify four assumptions, in this order:

1. `VERTICES` is nonempty.
2. The graph is loopless.
3. Every vertex has a positive-integer `f`-value.
4. Every vertex satisfies `f(v) <= d_G(v)`.

If anything is wrong, the function should **raise `ValueError` immediately and name the offending vertex or edge**.

---

## Comments-First Logic

Add this below `compute_degrees()` in `instance.py`:

```python
# ==================================================================================================
# VALIDATE INSTANCE
# ==================================================================================================
#
# These are GRAPH-LEVEL checks.
#
# They run once before the checker trusts the instance.
# They are separate from the later admissibility checks on a candidate pair (U, F).
#
# Failure behavior:
#
#     invalid instance -> raise ValueError immediately
#
# The error message should identify the vertex or edge that violated the rule.
#
#
# CHECK 1:
#     VERTICES must be nonempty.
#
# CHECK 2:
#     The graph must be loopless.
#
#     Every edge has the form:
#
#         (edge_id, u, v)
#
#     and must satisfy:
#
#         u != v
#
# CHECK 3:
#     Every vertex must have an f-value.
#
#     That f-value must be a positive integer:
#
#         type(f(v)) is int
#         f(v) > 0
#
# CHECK 4:
#     Compute the degrees using compute_degrees().
#
#     Then require:
#
#         f(v) <= d_G(v)
#
#     for every vertex.
#
# If every check passes, return normally without printing anything.
# =============================================================================================================================================


def validate_instance():
    # Check 1 — the vertex set must be nonempty.
    if not VERTICES:
        raise ValueError("VERTICES must be nonempty")

    # Check 2 — the multigraph must be loopless.
    for edge_id, u, v in EDGES:
        if u == v:
            raise ValueError(
                f"loop detected on edge {edge_id}: endpoints are ({u}, {v})"
            )

    # Check 3 — every vertex must have a positive integer f-value.
    for v in VERTICES:
        if v not in F_VALUES:
            raise ValueError(f"missing f-value for vertex {v}")

        f_value = F_VALUES[v]

        if type(f_value) is not int or f_value <= 0:
            raise ValueError(
                f"f({v}) must be a positive integer, got {f_value!r}"
            )

    # Check 4 — active-regime condition f(v) <= d_G(v).
    degrees = compute_degrees()

    for v in VERTICES:
        if F_VALUES[v] > degrees[v]:
            raise ValueError(
                f"active-regime violation at vertex {v}: "
                f"f({v})={F_VALUES[v]} > d_G({v})={degrees[v]}"
            )
```

## Prediction for the Locked Instance

With:

```text
f = (1, 1, 2, 2, 2)
d = (2, 3, 3, 2, 2)
```

all four checks should pass:

```text
VERTICES nonempty      ✓
no loops               ✓
all f-values positive  ✓
f(v) <= d_G(v)         ✓
```

So calling:

```python
validate_instance()
```

should produce **no output and no exception**.

That silence means the instance passed validation.

---

## Why the Missing-`f` Check Is Separate

This matters:

```python
if v not in F_VALUES:
    raise ValueError(...)
```

Without it, doing:

```python
F_VALUES[v]
```

on a missing vertex would raise a generic `KeyError`.

The explicit check instead gives a meaningful validator message such as:

```text
missing f-value for vertex 3
```

which tells you exactly which invariant failed.

---

> **RULE TO BANK:**
> A validator should **fail loudly, early, and specifically**. Check the structural assumptions first, then compute derived quantities such as degrees, and name the exact vertex or edge responsible for any failure.

===============================================================================================================================================================

# Task — Confirm the Valid Instance Passes

Before deliberately breaking anything, confirm the **known-correct instance** passes all four guards.

For this temporary check, add:

```python
validate_instance()
print("instance valid")
```

at the bottom of `instance.py`.



## Prediction Before Running

Run:

```bash
python instance.py
```

I expect exactly:

```text
instance valid
```

### Why

`validate_instance()` itself prints nothing.

It checks all four conditions and, because the locked instance is valid, reaches the end normally.

Only then does Python execute:

```python
print("instance valid")
```

If any validation condition failed, execution would stop at the `ValueError`, and `"instance valid"` would **never print**.

> **RULE TO BANK:**
> A passing validator is silent; a failing validator raises. When testing the passing path, put a temporary print **after** the validation call—if the message appears, execution made it through every guard.
===============================================================================================================================================================


# Break 1 — Prove the Loop Guard Rejects

## What the Task Is Asking

Temporarily corrupt the valid multigraph by changing:

```python
("e5", 2, 4)
```

to:

```python
("e5", 2, 2)
```

That creates a **loop at vertex `2`** because both endpoints of `e5` are now the same.

Then run:

```bash
python instance.py
```

The purpose is to prove that the looplessness guard does not merely exist—it actually rejects invalid data.

---

## Prediction — Which Check Fires?

**Check 2 — the loopless check** will fire.

Check 1 passes first because:

```python
VERTICES = frozenset({0, 1, 2, 3, 4})
```

is nonempty.

Then Python scans `EDGES`:

```text
e0 → 0 != 1 ✓
e1 → 0 != 1 ✓
e2 → 1 != 2 ✓
e3 → 2 != 3 ✓
e4 → 3 != 4 ✓
e5 → 2 == 2 ✗
```

At `e5`, this condition becomes true:

```python
if u == v:
```

so execution immediately raises `ValueError`.

Because the validator is **fail-fast**, Checks 3 and 4 are never reached.

---

# Exact Predicted Error Message

The code is:

```python
raise ValueError(
    f"loop detected on edge {edge_id}: endpoints are ({u}, {v})"
)
```

For:

```text
edge_id = "e5"
u = 2
v = 2
```

the f-string becomes exactly:

```text
loop detected on edge e5: endpoints are (2, 2)
```

Therefore the final line of the traceback should be:

```text
ValueError: loop detected on edge e5: endpoints are (2, 2)
```

---

## What Will Not Print

This line at the bottom:

```python
print("instance valid")
```

should **not execute**, because the exception stops the program first.

So you should *not* see:

```text
instance valid
```

---

## Run It

```bash
python instance.py
```

### Expected final traceback line

```text
ValueError: loop detected on edge e5: endpoints are (2, 2)
```

> **RULE TO BANK:**
> A fail-fast validator stops at the **first violated invariant**. Once `e5` is detected as a loop, execution halts immediately; later validation checks and the success print never run.
===================================================================================================================================================================

# Break 2 — Prove the Active-Regime Guard Rejects

## What the Task Is Asking

Temporarily violate:

[
f(v)\le d_G(v)
]

at vertex `3` by changing:

```python
3: 2,
```

to:

```python
3: 5,
```

### Important First

Make sure you have **restored Break 1** first:

```python
("e5", 2, 4)
```

not:

```python
("e5", 2, 2)
```

Otherwise the validator is fail-fast and the loop check will stop execution **before** it ever reaches the active-regime check.

---

## Prediction — Which Check Fires?

**Check 4 — the active-regime condition** will fire.

The earlier checks pass:

```text
Check 1 → VERTICES is nonempty          ✓
Check 2 → all edges are loopless        ✓
Check 3 → every f-value is positive int ✓
Check 4 → f(v) <= d_G(v)                ✗ at vertex 3
```

For vertex `3`:

```text
f(3) = 5
d_G(3) = 2
```

so Python evaluates:

```python
F_VALUES[3] > degrees[3]
```

as:

```text
5 > 2
→ True
```

and raises the exception.

---

## Exact Predicted Message

Your code constructs:

```python
raise ValueError(
    f"active-regime violation at vertex {v}: "
    f"f({v})={F_VALUES[v]} > d_G({v})={degrees[v]}"
)
```

At vertex `3`, that becomes exactly:

```text
active-regime violation at vertex 3: f(3)=5 > d_G(3)=2
```

So the **last traceback line** should be:

```text
ValueError: active-regime violation at vertex 3: f(3)=5 > d_G(3)=2
```

And this should **not** print:

```text
instance valid
```

because execution stops at the exception.

---

# Complete Temporary `instance.py` for Break 2

```python
# ==================================================================================================
# F7 CAPSTONE — TOY MULTIGRAPH INSTANCE
# ==================================================================================================
#
# This module contains:
#
# 1. VERTICES
# 2. EDGES
# 3. F_VALUES
# 4. compute_degrees()
# 5. validate_instance()
#
# IMPORTANT:
#
# This is the TEMPORARILY CORRUPTED version for Break 2.
#
# We deliberately set:
#
#     f(3) = 5
#
# even though:
#
#     d_G(3) = 2
#
# so validate_instance() should reject the instance.
#
# ==================================================================================================


VERTICES = frozenset({0, 1, 2, 3, 4})


EDGES = [
    ("e0", 0, 1),
    ("e1", 0, 1),
    ("e2", 1, 2),
    ("e3", 2, 3),
    ("e4", 3, 4),
    ("e5", 2, 4),
]


# TEMPORARY BREAK:
#
# Correct value:
#
#     3: 2
#
# Corrupted value for this test:
#
#     3: 5
F_VALUES = {
    0: 1,
    1: 1,
    2: 2,
    3: 5,
    4: 2,
}


# --------------------------------------------------------------------------------------------------
# COMPUTE DEGREES
# --------------------------------------------------------------------------------------------------
#
# Each explicit edge copy contributes:
#
#     +1 to each endpoint.
#
# Parallel copies therefore count separately.
#
# For the restored edge set:
#
#     degrees = {
#         0: 2,
#         1: 3,
#         2: 3,
#         3: 2,
#         4: 2,
#     }
#
# --------------------------------------------------------------------------------------------------


def compute_degrees():
    degrees = {v: 0 for v in VERTICES}

    for edge_id, u, v in EDGES:
        degrees[u] += 1
        degrees[v] += 1

    return degrees


# --------------------------------------------------------------------------------------------------
# VALIDATE INSTANCE
# --------------------------------------------------------------------------------------------------
#
# CHECK 1:
#     VERTICES must be nonempty.
#
# CHECK 2:
#     No edge may have u == v.
#
# CHECK 3:
#     Every vertex must have a positive integer f-value.
#
# CHECK 4:
#     Require:
#
#         f(v) <= d_G(v)
#
#     for every vertex.
#
# Invalid input raises ValueError immediately.
# --------------------------------------------------------------------------------------------------


def validate_instance():
    # Check 1 — vertex set must be nonempty.
    if not VERTICES:
        raise ValueError("VERTICES must be nonempty")

    # Check 2 — graph must be loopless.
    for edge_id, u, v in EDGES:
        if u == v:
            raise ValueError(
                f"loop detected on edge {edge_id}: endpoints are ({u}, {v})"
            )

    # Check 3 — every vertex must have a positive integer f-value.
    for v in VERTICES:
        if v not in F_VALUES:
            raise ValueError(f"missing f-value for vertex {v}")

        f_value = F_VALUES[v]

        if type(f_value) is not int or f_value <= 0:
            raise ValueError(
                f"f({v}) must be a positive integer, got {f_value!r}"
            )

    # Check 4 — active-regime condition f(v) <= d_G(v).
    degrees = compute_degrees()

    for v in VERTICES:
        if F_VALUES[v] > degrees[v]:
            raise ValueError(
                f"active-regime violation at vertex {v}: "
                f"f({v})={F_VALUES[v]} > d_G({v})={degrees[v]}"
            )


# --------------------------------------------------------------------------------------------------
# TEMPORARY VALIDATION CALL
# --------------------------------------------------------------------------------------------------
#
# Prediction:
#
# validate_instance() reaches Check 4 and raises:
#
#     ValueError: active-regime violation at vertex 3: f(3)=5 > d_G(3)=2
#
# Therefore:
#
#     print("instance valid")
#
# should never execute.
# --------------------------------------------------------------------------------------------------


validate_instance()
print("instance valid")
```

## Run

```bash
python instance.py
```

> **RULE TO BANK:**
> With fail-fast validation, restore each earlier corruption before testing the next guard. Otherwise the earlier violation masks the condition you are trying to test.

===================================================================================================================================================================

# Task — Build the First Checker Primitive: `f_of(U)`

## Design Decision — What if `U` Contains a Vertex Outside the Graph?

I would **check explicitly and raise our own `ValueError`**.

For example, if someone passes:

```python
{0, 7}
```

I would rather get:

```text
ValueError: U contains unknown vertex 7
```

than a bare:

```text
KeyError: 7
```

### Why

A natural `KeyError` tells us only that a dictionary lookup failed.

Our own exception tells us **what contract was violated**:

> The caller supplied a vertex set containing something that is not a vertex of this graph.

That makes debugging the checker much easier.

---

# What `f_of(U)` Must Compute

The mathematical quantity is:

[
f(U)=\sum_{v\in U}f(v).
]

So the computation is:

```text
start total at 0
↓
for each vertex v in U
↓
confirm v is valid
↓
look up F_VALUES[v]
↓
add it to total
↓
return total
```

For the locked assignment:

```python
F_VALUES = {
    0: 1,
    1: 1,
    2: 2,
    3: 2,
    4: 2,
}
```

we already know, for example:

```text
f({0,1}) = 1 + 1 = 2
f({2,3,4}) = 2 + 2 + 2 = 6
f({0,1,2}) = 1 + 1 + 2 = 4
```

These are hand-derived values from the oracle work, so they will later make excellent tests.

---

# Current Complete `primitives.py`

```python
# ==================================================================================================
# F7 CAPSTONE — CHECKER PRIMITIVES
# ==================================================================================================
#
# This module contains the small graph computations that the later:
#
#     admissibility checks
#     density evaluation
#     brute-force enumeration
#
# will rely on.
#
# The first three primitives are:
#
#     f_of(U)
#     internal_edge_count(U)
#     boundary(U)
#
# We build and verify them one at a time.
#
# This module imports the locked graph data from instance.py.
#
# It should remain silent on import:
#
#     no top-level print statements
#     no demonstration calls
#
# ==================================================================================================


from instance import EDGES, F_VALUES


# ==================================================================================================
# PRIMITIVE 1 — f_of(U)
# ==================================================================================================
#
# PURPOSE:
#
# Compute:
#
#     f(U) = sum of f(v) over every vertex v in U
#
#
# INPUT:
#
#     U
#
# A collection of vertices, for example:
#
#     {0, 1}
#
# or:
#
#     frozenset({2, 3, 4})
#
#
# OUTPUT:
#
#     the integer f(U)
#
#
# QUERY VALIDATION:
#
# validate_instance() protects the GRAPH INSTANCE itself.
#
# It does not protect every later query made to the checker.
#
# Therefore f_of(U) checks that every vertex supplied in U actually
# appears in the graph's f-value mapping.
#
# If an unknown vertex appears, fail loudly with a useful ValueError.
#
# Example invalid query:
#
#     U = {0, 7}
#
# Desired failure:
#
#     ValueError: U contains unknown vertex 7
#
#
# COMMENTS-FIRST ALGORITHM:
#
# 1. Start:
#
#        total = 0
#
# 2. For every vertex v in U:
#
#        verify that v is a known vertex
#
#        add F_VALUES[v] to total
#
# 3. Return total.
#
#
# HAND-DERIVED CHECKPOINTS:
#
#     f({0, 1})
#         = 1 + 1
#         = 2
#
#     f({2, 3, 4})
#         = 2 + 2 + 2
#         = 6
#
#     f({0, 1, 2})
#         = 1 + 1 + 2
#         = 4
#
# ==================================================================================================


def f_of(U):
    total = 0

    for v in U:
        if v not in F_VALUES:
            raise ValueError(f"U contains unknown vertex {v}")

        total += F_VALUES[v]

    return total
```

## One Useful Consequence

If:

```python
U = set()
```

then the loop runs zero times and:

```python
f_of(U)
```

returns:

```text
0
```

That is mathematically correct:

[
f(\varnothing)=0.
]

We do **not** need `f_of()` itself to reject the empty set. Later, **pair admissibility** is responsible for enforcing:

[
U\neq\varnothing.
]

That keeps the primitive mathematical and the admissibility logic separate.

> **RULE TO BANK:**
> A primitive should compute its mathematical quantity faithfully; validate inputs that make the computation undefined, but do not smuggle higher-level admissibility rules into it. `f_of(∅)=0`; the admissibility layer is what later rejects `U=∅`.

===================================================================================================================================================================

# Task — Update `f_of(U)` to Validate Against `VERTICES`

## What the Task Is Asking

The contract is slightly sharper now:

```text
VERTICES
→ tells us whether v is actually a vertex of G

F_VALUES
→ tells us the f-value assigned to that valid vertex
```

So `f_of(U)` should first verify:

```python
v in VERTICES
```

and only then look up:

```python
F_VALUES[v]
```

That keeps **vertex membership** and **f-value lookup** conceptually separate.

---

# Predictions Before Running

The locked assignment is:

```text
f(0) = 1
f(1) = 1
f(2) = 2
f(3) = 2
f(4) = 2
```

## Prediction 1 — `f_of({0, 1})`

[
f({0,1})=f(0)+f(1)
]

so:

```text
1 + 1 = 2
```

**Prediction:**

```python
f_of({0, 1}) == 2
```

---

## Prediction 2 — `f_of({2, 3, 4})`

[
f({2,3,4})=f(2)+f(3)+f(4)
]

so:

```text
2 + 2 + 2 = 6
```

**Prediction:**

```python
f_of({2, 3, 4}) == 6
```

---

## Prediction 3 — `f_of(VERTICES)`

All five values contribute:

```text
1 + 1 + 2 + 2 + 2
= 8
```

Therefore:

[
f(V(G))=8.
]

**Prediction:**

```python
f_of(VERTICES) == 8
```

This matches the hand-derived oracle work where the whole graph had:

```text
f(V) = 8
```

and was inadmissible with `F = ∅` because `8` is even.

---

# Current `primitives.py`

```python
# ==================================================================================================
# F7 CAPSTONE — CHECKER PRIMITIVES
# ==================================================================================================
#
# This module contains the small graph computations that the later:
#
#     admissibility checks
#     density evaluation
#     brute-force enumeration
#
# will rely on.
#
# The first three primitives are:
#
#     f_of(U)
#     internal_edge_count(U)
#     boundary(U)
#
# We build and verify them one at a time.
#
# This module imports the locked graph data from instance.py.
#
# It should remain silent on import:
#
#     no top-level print statements
#     no demonstration calls
#
# ==================================================================================================


from instance import EDGES, F_VALUES, VERTICES


# ==================================================================================================
# PRIMITIVE 1 — f_of(U)
# ==================================================================================================
#
# PURPOSE:
#
# Compute:
#
#     f(U) = sum of f(v) over every vertex v in U
#
#
# INPUT:
#
#     U
#
# A collection of vertices, for example:
#
#     {0, 1}
#
# or:
#
#     frozenset({2, 3, 4})
#
#
# OUTPUT:
#
#     the integer f(U)
#
#
# QUERY VALIDATION:
#
# validate_instance() protects the GRAPH INSTANCE itself.
#
# It does not protect every later query made to the checker.
#
# Therefore f_of(U) checks that every supplied vertex actually belongs to:
#
#     VERTICES
#
# before using that vertex to look up:
#
#     F_VALUES[v]
#
#
# Example invalid query:
#
#     U = {0, 7}
#
# Since:
#
#     7 not in VERTICES
#
# the function should raise:
#
#     ValueError: U contains unknown vertex 7
#
#
# COMMENTS-FIRST ALGORITHM:
#
# 1. Start:
#
#        total = 0
#
# 2. For every vertex v in U:
#
#        check whether v belongs to VERTICES
#
#        if not:
#            raise ValueError naming v
#
#        otherwise:
#            add F_VALUES[v] to total
#
# 3. Return total.
#
#
# HAND-DERIVED CHECKPOINTS:
#
#     f({0, 1})
#
#         = f(0) + f(1)
#         = 1 + 1
#         = 2
#
#
#     f({2, 3, 4})
#
#         = f(2) + f(3) + f(4)
#         = 2 + 2 + 2
#         = 6
#
#
#     f(VERTICES)
#
#         = 1 + 1 + 2 + 2 + 2
#         = 8
#
#
# NOTE:
#
# If U is empty, the loop executes zero times and the function returns:
#
#     0
#
# This is mathematically correct:
#
#     f(empty set) = 0
#
# The later admissibility function, not this primitive, is responsible for
# rejecting U = empty set.
#
# ==================================================================================================


def f_of(U):
    total = 0

    for v in U:
        if v not in VERTICES:
            raise ValueError(f"U contains unknown vertex {v}")

        total += F_VALUES[v]

    return total
```

> **RULE TO BANK:**
> Validate a vertex against `VERTICES`; use `F_VALUES` only after membership is established. Then (f(U)) is just an accumulator: **sum `f(v)` once for every vertex in `U`.**

===================================================================================================================================================================

# Primitive 2 — `internal_edge_count(U)`

## What the Task Is Asking

Now we need the primitive that computes:

[
e(U)=|E(G[U])|.
]

In words:

> Count **every actual edge copy whose two endpoints are both inside `U`**.

Because this is a multigraph, parallel copies count separately.

---

# Predictions First

The locked edges are:

```text
e0 = (0, 1)
e1 = (0, 1)
e2 = (1, 2)
e3 = (2, 3)
e4 = (3, 4)
e5 = (2, 4)
```

## Prediction 1 — `internal_edge_count({0, 1})`

Inside `{0,1}` are:

```text
e0 = (0,1)
e1 = (0,1)
```

Both parallel copies count.

Therefore:

```python
internal_edge_count({0, 1}) == 2
```

---

## Prediction 2 — `internal_edge_count({2, 3, 4})`

Inside `{2,3,4}` are all three triangle edges:

```text
e3 = (2,3)
e4 = (3,4)
e5 = (2,4)
```

Therefore:

```python
internal_edge_count({2, 3, 4}) == 3
```

---

## Prediction 3 — `internal_edge_count({0, 1, 2})`

Inside `{0,1,2}` are:

```text
e0 = (0,1)
e1 = (0,1)
e2 = (1,2)
```

Therefore:

```python
internal_edge_count({0, 1, 2}) == 3
```

This was the tight Day-38 case:

```text
e(U) = 3
f(U) = 4
f(U) - 1 = 3
```

---

## Prediction 4 — `internal_edge_count({1})`

A singleton vertex contains no loopless internal edge.

The edges incident with `1` all leave the set `{1}`:

```text
e0 = (0,1)
e1 = (0,1)
e2 = (1,2)
```

Therefore:

```python
internal_edge_count({1}) == 0
```

---

# Comments-First Algorithm

The function should reason like this:

```python
# Verify every supplied vertex belongs to VERTICES.
#
# Start the internal-edge count at 0.
#
# Scan every explicit edge copy in EDGES.
#
# For an edge (_, u, v):
#
#     if u is in U AND v is in U:
#         this edge lies completely inside U
#         add 1
#
# Otherwise:
#     the edge is not internal to U
#     do not count it
#
# Return the total.
#
# Parallel copies are separate entries in EDGES,
# so they are automatically counted separately.
```

---

# Complete Updated `primitives.py`

```python
# ==================================================================================================
# F7 CAPSTONE — CHECKER PRIMITIVES
# ==================================================================================================
#
# This module contains the small graph computations that the later:
#
#     admissibility checks
#     density evaluation
#     brute-force enumeration
#
# will rely on.
#
# The three core primitives are:
#
#     f_of(U)
#     internal_edge_count(U)
#     boundary(U)
#
# We build and verify them one at a time.
#
# This module imports the locked graph data from instance.py.
#
# It should remain silent on import:
#
#     no top-level print statements
#     no demonstration calls
#
# ==================================================================================================


from instance import EDGES, F_VALUES, VERTICES


# ==================================================================================================
# PRIMITIVE 1 — f_of(U)
# ==================================================================================================
#
# PURPOSE:
#
# Compute:
#
#     f(U) = sum of f(v) over every vertex v in U
#
#
# QUERY VALIDATION:
#
# Every supplied vertex must belong to VERTICES.
#
# Example:
#
#     U = {0, 7}
#
# should raise:
#
#     ValueError: U contains unknown vertex 7
#
#
# COMMENTS-FIRST ALGORITHM:
#
# 1. Start:
#
#        total = 0
#
# 2. For every vertex v in U:
#
#        verify v belongs to VERTICES
#
#        add F_VALUES[v] to total
#
# 3. Return total.
#
#
# HAND-DERIVED CHECKPOINTS:
#
#     f({0, 1}) = 2
#
#     f({2, 3, 4}) = 6
#
#     f(VERTICES) = 8
#
#
# If U is empty, the loop runs zero times and returns 0.
#
# That is mathematically correct:
#
#     f(empty set) = 0
#
# The later admissibility layer is responsible for rejecting an empty U.
#
# ==================================================================================================


def f_of(U):
    total = 0

    for v in U:
        if v not in VERTICES:
            raise ValueError(f"U contains unknown vertex {v}")

        total += F_VALUES[v]

    return total


# ==================================================================================================
# PRIMITIVE 2 — internal_edge_count(U)
# ==================================================================================================
#
# PURPOSE:
#
# Compute:
#
#     e(U) = |E(G[U])|
#
# In words:
#
#     count every explicit edge copy whose BOTH endpoints belong to U.
#
#
# MULTIGRAPH RULE:
#
# Parallel edges count separately.
#
# For example:
#
#     e0 = (0,1)
#     e1 = (0,1)
#
# are two distinct internal edges when:
#
#     U = {0,1}
#
#
# QUERY VALIDATION:
#
# Every vertex supplied in U must belong to VERTICES.
#
# An unknown vertex should fail loudly rather than silently participating
# in a graph computation.
#
#
# COMMENTS-FIRST ALGORITHM:
#
# 1. Verify every vertex in U belongs to VERTICES.
#
# 2. Start:
#
#        count = 0
#
# 3. Scan every explicit edge copy:
#
#        (edge_id, u, v)
#
# 4. If:
#
#        u in U
#
#    AND:
#
#        v in U
#
#    then the edge lies completely inside U.
#
#    Add:
#
#        count += 1
#
# 5. Otherwise, do not count that edge.
#
# 6. Return count.
#
#
# HAND-DERIVED CHECKPOINTS:
#
#     internal_edge_count({0,1})
#
#         e0, e1 are internal
#
#         = 2
#
#
#     internal_edge_count({2,3,4})
#
#         e3, e4, e5 are internal
#
#         = 3
#
#
#     internal_edge_count({0,1,2})
#
#         e0, e1, e2 are internal
#
#         = 3
#
#
#     internal_edge_count({1})
#
#         no loopless edge has both endpoints in {1}
#
#         = 0
#
# ==================================================================================================


def internal_edge_count(U):
    for v in U:
        if v not in VERTICES:
            raise ValueError(f"U contains unknown vertex {v}")

    count = 0

    for _edge_id, u, v in EDGES:
        if u in U and v in U:
            count += 1

    return count
```

## Why `_edge_id` Instead of `edge_id`?

This primitive needs the endpoints:

```python
u
v
```

but not the edge's name.

Writing:

```python
for _edge_id, u, v in EDGES:
```

still shows the full three-field edge structure, while the leading underscore communicates:

> “This value is intentionally unpacked but unused in this function.”

That also keeps the code friendly to linting tools such as Ruff.

---

> **RULE TO BANK:**
> `internal_edge_count(U)` scans **edge copies**, not endpoint pairs. An edge contributes exactly when **both endpoints lie in `U`**, and parallel copies each contribute `+1` independently.

==========================================================================================================================================================================

# Primitive 3 — `boundary(U)`

## Design Decision — What Should `boundary(U)` Return?

I would return a **list of edge IDs**:

```python
["e0", "e1", "e2"]
```

rather than full triples such as:

```python
[("e0", 0, 1), ("e1", 0, 1), ("e2", 1, 2)]
```

### Why

This representation fits both downstream consumers directly.

For **F-enumeration**, we need distinct edge copies. The IDs already preserve that distinction:

```text
e0
e1
```

remain separate even though both have endpoints `(0,1)`.

For the eventual checker result, we already decided that `F` will be represented as edge IDs:

```python
frozenset({"e2"})
```

And the density evaluator only needs:

```python
len(F)
```

not the endpoints of the selected edges.

So returning IDs avoids carrying endpoint information that the later `(U,F)` representation does not actually need.

A **list** is preferable to a set here because it preserves the stable order inherited from `EDGES`, which will make later subset enumeration deterministic.

> **DESIGN RULE TO BANK:**
> `boundary(U)` uses full edge triples to *decide* whether an edge crosses, but returns only the **edge-copy IDs**, because IDs are the representation that `F` needs downstream.

---

# Predictions First

The locked edge copies are:

```text
e0 = (0,1)
e1 = (0,1)
e2 = (1,2)
e3 = (2,3)
e4 = (3,4)
e5 = (2,4)
```

The boundary condition is:

> An edge belongs to (\partial_G(U)) exactly when **one endpoint is in `U` and the other is outside `U`**. 

In code, that is:

```python
(u in U) != (v in U)
```

---

## Prediction 1 — `boundary({0, 1})`

Check each edge:

```text
e0 = (0,1)
both endpoints inside
→ not boundary

e1 = (0,1)
both endpoints inside
→ not boundary

e2 = (1,2)
1 inside, 2 outside
→ boundary

e3, e4, e5
both endpoints outside
→ not boundary
```

Therefore:

```python
boundary({0, 1}) == ["e2"]
```

---

## Prediction 2 — `boundary({1})`

```text
e0 = (0,1)
0 outside, 1 inside
→ boundary

e1 = (0,1)
0 outside, 1 inside
→ boundary

e2 = (1,2)
1 inside, 2 outside
→ boundary
```

The remaining triangle edges have both endpoints outside `{1}`.

Therefore:

```python
boundary({1}) == ["e0", "e1", "e2"]
```

This is an important multigraph check: **both parallel copies appear separately in the boundary**.

---

## Prediction 3 — `boundary({2, 3, 4})`

The triangle edges:

```text
e3
e4
e5
```

have both endpoints inside the set, so they are internal.

The bridge:

```text
e2 = (1,2)
```

has:

```text
1 outside
2 inside
```

so it crosses.

Therefore:

```python
boundary({2, 3, 4}) == ["e2"]
```

---

## Prediction 4 — `boundary(VERTICES)`

If:

```python
U = VERTICES
```

then **every endpoint of every edge is inside `U`**.

There is no outside vertex for an edge to cross to.

Therefore:

```python
boundary(VERTICES) == []
```

or mathematically:

[
\partial_G(V(G))=\varnothing.
]

---

# Complete Updated `primitives.py`

```python
# ==================================================================================================
# F7 CAPSTONE — CHECKER PRIMITIVES
# ==================================================================================================
#
# This module contains the small graph computations that the later:
#
#     admissibility checks
#     density evaluation
#     brute-force enumeration
#
# will rely on.
#
# The three core primitives are:
#
#     f_of(U)
#     internal_edge_count(U)
#     boundary(U)
#
# This module imports the locked graph data from instance.py.
#
# It should remain silent on import:
#
#     no top-level print statements
#     no demonstration calls
#
# ==================================================================================================


from instance import EDGES, F_VALUES, VERTICES


# ==================================================================================================
# PRIMITIVE 1 — f_of(U)
# ==================================================================================================


def f_of(U):
    total = 0

    for v in U:
        if v not in VERTICES:
            raise ValueError(f"U contains unknown vertex {v}")

        total += F_VALUES[v]

    return total


# ==================================================================================================
# PRIMITIVE 2 — internal_edge_count(U)
# ==================================================================================================
#

def internal_edge_count(U):
    for v in U:
        if v not in VERTICES:
            raise ValueError(f"U contains unknown vertex {v}")

    count = 0

    for _edge_id, u, v in EDGES:
        if u in U and v in U:
            count += 1

    return count


# ==================================================================================================
# PRIMITIVE 3 — boundary(U)
# ==================================================================================================
#
# PURPOSE:
#
# Compute:
#
#     ∂_G(U)
#
# the set of actual edge copies having EXACTLY ONE endpoint in U.
#
#
# IMPORTANT DISTINCTION:
#
# INTERNAL EDGE:
#
#     both endpoints in U
#
# BOUNDARY EDGE:
#
#     exactly one endpoint in U
#
# These are different collections.
#
#
# RETURN REPRESENTATION:
#
# boundary(U) returns a LIST OF EDGE IDs.
#
# Example:
#
#     ["e0", "e1", "e2"]
#
# rather than:
#
#     [(id, u, v), ...]
#
#
# WHY EDGE IDs:
#
# 1. F-enumeration needs distinct edge copies.
#
#    e0 and e1 must remain separate even though both join 0 and 1.
#
# 2. The eventual F representation is:
#
#        frozenset({"e2"})
#
#    so returning IDs matches the downstream representation directly.
#
# 3. The ratio evaluator needs only:
#
#        len(F)
#
#    not the endpoints of the selected edges.
#
#
# WHY A LIST:
#
# The boundary is returned as a list rather than a set so that:
#
#     - explicit edge-copy identity is preserved,
#     - EDGES order is preserved,
#     - later subset enumeration is deterministic.
#
#
# QUERY VALIDATION:
#
# Every supplied vertex must belong to VERTICES.
#
#
# COMMENTS-FIRST ALGORITHM:
#
# 1. Verify every vertex in U belongs to VERTICES.
#
# 2. Start:
#
#        crossing_edges = []
#
# 3. Scan every explicit edge copy:
#
#        (edge_id, u, v)
#
# 4. Test:
#
#        (u in U) != (v in U)
#
#    This is the XOR condition.
#
#    It is True exactly when:
#
#        one endpoint is inside U
#        AND
#        the other endpoint is outside U
#
# 5. If the condition is True:
#
#        append edge_id
#
# 6. Return the list of crossing edge IDs.
#
#
# HAND-DERIVED CHECKPOINTS:
#
#     boundary({0,1})
#
#         = ["e2"]
#
#
#     boundary({1})
#
#         = ["e0", "e1", "e2"]
#
#
#     boundary({2,3,4})
#
#         = ["e2"]
#
#
#     boundary(VERTICES)
#
#         = []
#
# ==================================================================================================


def boundary(U):
    for v in U:
        if v not in VERTICES:
            raise ValueError(f"U contains unknown vertex {v}")

    crossing_edges = []

    for edge_id, u, v in EDGES:
        if (u in U) != (v in U):
            crossing_edges.append(edge_id)

    return crossing_edges
```

## The XOR Line to Bank

This line:

```python
if (u in U) != (v in U):
```

works because Boolean inequality behaves like XOR:

```text
True  != True   → False
False != False  → False

True  != False  → True
False != True   → True
```

Translated back to graph language:

```text
both inside
→ not boundary

both outside
→ not boundary

one inside, one outside
→ boundary
```

> **RULE TO BANK:**
> A boundary edge has **exactly one endpoint in `U`**. In Python, `(u in U) != (v in U)` expresses that condition directly. Return edge IDs so multigraph identity survives all the way into `F`.

==========================================================================================================================================================================

# F7 Capstone — `is_admissible(U, F)`

## Create the File

From:

```text
(.venv) foundation %
```

run:

```bash
code admissibility.py
```

Then verify:

```bash
ls admissibility.py
```

### Prediction

```text
admissibility.py
```

---

# Design Question 1 — What Should `is_admissible()` Return?

## Decision: return `True` or `False`

Unlike `validate_instance()`, an inadmissible pair is **not an error**.

The brute-force search is deliberately going to generate many candidate pairs and ask:

```text
Does this pair belong to A(G)?
```

Most candidates are expected to fail.

So:

```text
admissible pair     → True
inadmissible pair   → False
```

not:

```text
inadmissible pair   → raise exception
```

> **RULE TO BANK:**
> Validation failure means the *input instance is broken* → raise.
> Admissibility failure means the *candidate is simply not feasible* → return `False`.

---

# Design Question 2 — How Should We Test `F ⊆ ∂G(U)`?

`boundary(U)` returns a list of edge IDs such as:

```python
["e0", "e1", "e2"]
```

The clean subset test is to convert both collections to sets:

```python
F_set.issubset(boundary_set)
```

or equivalently:

```python
F_set <= boundary_set
```

I would use:

```python
F_set.issubset(boundary_set)
```

because it reads almost exactly like the mathematics:

[
F\subseteq\partial_G(U).
]

---

# Design Question 3 — Can `F` Contain the Same Edge ID Twice?

Mathematically, **no**.

(F) is a set of actual edge copies.

An edge copy is either:

```text
selected
```

or:

```text
not selected
```

You cannot select:

```text
e2 twice
```

because there is only one edge copy with ID `"e2"`.

Parallel edges are handled with **different IDs**:

```text
e0
e1
```

so both may simultaneously belong to `F`, but `"e0"` cannot occur twice.

## Representation Decision

The canonical representation of a candidate `F` should therefore be:

```python
frozenset({"e0", "e1"})
```

That representation automatically prevents duplicates.

Later, the F-subset enumerator should generate **frozensets**.

For robustness, `is_admissible()` will also reject a supplied collection containing duplicate IDs before converting it to a frozenset.

That prevents this:

```python
["e2", "e2"]
```

from accidentally becoming mathematically interpreted as a two-edge set.

> **RULE TO BANK:**
> Parallel copies are different IDs; duplicate uses of the **same** ID are not different edges.

---

# The Four Conditions

The manuscript defines admissibility by:

[
\varnothing\neq U\subseteq V(G),
]

[
F\subseteq\partial_G(U),
]

[
f(U)+|F|\text{ is odd},
]

and

[
f(U)+|F|\ge3.
]

These are exactly the four conditions the function should implement. 

---

# Comments-First Logic

```text
Take candidate (U, F)

1. Convert U to a set-like representation.

2. Check:
       U is nonempty
       U ⊆ VERTICES

   If not:
       return False

3. Make sure F does not contain the same edge ID twice.

   If it does:
       return False

4. Convert F to a frozenset.

5. Compute boundary(U).

6. Check:
       F ⊆ boundary(U)

   If not:
       return False

7. Compute:
       total = f(U) + |F|

8. Check parity:
       total must be odd

   If even:
       return False

9. Check lower bound:
       total >= 3

   If not:
       return False

10. All four mathematical conditions passed:
       return True
```

---

# Complete `admissibility.py`

```python
# ==================================================================================================
# F7 CAPSTONE — PAIR ADMISSIBILITY
# ==================================================================================================
#
# PURPOSE:
#
# Decide whether a candidate pair:
#
#     (U, F)
#
# belongs to the admissible family A(G).
#
# The four conditions are:
#
#     1. U is nonempty and U ⊆ V(G)
#
#     2. F ⊆ ∂_G(U)
#
#     3. f(U) + |F| is odd
#
#     4. f(U) + |F| >= 3
#
#
# IMPORTANT CONTRACT DISTINCTION:
#
# validate_instance()
#     -> validates the graph itself
#     -> invalid graph data raises ValueError
#
# is_admissible(U, F)
#     -> evaluates an ordinary candidate pair
#     -> inadmissibility is expected during enumeration
#     -> returns True or False
#
# ==================================================================================================


from instance import VERTICES
from primitives import boundary, f_of


# ==================================================================================================
# is_admissible(U, F)
# ==================================================================================================
#
# INPUT:
#
#     U
#         collection of vertices
#
#     F
#         collection of edge-copy IDs
#
#
# CANONICAL REPRESENTATION:
#
# Later enumeration will represent candidates as:
#
#     U = frozenset({...})
#     F = frozenset({...})
#
# A frozenset is appropriate because U and F are mathematical sets:
#
#     order does not matter
#     duplicate elements do not exist
#     the objects should not mutate while being evaluated
#
#
# DUPLICATE EDGE-ID RULE:
#
# F cannot contain the same edge ID twice.
#
# For example:
#
#     ["e2", "e2"]
#
# is not a valid representation of a two-edge set.
#
# There is only one edge copy named e2.
#
# Parallel copies instead have different identities:
#
#     e0
#     e1
#
# so:
#
#     frozenset({"e0", "e1"})
#
# is perfectly valid.
#
#
# COMMENTS-FIRST ALGORITHM:
#
# CONDITION 1:
#
#     Convert U to a frozenset.
#
#     Require:
#
#         U != empty
#
#     and:
#
#         U ⊆ VERTICES
#
#     Otherwise:
#
#         return False
#
#
# CONDITION 2:
#
#     First reject duplicate edge IDs if the supplied F collection
#     contains them.
#
#     Convert F to a frozenset.
#
#     Compute:
#
#         ∂_G(U)
#
#     Convert that boundary list to a set.
#
#     Require:
#
#         F ⊆ ∂_G(U)
#
#     Otherwise:
#
#         return False
#
#
# CONDITION 3:
#
#     Compute:
#
#         total = f(U) + |F|
#
#     Require total to be odd.
#
#     Otherwise:
#
#         return False
#
#
# CONDITION 4:
#
#     Require:
#
#         total >= 3
#
#     Otherwise:
#
#         return False
#
#
# If all four conditions hold:
#
#     return True
#
# ==================================================================================================


def is_admissible(U, F):
    # Convert U to its mathematical set representation.
    U_set = frozenset(U)

    # Condition 1 — U must be nonempty and contained in V(G).
    if not U_set:
        return False

    if not U_set.issubset(VERTICES):
        return False

    # F is mathematically a set of edge copies.
    #
    # If the caller supplied something like:
    #
    #     ["e2", "e2"]
    #
    # reject it rather than allowing the duplicate to affect |F|.
    F_items = list(F)

    if len(F_items) != len(set(F_items)):
        return False

    F_set = frozenset(F_items)

    # Condition 2 — every selected edge copy must belong to ∂_G(U).
    boundary_set = frozenset(boundary(U_set))

    if not F_set.issubset(boundary_set):
        return False

    # Compute the quantity used by both remaining conditions.
    total = f_of(U_set) + len(F_set)

    # Condition 3 — f(U) + |F| must be odd.
    if total % 2 == 0:
        return False

    # Condition 4 — f(U) + |F| must be at least 3.
    if total < 3:
        return False

    # All four admissibility conditions hold.
    return True
```

---

# Predictions for the Locked Winner

Later, for:

```python
U = frozenset({0, 1})
F = frozenset({"e2"})
```

we already know:

```text
U nonempty and valid            ✓

boundary({0,1}) = ["e2"]
F ⊆ boundary                    ✓

f(U) = 2
|F| = 1

f(U) + |F| = 3

3 odd                           ✓
3 >= 3                          ✓
```

Therefore:

```python
is_admissible(
    frozenset({0, 1}),
    frozenset({"e2"}),
)
```

should return:

```text
True
```

> **RULE TO BANK:**
> `is_admissible(U, F)` is a predicate: it should mirror the mathematical definition directly and return `True` only if **all four conditions** hold. Inadmissibility is ordinary search behavior, not an exception.


==========================================================================================================================================================================

Yes — this is exactly a control-flow issue worth pinning down before the tests.

### 1. For `is_admissible({0}, {"e0"})`, which condition actually fires?

We have:

[
f({0})=1,\qquad |F|=1,
]

so

[
f(U)+|F|=1+1=2.
]

After Conditions 1 and 2 pass, the code reaches:

```python
total = f_of(U_set) + len(F_set)
```

and gets:

```text
total = 2
```

Then it checks **Condition 3 first**:

```python
if total % 2 == 0:
    return False
```

Since:

```text
2 % 2 == 0
```

is `True`, the function immediately returns:

```text
False
```

**Condition 4 is never reached.**

So the control flow is:

```text
Condition 1: U nonempty and valid       PASS
Condition 2: F subset of boundary       PASS
Condition 3: total must be odd          FAIL
             return False
Condition 4: total >= 3                 NEVER EXECUTED
```

Does that matter?

For the **final return value**, no:

```text
False is False
```

But it absolutely matters for **diagnostics and test design**. If you claim a test proves Condition 4 works, but the candidate actually dies at Condition 3 first, then you have not tested Condition 4 at all.

---

### 2. Can we construct a pair where Condition 4 alone rejects?

Yes. ✅

To reach Condition 4, the total must already be **odd**.

To fail Condition 4:

[
f(U)+|F|<3.
]

Since `U` is nonempty and every `f(v)` is positive,

[
f(U)+|F|\ge1.
]

The only positive odd number below `3` is:

[
1.
]

So we need:

[
f(U)=1,\qquad |F|=0.
]

Our instance has:

```text
f(0) = 1
f(1) = 1
```

Therefore either of these isolates Condition 4:

```python
is_admissible(frozenset({0}), frozenset())
```

or:

```python
is_admissible(frozenset({1}), frozenset())
```

For `{0}`:

```text
Condition 1: {0} nonempty, {0} ⊆ VERTICES    PASS

Condition 2: ∅ ⊆ boundary({0})                PASS

total = f({0}) + 0
      = 1

Condition 3: 1 is odd                         PASS

Condition 4: 1 >= 3                           FAIL
```

So this is the correct future test:

```python
def test_rejects_total_below_three():
    assert not is_admissible(frozenset({0}), frozenset())
```

> **RULE TO BANK:** A test for a specific guard must choose input that **passes every earlier guard**. Otherwise an earlier `return` can make the test pass while the condition you intended to test was never executed.
=====================================================================================================================================================================

# The Evaluator — Exact Rational Arithmetic

## Where Should `density(U, F)` Live?

I would put it in a **new file, `evaluator.py`**.

`primitives.py` promises the low-level quantities from which everything else is built: (f(U)), (e(U)), and (\partial_G(U)). `density()` is one layer higher: it combines primitives according to the paper's **objective function**, so `evaluator.py` makes that responsibility explicit and gives the later search loop a clean module to import.

Create it with:

```bash
code evaluator.py
```

Then:

```bash
ls evaluator.py
```

Prediction:

```text
evaluator.py
```

---

# Contract Decision — Should `density()` Check Admissibility?

## Decision: trust the caller

`density(U, F)` should **not call `is_admissible()` again**.

The future search loop will have the structure:

```python
if is_admissible(U, F):
    value = density(U, F)
```

So having `density()` repeat all four admissibility checks would duplicate work and blur the responsibilities of the two functions:

```text
is_admissible()
    answers: may this pair compete?

density()
    answers: what is this pair's exact objective value?
```

The contract is therefore:

> `density(U, F)` expects the caller to supply an admissible pair.

If someone violates that contract and gives it a pair with

[
f(U)+|F|-1=0,
]

then `Fraction` will raise `ZeroDivisionError`. If an inadmissible pair has a nonzero denominator, `density()` may still mechanically compute a rational number, but that number is **not a legitimate candidate value for the optimization problem**.

That distinction is useful: the evaluator does arithmetic; admissibility decides mathematical eligibility.

---

# Why `Fraction`

The objective is

[
\rho_f(U,F)
===========

\frac{2(e(U)+|F|)}
{f(U)+|F|-1}.
]

Using ordinary `/` would produce a Python `float`.

For example,

[
\frac43
]

would become approximately:

```text
1.3333333333333333
```

But:

```python
Fraction(4, 3)
```

stores the rational number **exactly**.

That matters because this checker is supposed to determine exact maxima, ties, and oracle values—not approximate them.

---

# Predictions Before Running

## Prediction 1 — The Winner

Take:

```python
U = frozenset({0, 1})
F = frozenset({"e2"})
```

From the hand derivation:

[
e(U)=2
]

because `e0` and `e1` are both internal.

Also:

[
f(U)=1+1=2
]

and:

[
|F|=1.
]

So the numerator is:

[
2(e(U)+|F|)
===========

# 2(2+1)

6.

]

The denominator is:

[
f(U)+|F|-1
==========

# 2+1-1

2.

]

Therefore:

[
\rho_f(U,F)=\frac62=3.
]

Prediction:

```python
density(
    frozenset({0, 1}),
    frozenset({"e2"}),
) == Fraction(3, 1)
```

---

## Prediction 2 — The Triangle

Take:

```python
U = frozenset({2, 3, 4})
F = frozenset({"e2"})
```

We already established:

[
e(U)=3
]

from triangle edges `e3`, `e4`, `e5`.

Also:

[
f(U)=2+2+2=6
]

and:

[
|F|=1.
]

Numerator:

[
2(3+1)=8.
]

Denominator:

[
6+1-1=6.
]

Thus:

[
\rho_f(U,F)
===========

# \frac86

\frac43.
]

Prediction:

```python
density(
    frozenset({2, 3, 4}),
    frozenset({"e2"}),
) == Fraction(4, 3)
```

This is precisely the case that shows why floating-point arithmetic is the wrong representation.

---

## Prediction 3 — The Tight `{0,1,2}` Case

Take:

```python
U = frozenset({0, 1, 2})
F = frozenset({"e3"})
```

We already established:

[
e(U)=3
]

because:

```text
e0
e1
e2
```

are internal.

And:

[
f(U)=1+1+2=4.
]

With:

[
|F|=1,
]

the numerator is:

[
2(3+1)=8.
]

The denominator is:

[
4+1-1=4.
]

Therefore:

[
\rho_f(U,F)=\frac84=2.
]

Prediction:

```python
density(
    frozenset({0, 1, 2}),
    frozenset({"e3"}),
) == Fraction(2, 1)
```

This is one of the competitors attaining the hand-derived **second-best value (2)**.

---

# Complete `evaluator.py`

```python
# ==================================================================================================
# F7 CAPSTONE — EXACT OBJECTIVE EVALUATOR
# ==================================================================================================
#
# PURPOSE:
#
# Evaluate the modified set-pair density:
#
#                         2(e(U) + |F|)
#     rho_f(U, F) = ---------------------------
#                      f(U) + |F| - 1
#
# for a candidate pair:
#
#     (U, F)
#
#
# EXACTNESS RULE:
#
# This checker must use exact rational arithmetic.
#
# Ordinary Python division:
#
#     numerator / denominator
#
# produces a float.
#
# Some rational numbers cannot be represented exactly as binary floating-point
# numbers. For example:
#
#     4 / 3
#
# becomes approximately:
#
#     1.3333333333333333
#
# But the mathematics of this problem is rational arithmetic, and the checker
# must compare candidate values exactly.
#
# Therefore this evaluator constructs:
#
#     Fraction(numerator, denominator)
#
# using Python's standard-library fractions module.
#
#
# RESPONSIBILITY SEPARATION:
#
# is_admissible(U, F)
#
#     decides whether a candidate pair is allowed to compete.
#
# density(U, F)
#
#     evaluates the objective exactly.
#
# density() does NOT repeat the admissibility test.
#
# Its contract is:
#
#     the caller must supply an admissible pair.
#
# The later search loop will therefore have the shape:
#
#     if is_admissible(U, F):
#         value = density(U, F)
#
#
# CONSEQUENCE OF THAT CONTRACT:
#
# If a caller ignores the contract and supplies an inadmissible pair with:
#
#     f(U) + |F| - 1 = 0
#
# then Fraction will raise ZeroDivisionError.
#
# If an inadmissible pair happens to have a nonzero denominator, density() may
# mechanically return a rational value, but that value is not a valid candidate
# for the optimization problem.
#
# ==================================================================================================


from fractions import Fraction

from primitives import f_of, internal_edge_count


# ==================================================================================================
# density(U, F)
# ==================================================================================================
#
# COMMENTS-FIRST ALGORITHM:
#
# 1. Compute the number of internal edge copies:
#
#        e_U = e(U)
#
#
# 2. Compute:
#
#        f_U = f(U)
#
#
# 3. Compute the number of selected boundary edge copies:
#
#        F_size = |F|
#
#
# 4. Build the numerator:
#
#        numerator = 2 * (e_U + F_size)
#
#
# 5. Build the denominator:
#
#        denominator = f_U + F_size - 1
#
#
# 6. Construct and return the EXACT rational value:
#
#        Fraction(numerator, denominator)
#
#
# IMPORTANT:
#
# Do NOT write:
#
#        numerator / denominator
#
# because that would produce a float.
#
#
# HAND-DERIVED CHECKPOINTS:
#
# WINNER:
#
#     U = {0,1}
#     F = {e2}
#
#     e(U) = 2
#     f(U) = 2
#     |F|  = 1
#
#     numerator   = 2(2 + 1) = 6
#     denominator = 2 + 1 - 1 = 2
#
#     density = Fraction(6, 2)
#             = Fraction(3, 1)
#
#
# TRIANGLE:
#
#     U = {2,3,4}
#     F = {e2}
#
#     e(U) = 3
#     f(U) = 6
#     |F|  = 1
#
#     numerator   = 2(3 + 1) = 8
#     denominator = 6 + 1 - 1 = 6
#
#     density = Fraction(8, 6)
#             = Fraction(4, 3)
#
#
# TIGHT COMPETITOR:
#
#     U = {0,1,2}
#     F = {e3}
#
#     e(U) = 3
#     f(U) = 4
#     |F|  = 1
#
#     numerator   = 2(3 + 1) = 8
#     denominator = 4 + 1 - 1 = 4
#
#     density = Fraction(8, 4)
#             = Fraction(2, 1)
#
# ==================================================================================================


def density(U, F):
    e_U = internal_edge_count(U)
    f_U = f_of(U)
    F_size = len(F)

    numerator = 2 * (e_U + F_size)
    denominator = f_U + F_size - 1

    return Fraction(numerator, denominator)
```

## The Three Exact Predictions

```python
density(frozenset({0, 1}), frozenset({"e2"}))
# Fraction(3, 1)

density(frozenset({2, 3, 4}), frozenset({"e2"}))
# Fraction(4, 3)

density(frozenset({0, 1, 2}), frozenset({"e3"}))
# Fraction(2, 1)
```

> **RULE TO BANK:** The mathematics is rational, so the implementation stays rational from construction through comparison. Build `Fraction(numerator, denominator)` directly; never compute the quotient as a float first.
===================================================================================================================================================================

# What's your instinct for generating all subsets of ["e0", "e1", "e2"] with stdlib? Even a rough idea — a loop shape, a module you half-remember, anything. The answer shapes how the search loop reads, and I want your thinking on record first.

My first instinct is **`itertools.combinations`**, wrapped in a loop over subset sizes.

For:

```python
edges = ["e0", "e1", "e2"]
```

I’d think:

```python
for r in range(len(edges) + 1):
    for combo in combinations(edges, r):
        ...
```

The outer loop chooses the subset size:

```text
r = 0  → choose 0 edges
r = 1  → choose 1 edge
r = 2  → choose 2 edges
r = 3  → choose all 3 edges
```

Then `combinations(edges, r)` generates every choice of exactly that size.

So mentally I expect:

```text
()
("e0",)
("e1",)
("e2",)
("e0", "e1")
("e0", "e2")
("e1", "e2")
("e0", "e1", "e2")
```

That is all

[
2^3=8
]

subsets.

Since our mathematical (F) is a set, I would probably convert each tuple immediately to:

```python
frozenset(combo)
```

so the search loop receives candidates in the same representation we have already committed to:

```python
frozenset()
frozenset({"e0"})
frozenset({"e0", "e1"})
...
```

The other obvious route is a binary/bitmask loop from `0` through `2**n - 1`, where each bit means “include this edge or don’t.” That works, but `itertools.combinations` reads much more like the mathematics: **for every possible cardinality, choose every subset of that cardinality.**

> **RULE TO BANK:** To generate the power set of a finite list with stdlib, iterate `r = 0, ..., n` and generate `combinations(items, r)` for each size.

===================================================================================================================================================================

# Search — Exact Maximizer Over All Admissible Pairs

Create the new file:

```bash
code search.py
```

Then confirm:

```bash
ls search.py
```

Expected:

```text
search.py
```

Before running it later, make sure the temporary `print(...)` test blocks have been removed from `instance.py` and `admissibility.py`. These are now imported modules and should be silent.

## Result Contract

The F4 construct I want here is a **frozen dataclass**:

```python
@dataclass(frozen=True)
class SearchResult:
    ...
```

It gives us exactly what the oracle expects:

```python
result.value
result.U
result.F
```

while `frozen=True` makes the completed result immutable.

### What if there is no admissible pair?

Return:

```python
SearchResult(
    value=Fraction(0, 1),
    U=None,
    F=None,
)
```

The value is (0), as required by the definition, while `None` makes it explicit that **there is no maximizing admissible pair to report**.

We should not use `frozenset()` for `U` and `F` in that case, because that would misleadingly look like the pair ((\varnothing,\varnothing)), which is itself inadmissible.

There is another subtle reason not to initialize the "best" result as value zero: an admissible pair could theoretically have density exactly `0`. If we initialized with zero and only replaced it on a strict improvement, we might never record that legitimate maximizing pair. So the internal search sentinel should be:

```python
best = None
```

and the **first admissible pair always becomes the current best**.

## What happens on a tie?

Keep the **first maximizer encountered**.

So we update only when:

```python
value > best.value
```

not when:

```python
value >= best.value
```

That tie rule is deterministic because:

* vertices will be enumerated from `sorted(VERTICES)`;
* `itertools.combinations` respects that order;
* `boundary(U)` preserves the stable order of `EDGES`;
* F-subsets therefore also have deterministic enumeration order.

For our locked instance the true winner is unique anyway, but the search function should still have a defined general tie contract.

---

# Comments-First Search Shape

Conceptually:

```text
best = None

put VERTICES into stable sorted order

for U-size = 1 through |V|:
    generate every U of that size

    turn U into frozenset

    compute boundary(U) ONCE

    for F-size = 0 through |boundary(U)|:
        generate every F of that size

        turn F into frozenset

        if pair is not admissible:
            skip it

        compute exact density

        if this is the first admissible pair:
            save it

        otherwise if its value is STRICTLY greater:
            replace the best result

        if its value merely ties:
            keep the earlier result

after enumeration:

    if no admissible pair was ever found:
        return value 0 with U=None and F=None

    otherwise:
        return the saved maximizer
```

The important nesting is:

[
U
\longrightarrow
\partial_G(U)
\longrightarrow
F\subseteq\partial_G(U)
\longrightarrow
\text{admissibility}
\longrightarrow
\rho_f(U,F).
]

We compute `boundary(U)` **once per U**, not once for every F candidate.

---

# Complete `search.py`

```python
# ==================================================================================================
# F7 CAPSTONE — EXHAUSTIVE SEARCH
# ==================================================================================================
#
# PURPOSE:
#
# Enumerate every candidate pair:
#
#     (U, F)
#
# where:
#
#     nonempty U ⊆ V(G)
#
# and:
#
#     F ⊆ ∂_G(U)
#
# Filter those candidates through:
#
#     is_admissible(U, F)
#
# evaluate every admissible pair exactly using:
#
#     density(U, F)
#
# and return a maximizer.
#
#
# RESULT CONTRACT:
#
# The search returns an immutable SearchResult with three named fields:
#
#     result.value
#     result.U
#     result.F
#
#
# If at least one admissible pair exists:
#
#     value = exact Fraction giving the maximum density
#     U     = frozenset of maximizing vertices
#     F     = frozenset of maximizing boundary-edge IDs
#
#
# If NO admissible pair exists:
#
#     value = Fraction(0, 1)
#     U     = None
#     F     = None
#
# The None values matter:
#
#     they mean there is no admissible maximizing pair to report.
#
# We do NOT use:
#
#     U = frozenset()
#     F = frozenset()
#
# because that would look like the actual pair (empty set, empty set),
# and empty U is inadmissible.
#
#
# TIE CONTRACT:
#
# If multiple admissible pairs attain the same maximum value,
# keep the FIRST one encountered.
#
# Therefore the best result is replaced only when:
#
#     new_value > best.value
#
# not when:
#
#     new_value >= best.value
#
#
# DETERMINISM:
#
# VERTICES is a frozenset, so its iteration order is not the search order.
#
# Before enumeration we use:
#
#     sorted(VERTICES)
#
# itertools.combinations preserves the order of its input.
#
# boundary(U) also returns edge IDs in stable EDGES order.
#
# Therefore both the U-enumeration and F-enumeration are deterministic,
# which also makes the "first maximizer wins" tie rule deterministic.
#
# ==================================================================================================


import itertools
from dataclasses import dataclass
from fractions import Fraction

from admissibility import is_admissible
from evaluator import density
from instance import VERTICES
from primitives import boundary


# ==================================================================================================
# SEARCH RESULT
# ==================================================================================================
#
# A dataclass gives us a small record with named fields:
#
#     value
#     U
#     F
#
# frozen=True makes a completed result immutable.
#
# U and F are normally frozensets.
#
# They are None only when the admissible family is empty.
#
# ==================================================================================================


@dataclass(frozen=True)
class SearchResult:
    value: Fraction
    U: frozenset | None
    F: frozenset | None


# ==================================================================================================
# find_max_density()
# ==================================================================================================
#
# COMMENTS-FIRST ALGORITHM:
#
# 1. Start with:
#
#        best = None
#
#    None means:
#
#        no admissible pair has been encountered yet.
#
#    We deliberately do NOT initialize best to a zero-valued SearchResult.
#
#    Why?
#
#    An admissible pair could itself have density 0.
#
#    We still need to record its U and F if it is the maximizer.
#
#
# 2. Put the vertices in deterministic order:
#
#        vertices = sorted(VERTICES)
#
#
# 3. Enumerate every NONEMPTY subset U.
#
#    If there are n vertices, U can have sizes:
#
#        1, 2, ..., n
#
#    For every size:
#
#        itertools.combinations(vertices, U_size)
#
#    generates every U of exactly that cardinality.
#
#
# 4. Convert each generated U tuple to:
#
#        frozenset
#
#    because U is mathematically a set.
#
#
# 5. Compute:
#
#        boundary(U)
#
#    ONCE for this U.
#
#    The returned list contains the distinct boundary-edge IDs in
#    deterministic EDGES order.
#
#
# 6. Enumerate every subset F of that boundary.
#
#    If the boundary has b edge copies, F may have sizes:
#
#        0, 1, ..., b
#
#    For each size:
#
#        itertools.combinations(boundary_edges, F_size)
#
#    generates every F of that cardinality.
#
#
# 7. Convert each generated F tuple to:
#
#        frozenset
#
#
# 8. Ask:
#
#        is_admissible(U, F)
#
#    If False:
#
#        continue
#
#    Inadmissible pairs are ordinary search candidates that simply
#    do not participate in the optimization.
#
#
# 9. For an admissible pair, compute:
#
#        value = density(U, F)
#
#    density() returns an exact Fraction.
#
#
# 10. If:
#
#         best is None
#
#     then this is the FIRST admissible pair.
#
#     Save it immediately, even if its density happens to be 0.
#
#
# 11. Otherwise compare exactly:
#
#         value > best.value
#
#     If strictly greater:
#
#         replace best.
#
#     If equal:
#
#         do nothing.
#
#     Therefore the first maximizer encountered wins a tie.
#
#
# 12. After every candidate has been examined:
#
#     if best is still None:
#
#         the admissible family was empty
#
#         return:
#
#             value = Fraction(0, 1)
#             U = None
#             F = None
#
#     otherwise:
#
#         return best
#
# ==================================================================================================


def find_max_density():
    best = None

    vertices = sorted(VERTICES)

    # Enumerate every nonempty vertex subset U.
    for U_size in range(1, len(vertices) + 1):
        for U_combo in itertools.combinations(vertices, U_size):
            U = frozenset(U_combo)

            # Compute ∂_G(U) once for this U.
            boundary_edges = boundary(U)

            # Enumerate every subset F of ∂_G(U), including the empty set.
            for F_size in range(len(boundary_edges) + 1):
                for F_combo in itertools.combinations(boundary_edges, F_size):
                    F = frozenset(F_combo)

                    # Only admissible pairs participate in the optimization.
                    if not is_admissible(U, F):
                        continue

                    # Evaluate the objective using exact rational arithmetic.
                    value = density(U, F)

                    # The first admissible pair becomes the initial best pair.
                    if best is None:
                        best = SearchResult(value=value, U=U, F=F)
                        continue

                    # Replace the current best only on a STRICT improvement.
                    #
                    # Equality leaves the first encountered maximizer in place.
                    if value > best.value:
                        best = SearchResult(value=value, U=U, F=F)

    # No admissible pair was found.
    if best is None:
        return SearchResult(
            value=Fraction(0, 1),
            U=None,
            F=None,
        )

    return best
```

For our locked oracle, once we run this, the prediction is:

```python
result.value == Fraction(3, 1)
result.U == frozenset({0, 1})
result.F == frozenset({"e2"})
```

> **RULE TO BANK:** Exhaustive optimization needs three separate ideas: **enumerate every candidate, filter feasibility, then compare objective values**. Use `None` to mean “no feasible candidate seen yet,” and update on `>` rather than `>=` when the contract is “first maximizer wins ties.”

===================================================================================================================================================================

# Step 6 — Permanent Test Suite

I’d keep this to the **seven required tests**. The runner-up test is useful later, but it is not necessary to establish the checker contract or the locked oracle.

One small improvement to your suggested parity case: for Test 4 I’m using a pair with total (4), rather than `({0,1}, ∅)` with total (2). That makes the parity guard **genuinely isolated**: Conditions 1–2 pass, Condition 3 fails, and Condition 4 would have passed if execution reached it.

Create:

```bash
code test_checker.py
```

Confirm:

```bash
ls test_checker.py
```

Expected:

```text
test_checker.py
```

## Complete `test_checker.py`

```python
# ==================================================================================================
# F7 CAPSTONE — EXACT CHECKER TEST SUITE
# ==================================================================================================
#
# PURPOSE:
#
# Turn the hand-derived examples and interactive guard checks into permanent,
# automatically repeatable tests.
#
# The suite checks:
#
#     1. a known admissible pair is accepted
#     2. condition 1 rejects empty U
#     3. condition 2 rejects an edge outside the boundary
#     4. condition 3 rejects even f(U) + |F|
#     5. condition 4 rejects an odd total below 3
#     6. parallel edge copies are counted separately
#     7. exhaustive search reproduces the hand-derived exact optimum
#
# Exact rational results use Fraction.
#
# No floating-point approximation belongs in the oracle test.
# ==================================================================================================


from fractions import Fraction

from admissibility import is_admissible
from primitives import boundary, internal_edge_count
from search import find_max_density


# ==================================================================================================
# TEST 1 — ACCEPT A KNOWN ADMISSIBLE PAIR
# ==================================================================================================
#
# Hand-derived winner:
#
#     U = {0, 1}
#     F = {e2}
#
# Check:
#
#     U is nonempty and valid
#     boundary(U) = {e2}
#     f(U) + |F| = 2 + 1 = 3
#     3 is odd
#     3 >= 3
#
# Therefore the pair must be admissible.
# ==================================================================================================


def test_accepts_valid_pair():
    U = frozenset({0, 1})
    F = frozenset({"e2"})

    assert is_admissible(U, F) is True


# ==================================================================================================
# TEST 2 — CONDITION 1: REJECT EMPTY U
# ==================================================================================================
#
# U must be nonempty.
#
# The empty set violates condition 1 immediately.
# ==================================================================================================


def test_rejects_empty_U():
    U = frozenset()
    F = frozenset()

    assert is_admissible(U, F) is False


# ==================================================================================================
# TEST 3 — CONDITION 2: REJECT NONBOUNDARY EDGE
# ==================================================================================================
#
# For:
#
#     U = {0, 1}
#
# the boundary is:
#
#     {e2}
#
# Edge e3 exists in the graph, but:
#
#     e3 = (2, 3)
#
# has neither endpoint in U.
#
# Therefore:
#
#     e3 not in boundary(U)
#
# and:
#
#     F = {e3}
#
# violates:
#
#     F ⊆ boundary(U)
# ==================================================================================================


def test_rejects_nonboundary_edge_in_F():
    U = frozenset({0, 1})
    F = frozenset({"e3"})

    assert is_admissible(U, F) is False


# ==================================================================================================
# TEST 4 — CONDITION 3: REJECT EVEN f(U) + |F|
# ==================================================================================================
#
# We deliberately choose a pair where the parity condition is the
# relevant failure:
#
#     U = {2}
#     F = {e2, e3}
#
# For U = {2}:
#
#     boundary(U) = {e2, e3, e5}
#
# so F is a valid subset of the boundary.
#
# Also:
#
#     f(U) = 2
#     |F|  = 2
#
# therefore:
#
#     f(U) + |F| = 4
#
# Condition 1 passes.
# Condition 2 passes.
# Condition 3 fails because 4 is even.
#
# Notice:
#
#     4 >= 3
#
# so the lower-bound condition would pass.
#
# This isolates the parity guard cleanly.
# ==================================================================================================


def test_rejects_even_fU_plus_F_size():
    U = frozenset({2})
    F = frozenset({"e2", "e3"})

    assert is_admissible(U, F) is False


# ==================================================================================================
# TEST 5 — CONDITION 4: REJECT TOTAL BELOW THREE
# ==================================================================================================
#
# Use the banked guard-isolation example:
#
#     U = {0}
#     F = empty
#
# Then:
#
#     f(U) = 1
#     |F|  = 0
#
# so:
#
#     f(U) + |F| = 1
#
# Condition 1:
#
#     U is nonempty and valid
#
#     PASS
#
# Condition 2:
#
#     empty F is a subset of every boundary
#
#     PASS
#
# Condition 3:
#
#     1 is odd
#
#     PASS
#
# Condition 4:
#
#     1 >= 3
#
#     FAIL
#
# Therefore this test actually reaches and exercises the fourth guard.
# ==================================================================================================


def test_rejects_total_below_three():
    U = frozenset({0})
    F = frozenset()

    assert is_admissible(U, F) is False


# ==================================================================================================
# TEST 6 — PARALLEL EDGE COPIES REMAIN DISTINCT
# ==================================================================================================
#
# The graph contains:
#
#     e0 = (0, 1)
#     e1 = (0, 1)
#
# These are parallel but DISTINCT edge copies.
#
#
# For:
#
#     U = {0, 1}
#
# both copies are internal, so:
#
#     e(U) = 2
#
#
# For:
#
#     U = {1}
#
# both copies cross the boundary, along with e2:
#
#     boundary({1}) = ["e0", "e1", "e2"]
#
# If the implementation accidentally collapsed parallel endpoint pairs,
# this test would fail.
# ==================================================================================================


def test_parallel_edge_copies_are_counted_separately():
    assert internal_edge_count(frozenset({0, 1})) == 2

    boundary_edges = boundary(frozenset({1}))

    assert boundary_edges == ["e0", "e1", "e2"]


# ==================================================================================================
# TEST 7 — KNOWN-ANSWER ORACLE
# ==================================================================================================
#
# This is the central end-to-end test.
#
# The exhaustive checker must reproduce the independently hand-derived optimum:
#
#     optimal value = 3
#
#     unique maximizing U:
#
#         {0, 1}
#
#     unique maximizing F:
#
#         {e2}
#
#
# Exactness matters:
#
#     result.value
#
# must equal:
#
#     Fraction(3, 1)
#
# exactly.
#
# No pytest.approx.
# No float comparison.
# ==================================================================================================


def test_bruteforce_checker_returns_hand_derived_optimum():
    result = find_max_density()

    assert result.value == Fraction(3, 1)
    assert result.U == frozenset({0, 1})
    assert result.F == frozenset({"e2"})
```

## Prediction Before Running

Pytest should discover exactly **7 tests**:

```text
test_accepts_valid_pair
test_rejects_empty_U
test_rejects_nonboundary_edge_in_F
test_rejects_even_fU_plus_F_size
test_rejects_total_below_three
test_parallel_edge_copies_are_counted_separately
test_bruteforce_checker_returns_hand_derived_optimum
```

My prediction is:

```text
7 collected
7 passed
```

Before running, make sure the temporary interactive `print(...)` blocks have been removed from imported modules such as `instance.py` and `admissibility.py`. Those modules should now be silent again.

Then run:

```bash
python -m pytest test_checker.py -v
```

Expected final tally:

```text
7 passed
```

> **RULE TO BANK:** A guard test must reach the guard it claims to test. Make every earlier condition pass; where possible, make later conditions pass too. Then a green test is evidence about the intended condition rather than an accidental earlier rejection.


===================================================================================================================================================================
# What that comment means
# noqa: SIM103

means:

Ruff, I know you would prefer this rewritten, but I am deliberately keeping this form.

We are keeping the explicit fourth guard because it mirrors the mathematical admissibility definition and the tests we wrote for each condition.

Do not change the logic. Do not change return True. Do not edit gym.py or day11_capstone.py.
=====================================

Step 1: Complete

=====================================

**Step 2: the edge-case pass**
The plan's phrase is "edge cases" — one deliberate look for brittleness before the capstone is called hardened. This is a thinking exercise first, not a coding one.
Your instinct first, as promised: look at the five capstone modules in your mind's eye — instance, primitives, admissibility, evaluator, search. 
**Where would you poke it if you wanted it to break? What input, what call pattern, what assumption does the code lean on that nothing currently tests?** 

Give me one or two candidates — wrong answers are fine, the muscle is the point.
Then I'll put my two on the table and we'll decide together which (if any) earn a test or a fix, and which get explicitly declined as out of contract — because "we considered it and ruled it out of scope" is also a legitimate hardening outcome, as long as it's recorded.


My first two places to poke would be these:

### 1. Duplicate edge IDs in `EDGES`

This is the one that worries me most because our entire downstream representation of (F) depends on **edge IDs being unique identifiers for edge copies**.

Suppose someone accidentally wrote:

```python
EDGES = [
    ("e0", 0, 1),
    ("e0", 0, 1),  # duplicate ID
    ...
]
```

The multigraph still has two physical edge copies, and `internal_edge_count()` would correctly count both. But `boundary()` returns IDs, and later:

```python
frozenset(F_combo)
```

would collapse two `"e0"` values into one element. Then

```python
len(F)
```

would no longer equal the number of selected edge copies.

So there's a hidden contract right now:

> **Every edge copy must have a unique edge ID.**

Nothing in `validate_instance()` currently proves that. Given how fundamental ID identity became when we designed `boundary()`, this feels like a genuine hardening candidate rather than cosmetic defensiveness.

### 2. `validate_instance()` exists, but nothing forces the search to call it

Right now the architecture appears to rely on the programmer remembering:

```python
validate_instance()
```

before trusting the checker.

If somebody edits the instance later and directly runs:

```python
find_max_density()
```

the search doesn't establish for itself that the graph satisfies the assumptions it depends on.

That makes me want to ask whether the intended public contract is:

```text
caller must validate first
```

or:

```text
find_max_density() refuses to search an invalid instance
```

Either can be legitimate, but at the moment I think we're relying on the former **implicitly**, which is where brittleness lives.

A nearby third poke would be an edge whose endpoint isn't in `VERTICES`; `compute_degrees()` would currently hit a dictionary lookup failure rather than one of our carefully named validation errors. But I'd rank **unique edge IDs** and **who owns the validation call** above it for this pass.

> **RULE TO BANK:** Edge-case hardening is often about finding **unstated invariants**. Here, “edge IDs are unique” and “validation has already happened” are assumptions the current happy-path tests never have to challenge.

========================================================
Both candidates are genuine, and the first one is the sharper find of the two — It's an unstated invariant the entire F-representation stands on. 

My first was exactly your first: **duplicate edge IDs.** Your trace of the failure is precise — the physical copies survive in `internal_edge_count` (it never looks at IDs), but the moment `boundary()`'s ID list meets `frozenset(F_combo)`, two `"e0"`s collapse into one and `len(F)` silently undercounts. Silence is the worst failure class there is, and it's precisely the kind of invariant `validate_instance()` exists to pin. 
**Verdict: fix it.** A fifth check — every edge ID unique, culprit named — plus a break-and-restore proof like the others got.

My second was your *third*: **the unknown-endpoint edge** — `("e6", 4, 9)` would crash `compute_degrees()` with a bare `KeyError: 9`, the mechanical symptom instead of the named contract violation, exactly the failure mode of my `f_of` design speech argued against. It's the same principle we applied to queries, not yet applied to the instance's own edges. 
**Verdict: fix it too** — it's a two-line check and it completes the validator's coverage of the data it validates. (Notice the pleasing symmetry: your Check 3 validates that F_VALUES' keys are legal; nothing validates that EDGES' endpoints are. Same gap, other structure.)

Your second — **who owns the validation call** — is the interesting judgment call. My honest recommendation: **resolve it by contract, not by code.** Having `find_max_density()` call `validate_instance()` on every invocation is defensible, but it blurs the layering the same way `density()` re-checking admissibility would have — you argued that separation yourself, and the argument holds here: validation is an *instance-lifecycle* event, search is a *query*. The cleaner resolution is to make the implicit contract explicit: a comment block in `search.py` stating "contract: the instance has been validated; this function trusts instance.py's data," and — the part with teeth — the *test suite* calling `validate_instance()` once, so any instance edit that breaks an invariant fails CI before any search result gets believed. Contract documented, contract enforced, layering intact. **Verdict: document + test, no code change.** If you disagree and want the search to self-validate, make the case.

So the step-2 work list: (1) add the uniqueness check to `validate_instance()`, break-and-prove it; (2) add the endpoint-membership check, break-and-prove it; (3) the contract comment in `search.py`; (4) one new test — `test_instance_is_valid` — calling `validate_instance()` in the suite, taking it to 8 green.

Order them however you like. Write the uniqueness check first if you're taking my sequence — comments-first, and predict the error message your f-string will produce for a duplicated `"e0"` before you break it.

========================================================

I’d take that sequence. We’ll add **only the uniqueness invariant first**, prove it rejects a corrupted instance, restore it, and then move to endpoint membership. That keeps each hardening change independently observable.

## Prediction before we break anything

For the deliberate corruption, change:

```python
("e1", 0, 1),
```

temporarily to:

```python
("e0", 0, 1),
```

so the first two physical edge copies now both claim the ID `"e0"`.

I’d make the new guard raise:

```python
raise ValueError(f"duplicate edge ID {edge_id!r}")
```

Because `edge_id == "e0"`, the exact message constructed by the f-string will be:

```text
duplicate edge ID 'e0'
```

and the traceback’s final line will therefore be:

```text
ValueError: duplicate edge ID 'e0'
```

The quotes appear because `!r` uses the string’s representation. That is useful here because it makes the offending ID visually unambiguous.

---

# Complete updated `instance.py`

This is the **valid version** with the new uniqueness check added. Do not corrupt `e1` until after you have saved this version.

```python
# ==================================================================================================
# F7 CAPSTONE — TOY MULTIGRAPH INSTANCE
# ==================================================================================================


## Now prove Check 5 rejects

Temporarily change only:

```python
("e1", 0, 1),
```

to:

```python
("e0", 0, 1),
```

Then, **temporarily at the bottom of `instance.py`**, add:

```python
validate_instance()
```
must be flush left in code
You do not need a success print for this break case; we specifically expect the call to fail.

Run:

```bash
python instance.py
```

### Exact prediction

Checks 1–4 should pass. Then the uniqueness loop sees:

```text
first edge:   edge_id = "e0" → new → record it
second edge:  edge_id = "e0" → already seen → reject
```

The traceback should end with exactly:

```text
ValueError: duplicate edge ID 'e0'
```

Paste that last line when you run it.

After we see it fire, we will restore `"e1"` **and remove the temporary bottom-level `validate_instance()` call** before moving to the unknown-endpoint guard.

> **RULE TO BANK:** If downstream code uses an ID as the identity of a mathematical object, uniqueness of that ID is not cosmetic metadata—it is an invariant the validator must prove.

==============================================================================

Perfect. ✅ The guard behaved exactly as designed:

ValueError: duplicate edge ID 'e0'

So we have now proved, not merely assumed, that duplicate edge IDs are rejected before they can silently corrupt the F-representation.

# First restore the instance

Change the second edge back to:

("e1", 0, 1),

# and remove the temporary flush-left:

validate_instance()

from the bottom.

# Now we can add the unknown-endpoint guard.

# There is one important control-flow point here: this new check must occur before compute_degrees(). Otherwise an edge such as

("e6", 4, 9)

would reach:

degrees[9] += 1

# first and die with a bare:

KeyError: 9

# before our validator had a chance to produce the named contract violation. So endpoint membership belongs among the structural edge checks, before degree computation.

Exact failure message I recommend

For an edge with an endpoint outside VERTICES:

raise ValueError(
    f"edge {edge_id} has endpoint outside VERTICES: ({u}, {v})"
)

If we deliberately change e5 to:

("e5", 2, 9),

the exact predicted traceback line will be:

ValueError: edge e5 has endpoint outside VERTICES: (2, 9)

-------

# **Before the next break, prediction**

We will temporarily change:

("e5", 2, 4),

to:

("e5", 2, 9),

and temporarily put this flush-left at the bottom again:

validate_instance()

Then:

python instance.py

should end with:

ValueError: edge e5 has endpoint outside VERTICES: (2, 9)

>Notice why we reordered the validator: structural facts needed to compute a derived quantity must be validated before computing that quantity. That is what prevents KeyError: 9 from beating our own guard to the punch.

**RULE TO BANK:** Validate the prerequisites of a computation before performing the computation. If compute_degrees() assumes every endpoint is a known vertex, endpoint membership must be established first.

==============================================================================
# RESTORE AND RERUN | (.venv) cherinefons@Mac foundation % python instance.py | (.venv) cherinefons@Mac foundation % 
# That confirms the instance is restored and the module is silent again
==============================================================================

2. Add the contract comment to search.py

We are not importing or calling validate_instance() here.

Add this to the large comment immediately above find_max_density() — I would place it before COMMENTS-FIRST ALGORITHM:

# CALLER CONTRACT:
#
# find_max_density() assumes that the data in instance.py has already
# passed:
#
#     validate_instance()
#
# The search does NOT repeat instance validation.
#
# Instance validation is an instance-lifecycle responsibility; exhaustive
# search is a separate query responsibility.
#
# The test suite enforces this contract by calling validate_instance()
# directly before the checker is considered trustworthy.
#

That makes the architectural decision explicit:

instance lifecycle → validate_instance()
search query       → find_max_density()

No redundant validation, but no hidden assumption either.

---------------------------------

3. Add test_instance_is_valid

At the top of test_checker.py, add the import:

from instance import validate_instance

So that portion of the imports should now include:

from fractions import Fraction


from admissibility import is_admissible
from instance import validate_instance
from primitives import boundary, internal_edge_count
from search import find_max_density

Then add this test. I would put it first, because logically the instance itself should be established before we test operations on it:

# ==================================================================================================
# TEST 1 — THE LOCKED INSTANCE ITSELF IS VALID
# ==================================================================================================
#
# The checker assumes that instance.py satisfies all graph-level invariants.
#
# validate_instance() is fail-fast:
#
#     invalid instance -> raises ValueError
#     valid instance   -> returns normally
#
# Therefore this test passes simply by reaching the end of the function
# without an exception.
#
# This gives the search contract teeth:
#
#     find_max_density() trusts validated instance data,
#
# while the test suite guarantees that the locked instance actually passes
# that validation.
# ==================================================================================================


def test_instance_is_valid():
    validate_instance()

-------------

The behavior under test is simply:

no exception was raised.

Pytest considers that a passing test.

My existing seven tests can remain exactly as they are. Their numbering in the decorative comments can be shifted for documentation only; pytest does not care.


Prediction Before Running the Full Suite

You previously had:

7 tests

We just added:

+ 1 test_instance_is_valid

Therefore I predict:

8 collected
8 passed

Run:

python -m pytest test_checker.py -v

The important final line should be approximately:

============================== 8 passed in ... ==============================

No pytest.approx, no expected failures, no skipped tests: eight green.

4. One final check before committing

Run:

git status

At minimum, the Step-2 files should be:

modified:   instance.py
modified:   search.py
modified:   test_checker.py

Then I would run one targeted lint check as the final hygiene confirmation:

ruff check instance.py search.py test_checker.py

Prediction:

All checks passed!

5. Commit Step 2

Once you have:

python instance.py
→ silent


python -m pytest test_checker.py -v
→ 8 passed


ruff check instance.py search.py test_checker.py
→ All checks passed!

stage exactly these files:

git add instance.py search.py test_checker.py

Check them:

git status

Then commit:

git commit -m "f7d6: harden instance validation and document search contract"

So the complete Step-2 proof chain is:

python instance.py
python -m pytest test_checker.py -v
ruff check instance.py search.py test_checker.py
git status
git add instance.py search.py test_checker.py
git status
git commit -m "f7d6: harden instance validation and document search contract"

RULE TO BANK: A contract does not have to be enforced redundantly at every layer. It does need to be explicitly documented at the consumer and executable somewhere in the verification path. Here, search trusts validated data, while the test suite proves that trust is justified.
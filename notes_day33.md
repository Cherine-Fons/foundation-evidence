# Day 33 — F6D5: Grow the Test Suite + Type Hints

## What We Are Doing

Today shifts away from plotting and back to **testing discipline**.

There are two halves:

```text
Half 1 → expand the pytest test suite
Half 2 → add type hints to two function signatures
```

`pytest` returns from F4 / Day 21, but now it will be applied to **numeric helper functions**, including a function that uses NumPy.

This matters because assertion-thinking is a core part of building reliable mathematical software: a test encodes what a function is supposed to do and automatically checks whether the implementation satisfies that claim.

---

# Half 1 — Numeric Helpers + Pytest

Before writing tests, I first need some functions to test.

Today I am creating a new module:

```text
finance_utils.py
```

It will contain three small numeric helper functions.

---

## What I Need

I am using tools I already have:

```text
Python
NumPy
pytest
```

No plotting or Matplotlib today.

The new project file is:

```text
finance_utils.py
```

Later, I will create a pytest file that tests the functions inside it.

---

# Module Discipline

`finance_utils.py` is a **module**, not a script.

That means it should stay silent when imported.

It should contain:

```text
imports
function definitions
```

but **no top-level prints or function calls**.

> **Module rule:** functions return values; they do not print their answers.

The test file will perform the checking.

---

# The Three Functions

## 1. `simple_return`

Specification:

```python
simple_return(old_price, new_price)
```

It computes:

```python
(new_price - old_price) / old_price
```

This is ordinary Python arithmetic and does **not** require NumPy.

---

## 2. `future_value`

Specification:

```python
future_value(principal, annual_rate, years)
```

It computes compound future value:

```python
principal * (1 + annual_rate) ** years
```

This is the compound-interest function I have already worked with.

---

## 3. `mean_return`

Specification:

```python
mean_return(returns)
```

This is today's **NumPy-facing function**.

It should:

```text
receive a list
→ convert it to a NumPy array
→ compute the mean
→ return the mean
```

Because this function uses NumPy, the module needs:

```python
import numpy as np
```

at the top.

---

# Environment Setup

Work from:

```text
foundation %
```

with the virtual environment active.

Create the module:

```bash
code finance_utils.py
```

Then verify the filename:

```bash
ls finance_utils.py
```

---

# First Task

My first task is to write `finance_utils.py` containing:

```python
import numpy as np
```

followed by the three function definitions:

```text
simple_return(...)
future_value(...)
mean_return(...)
```

The file should contain **no print statements and no top-level function calls**.

The structure should therefore be:

```python
import numpy as np


def simple_return(old_price, new_price):
    ...


def future_value(principal, annual_rate, years):
    ...


def mean_return(returns):
    ...
```

I supply the function bodies from the specifications.

---

# Verify That the Module Imports

After saving the file, run:

```bash
python -c "import finance_utils; print('ok')"
```

`python -c` runs the quoted Python statement directly from the terminal.

This command:

```python
import finance_utils
```

tries to load and parse the entire module.

Only after that succeeds does:

```python
print("ok")
```

run.

---

# My Prediction

If `finance_utils.py` has valid Python syntax and imports correctly, I predict:

```text
ok
```

If the module contains a syntax or structural error, Python will **not** reach the `print("ok")`; instead, it will show a traceback describing the import failure.

> **Import-check logic:** successful import → `ok`; broken module → traceback.

---

# What Comes Next

Once `finance_utils.py` imports cleanly, the next step is to build the **pytest test file** for these functions.

The tests will include float comparisons using a **tolerance**, connecting today's testing work back to the floating-point tolerance work from F5 such as `np.allclose`.

After the test-suite half, Day 33 moves to the second component:

```text
type hints on two function signatures
```

The specific type-hint work comes after the testing portion.

=====================================================================================================================================================================

Put exactly this in `finance_utils.py`:

```python
import numpy as np


def simple_return(old_price, new_price):
    return (new_price - old_price) / old_price


def future_value(principal, annual_rate, years):
    return principal * (1 + annual_rate) ** years


def mean_return(returns):
    returns_array = np.array(returns)
    return returns_array.mean()
```

A couple of things to notice:

* `import numpy as np` is at the top because `mean_return()` uses NumPy.
* Each function **returns** a value.
* There are **no `print()` statements**.
* There are **no function calls at the bottom** of the file.

So this is a silent reusable module.

After saving it, run:

```bash
python -c "import finance_utils; print('ok')"
```

Prediction:

```text
ok
```

if the module imports cleanly.

=====================================================================================================================================================================

# Day 33 — Write the Pytest File

Create:

```bash
code test_finance_utils.py
```

Verify:

```bash
ls test_finance_utils.py
```

Then put this in the file:

```python
import pytest
from finance_utils import simple_return, future_value, mean_return


def test_simple_return():
    assert simple_return(100, 110) == pytest.approx(0.1)


def test_future_value():
    assert future_value(1000, 0.10, 2) == pytest.approx(1210.0)


def test_mean_return():
    assert mean_return([0.1, 0.2, 0.3]) == pytest.approx(0.2)
```

## Verify the Expected Values First

### Test 1

```text
(110 - 100) / 100
= 10 / 100
= 0.1
```

So:

```python
pytest.approx(0.1)
```

is correct.

### Test 2

```text
1000 × (1 + 0.10)²
= 1000 × 1.10²
= 1000 × 1.21
= 1210.0
```

So:

```python
pytest.approx(1210.0)
```

is correct.

### Test 3

```text
(0.1 + 0.2 + 0.3) / 3
= 0.6 / 3
= 0.2
```

So:

```python
pytest.approx(0.2)
```

is correct.

---

## Why `pytest.approx()`?

These functions return floating-point values.

Instead of demanding exact binary equality:

```python
actual == expected
```

we use:

```python
actual == pytest.approx(expected)
```

which allows tiny floating-point representation differences.

> **Testing rule:** when the mathematically expected answer is a float, compare within tolerance rather than assuming exact binary equality.

---

# Prediction Before Running Pytest

Run:

```bash
python -m pytest test_finance_utils.py -v
```

I predict pytest will discover exactly **three tests** because all three function names begin with:

```text
test_
```

and all three should report:

```text
PASSED
```

So the final summary should be approximately:

```text
test_finance_utils.py::test_simple_return PASSED
test_finance_utils.py::test_future_value PASSED
test_finance_utils.py::test_mean_return PASSED

3 passed
```

> **Prediction: `3 passed` with no failures.**

The important conceptual shift today is that we are no longer merely calculating answers—we are encoding those expected mathematical results as **permanent executable assertions**.

=====================================================================================================================================================================

## Half 2 — Type Hints

Update only the two function signatures in `finance_utils.py`.

```python
def simple_return(old_price: float, new_price: float) -> float:
    return (new_price - old_price) / old_price


def future_value(principal: float, annual_rate: float, years: int) -> float:
    return principal * (1 + annual_rate) ** years
```

Leave `mean_return()` unchanged for now.

---

## What the Type Hints Mean

```python
old_price: float
```

means:

> `old_price` is intended to receive a floating-point number.

And:

```python
-> float
```

means:

> the function is intended to return a float.

For:

```python
def future_value(
    principal: float,
    annual_rate: float,
    years: int,
) -> float:
```

the distinction is:

```text
principal   → float
annual_rate → float
years       → int
return      → float
```

> **Type hints document intent. They do not enforce the types at runtime.**

---

# Prediction Before Re-Running the Tests

I predict:

```text
3 passed
```

again.

Why? Because adding:

```python
: float
: int
-> float
```

does **not change the function bodies** or the arithmetic they perform.

The functions still compute exactly the same expressions:

```python
(new_price - old_price) / old_price
```

and:

```python
principal * (1 + annual_rate) ** years
```

So the tests should behave identically.

> **Prediction:** the annotations change the function's documented interface, not its computation.

---

## Prove It With Pytest

Run:

```bash
python -m pytest test_finance_utils.py -v
```

Expected:

```text
test_simple_return PASSED
test_future_value PASSED
test_mean_return PASSED

3 passed
```

---

## Then Check With Ruff

Run:

```bash
ruff check finance_utils.py
```

Prediction:

```text
All checks passed!
```

So today's pattern is:

```text
add type hints
→ behavior should stay unchanged
→ pytest proves behavior still works
→ ruff checks the updated code
```

Paste the pytest and Ruff output after you run them.

===============================================================================================================================================================

# Day 33 — Verify the Two Files Before Commit

That **`9 passed`** result is actually better than the targeted three-test run because you accidentally ran the entire accumulated suite:

```text
6 existing tests
+ 3 new finance tests
= 9 tests total
```

So you have now confirmed that the new finance utilities and type hints introduced **no regressions anywhere else in the project**.

Before formatting and committing, verify that the responsibilities of the two files are still separated correctly.

## 1. Check the test file

At `foundation %`:

```bash
cat test_finance_utils.py
```

It should contain **only** the imports and the three tests:

```python
import pytest
from finance_utils import simple_return, future_value, mean_return


def test_simple_return():
    assert simple_return(100, 110) == pytest.approx(0.1)


def test_future_value():
    assert future_value(1000, 0.10, 2) == pytest.approx(1210.0)


def test_mean_return():
    assert mean_return([0.1, 0.2, 0.3]) == pytest.approx(0.2)
```

It should **not** contain implementations such as:

```python
def simple_return(...):
```

or:

```python
def future_value(...):
```

Those belong in the module being tested.

> **Test file = expected behavior expressed as assertions.**
> **Module file = actual implementation.**

---

## 2. Check the module

Then run:

```bash
cat finance_utils.py
```

It should look like:

```python
import numpy as np


def simple_return(old_price: float, new_price: float) -> float:
    return (new_price - old_price) / old_price


def future_value(principal: float, annual_rate: float, years: int) -> float:
    return principal * (1 + annual_rate) ** years


def mean_return(returns):
    returns_array = np.array(returns)
    return returns_array.mean()
```

The two type-hinted signatures should be in **`finance_utils.py`**, not the test file:

```python
def simple_return(old_price: float, new_price: float) -> float:
```

and:

```python
def future_value(principal: float, annual_rate: float, years: int) -> float:
```

---

## What We Are Verifying

The clean architecture is:

```text
finance_utils.py
    ↓
contains implementations

test_finance_utils.py
    ↓
imports those implementations
    ↓
asserts known answers
```

And today's suite result is now:

```text
pytest discovered 9 tests
→ all 9 executed
→ all 9 passed
→ no regressions
```

Run:

```bash
cat test_finance_utils.py
cat finance_utils.py
```

and paste both outputs. If the test file is clean, the next step is straight to **Black + Ruff + the f6d5 commit**.

===============================================================================================================================================================

# Day 33 — F6D5: Grow the Test Suite + Type Hints RECAP

## Numeric Helper Module

Today I created a reusable module:

```text
finance_utils.py
```

It contains the actual implementations:

```python
import numpy as np


def simple_return(old_price: float, new_price: float) -> float:
    return (new_price - old_price) / old_price


def future_value(principal: float, annual_rate: float, years: int) -> float:
    return principal * (1 + annual_rate) ** years


def mean_return(returns):
    returns_array = np.array(returns)
    return returns_array.mean()
```

The module stays **silent**:

* no top-level `print()`
* no top-level function calls
* functions compute and `return` values

> **Module = implementation. Test file = assertions about the implementation.**

---

# Test File Separation

The tests live separately in:

```text
test_finance_utils.py
```

```python
import pytest
from finance_utils import simple_return, future_value, mean_return


def test_simple_return():
    assert simple_return(100, 110) == pytest.approx(0.1)


def test_future_value():
    assert future_value(1000, 0.10, 2) == pytest.approx(1210.0)


def test_mean_return():
    assert mean_return([0.1, 0.2, 0.3]) == pytest.approx(0.2)
```

The test file **imports** the functions from the module rather than redefining them.

> **`finance_utils.py` contains what the program does.**
> **`test_finance_utils.py` contains claims about what it should do.**

---

# Assertion Thinking

Before writing each test, I derived the expected result independently.

## Simple Return

```text
(110 - 100) / 100
= 10 / 100
= 0.1
```

## Future Value

```text
1000 × (1 + 0.10)²
= 1000 × 1.10²
= 1000 × 1.21
= 1210.0
```

## Mean Return

```text
(0.1 + 0.2 + 0.3) / 3
= 0.6 / 3
= 0.2
```

> **A test should compare the function against an answer I already know independently. I do not use the function itself to decide what its expected answer should be.**

---

# `pytest.approx()` for Floating-Point Tests

All three tests use:

```python
pytest.approx(expected_value)
```

instead of relying on exact floating-point equality.

For example:

```python
assert mean_return([0.1, 0.2, 0.3]) == pytest.approx(0.2)
```

Floating-point arithmetic can contain tiny representation differences, so numerical tests should compare within a tolerance.

> **F5 tolerance lesson → F6 testing lesson:** numerical equality often means “equal within a sufficiently small tolerance,” not necessarily identical binary representations.

---

# Growing the Test Suite

Running:

```bash
python -m pytest
```

without specifying a filename caused pytest to discover the **entire repository test suite**.

It collected:

```text
9 items
```

consisting of:

```text
test_finance_utils.py → 3 tests
test_helpers.py       → 5 tests
test_multigraph.py    → 1 test
```

Total:

```text
3 + 5 + 1 = 9 tests
```

Result:

```text
9 passed
```

The suite therefore grew from:

```text
6 tests → 9 tests
```

and all older tests remained green.

> **Running the whole suite checks for regressions:** new work passed without breaking previously tested behavior.

---

# The Test-File Mix-Up

During the lesson, function implementations were temporarily placed in the test file.

That created the wrong separation of responsibilities.

The correct structure is:

```text
finance_utils.py
    ↓
actual function implementations


test_finance_utils.py
    ↓
imports those functions
    ↓
tests them with assertions
```

The files were cleaned up, and pytest again discovered the full expected suite.

> **A test-suite count unexpectedly shrinking is itself a warning signal.** If pytest suddenly discovers fewer tests than expected, check whether test functions or files were accidentally overwritten, renamed, or removed.

---

# Type Hints

Type hints document the intended input and output types of a function.

The syntax is:

```python
def function_name(parameter: type) -> return_type:
```

For example:

```python
def simple_return(old_price: float, new_price: float) -> float:
```

means:

```text
old_price → intended float
new_price → intended float
return    → intended float
```

And:

```python
def future_value(
    principal: float,
    annual_rate: float,
    years: int,
) -> float:
```

documents:

```text
principal   → float
annual_rate → float
years       → int
return      → float
```

---

# Type Hints Do Not Change Runtime Behavior

Adding:

```python
: float
: int
-> float
```

does not change the arithmetic inside the functions.

The function bodies remained identical.

After adding the hints, the complete pytest suite still produced:

```text
9 passed
```

> **Type hints describe the intended interface; they do not themselves enforce those types at runtime.**

---

# Finish F6D5

Save these notes as:

```text
notes_day33.md
```

Then format the two Python files:

```bash
black finance_utils.py test_finance_utils.py
```

Lint them:

```bash
ruff check finance_utils.py test_finance_utils.py
```

Expected Ruff result:

```text
All checks passed!
```

Then inspect the repository:

```bash
git status
```

You want the Day 33 files to be:

```text
finance_utils.py
test_finance_utils.py
notes_day33.md
```

with no stray scratch files and no PNG artifacts appearing.

Then stage exactly those three:

```bash
git add finance_utils.py test_finance_utils.py notes_day33.md
```

Commit:

```bash
git commit -m "f6d5: grow test suite (finance_utils, pytest.approx), add type hints"
```

Since all three are new files, the clean expected shape is:

```text
3 files changed
create mode ... finance_utils.py
create mode ... test_finance_utils.py
create mode ... notes_day33.md
```

That closes **f6d5**.



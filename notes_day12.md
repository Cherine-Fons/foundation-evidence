Specification day:

Write the four-line spec for the degree tally helper, in prose:

Name — verb-ish, lowercase, underscores.
Input — exact type and shape.
Output — exact type and shape.
Invariant — what must always be true of the output (the sum-of-degrees sanity check from Saturday).

Show me those four lines and we'll refine, then you spec the other three helpers.

-----------------------------------------------------------------------------------------------------------------
### Degree tally helper

**Name** — compute_degrees
**Input** — A list of two-integer tuples, where each tuple (u, v) represents one edge; repeated edges are allowed.
**Output** — A dictionary whose keys are exactly the vertices appearing in at least one edge, each mapped to its integer degree; vertices appearing in no edge are absent.
**Invariant** — The sum of all degree values equals twice the number of edges.

### Differences helper

**Name** — abs_diffs
**Input** — A list of numbers representing values in sequence order.
**Output** — A list containing the absolute difference between each value and the value immediately before it.
**Invariant** — Every output value is nonnegative, and the output length is `max(len(values) - 1, 0)`.

### Candidate-filtering helper

**Name** — find_over_capacity
**Input** — A dictionary of vertex degrees and a dictionary of capacities for those vertices.
Assumption — Every vertex appearing in degrees also has an entry in capacities.
**Output** — A list containing the vertices whose degree strictly exceeds their capacity; equality does not qualify.
**Invariant** — The output list is always a subset of the vertices supplied in the degree dictionary.

### Admissibility predicate

**Name** — is_admissible
**Input** — Two integers representing the pair to be tested against the admissibility conditions.
**Output** — True when the pair satisfies the conditions and False when it does not.
**Invariant** — For every valid input, the function always returns either True or False, never a number, string, or None; it returns True exactly when a + b is even and a <= b.
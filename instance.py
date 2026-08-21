# ==================================================================================================
# F7 CAPSTONE — TOY MULTIGRAPH INSTANCE
# ==================================================================================================
#
# This module contains the fixed toy instance that the brute-force checker
# will eventually verify.
#
# It currently contains:
#
# 1. VERTICES
# 2. EDGES — explicit multigraph edge copies
# 3. F_VALUES — the locked vertex function f
# 4. compute_degrees() — computes degrees with multiplicity
# 5. validate_instance() — checks the graph-level assumptions
#
# IMPORTANT:
#
# These are INSTANCE-LEVEL definitions and checks.
#
# They are separate from the later PAIR-LEVEL admissibility conditions
# imposed on candidate pairs (U, F).
#
# ==================================================================================================


# --------------------------------------------------------------------------------------------------
# VERTICES
# --------------------------------------------------------------------------------------------------
#
# The toy multigraph has five vertices:
#
#     V = {0, 1, 2, 3, 4}
#
# A frozenset is used because:
#
# - the vertex set is fixed,
# - order is not mathematically important,
# - membership checks will be frequent,
# - the instance should not accidentally mutate this set.
#
# If deterministic iteration order is ever needed, use:
#
#     sorted(VERTICES)
#
# --------------------------------------------------------------------------------------------------


VERTICES = frozenset({0, 1, 2, 3, 4})


# --------------------------------------------------------------------------------------------------
# EDGES
# --------------------------------------------------------------------------------------------------
#
# Every edge copy is represented by:
#
#     (edge_id, endpoint_u, endpoint_v)
#
# The graph contains six actual edge copies:
#
#     e0 = (0, 1)
#     e1 = (0, 1)    parallel copy of e0
#     e2 = (1, 2)    bridge
#     e3 = (2, 3)
#     e4 = (3, 4)
#     e5 = (2, 4)
#
# Structure:
#
#     0 ══ 1 ── 2
#                / \
#               3 ── 4
#
# e0 and e1 have the same endpoints but are DISTINCT edges.
#
# EDGES is deliberately a list:
#
# - each edge copy is preserved,
# - parallel copies remain distinct,
# - each copy contributes separately to degree and edge counts,
# - the input order remains deterministic.
#
# Never replace the multigraph by a set of endpoint pairs such as:
#
#     {(0, 1), ...}
#
# because that would collapse parallel copies.
#
# --------------------------------------------------------------------------------------------------


EDGES = [
    ("e0", 0, 1),
    ("e1", 0, 1),
    ("e2", 1, 2),
    ("e3", 2, 3),
    ("e4", 3, 4),
    ("e5", 2, 4),
]


# --------------------------------------------------------------------------------------------------
# F-VALUES
# --------------------------------------------------------------------------------------------------
#
# The locked positive integer vertex function is:
#
#     f = (1, 1, 2, 2, 2)
#
# Meaning:
#
#     f(0) = 1
#     f(1) = 1
#     f(2) = 2
#     f(3) = 2
#     f(4) = 2
#
# A dictionary represents the mapping:
#
#     vertex -> f-value
#
# This assignment was chosen so that the hand-derived unique maximizing pair is:
#
#     U* = {0, 1}
#     F* = {e2}
#
# with exact modified set-pair density:
#
#     3
#
# --------------------------------------------------------------------------------------------------


F_VALUES = {
    0: 1,
    1: 1,
    2: 2,
    3: 2,
    4: 2,
}


# ==================================================================================================
# COMPUTE DEGREES
# ==================================================================================================
#
# PURPOSE:
#
# Compute:
#
#     d_G(v)
#
# for every vertex v.
#
# The degree counts MUST include multiplicity.
#
#
# COMMENTS-FIRST ALGORITHM:
#
# 1. Start every vertex with degree 0.
#
# 2. Walk through EDGES exactly once.
#
# 3. Each edge has the form:
#
#        (edge_id, u, v)
#
# 4. Every loopless edge copy contributes:
#
#        +1 to degree(u)
#        +1 to degree(v)
#
# 5. Because parallel edges are separate entries in EDGES,
#    multiplicity is counted automatically.
#
# 6. Return the completed:
#
#        vertex -> degree
#
#    dictionary.
#
#
# HAND-DERIVED EXPECTED DEGREES:
#
#     {
#         0: 2,
#         1: 3,
#         2: 3,
#         3: 2,
#         4: 2,
#     }
#
# Sanity check:
#
#     2 + 3 + 3 + 2 + 2 = 12
#
#     2 * |E| = 2 * 6 = 12
#
# ==================================================================================================


def compute_degrees():
    degrees = {v: 0 for v in VERTICES}

    for edge_id, u, v in EDGES:
        degrees[u] += 1
        degrees[v] += 1

    return degrees


# ==================================================================================================
# VALIDATE INSTANCE
# ==================================================================================================
#
# PURPOSE:
#
# These are GRAPH-LEVEL checks.
#
# They run once before the checker trusts the instance.
#
# They are NOT the later admissibility conditions on a candidate pair (U, F).
#
#
# FAILURE BEHAVIOR:
#
#     invalid instance -> raise ValueError immediately
#
# The validator stops at the FIRST violation it encounters.
#
# This is deliberate:
#
#     any invalid foundational condition is enough to stop the checker.
#
# An alternative design could collect every violation and report them together,
# but this checker uses fail-fast validation.
#
#
# CHECK 1:
#
#     VERTICES must be nonempty.
#
#
# CHECK 2:
#
#     The graph must be loopless.
#
#     Every edge:
#
#         (edge_id, u, v)
#
#     must satisfy:
#
#         u != v
#
#
# CHECK 3:
#
#     Every vertex must have an f-value.
#
#     Every f-value must be a positive integer:
#
#         type(f(v)) is int
#         f(v) > 0
#
#
# CHECK 4:
#
#     Compute the degree dictionary.
#
#     Then require:
#
#         f(v) <= d_G(v)
#
#     for every vertex.
#
#
# LOCKED-INSTANCE PREDICTION:
#
#     f = (1, 1, 2, 2, 2)
#     d = (2, 3, 3, 2, 2)
#
# Therefore:
#
#     1 <= 2
#     1 <= 3
#     2 <= 3
#     2 <= 2
#     2 <= 2
#
# All four checks should pass.
#
# ==================================================================================================


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
            raise ValueError(f"f({v}) must be a positive integer, got {f_value!r}")

    # Check 4 — require f(v) <= d_G(v) at every vertex.
    degrees = compute_degrees()

    for v in VERTICES:
        if F_VALUES[v] > degrees[v]:
            raise ValueError(
                f"active-regime violation at vertex {v}: "
                f"f({v})={F_VALUES[v]} > d_G({v})={degrees[v]}"
            )


# ==================================================================================================
# TEMPORARY PASSING-CASE CHECK
# ==================================================================================================
#
# The locked instance is known to satisfy all four validation conditions.
#
# Prediction:
#
#     validate_instance()
#
# reaches the end normally without raising ValueError.
#
# Then:
#
#     print("instance valid")
#
# executes.
#
# Expected terminal output:
#
#     instance valid
#
# This block is TEMPORARY.
# We will remove it after exercising the validator.
# ==================================================================================================

# ==================================================================================================
# F7 CAPSTONE — TOY MULTIGRAPH INSTANCE
# ==================================================================================================
#
# This module contains the fixed toy instance that the brute-force checker
# will verify.
#
# It contains:
#
# 1. VERTICES
# 2. EDGES — explicit multigraph edge copies
# 3. F_VALUES — the locked vertex function f
# 4. compute_degrees() — computes degrees with multiplicity
# 5. validate_instance() — checks the graph-level assumptions
#
#
# IMPORTANT:
#
# These are INSTANCE-LEVEL definitions and checks.
#
# They are separate from the later PAIR-LEVEL admissibility conditions
# imposed on candidate pairs (U, F).
#
# This module must remain silent on import.
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
# - membership checks are frequent,
# - the instance should not accidentally mutate this set.
#
# --------------------------------------------------------------------------------------------------


VERTICES = frozenset({0, 1, 2, 3, 4})


# --------------------------------------------------------------------------------------------------
# EDGES
# --------------------------------------------------------------------------------------------------
#
# Every physical edge copy is represented by:
#
#     (edge_id, endpoint_u, endpoint_v)
#
# The graph contains six edge copies:
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
# Parallel copies have:
#
#     the same endpoints
#     different edge IDs
#
# Edge IDs must remain unique because boundary(U) and candidate F
# represent physical edge copies by their IDs.
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
# Degree counts include multiplicity.
#
#
# COMMENTS-FIRST ALGORITHM:
#
# 1. Start every vertex with degree 0.
#
# 2. Walk through every explicit edge copy.
#
# 3. Every loopless edge:
#
#        (edge_id, u, v)
#
#    contributes:
#
#        +1 to degree(u)
#        +1 to degree(v)
#
# 4. Parallel copies occur as separate entries, so multiplicity is
#    counted automatically.
#
# 5. Return the degree dictionary.
#
#
# HAND-DERIVED RESULT:
#
#     {
#         0: 2,
#         1: 3,
#         2: 3,
#         3: 2,
#         4: 2,
#     }
#
# ==================================================================================================


def compute_degrees():
    degrees = {v: 0 for v in VERTICES}

    for _edge_id, u, v in EDGES:
        degrees[u] += 1
        degrees[v] += 1

    return degrees


# ==================================================================================================
# VALIDATE INSTANCE
# ==================================================================================================
#
# PURPOSE:
#
# Prove that the graph data satisfies the structural assumptions required
# by the checker before any search result is trusted.
#
#
# FAILURE CONTRACT:
#
#     invalid instance -> raise ValueError immediately
#
# The validator is fail-fast:
#
#     first detected violation -> stop
#
#
# CHECK 1 — NONEMPTY VERTEX SET
#
#     VERTICES must be nonempty.
#
#
# CHECK 2 — LOOPLESS EDGES
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
# CHECK 3 — VALID EDGE ENDPOINTS
#
#     Every endpoint appearing in EDGES must belong to VERTICES.
#
#     Require:
#
#         u in VERTICES
#         v in VERTICES
#
# This check MUST occur before compute_degrees().
#
# Otherwise an unknown endpoint could cause a bare dictionary KeyError
# instead of a named validation error.
#
#
# CHECK 4 — UNIQUE EDGE IDs
#
#     Every physical edge copy must have a unique ID.
#
# This is essential because:
#
#     boundary(U)
#
# returns edge IDs, and:
#
#     F
#
# is represented as a frozenset of edge IDs.
#
# Duplicate IDs could therefore collapse distinct physical edge copies
# and silently corrupt |F|.
#
#
# CHECK 5 — VALID f-VALUES
#
#     Every vertex must have an f-value.
#
#     Every f-value must be a positive integer:
#
#         type(f(v)) is int
#         f(v) > 0
#
#
# CHECK 6 — ACTIVE REGIME
#
#     After the structural edge checks have passed, compute degrees.
#
#     Require:
#
#         f(v) <= d_G(v)
#
#     at every vertex.
#
# ==================================================================================================


def validate_instance():
    # Check 1 — VERTICES must be nonempty.
    if not VERTICES:
        raise ValueError("VERTICES must be nonempty")

    # Check 2 — every edge must be loopless.
    for edge_id, u, v in EDGES:
        if u == v:
            raise ValueError(
                f"loop detected on edge {edge_id}: endpoints are ({u}, {v})"
            )

    # Check 3 — every edge endpoint must belong to VERTICES.
    for edge_id, u, v in EDGES:
        if u not in VERTICES or v not in VERTICES:
            raise ValueError(
                f"edge {edge_id} has endpoint outside VERTICES: ({u}, {v})"
            )

    # Check 4 — every physical edge copy must have a unique edge ID.
    seen_edge_ids = set()

    for edge_id, _u, _v in EDGES:
        if edge_id in seen_edge_ids:
            raise ValueError(f"duplicate edge ID {edge_id!r}")

        seen_edge_ids.add(edge_id)

    # Check 5 — every vertex must have a positive integer f-value.
    for v in VERTICES:
        if v not in F_VALUES:
            raise ValueError(f"missing f-value for vertex {v}")

        f_value = F_VALUES[v]

        if type(f_value) is not int or f_value <= 0:
            raise ValueError(
                f"f({v}) must be a positive integer, got {f_value!r}"
            )

    # Check 6 — require f(v) <= d_G(v) at every vertex.
    degrees = compute_degrees()

    for v in VERTICES:
        if F_VALUES[v] > degrees[v]:
            raise ValueError(
                f"active-regime violation at vertex {v}: "
                f"f({v})={F_VALUES[v]} > d_G({v})={degrees[v]}"
            )
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
# If U is empty, the loop executes zero times and returns 0.
#
# This is mathematically correct:
#
#     f(empty set) = 0
#
# The later admissibility layer is responsible for rejecting empty U.
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
# Count every explicit edge copy whose BOTH endpoints belong to U.
#
#
# MULTIGRAPH RULE:
#
# Parallel copies count separately.
#
# For example:
#
#     e0 = (0,1)
#     e1 = (0,1)
#
# both contribute when:
#
#     U = {0,1}
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
# 5. Return count.
#
#
# HAND-DERIVED CHECKPOINTS:
#
#     internal_edge_count({0,1}) = 2
#
#     internal_edge_count({2,3,4}) = 3
#
#     internal_edge_count({0,1,2}) = 3
#
#     internal_edge_count({1}) = 0
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

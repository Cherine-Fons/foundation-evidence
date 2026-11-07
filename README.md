# Python Algorithm Foundations

Python implementations of graph algorithms, exact combinatorial optimization, deterministic search, and mathematical verification. The code emphasizes explicit problem specifications, exact arithmetic, input validation, and tests against hand-derived reference results.

## Authorship

I wrote every line of Python code in this repository. Every code commit is my own work, dated as it was written.

## Graph optimization and exact computation

The [set-pair density checker](search.py) evaluates a combinatorial optimization problem on an explicitly represented multigraph. Its components separate graph data, admissibility, exact objective evaluation, and exhaustive search:

| Component | Implementation |
|---|---|
| Multigraph instance and structural validation | [`instance.py`](instance.py) |
| Vertex sums, internal edges, and boundary-edge calculations | [`primitives.py`](primitives.py) |
| Candidate-pair admissibility | [`admissibility.py`](admissibility.py) |
| Exact rational objective evaluation | [`evaluator.py`](evaluator.py) |
| Deterministic exhaustive maximization | [`search.py`](search.py) |
| Correctness and regression tests | [`test_checker.py`](test_checker.py) |

The checker distinguishes parallel edge copies, uses Python's `Fraction` for exact comparisons, and verifies results against independently derived small-instance expectations.

## Graph processing

[`read_edges.py`](read_edges.py), [`helpers.py`](helpers.py), and [`analyze_graph.py`](analyze_graph.py) implement an edge-list processing pipeline. The modules validate input rows, compute vertex degrees, and identify capacity violations.

## Exact optimization over structured records

The [ledger modules](ledger_search.py) implement a separate data-processing and optimization pipeline:

- [`ledger_parser.py`](ledger_parser.py) and [`ledger_model.py`](ledger_model.py) — validated input and typed records.
- [`ledger_eligibility.py`](ledger_eligibility.py) and [`ledger_evaluator.py`](ledger_evaluator.py) — feasibility rules and exact rational scoring.
- [`ledger_search.py`](ledger_search.py) and [`ledger_report.py`](ledger_report.py) — deterministic subset search and results reporting.
- [`test_exit.py`](test_exit.py) and [`EXIT_ORACLE.md`](EXIT_ORACLE.md) — regression tests and a hand-derived reference result.

## Numerical and data utilities

Additional Python modules cover return calculations, data manipulation, and numerical visualization, including [`finance_utils.py`](finance_utils.py), [`prices_series.py`](prices_series.py), and [`capstone_charts.py`](capstone_charts.py).

## Running the code

With Python 3 installed, install the dependencies and run the selected test suites:

```bash
python3 -m pip install -r requirements.txt
python3 -m pytest -q test_checker.py test_exit.py
```

To run the graph-processing example:

```bash
python3 analyze_graph.py
```

The code and its tests are retained alongside the original Git commit history.

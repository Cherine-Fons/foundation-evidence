## What it does 

This tool reads graph edges from a text file, validates each row, computes the degree of every vertex, and checks those degrees against capacity limits. It then prints a report summarizing the valid and invalid input rows and identifying any vertices that exceed their allowed capacity. `analyze_graph.py` connects the parser and helper modules into a single workflow, keeping input validation separate from graph analysis.

## Files
`read_edges.py` — reads and validates the edge data.
`helpers.py` — contains the graph-analysis functions, including degree counting and capacity filtering.
`analyze_graph.py`— runs the full workflow and prints the results.
`edges.txt` — contains the graph data used as input.

## How to run

From the project folder, run:

python analyze_graph.py

## Input format

Each line of edges.txt should contain exactly two integers separated by a comma, such as 2,5. Valid rows are converted into edges; malformed rows are collected and reported instead of causing the program to crash.

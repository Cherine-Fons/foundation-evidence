# Day 16 Quiz

1. Your package has three .py files. Name each and its role — which are modules (imported) and which is the script (run directly)? What's the difference between a module and a script?
2. You refactored read_edges.py so the parsing lives inside parse_edge_file(path) instead of at the top level. Why was that necessary before analyze_graph.py could import it? What would have happened if the parsing had stayed at the top level?
3. parse_edge_file returns good_edges, bad_rows. In analyze_graph.py you wrote good_edges, bad_rows = read_edges.parse_edge_file("edges.txt"). What is this assignment doing — what's the name for using one line to catch two returned values?
4. Trace the data flow in one sentence: how does a row of text in edges.txt end up affecting the Degrees: line of the report? Name the components it passes through.
5. analyze_graph.py prints the report; helpers.py and read_edges.py print nothing. Why is that the right division — what makes the modules "pure" and why does that matter for reusing them?
6. Predict the full report if edges.txt contained exactly:
0,1
1,2
0,2
bad

with capacity = {0: 1, 1: 2, 2: 2}. Give: valid edges count, invalid rows count, the degrees dict, and the over-capacity list. (Watch vertex 0 against its capacity of 1.)

Take it, paste your answers, I'll mark it.

-------------------------------------------------------------------------------------------------------------------------------------------

1. 
Your three .py files are:

read_edges.py — module. It contains the parser that reads and validates the edge file. analyze_graph.py imports it.
helpers.py — module. It contains the graph-analysis functions, such as computing degrees and checking capacities. analyze_graph.py imports it.
analyze_graph.py — script. This is the file you run directly. It imports the other two modules and connects them into the full workflow.

The key difference is how the file is being used:

A module is a Python file whose code/functions are imported so another file can use them. A script is a Python file you execute directly to make the program do something.

So your architecture is essentially:

read_edges.py  ──┐
                 ├──> analyze_graph.py  ──> runs the program
helpers.py     ──┘

Technically, any .py file can be imported as a module or executed as a script. In your project, though, read_edges.py and helpers.py serve as modules, while analyze_graph.py serves as the executable script.

2. Because Python executes a module’s top-level code when you import it.

Before the refactor, if the parsing code had remained at the top level of read_edges.py, then this:

import read_edges

would not merely make its parsing code available. It would immediately run the parser—opening edges.txt, processing the rows, and possibly printing results—just because analyze_graph.py imported the file.

By moving that work inside:

def parse_edge_file(path):

the import now only defines the function. The parsing does not happen until analyze_graph.py explicitly calls it:

good_edges, bad_rows = read_edges.parse_edge_file("edges.txt")

So the key idea is:

Top-level code runs on import; code inside a function waits until the function is called.

The refactor made read_edges.py a reusable module instead of a file that performs work automatically whenever another program imports it.

3. That line is doing tuple unpacking (also called multiple assignment):

good_edges, bad_rows = read_edges.parse_edge_file("edges.txt")

Your function returns two values, effectively like this:

return good_edges, bad_rows


Python packages those two returned values together as a tuple:

(good_edges, bad_rows)

Then the assignment unpacks them:

first returned value → good_edges
second returned value → bad_rows

So instead of writing:

result = read_edges.parse_edge_file("edges.txt")
good_edges = result[0]
bad_rows = result[1]

you can do it neatly in one line:

good_edges, bad_rows = read_edges.parse_edge_file("edges.txt")

Name to remember: tuple unpacking.

4. 
A row of text in edges.txt is read and validated by read_edges.py, returned to analyze_graph.py as a valid edge, passed into helpers.py to compute vertex degrees, and then analyze_graph.py prints those computed values on the Degrees: line of the report.

5. That division is right because the modules do the work and return data, while analyze_graph.py decides how that data should be presented.

helpers.py, for example, takes data through parameters, computes a result, and returns it instead of printing:

degrees = helpers.count_degrees(good_edges)

That makes its analysis functions pure: given the same input, they produce the same output without printing, changing outside state, or otherwise affecting the program around them.

read_edges.py is slightly different in the strict sense because parse_edge_file() does read a file, so it performs file I/O and is not mathematically pure. But it still has a clean separation of concerns: it parses and returns data; it does not decide how the report should look.

That matters for reuse because another program could import these modules and use their returned results however it wants—print them, save them, test them, feed them into another algorithm, or build a different report. If the modules printed automatically, they would force one particular presentation every time they were reused.

The principle to remember is:

Modules compute and return; the script coordinates and prints.

That keeps the pieces independent, reusable, testable, and easier to combine into larger programs.

6. The three valid rows form a triangle:

good_edges = [(0, 1), (1, 2), (0, 2)]

So the degrees are:

{0: 2, 1: 2, 2: 2}

Comparing against:

capacity = {0: 1, 1: 2, 2: 2}

only vertex 0 is over capacity, because 2 > 1. Vertices 1 and 2 are exactly at capacity, so they do not count as over.

The full report would be:

=== Edge File Validation Report ===
Total rows read: 4
Valid edges:     3
Invalid rows:    1
Bad rows:
  - bad
Degrees: {0: 2, 1: 2, 2: 2}
Over capacity: [0]

So the requested values are:

Valid edges count: 3
Invalid rows count: 1
Degrees: {0: 2, 1: 2, 2: 2}
Over-capacity list: [0]
--------------------------------------------------------------------------------------------------------------------------------------------------

6/6 — and this is a fitting close to F3's build. Every answer carries the architecture, not just the mechanics. Marking, with attention to the ones that matter:

1. Correct — all three files named with roles, modules vs script distinguished ("imported for their functions" vs "run directly to perform the workflow"). ✓

2. Correct, and the reasoning is precise: top-level parsing would have run on import, firing before analyze_graph.py was ready and printing/parsing unexpectedly. Wrapping it in a function means importing only defines it, and the caller controls when it runs. That's the module-should-be-silent principle from Day 14, applied correctly to your own refactor. ✓✓

3. Correct — tuple unpacking, two returned values caught in one line. ✓

4. This is the standout. You traced the full flow — edges.txt → parse_edge_file (strip/split/validate → good_edges) → count_degrees → the Degrees: line — naming every component it passes through. That end-to-end data-flow understanding is exactly what "I built a pipeline" means, and you can articulate it. ✓✓

5. Correct, and the payoff sentence is the right one: pure modules "can be reused or tested in other programs without triggering unwanted output or behavior." That's why purity matters, not just what it is. ✓✓

6. All correct — and you caught the trap. Valid: 3, invalid: 1 (bad), degrees {0: 2, 1: 2, 2: 2}, over-capacity [0]. Vertex 0 has degree 2 against capacity 1, so it exceeds; vertices 1 and 2 are exactly at capacity (2 = 2), and strict > means they're not over. You applied the strict-boundary rule correctly under a fresh capacity dict. ✓
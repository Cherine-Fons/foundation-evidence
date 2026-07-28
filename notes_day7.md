## Day 7 (Tue Jul 28) — `for`, `range`, lists — ~3.5 h · commits `f2d1:`
*Read: Primer Ch 3 (lists section) + Ch 4 (loops). [Primer Ch 3 Simple Ex 2; Ch 3 Review Q1, Q3]*

EXERCISE 1 Interpreter warm-up, *[predict]* each before running: `list(range(5))` · `list(range(1, 10, 2))` · `range(3)` on its own line · `len(range(100))`.

1. list(range(5))       
PREDICTION:
1
2
3
4
5

CORRECTION: [0, 1, 2, 3, 4]

2. list(range(1, 10, 2))
PREDICTION:
1
10
2

CORRECTION: [1, 3, 5, 7, 9]


3. range(3)          # typed on its own line, bare — no list()
PREDICTION:
Error

4. len(range(100))
PREDICTION:
I have no idea


NOTES:
#1 — list(...) takes something iterable—such as a range—and collects its values into a list. Creates numbers from 0 up to—but not including—5. list() converts them into an actual list.

#2 — list(range(...))creates a list of integers from a sequence. Read the three arguments as range(start, stop, step). So range(1, 10, 2) means: start at 1, stop before 10, step by 2. Stopping before stop — the stop is never included.

#3 — range() creates a range object representing 0, 1, 2, but does not convert it into a list. Its the lazy object echoing itself.

#4 — len(...) returns how many numbers the range contains. range(100) represents integers 0 through 99, so its length is 100.

>>> list(range(5))
[0, 1, 2, 3, 4]
>>> list(range(1, 10, 2))
[1, 3, 5, 7, 9]
>>> range(5)
range(0, 5)
>>> len(range(100))
100
>>> 

EXERCISE 2 First loops: a `for` loop that prints each element of a list of exercise names; then one that prints a running total of a list of set-counts. *[predict]* the totals line by line on paper first.

The goal: given a list of exercise names, print each one on its own line.

Two pieces you need. First, a list of strings: 
exercises = ["squat", "bench", "deadlift"]

Second, the for loop. The shape is:

for name in exercises:
    print(name)

Here:

exercises is the variable name.
= assigns a value to that variable.
["squat", "bench", "deadlift"] is one list containing three strings.
The square brackets mark the boundaries of the list.
The commas separate the items

python:

exercises = ["squat", "bench", "deadlift"]

for name in exercises:
    print(name)

Read the loop as:

For each name in the list called exercises, print that name
name gets its value from the loop, not from me. On the first pass Python sets name = "squat", runs the body, then sets name = "bench", runs the body again, then "deadlift". I never assign name myself.

PREDICTION: (remove name = since its print(name) and not print("name ="), print(name) prints only the value)
name = squat
name = bench
name = deadlift


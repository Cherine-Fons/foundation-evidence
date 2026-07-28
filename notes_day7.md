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
name = deadlifT

RUN:
cherinefons@Mac foundation % python3 day7_progress.py
squats
bench
deadlifts


NEXT: The running-total loop. Goal: given a list of set-counts, print a running total — the sum so far, updated as you go down the list.

New idea here: a variable that lives outside the loop and gets updated inside it. The loop variable (name last time) resets each pass; this new variable has to survive across passes so it can accumulate. That's the whole lesson.

lINE 1: sets = [ 3, 4, 5, 3 ]       a list of numbers, not strings

LINE 2: total = 0

This is the variable that survives across passes. It starts at 0 because you haven't added anything yet. Critically, it sits at the left margin — outside and above the loop — so it's created once, not reset every pass. If it were inside the loop, it'd reset to 0 every time and never accumulate.

The loop is going to add each set-count to total, one at a time, and print total after each addition. Starting from total = 0, walk the list [3, 4, 5, 3]:

PREDICTIONS:
After adding the first element (3): total = 3?
After adding the second (4): total = 7
After adding the third (5): total = 12
After adding the fourth (3): total = 15

CORRECT.

NOW BUILD THE LOOP THAT PRODUCES IT:
LINE 3: for count in sets:

sets = [ 3, 4, 5, 3 ]
total = 0
for count in sets:
    print(count)

PREDICTION: (missing step, so wrong prediction. The prediction 3, 7, 12, 15 needs two things the loop body doesn't have: it needs to add each count into total, and print total — not count.)
3
7
12
15

LINE 4 should be: total = total + count
Read it right-to-left: take the current total, add this pass's count, and store the result back into total. That's how total grows instead of resetting. First pass: total = 0 + 3 → 3. Second: total = 3 + 4 → 7. And so on — my predicted numbers.

LINE 5: print(total)
so full program before running is as follows:

sets = [ 3, 4, 5, 3 ]
total = 0
for count in sets:
    total = total + count
    print(total)

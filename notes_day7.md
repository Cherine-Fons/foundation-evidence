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

EXERCISE 3 Lists as objects: build `weights = [60, 80, 100, 120]`; index `weights[0]`, `weights[-1]`; slice `weights[1:3]`; `.append()`, then re-slice. One sentence in `notes_day7.md`: does a list slice give you a copy or the same list? (Primer Ch 3 Review Q3 — you'll test this properly on Day 10.)
This is about reaching into a list: grabbing single elements, grabbing slices, and adding to it.

In interpreter at >>>:
Type:
weights = [60, 80, 100, 120]

Now indexing — reaching in by position. The key idea: positions start at 0, not 1. So the first element is at index 0, the second at index 1, and so on. Negative indexing counts from the end: -1 is the last element, -2 second-to-last.

PREDICTION:
weights[0]      60
weights[-1]     120

CORRECT. RUN:
>>> weights = [ 60, 80, 100, 120 ]
>>> weights[0]
60
>>> weights[-1]
120
>>> 

NEXT: weights[1:3]   

A slice, not a single element. [1:3] means "from index 1 up to but not including index 3" — same stop-is-excluded rule as range. So it pulls positions 1 and 2. Predict what those two elements are (remember 0-based: position 1 is the second element), then run. Give me the prediction and output.

PREDICT: [80, 100]
RUN:
>>> weights[1 : 3]
[80, 100]
>>> 

CORRECT

Last piece — .append(), which adds to the end of the list. This one changes the list in place. 
Type at >>>: weights.append(140)
then type weights on its own line:

>>> weights.append(140)
>>> weights
[60, 80, 100, 120, 140]
>>> 

PREDICTION: running weights[1 : 3] after append gives same answer as before [80, 100]
correct

Now the note. Here's the thing to notice for the copy-vs-same question: every time you slice, Python hands you a new list containing those elements. The original weights is never altered by slicing — you saw that: slicing it multiple times left weights itself intact. (Contrast .append, which did change weights.) So: a slice returns a copy. You'll test the deeper version of this on Day 10 (what happens with nested lists).

Slicing makes a new list from the elements you select, so the original list stays unchanged. I could slice weights several times and still see that weights itself was intact, unlike .append(), which actually changed the original list. The main rule is: a slice gives you a copy rather than modifying the list you sliced.


EXERCISE 4 Primer Ch 3 Simple Ex 2, gym edition: from a list of session volumes, build (with loops, not comprehensions yet) a list of day-over-day absolute differences, then a list of percentage changes. Hand-check both against a 4-element example on paper before running.

The biggest step today. Goal: from a list of session volumes, build two new lists — the day-over-day absolute differences, and the percentage changes. 

Before any code, the paper work the sheet demands. Take a 4-element example:

volumes = [1000, 1100, 1050, 1200]

"Day-over-day difference" means each value compared to the one before it. So you compare element 1 to element 0, element 2 to element 1, element 3 to element 2. The first element has nothing before it, so it produces no difference — 4 volumes give 3 differences. That off-by-one is the crux of the exercise.

On paper, compute the three absolute differences by hand:

element 1 − element 0 = 1100 − 1000 = 100
element 2 − element 1 = 1050 − 1100 = 50        (absolute difference)
element 3 − element 2 = 1200 − 1050 = 150

Now the loop. This one needs a different tool than before. Last time we looped over elements (for count in sets). But here we need each element and the one before it — so we have to loop over positions (indices), so you can reach both volumes[i] and volumes[i-1].

Two new pieces. First, in the editor, set up the data and an empty list to collect results:

volumes = [1000, 1100, 1050, 1200]
abs_diffs = []

abs_diffs = [] is an empty list — the accumulator, same idea as total = 0 but for collecting values instead of summing them. It starts empty; the loop will .append() into it.

The loop header. You need positions 1, 2, 3 — not 0, because element 0 has nothing before it. So you loop over a range that starts at 1 and runs to the end of the list:

for i in range(1, len(volumes)):

Unpack it: len(volumes) is 4. So range(1, 4) produces 1, 2, 3 — exactly the positions that have a predecessor. i takes each of those in turn. Starting at 1 (not 0) is what skips the first element; stopping at len (excluded) is what avoids running off the end.

This is why you loop over indices here instead of elements: i lets you grab two things per pass — volumes[i] (current) and volumes[i-1] (the one before).

i takes index values, not the elements themselves. range(1, len(volumes)) is range(1, 4), which produces the numbers 1, 2, 3. Those are positions.

The values — 1100, 1050, 1200 — are volumes[1], volumes[2], volumes[3]. That's what you get when you look up those indices. But i itself is 1, then 2, then 3.

That distinction is the whole reason this loop works: i is a position, and you use it to reach into the list at volumes[i] and volumes[i-1].



Type that header (left margin, colon). Then predict: for volumes = [1000, 1100, 1050, 1200], what three values will i take? 

PREDICTION: 1100, 1050, 1200
WRONG : i takes index values, not the elements themselves. range(1, len(volumes)) is range(1, 4), which produces the numbers 1, 2, 3. Those are positions.

i is 1, then 2, then 3. Three passes, one per position that has a predecessor.

Now the loop body. On each pass you compute one absolute difference and append it. Two indented lines.

Line — compute the difference:

    diff = abs(volumes[i] - volumes[i - 1])

Walk it for the first pass, i = 1: volumes[1] - volumes[0] = 1100 − 1000 = 100. abs(...) wraps it so a negative result (like pass 2's −50) comes out positive. abs() is a built-in — absolute value.

Line — append into the accumulator:

    abs_diffs.append(diff)

Adds this pass's diff to the abs_diffs list we started empty. Same .append we used on weights.

Both lines indented, inside the loop. After the loop (back at the left margin, not indented), add a print so we can see the result:
print(abs_diffs)


volumes = [1000, 1100, 1050, 1200]
abs_diffs = []
for i in range(1, len(volumes)):
    diff = abs(volumes[i] - volumes[i - 1])
    abs_diffs.append(diff)
print(abs_diffs)

PREDICITION: [100, 50, 150]
CORRECT

Now the second half — percentage changes. Same structure, different formula. 
PREDICT FIRST: for volumes = [1000, 1100, 1050, 1200]:

percentage change from one day to the next = (difference ÷ the previous value) × 100. 
So for pass 1: (1100 − 1000) / 1000 × 100 = 10
for pass 2: (1050 - 1100) / 1100 x 100 = -4.5
or pass 3: (1200 - 1050) / 1050 x 100 = 14.28

BUILD IT:

volumes = [1000, 1100, 1050, 1200]
abs_diffs = []
pct_changes = []

for i in range(1, len(volumes)):
    diff = abs(volumes[i] - volumes[i - 1])
    abs_diffs.append(diff)
print(abs_diffs)

for i in range(1, len(volumes)):
    pct = (volumes[i] - volumes[i - 1]) / volumes[i - 1] * 100
    pct_changes.append(pct)
print(pct_changes)


RUN:

[100, 50, 150]
[10.0, -4.545454545454546, 14.285714285714285]
cherinefons@Mac foundation % 

EXERCISE 5 `day7_progress.py`: script that loops over a hard-coded list of weekly volumes and prints one formatted line per week (f-strings are Week-1 property — use them).

weekly = [1000, 1100, 1050, 1200]
for i in range(len(weekly)):
    print(f"Week {i + 1}: {weekly[i]}")

Two things to hold here:

range(len(weekly)) starts at 0 here — you want every week, no predecessor trick, so no range(1, ...).
{i + 1} displays the human week number: i runs 0,1,2,3 but you print 1,2,3,4. That's the off-by-one handled deliberately.

>>> weekly = [1000, 1100, 1050, 1200]
... for i in range(len(weekly)):
...     print(f"Week {i + 1}: {weekly[i]}")
...     
Week 1: 1000
Week 2: 1100
Week 3: 1050
Week 4: 1200
>>> 

EXERCISE the bug hunt. Three broken snippets; retype each, run it, read the error, fix it, one sentence on the cause. This is deliberate: you make the bug so the traceback becomes familiar.

6 Bug hunt — retype, run, diagnose, fix, one sentence each:
   - a loop whose body forgets the indent
   - `for i in range(len(xs)):` used where `for x in xs:` was all that was needed (construct both, explain when the index form is actually required)
   - an off-by-one: printing weeks "1..n" from `range(n)`.


Bug 1 — the forgotten indent. Type this exactly (no indent on the print):

for x in [1, 2, 3]:
print(x)

prediction: Indentationerror
Exactly right. IndentationError: expected an indented block after 'for' statement — Python requires the body of a loop to be indented, and without it there's no "inside" to the loop. Your fix (indent the print) makes it run: 1, 2, 3. 


>>> for x in [1, 2, 3]:
... print(x)
... 
  File "<python-input-12>", line 2
    print(x)
    ^^^^^
IndentationError: expected an indented block after 'for' statement on line 1
>>> for x in [1, 2, 3]:
...     print(x)
...     
1
2
3
>>> 

Bug 2 — index loop where a plain loop was all you needed. This one doesn't crash; it's about style. First, the clumsy version — type and run:

First (the index form):

xs = ["a", "b", "c"]
for i in range(len(xs)):
    print(xs[i])


prediction:
a
b
c

COMMENT: 
Here, i takes the index values:

0
1
2

Then xs[i] uses each index to retrieve the corresponding element:

xs[0]   # "a"
xs[1]   # "b"
xs[2]   # "c"


Second (the plain form):

for x in xs:
    print(x)

prediction:
a
b
c

COMMENT:
The plain loop is more direct:

for x in xs:
    print(x)

Here, x receives each element itself:

x = "a"
x = "b"
x = "c"

So when you only need each value, the plain loop is cleaner because there is no reason to create an index and then use it merely to recover the value.
 


RUN:

>>> xs = ["a", "b", "c"]
... for i in range(len(xs)):
...     print(xs[i])
...     
a
b
c
>>> for x in xs:
...     print(x)
...     
a
b
c
>>> 

Both print a b c
QUESTION: a) when do you actually need the index form? Recall Exercise 4 — the diffs loop used range(1, len(volumes)) and reached volumes[i-1]. b) Could a plain for x in volumes have reached the previous element?

ANSWER: a) You need an index when the position of the element matters, especially when you must use that position to reach another element. b) Not by iteself. A plain loop could reach the previous element only if you stored that previous value yourself. The index loop is convenient because i lets you directly access both volumes[i] and volumes[i - 1].

Bug 3 — the off-by-one. Type and run:

n = 3
for week in range(n):
    print("Week", week)

PREDICTION:
Week 0
Week 1
Week 2

Correct

Two ways to fix it — pick one:

change what you print: print("Week", week + 1), or
change the range: range(1, n + 1) so it produces 1, 2, 3

Correction: 
n = 3
for week in range(n):


RUN:
>>> n = 3
... for week in range(n):
...     print("Week", week + 1)
...     
Week 1
Week 2
Week 3
>>> 
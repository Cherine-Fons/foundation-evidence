## Day 15 Quiz

1. When you first read edges.txt and printed each line, blank lines appeared between them. Why? What method removes the cause, and what does it strip?
2. "3,4".split(",") returns what — and what type are the two pieces? Why do you then wrap them in int(...) before using them as an edge?
3. What does try/except do? Write the skeleton (just the shape, with a comment in each block).
4. Your parser hit the row 5 (one field) and it caused an IndexError before you added try/except. Why IndexError specifically — what line failed and why?
5. The row 7,8,9 did not throw any error, yet it's a bad row. Explain what your parser did with it before you added the length check, and why try/except alone couldn't catch it. What class of bug is this (name the family)?
6. Why does if bad_rows: correctly skip the "Bad rows:" section when the file is clean? What is an empty list's truth value?
7. Predict the report for a file containing exactly these four rows:
0,1
x,2
3,4,5
2,3

Give: total rows, valid count, invalid count, and which rows are bad.
_____________________________________________________________________________________________________________

1. 
Each line read from the file already ended with a newline character \n, and print() added another newline of its own, so we saw an extra blank line between entries.

Use:

line.strip()

strip() removes whitespace from both ends of the string, including the trailing newline \n, spaces, and tabs.

2. 
"3,4".split(",")

returns:

["3", "4"]

Both pieces are strings (str), because .split() divides a string into smaller strings; it does not automatically convert them into numbers.

So before using them as integer vertex labels for an edge, we convert them:

u = int("3")
v = int("4")

giving:

u = 3
v = 4

and then:

edge = (u, v)   # (3, 4)

You need int(...) because "3" and 3 are different values: "3" is text, while 3 is an integer you can use as numeric vertex data.

4. 
The row "5" splits into only one piece:

parts = "5".split(",")
# ["5"]

Then a line such as:

v = int(parts[1])

fails with an IndexError because parts[1] asks for the second element, but the list contains only one element at index 0.

So the error means: the code tried to access a list position that does not exist.


5. 
Before the length check, the bad row 7,8,9 was reduced to:

["7", "8"]

The parser silently dropped the extra 9, then converted the remaining two strings into the edge (7, 8), so the row looked valid even though it was malformed. try/except could not catch it because no exception occurred—Python was able to process everything it was given.

This is a silent validation/logic bug: invalid input is accepted and turned into a plausible-looking result instead of causing an obvious failure.

6. 
if bad_rows: checks whether the list is truthy. A nonempty list is True, but an empty list [] is False, so when the file is clean and bad_rows stays empty, Python skips that whole section.

bad_rows = []

if bad_rows:
    print("Bad rows:")

Nothing prints because:

bool([])   # False

So the rule is: empty list = falsey; nonempty list = truthy.

SUPPLEMENTAL:

hink of if bad_rows: as Python asking:

“Does this list contain anything?”

If:

bad_rows = []

then the list is empty, so Python treats it like False and skips the block.

if bad_rows:
    print("Bad rows:")

Nothing prints.

But if:

bad_rows = ["7,8,9"]

then the list contains something, so Python treats it like True and runs:

print("Bad rows:")

So the simple rule is:

[]          # false
["bad row"] # true

if bad_rows: is basically shorthand for:

“If there is at least one bad row, run this section.”

7. 
The report will be:

=== Edge File Validation Report ===
Total rows read: 4
Valid edges:     2
Invalid rows:    2
Bad rows:
  - x,2
  - 3,4,5

Why:

0,1 → two fields, both convert to integers → valid edge (0, 1)
x,2 → two fields, but int("x") raises ValueError → bad row
3,4,5 → three fields, so len(parts) != 2 → you deliberately raise ValueError → bad row
2,3 → two fields, both integers → valid edge (2, 3)

So by the end:

good_edges == [(0, 1), (2, 3)]
bad_rows == ["x,2", "3,4,5"]
_______________________________________________________________________________________________________________

## KEY

7/7 — and this closes F3's teaching content on a strong note. Marking, with attention to the two that carry the real weight:

1. Correct — trailing \n plus print's own newline; .strip() removes leading/trailing whitespace including the newline. ✓

2. Correct — ["3", "4"], two strings, and int() because split always yields strings but graph work needs numbers. The "split always returns strings" point is the one people forget; you have it. ✓

3. Correct skeleton, both blocks commented. ✓

4. Correct — "5".split(",") → ["5"], one element, so parts[1] is out of range → IndexError. Precise. ✓

5. This is the one that matters most, and your answer is exactly right: the parser read parts[0] and parts[1], ignored the third field, built (7, 8), threw no error, and landed it in good edges. And you named the family correctly — silent failure / silent bad data: wrong result, no crash, try/except can't catch it because nothing was thrown. That's the whole point of the day, understood at the level of why validation must go beyond exception-catching. ✓✓

6. Correct — empty list is falsy, so if bad_rows: is False and skips the block. ✓

7. All correct: total 4, valid 2 (0,1 and 2,3), invalid 2 (x,2 → ValueError from int("x"); 3,4,5 → three fields, rejected by the length check). You even tagged which validation catches each bad row. ✓


Day 10 End-of-Day Quiz

1. s = set([4, 4, 5, 5, 5, 6]). Predict s and len(s). What does set() do to duplicates?
2. a = {1, 2, 3}, b = {2, 3, 4}. Predict a | b and a & b. Which is union, which is intersection?
3. t = (1, 2). Predict the error type for t[0] = 9. Why is a tuple allowed as a dict key but a list isn't?
4. (Copy vs reference.) Predict a after each:
a = [1, 2, 3] / b = a / b.append(4) → a is ?
a = [1, 2, 3] / c = a[:] / c.append(4) → a is ?
Explain the difference in one sentence.
5. (Shallow copy — the hard one.) outer = [[1, 2], [3, 4]] / copy = outer[:] / copy[0].append(9). Predict outer. Why does the "copy" still change?
6. (Aliasing trap.) row = [0, 0] / grid = [row, row, row] / grid[1][0] = 5. Predict grid. Why do all three rows change, and what one change fixes it?
7. x = 5, y = 9. Write the one-line swap. What are x and y after?
8. head, *rest = [1, 2, 3, 4, 5]. Predict head and rest.
9. s = {} — predict type(s). How do you make an actual empty set?
10. (Day-9 carry-forward.) pairs = [("x","odd"), ("y","even"), ("z","odd")]. Write the loop building type → list of letters. Result?

---------------------------------------------------------------------------------------------------------

1. 
s = set([4, 4, 5, 5, 5, 6])
s

(4 , 5, 6)

len(s)
3

2. 
a = {1, 2, 3}, b = {2, 3, 4}
a | b is {1,2,3,4} union
a & b is {2,3}  intersection

3. TypeError: 'tuple' object does not support item assignment
A tuple can be a dictionary key because it is immutable, so its contents stay stable after creation and Python can hash it reliably. A list is mutable—its contents can change—so it is unhashable and cannot be used as a dictionary key.

4. a = [1, 2, 3] / b = a / b.append(4) → a is ?
a = [1, 2, 3, 4]

a = [1, 2, 3] / c = a[:] / c.append(4) → a is ?
a = [1, 2, 3]

Difference: b = a creates another reference to the same list, while c = a[:] creates a separate shallow copy.

5. outer = [[1, 2], [3, 4]] / copy = outer[:] / copy[0].append(9). 
Predict outer. 

[[1, 2, 9], [3, 4]] 

outer[:] creates a new outer list, but it does not copy the inner lists. Both outer[0] and copy[0] still refer to the same inner list, so appending 9 through copy[0] changes the shared inner list seen by both.

6. row = [0, 0] / grid = [row, row, row] / grid[1][0] = 5. 
Predict grid.

[[5, 0], [5, 0], [5, 0]]

All three positions in grid refer to the same row list, not three separate copies. Changing grid[1][0] changes that one shared list, so the change appears in every row.

fix:
row = [0, 0]
grid = [row[:], row[:], row[:]]

7. 
x = 5
y = 9
x, y = y, x
x
y

Predict x and y after the swap line.

9
5

8. 
head = 1
rest = [2, 3, 4, 5]

9. <class 'dict'>
{} creates an empty dictionary, not a set. To create an empty set, use:
s = set()

10. 
pairs = [("x", "odd"), ("y", "even"), ("z", "odd")]

by_type = {}

for letter, letter_type in pairs:
    if letter_type not in by_type:
        by_type[letter_type] = [letter]
    else:
        by_type[letter_type].append(letter)

print(by_type)

output:

{'odd': ['x', 'z'], 'even': ['y']}

---------------------------------------------------------------------------------------------------------------------
KEY:

10/10 — and every single reference/aliasing question is clean, which is exactly what tomorrow's capstone needs. Marking:

1. Correct — {4, 5, 6}, len 3, dedup explained. One tiny notation thing (not an error): a set displays with curly braces {4, 5, 6}, not parentheses (4, 5, 6) — parens would be a tuple. Your value and count are right; just the bracket style in how you wrote it. ✓

2. Correct — union {1,2,3,4}, intersection {2,3}, both labeled right. ✓

3. Correct, and the hashability explanation is precise — immutable → stable → hashable → usable as key. ✓

4. Both correct — b = a shares (a becomes [1,2,3,4]), c = a[:] is independent (a stays [1,2,3]), difference stated cleanly. ✓

5. Correct — [[1, 2, 9], [3, 4]], and your explanation nails the shallow-copy mechanism: new outer list, shared inner lists. ✓✓

6. Correct — all three rows [5, 0], the "same row list referenced three times" reasoning is right, and your fix (row[:] for each) is right. ✓✓

7. Correct — x=9, y=5. ✓

8. Correct — head=1, rest=[2,3,4,5]. ✓

9. Correct — {} is dict, set() for empty set. ✓

10. Grouping pattern cold, correct — {'odd': ['x', 'z'], 'even': ['y']}. The Day-9 carry-forward is still locked. ✓

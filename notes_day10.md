Day 10 Warm-Up (accumulation pattern)

1. words = ["hi", "bye", "hi", "hi"]. Write the loop that counts each word into a dict. What's the result, and trace counts after the first two words.
2. pairs = [("a", "vowel"), ("b", "consonant"), ("e", "vowel")]. Write the loop that builds a dict of type → list of letters. What's the result?



1. 
words = ["hi", "bye", "hi", "hi"]
counts = {}
for word in words:
    if word not in counts:
        counts[word] = 1
    else:
        counts[word] = counts[word] + 1
print(counts)

Trace:
{'hi': 1}
{'hi': 1 , 'bye': 1}
{'hi': 2, 'bye': 1}
{'hi': 3, 'bye': 1}

2. 
pairs = [("a", "vowel"), ("b", "consonant"), ("e", "vowel")]
by_type = {}
for letter, letter_type in pairs:
    if letter_type not in by_type:
        by_type[letter_type] = [letter]
    else:
        by_type[letter_type].append(letter)

print(by_type)

{'vowel': ['a', 'e'], 'consonant': ['b']}
------------------------------------------------------------------------------------------------------------------------

## Day 10 (Fri Jul 31) — Sets, tuples, copy vs reference — ~3.5 h · commits `f2d4:`
*Read: Primer Ch 3 (sets, tuples, copy/mutability sections). [Primer Ch 3 Review Q1, Q4; slides "Copy vs reference"]*

1. Sets: build one from a list with duplicates; *[predict]* the length; `in` membership; add; union and intersection of two small sets. Primer Ch 3 Review Q4: write your own example of a task a set makes trivial that a list makes clumsy (deduplicating vertices touched in a session log is a fine choice).
2. Tuples: build one; *[predict]* what happens on item assignment (name the error type first). One sentence per Ch 3 Review Q1: one situation each where you'd prefer a tuple / a list. Tuples as dict keys: a dict keyed by `(a, b)` pairs — store one value under a pair key and read it back. Note in `notes_day10.md` why a list can't do that job.
3. **Copy vs reference, the drill of the week** *[predict all before running]*: `a = [1, 2, 3]` · `b = a` · `b.append(4)` · what is `a`? Then `c = a[:]` · `c.append(5)` · what is `a`? Then the same experiment where the list holds an inner list and you copy with `[:]` — mutate the inner list through the copy and see what the "copy" shares. Three written sentences reconciling all of it (Ch 3 Review Q3 answered for real).
4. Unpacking: `head, *rest = nums` (slides Ch 3 snippet, retyped); swap two variables in one line; unpack `(a, b)` pairs in a `for` over `.items()`.
5. Bug hunt — retype, run, fix, one sentence each:
   - a function that "resets" a list parameter with `xs = []` and surprises its caller by changing nothing
   - a dict built in a loop where every key gets the *same* list object appended to (the aliasing trap inside the accumulation pattern)
   - `s = {}` believed to be an empty set — check `type(s)` and fix.

**Done when:** you can explain, without notes, why `b = a` is not a copy, what `a[:]` does and doesn't copy, and when a tuple is the right key.

------------------------------------------------------------------------------------------------------------------------
EXERCISE 1 sets

A set is a collection with no duplicates and no order. Its whole job: hold unique things. Where a list keeps everything you put in (including repeats) in order, a set silently collapses duplicates and doesn't track position.

In >>>, build one from a list that has duplicates:

nums = [1, 2, 2, 3, 3, 3, 4]
s = set(nums)

set(...) converts a list to a set, dropping duplicates as it goes. 
Predict: the list has 7 elements — how many does the set have? 4
What values survive? 1, 2, 3, 4

run:
s 
{1, 2, 3, 4}

len(s)
4

2 in s
True

5 in s
False

s.add(5)
nothing

s
{1, 2, 3, 4, 5}

2 in s / 5 in s — membership, True/False. Fast on sets (that's their other advantage).
s.add(5) — adds an element (sets use .add, not .append).
final s — what's in it now

— union and intersection, combining two sets.
a | b — union: everything in either set (duplicates collapsed, so 3 appears once).
a & b — intersection: only what's in both sets.
Predict each:
a = {1, 2, 3}       
b = {3, 4, 5}
a | b       {1, 2, 3, 4, 5}
a & b       {3}

>>> a = {1, 2, 3}       
>>> 
>>> b = {3, 4, 5}
>>> a | b
{1, 2, 3, 4, 5}
>>> a & b
{3}
>>> 
-----------------------------------------------------------------------------------------------------------------------
EXERCISE 2 tuples 

A tuple is like a list, but immutable: once made, you can't change its contents. That one property is the whole point, and it's what lets tuples do a job lists can't.

Build it:
point = (3, 4)
point[0]
point[0] = 5

(3, 4) — round brackets make a tuple (vs. square for a list).
point[0] — indexing works just like a list.
point[0] = 5 — trying to change an element. Predict the error type first: you've met one for missing dict keys (KeyError), one for out-of-range... this is "you tried to modify something that can't be modified." Take your best guess at the name.

Prediction:
point[0]
3

point[0] = 5
SyntaxError

>>> point = (3,4)
>>> point[0]
3
>>> point[0] = 5
Traceback (most recent call last):
  File "<python-input-89>", line 1, in <module>
    point[0] = 5
    ~~~~~^^^
TypeError: 'tuple' object does not support item assignment
>>> 

Note: 
A SyntaxError means the code is malformed — Python can't even understand it (like your missing colon). It's caught before running.
A TypeError means the code is valid Python, but you asked an object to do something its type doesn't allow.

So the tell: assignment-to-an-element is legal syntax, so a failure there is about the object's type/behavior (TypeError), not malformed code (SyntaxError). point[0] returned 3 correctly — reading is fine; only writing is blocked.

Why immutability matters: tuples can be dict keys, lists can't. 
Predict each:
d = {}
d[(0, 1)] = "edge A"
d[(1, 2)] = "edge B"
d[(0, 1)]

prediction: 'edge A'

try
d[[0, 1]] = "nope"
 prediction = Type Error

 >>> d = {}
>>> 
>>> d = {}
>>> d[(0,1)] = "edge A"
>>> d[(1,2)] = "edge B"
>>> d[(0,1)]
'edge A'
>>> d[[0, 1]] = "nope"
Traceback (most recent call last):
  File "<python-input-96>", line 1, in <module>
    d[[0, 1]] = "nope"
    ~^^^^^^^^
TypeError: cannot use 'list' as a dict key (unhashable type: 'list')
>>> 

The word to notice is unhashable. The short version of why: dicts need keys that are guaranteed stable — if a key could change after you stored something under it, the dict couldn't find it again. Tuples are immutable, so they're stable → usable as keys. Lists can change, so they're forbidden. You don't need the full mechanism now; the rule is: immutable things (tuples) can be keys; mutable things (lists) can't.

This connects straight to your capstone: your multigraph edges will be (u, v) tuples, and you'll key a dict by those pairs — exactly what you just did with (0, 1) → "edge A". That's not a coincidence; it's why the sheet drills tuples now.

Conclusion:
Use a tuple for a fixed pair such as an edge (0, 1) that should not change, and use a list when you need a collection you may add to, remove from, or modify. A list cannot be a dictionary key because it is mutable, so its contents—and therefore its identity for lookup—could change; dictionary keys must be hashable and stable.
-----------------------------------------------------------------------------------------------------------------------
EXERCISE 3 copy vs reference

The one idea up front: b = a does not copy a list — it makes a second name for the same list. One list, two labels. Change it through either name and both names see it, because there's only one underlying list.

prove it:
a = [1, 2, 3]
b = a
b.append(4)
a

The key prediction: b.append(4) adds to the list through b. What is a afterward — still [1, 2, 3], or [1, 2, 3, 4]? (If b were a real copy, a would be untouched. If b is just another name for the same list, a changes too.)

Predict what a prints, run all four lines:
[1, 2, 3, 4]

>>> a = [1, 2, 3]
... b = a
... b.append(4)
... a
... 
[1, 2, 3, 4]
>>> 

This is the thing that surprises people and causes silent bugs: you think you have two independent lists, you modify one, and the "other" changes too — because they were never separate.

Now the fix — how to make a real copy. Predict this block:

c = a[:]
c.append(5)
a

a[:] is a full slice — and a slice, as you learned on Day 7, returns a new list. So c is a genuine copy, independent of a. Then c.append(5) changes only c.

The key prediction: after appending 5 to c, what is a? Does it stay [1, 2, 3, 4], or become [1, 2, 3, 4, 5]? (Contrast with what just happened — this time it's a real copy.)

Predict a, run all three lines:
[1, 2, 3, 4]

but running c gives:
[1, 2, 3, 4, 5]

>>> c = a[:]
... c.append(5)
... a
... 
[1, 2, 3, 4]
>>> c
[1, 2, 3, 4, 5]
>>> 
Exactly right, and you tested it the smart way — checking both a and c to see they diverged. a stayed [1, 2, 3, 4] (untouched), while c became [1, 2, 3, 4, 5]. This time they're independent, because a[:] made a real copy — a separate list. Appending to c couldn't touch a.

So the contrast, side by side:

b = a → same list, two names. Change one, both change.
c = a[:] → new independent list. Change one, the other is safe.

That's the whole distinction, and it's the drill's core. But there's a sting in the tail — a case where a[:] looks like a copy but isn't fully. Predict this carefully:

outer = [[1, 2], [3, 4]]
copy = outer[:]
copy[0].append(99)
outer

Here outer is a list containing lists. outer[:] copies the outer list — but the inner lists are still shared (the copy holds references to the same inner lists). So copy[0] and outer[0] are the same inner list.

The key prediction: copy[0].append(99) appends to the inner list at position 0. Does outer change? Look at outer[0] — is it still [1, 2], or [1, 2, 99]?

Predict what outer prints, run.

>>> outer = [[1,2],[3,4]]
>>> copy = outer[:]
>>> copy[0].append(99)
>>> outer
[[1, 2, 99], [3, 4]]

outer[:] copied the outer list — so outer and copy are different outer lists. But the copy didn't reach inside: both outer lists still hold references to the same two inner lists. So copy[0] and outer[0] are literally the same inner list [1, 2]. Append 99 through one name, both see it.

Contrast with the earlier flat case: c = a[:] gave you a fully independent copy because the elements were plain numbers — numbers can't be shared-and-mutated the way lists can. The moment your list contains other lists (or dicts), [:] only copies the top layer. This is called a shallow copy: one level deep, shared underneath.

Why this matters for you specifically: your accumulation pattern builds dicts whose values are lists. If you ever copy such a structure with [:] and then mutate an inner list, you can silently corrupt the "original." It's the exact bug family the sheet's Day-10 bug hunt (Exercise 5) makes you trigger on purpose — the "same list object appended to every key" trap.

Conclusion:

b = a does not make a copy; a and b refer to the same list, and appending through b changes a too, proving they share one object.

c = a[:] makes a new outer list, so appending 5 to c does not change the original flat list a.

For a nested list, outer[:] still copies only the outer list; the inner lists remain shared, so changing an inner list through the copy also changes what appears inside the original.
----------------------------------------------------------------------------------------------------------------------
EXERCISE 4 unpacking

Three quick moves, all about pulling values out of collections into separate variables.

First, star-unpacking. Predict, run in >>>:

nums = [10, 20, 30, 40]
head, *rest = nums
head
rest

head, *rest = nums splits the list: head grabs the first element, and *rest (the star) scoops up everything else into a list. So head = 10, rest = [20, 30, 40].

Predict what head and rest each hold, run.

>>> nums = [10, 20, 30, 40]
... head, *rest = nums
... head
... rest
... 
[20, 30, 40]
>>> head
10

Now the other two unpacking moves. Predict each, then run:

Swap:

x = 1
y = 2
x, y = y, x
x
y

Predict x and y after the swap line.

2
1


Pair unpacking in a loop:

pairs = [(1, "a"), (2, "b")]
for num, letter in pairs:
    print(num, letter)

Predict the two printed lines.

1 a 
2 b

>>> pairs = [(1, "a"), (2, "b")]
... for num, letter in pairs:
...     print(num, letter)
...     
1 a
2 b
>>> 


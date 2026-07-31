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
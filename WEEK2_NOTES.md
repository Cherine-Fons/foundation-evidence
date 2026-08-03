Week 2 self-quiz — 10 questions, own words, no references. Answer in WEEK2_NOTES.md. Where a question asks for code, write it out. Predict any outputs before checking.

Week 2 Self-Quiz

1. for vs while — when is each the honest choice?
2. What does range(2, 12, 3) produce, and what type is range(3) before you list() it?
3. List vs tuple — one preference situation each, and which can key a dict, and why?
4. Why is b = a not a copy? What does a[:] copy, and what does it not copy?
5. What does enumerate yield per step? What does zip do with unequal-length lists?
6. The accumulation pattern: what are its two cases, and where did you use it twice this week?
7. Dict lookup vs scanning a list — why does the difference matter?
8. What error do you get from a missing dict key, and what are two ways to handle it?
9. {} — set or dict? How do you get the other one?
10. In Capstone B, why must the degree-counting convention be written as a comment before the code?
-------------------------------------------------------------------------------------------------------------------

1. 
Use a for loop when you already have a collection or sequence to move through:
e.g:
for value in values:
    print(value)

Use a while loop when repetition should continue until a condition changes, and you do not necessarily know the number of passes beforehand:

e.g:
while total < cap:
    total = total + 1

The rule is:

Use for when you know what you are looping over; use while when you know the condition that must remain true.

A while loop also requires you to update something that can eventually make its condition false—or you create an infinite loop.

2. 
range(2, 12, 3) starts at `2`, adds `3` each time, and stops before `12`, so:
work from the inside outward:

range(2, 12, 3) means start at 2, increase by 3 each time, and stop before 12.
It generates the values 2, 5, 8, 11.
list(...) collects those values into a list.

Result:

[2, 5, 8, 11]

so
list(range(2, 12, 3))
# [2, 5, 8, 11]

Before you apply `list()`, `range(3)` is a **`range` object**:

type(range(3))
# <class 'range'>

At the REPL, it displays as:
range(0, 3)

It represents `0, 1, 2`, but it is not yet a list.

3. 
Use a list when the collection may change, such as adding exercises to a workout:

e.g:
exercises = ["squat", "bench"]
exercises.append("deadlift")

Use a tuple for fixed data that should not change, such as an edge:

edge = (0, 1)

A tuple can be a dictionary key because it is immutable and therefore hashable, provided everything inside it is also hashable. A list cannot be a dictionary key because it is mutable—its contents could change after Python has used it for lookup.

4. 
**b = a is not a copy because it gives the same list object a second name:**

a = [1, 2, 3]
b = a
b.append(4)

print(a)  # [1, 2, 3, 4]

**Appending through b changes a because both variables point to the same list.**

a[:] creates a new outer list containing the same elements:

a = [1, 2, 3]
c = a[:]
c.append(4)

print(a)  # [1, 2, 3]
print(c)  # [1, 2, 3, 4]

**But slicing is only a shallow copy. If the list contains inner lists, those inner lists are still shared:**

a = [[1, 2], [3, 4]]
c = a[:]

c[0].append(9)

print(a)  # [[1, 2, 9], [3, 4]]

So the rule is: b = a copies only the reference; a[:] copies the outer list, but not mutable objects nested inside it.

5. 
**enumerate yields two things on each pass: the index and the item.**
e.g:
names = ["a", "b", "c"]

for i, name in enumerate(names):
    print(i, name)

It yields:

(0, "a")
(1, "b")
(2, "c")

**zip pairs items by position and stops when the shorter list runs out:**

a = [1, 2, 3]
b = [10, 20]

list(zip(a, b))

produces:

[(1, 10), (2, 20)]

The extra 3 is silently ignored.

6. The accumulation pattern has two cases: if the key is new, create it with a starting value; if the key already exists, update what is already stored there. I used it on day 7. 

7. A dictionary lookup goes straight to the value for a key:

e.g:

prices["apple"]

Scanning a list checks items one by one until it finds a match:

for item in prices:
    if item[0] == "apple":
        ...

The difference matters because dictionary lookup is usually much faster—roughly constant time—while list scanning takes longer as the list grows. For tiny data, either works; for large data or repeated lookups, the dictionary is the honest structure because it expresses “find this key” directly and avoids rechecking unrelated items.

8. A missing dictionary key raises a KeyError. We can handle it by using d.get(key) or d.get(key, default), or by checking if key in d: before using d[key]

9. {} creates an empty dictionary.

s = {}
type(s)   # <class 'dict'>

To create an empty set, use:

s = set()
type(s)   # <class 'set'>

10. The comment states the mathematical convention the code is implementing, so a later reader can verify that incrementing both u and v for every edge is intentional and that the resulting degree counts are trustworthy.


-----------------------------------------------------------------------------------------------------------------------
10/10 — and this is a fitting close to the week. This is the written companion to the capstone, and it shows the concepts are genuinely internalized, not memorized. Marking the ones that carry weight:

1. Correct, and your closing formulation is the sharp one: "use for when you know what you're looping over; use while when you know the condition that must remain true." That's the honest distinction. ✓

2. Correct — [2, 5, 8, 11] (11 included because it's before the stop of 12), and range(3) is a range object displaying as range(0, 3), not yet a list. ✓

3. Correct, and you added the precise caveat most people miss — a tuple is hashable "provided everything inside it is also hashable." That's the exact condition. ✓✓

4. Fully correct with all three levels: b = a copies the reference, a[:] copies the outer list, and the shallow-copy sting (nested lists stay shared). Worked examples for each. This was the hardest concept in F2 and your note is complete. ✓✓

5. Correct — enumerate yields (index, item), zip pairs by position and silently drops the extra. ✓

6. Correct on the two cases, but thin on the second half. You wrote "I used it on day 7" — but the accumulation pattern isn't the Day-7 running total; it's the dict-building pattern from Day 9, and the question asks where you used it twice. The two places: the grouping form (type → list of items) and the counting form (item → count), both on Day 9 — and a third time in today's capstone (the degree tally). Go back and fix this one answer: name the two Day-9 uses (grouping and counting) plus the capstone degree tally. The pattern is clearly locked in your code; the note just under-credits where it appeared. ⚠️

7. Correct, and "the dictionary is the honest structure because it expresses 'find this key' directly" is exactly right — it's about intent and speed. ✓

8. Correct — KeyError, and both handling routes (.get with/without default, or in check). ✓

9. Correct — {} is dict, set() for the empty set. ✓

10. Correct — the comment records the convention so a later reader can trust the count is intentional, not accidental. ✓

So: 10/10 on substance, with Q6 needing one fix — expand it to name the grouping and counting forms (Day 9) and the capstone degree tally as the "twice" (really three times). Do that edit, then this is complete.


FIX:

The accumulation pattern appeared in both forms on Day 9:

Grouping form — for ticker, sector in pairs: building a dict of sector → list of tickers. New key: start a fresh list [ticker]. Seen key: .append(ticker) to the existing list.
Counting form — for food in foods: building a dict of food → count. New key: set to 1. Seen key: count + 1.

And a third time today: the capstone degree tally — for u, v in edges: counting each vertex's degree, the counting form run twice per edge.

So the "twice this week" the question asks about is the grouping and counting versions on Day 9 (with the capstone as a third).


In my own words:

The accumulation pattern showed up in two main ways on Day 9. In the grouping version, I built a dictionary where each sector stored a list of tickers: a new sector started with [ticker], and an existing sector had the next ticker appended to its list. In the counting version, I built a dictionary where each food stored a count: a new food started at 1, and a repeated food had its count increased by 1.

I used the same counting pattern again in the capstone degree tally, except each edge updated two vertices, so the counting logic ran once for u and once for v. The “twice this week” refers to the grouping and counting versions from Day 9, with the degree tally as a third use.


REFLECTION:
I would like to drill the programs we wrote this week. No confusion:
writing the accumulation pattern cold, the index-looprange(1, len(...)) with i-1, initializing the accumulator outside the loop are good things to drill. 
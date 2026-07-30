Day 9 End-of-Day Quiz

1. d = {"cat": 3, "dog": 5}. Predict each: d["cat"] · d["bird"] · d.get("bird") · d.get("bird", 0). Name the error type the second one raises.
2. d = {"cat": 3, "dog": 5}. Predict True/False: "cat" in d · "bird" in d · 3 in d. Does in test keys or values?
3. .keys(), .values(), .items() — what does each give you? Which one yields pairs, and how many variables does for _ , _ in d.items() need?
4. (The accumulation pattern — grouping.) Given pairs = [("dog","pet"), ("lion","wild"), ("cat","pet")], write from scratch the loop that builds a dict of type → list of animals. State the two cases and what each does.
5. (The accumulation pattern — counting.) Given letters = ["a","b","a","c","a","b"], write the loop that counts each letter. What's the result dict? Hand-trace counts after the first three letters.
6. In the counting loop, when you hit a letter you've seen before, why does counts[letter] = counts[letter] + 1 work — read the right side first: what is counts[letter] on the right before the assignment?
7. Nested lookup: data = {"apple": {"color": "red", "sizes": [2, 4, 6]}}. Predict data["apple"]["color"] and data["apple"]["sizes"][-1]. What does each bracket in the chain do?
8. Merge sequencing: you merge two dicts by summing, then drop zeros. Why must the zero-drop be a separate final pass rather than done during the merge? Give the one-sentence reason.
9. (Day-8 carry-forward.) nums = [5, 5, 8, 8], total = 0, loop adding each with if total + n > 20: break. What are the printed totals, and does it break?


Answers:
1. 3
   KeyError
   None
   0

2. True
False
False
Tests only Keys

3. Given:

d = {"cat": 3, "dog": 5}
d.keys() gives the dictionary’s keys:
dict_keys(['cat', 'dog'])

d.values() gives the dictionary’s values:
dict_values([3, 5])

d.items() gives key-value pairs:
dict_items([('cat', 3), ('dog', 5)])

Because .items() yields two-part pairs, the loop needs two variables:

for animal, number in d.items():
    print(animal, number)

Output:

cat 3
dog 5

On each pass, the first variable receives the key and the second receives its value.

4. 
pairs = [("dog", "pet"), ("lion", "wild"), ("cat", "pet")]

by_type = {}

for animal, animal_type in pairs:
    if animal_type not in by_type:
        by_type[animal_type] = [animal]
    else:
        by_type[animal_type].append(animal)

print(by_type)

The two cases are:

**The type is not yet in the dictionary: create the key and start a new list containing the animal.
by_type[animal_type] = [animal]
**The type is already in the dictionary: append the animal to the list that already exists.
by_type[animal_type].append(animal)

5. 
letters = ["a","b","a","c","a","b"]
counts = {}
for letter in letters:
    if letter not in counts:
        counts[letter] = 1
    else:
        counts[letter] = counts[letter] + 1
print(counts)


Output:
{'a': 3, 'b': 2, 'c': 1}

Hand-trace of first three letters:
{'a': 1}
{'a': 1, 'b': 1}
{'a': 2, 'b': 1}

6. Python evaluates the right side first:

counts[letter] = counts[letter] + 1

Suppose letter is "a" and the dictionary currently contains:

counts = {"a": 2, "b": 1}

Then the right side:

counts[letter] + 1

becomes:

counts["a"] + 1
2 + 1
3

Only after calculating 3 does Python assign it back to the same dictionary entry:

counts["a"] = 3

So counts[letter] on the right is the existing count before the update. The line reads: “Look up this letter’s current count, add one, and replace the old count with the new count.”

7. data["apple"]["color"]
"red"

["apple"]["sizes"][-1]
6
Each bracket acts on the value produced by everything immediately to its left.

8. The zero-drop must happen after the merge because a quantity that is zero partway through could change when later values are added, so only the final combined total should decide whether the key is removed.

9. The printed totals are:

5
10
18

Pass by pass:

0 + 5 = 5    → add and print 5
5 + 5 = 10   → add and print 10
10 + 8 = 18  → add and print 18
18 + 8 = 26  → exceeds 20, so break

Yes, it breaks on the fourth element. That final 8 is not added, so the final total remains 18.

Correction:

1. All four correct, KeyError named. ✓
2. All correct, "tests only keys" — including 3 in d being False (3 is a value, not a key). ✓
3. Correct, and you noted the pairs come as ('cat', 3) tuples and need two variables to unpack. ✓
4. Grouping pattern, cold, correct — both cases stated precisely (new → fresh [animal] list, seen → append). ✓
5. Counting pattern correct, and the three-step hand-trace is right: {'a':1} → {'a':1,'b':1} → {'a':2,'b':1}. Crucially, on step 3 the b count stayed at 1 while a incremented — that's the "untouched keys stay put" rule you slipped on yesterday, now handled clean. ✓
6. This is the standout. You explained right-side-first evaluation with a worked example, and nailed the key insight: counts[letter] on the right is the existing count before the update. That's genuine understanding of assignment semantics, not memorization. ✓✓
7. Both correct — "red" and 6 — and "each bracket acts on the value produced by everything to its left" is exactly the chained-lookup mental model. ✓
8. The sequencing reason, stated in one clean sentence. ✓
9. Correct — 5, 10, 18, breaks on the fourth element, final 8 not added. The check-before-adding order and the Day-8 carry-forward both held. ✓
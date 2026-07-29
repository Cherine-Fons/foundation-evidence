Day 8 End-of-Day Quiz

1. Predict exactly: n = 4 / while n > 0: /     print(n) /     n = n - 2. What prints, and how many passes?
2. What single change turns a working while loop into an infinite one? What's the one keystroke that stops a runaway loop?
3. break vs continue — one sentence each. For for x in [1,2,3,4]: with if x == 2: continue then print(x) — what prints? Then swap continue for break — what prints now?
4. readings = [10, 20, None, 30], loop with if r is None: break then print(r). What prints? Why does 30 never appear? And why is None, not == None?
5. enumerate: predict for i, x in enumerate(["a","b","c"], start=1): print(i, x). What does enumerate yield each pass, and why does the for need two variables?
6. zip: a = [1,2,3,4], b = [10,20]. Predict every line of for x, y in zip(a,b): print(x, y). How many lines, and what happened to a's extra elements? Why is that silence a risk?
7. Accumulator + break: vals = [3, 3, 3, 3], cap = 8, total = 0. Loop: if total + v > cap: break else add and print total. What are the printed totals, and at which element does it stop?
8. (Day-7 carry-forward.) nums = [40, 55, 50, 70]. Write the index loop that builds the list of day-over-day absolute differences. What range do you loop over, and what does it produce? Read these values.



Answers:

1. n=4
   while n > 0:
       print(n)
       n = n - 2

prediction:
Pass 1: is 4 > 0? yes → print 4 → n becomes 2
Pass 2: is 2 > 0? yes → print 2 → n becomes 0
Pass 3: is 0 > 0? no → stop  

2. leaving n = n - 2 out will cause an infinite loop and Ctrl + C stops it.
3. break exits the loop immediately — jumps out entirely, skips any remaining passes.
continue skips the rest of the current pass and jumps to the next one — the loop keeps going.
for x in [1, 2, 3, 4]:
    if x == 2:
        continue
    print(x)

1
3
4

for x in [1, 2, 3, 4]:
    if x == 2:
        break
    print(x)

 1   

 4. readings = [10, 20, None, 30]

for r in readings:
    if r is None:
        break
    print(r)


what prints? 
10
20

30 never appears because when the loop reaches None, the condition becomes true (r is None). break immediately exits the entire loop, so Python never continues to the next item, 30.
Also, we use:

r is None

rather than:

r == None

because None is a unique special object, and is checks whether r is that exact object. == asks whether two values are equal, which is a different kind of test and can be affected by custom equality rules.

So the standard Python rule is:

if r is None:

and:

if r is not None:

5. exercises = ["a", "b", "c"]

   for i, x in enumerate(exercises, start=1):
       print(i, x)

predicition:
on each pass, enumerate yields two values
(1, "a")
(2, "b")
(3, "c")

The loop needs two variables because those two values are unpacked separately:

i receives the number.
x receives the exercise.

6. a = [1, 2, 3, 4]
   b = [10, 20]

   for x, y in zip(a, b):
       print(x, y)


output:
1 10
2 20

There are 2 lines because zip(a, b) stops as soon as the shorter list, b, runs out of elements. The extra values 3 and 4 in a are silently ignored.

That silence is risky because Python gives no error or warning, so missing or mismatched data can disappear without you noticing.

7. 
vals = [3, 3, 3, 3]
cap = 8
total = 0

for v in vals:
    if total + v > cap:
        break

    total = total + v
    print(total)

prediction:
3
6   

First 3:  0 + 3 = 3   → add it, print 3
Second 3: 3 + 3 = 6   → add it, print 6
Third 3:  6 + 3 = 9   → exceeds cap 8, so break

8. 
nums = [40, 55, 50, 70]
gaps = []

for i in range(1, len(nums)):
    diff = abs(nums[i] - nums[i - 1])
    gaps.append(diff)

print(gaps)

we loops over :
range(1, len(nums)) which is range(1, 4)
i takes values 1, 2, 3
Read each pass:
i = 1: abs(55 - 40) = 15
i = 2: abs(50 - 55) = 5
i = 3: abs(70 - 50) = 20

output:
[15, 5, 20]


CORRECTION:

Full marks — 8/8, and this one's cleaner than yesterday's. Marking each:

1. Correct — 4, 2, three condition-checks but two prints (the third check fails). You traced the check-then-print order perfectly, including the final 0 > 0 → stop. ✓

2. Correct — remove the update line, Ctrl+C stops it. ✓

3. Both correct. continue → 1, 3, 4 (skips 2, keeps going); break → 1 (stops at 2 entirely). You've got the distinction cold. ✓

4. Correct, and your is vs == explanation is genuinely good — "None is a unique special object, is checks exact-object identity" is exactly right, and you even noted == can be affected by custom equality rules, which is the real reason the idiom exists. That's beyond what I taught you; nice. ✓✓

5. Correct — yields the pair, two variables unpack it, start=1 gives 1/2/3. ✓

6. Correct — two lines, extras silently dropped, and you named the risk precisely (no error, data disappears unnoticed). ✓

7. Correct — 3, 6, breaks at the third element when 6 + 3 = 9 > 8. Check-before-adding order handled right. ✓

8. Correct, cold, and you read the given list this time — 15, 5, 20 from [40, 55, 50, 70], not autofilled from a remembered example. That was the exact habit flagged yesterday, and it's fixed. ✓


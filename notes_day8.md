**Day 8 Warm-Up (index loops from yesterday)**

1. nums = [5, 12, 8, 20]. Write the loop that builds gaps, the list of day-over-day absolute differences. Then say what range you loop over and why it starts where it does.
For that same nums, what does nums[i] - nums[i-1] equal when i = 3? Give the two elements you're subtracting and the result. Read the list above — use those exact values.
2. data = [100, 100, 100]. Predict exactly what gaps (the absolute-differences list) contains after the loop runs. How many elements, and what are they?


1) We are building a new list called gaps. The goal to compare each number with the number before it. We do not compare 5 with anything because it is the first value and has no previous value. 

**STEP 1**
Create the original list: 
nums = [5, 12, 8, 20]

The indexes (positions) are 0 that has value 5, 1 that has value 12, 2 that has value 8 and 3 that has value 20.

**STEP 2**
Create an empty result list:
gaps = []

This is where we will store each absolute difference.

**STEP 3**
Choose the indexes for the loop:
for i in range(1, len(nums)):

So len(nums) is 4, therefore range(1, 4) which gives 1,2,3. I loop over range(1, len(nums)) because each calculation compares the current number with the number immediately before it. The loop starts at index 1 because index 0 is the first item and has no previous item to compare with; starting at 0 would incorrectly use index -1, then nums[i - 1] which is nums[-1], which refers to the last item in the list.

**STEP 4**
Calculate each absolute difference. Inside the loop we write:
diff = abs(nums[i] - nums[i-1])

So the loop works like this:
i = 1: abs(nums[1] - nums[0]) = abs(12 - 5)  = 7
i = 2: abs(nums[2] - nums[1]) = abs(8 - 12)  = 4
i = 3: abs(nums[3] - nums[2]) = abs(20 - 8)  = 12

**STEP5**
Add each result to gaps:
gaps.append(diff)

So after each pass this is what we get:
After i = 1: gaps = [7]
After i = 2: gaps = [7, 4]
After i = 3: gaps = [7, 4, 12]

Complete program:

nums = [5, 12, 8, 20]
gaps = []
for i in range(1, len(nums)):
    diff = abs(nums[i] - nums[i-1])
    gaps.append(diff)
print(gaps)

2) data = [100, 100, 100]
   gaps = []
   for i in range(1, len(data)):
       diff = abs(date[i] - data[i-1])
       gaps.append(diff)
   print(gaps)

The loop runs for i = 1 and i = 2
i = 1: abs(data[1] - data[0]) = abs(100 - 100) = 0
i = 2: abs(data[2] - data[1]) = abs(100 - 100) = 0

I predict that gap contains: 
   [0,0]    


## Day 8 (Wed Jul 29) — `while`, `break`/`continue`, `enumerate`, `zip` — ~3.5 h · commits `f2d2:`
*Read: Primer Ch 4 (iteration + loop-control sections). [Primer Ch 4 Review Q1–Q2; Ch 4 Simple Ex 1–3; Ch 4 Advanced Ex 2]*

1. *[predict]* warm-ups: a `while` counting down from 3 · the same loop with the update line missing (predict, then Ctrl+C when it proves you right) · `break` on a matched value · `continue` skipping odd numbers.
2. Primer Ch 4 Simple Ex 1, gym edition: loop over a list of daily training loads and print a flag line for any load whose deviation from a target exceeds a threshold you set.
3. Primer Ch 4 Simple Ex 2: read values from a list until a sentinel (`None`) appears, then stop. One sentence: `for`-with-`break` vs `while` — which did you choose and why (Ch 4 Review Q1).
4. Primer Ch 4 Simple Ex 3: `enumerate` over a list of exercise names, printing index and value; then the same starting at 1. *[predict]* what `enumerate` yields — the pair, not the value.
5. `zip` two lists (exercise names, weights) and print combined lines. *[predict]* what happens when the lists have unequal lengths — check yourself, write the answer down.
6. Primer Ch 4 Advanced Ex 2, gym edition: process a list of planned lifts and stop early the moment cumulative tonnage would breach a cap you define in a comment first.


1. EXERCISE 1  while loops. A 'for' loop runs a known number of times (once per item). A while loop runs as long as a condition stays true — you don't necessarily know in advance how many passes that'll be. That's the distinction the whole day builds on.

First one: a countdown from 3. In the >>> tab, type:

n = 3
while n > 0:
    print(n)
    n = n - 1

Three things to see before you run it: 
while n > 0: checks the condition before each pass — when it's false, the loop stops. n = n - 1 is what moves n toward the exit; without it the condition would never become false. The colon and indent are the same rules as for.
n = n - 1 decreases n by 1 each pass. The loop keeps going while n > 0 is true. So each time you subtract 1, n gets closer to 0 — and once it reaches 0, the condition n > 0 becomes false, and the loop stops. That stopping is "the exit."
The point: n = n - 1 is the line that makes the loop eventually end. Without it, n would stay 3 forever, n > 0 would always be true, and the loop would never stop.

prediction:
2
1

after running in python interpreter:
>>> n=3
>>> while n > 0:
...     print(n)
...     n = n - 1
...     
3
2
1
>>> 
CONCLUSION:
The loop checks n > 0 first, then runs the body. On the very first pass n is still 3, and 3 > 0 is true, so it prints 3 before subtracting. Only after printing does n = n - 1 drop it to 2.

Walk the passes:

Pass 1: is 3 > 0? yes → print 3 → n becomes 2
Pass 2: is 2 > 0? yes → print 2 → n becomes 1
Pass 3: is 1 > 0? yes → print 1 → n becomes 0
Pass 4: is 0 > 0? no → stop

So it prints the starting value too. 
The mental model to lock: the condition is checked at the top of each pass, and the body runs with n at its current value before the decrement. My prediction started counting from after the first subtract — that's the off-by-one to notice.

Next, type the same countdown, but leave out the n = n - 1 line:

n = 3
while n > 0:
    print(n)

Predict first: with no line to decrease n, what happens? Is n > 0 ever false? What will the screen do?
3
3
.
.
It continues until we interrupt the program with Ctrl+C. 

CONCLUSION:
The lesson locked: a while loop needs its condition to eventually become false, or it runs forever. The line that moves toward the exit (n = n - 1 in the working version) is not optional — it's what makes the loop terminate. Forgetting it is the single most common while bug.

NEXT,
break and continue — two ways to steer a loop from inside its body.
**break exits the loop immediately — jumps out entirely, skips any remaining passes.**
**continue skips the rest of the current pass and jumps to the next one — the loop keeps going.**

>>> for x in [1, 2, 3, 4, 5]:
 ...     if x == 3:
 ...         break
 ...     print(x)

 Trace it: x=1 → is it 3? no → print 1. x=2 → no → print 2. x=3 → yes → break, jump out entirely. So 4 and 5 never happen.

 prediction and run are the same: 
1
2
>>> 
Note the order inside the pass: the if check happens before print(x), so when x hits 3, break jumps out and 3 never prints.

Now continue — the contrast. 

for x in [1, 2, 3, 4, 5]:
    if x % 2 == 1:
        continue
    print(x)

Recall % is remainder: x % 2 == 1 is true for odd numbers. So when x is odd, continue fires — skips the rest of this pass (skips print) and moves to the next number. When x is even, the if is false, so print(x) runs.

Trace it: x=1 (odd) → continue, skip print. x=2 (even) → print 2. And so on. Predict exactly what prints, then run. Show me both.

prediction and run are the same: 
2
4


EXERCISE 2 
flag training loads that stray too far from a target. This one's a for loop with a conditional inside (not while — read the goal, pick the honest tool). 

The setup: you have a list of daily loads, a target, and a threshold. For each load, if it deviates from the target by more than the threshold, print a flag line. "Deviation" = absolute difference from target — the abs() we drilled yesterday, reused.

Build it in pieces. First, the data — type into the file:

loads = [100, 105, 130, 98, 75]
target = 100
threshold = 20

target is where you want the loads to sit; threshold is how far off is "too far." Type those three lines, tell me when in, then predict on paper (before any loop): eyeballing the list, which loads are more than 20 away from 100? That prediction is your check for when the code runs.

30 is 30 away, 75 is 25 away, both exceed 20. The other three (100, 105, 98) are within 20, so they shouldn't flag. That's your expected output.

Now the loop. You want to check each load against the target, so loop over the values — plain for load in loads, no index needed here (you're not reaching neighbors). Type below the data:

for load in loads:
    deviation = abs(load - target)
    if deviation > threshold:
        print(f"FLAG: {load} is {deviation} off target")

Read the structure:

deviation = abs(load - target) — how far this load is from target, sign dropped (30 away is 30 whether over or under).
if deviation > threshold: — only the too-far ones pass this gate. Note > strictly: a load exactly 20 off would not flag. That's a boundary decision — just be aware you chose it. If deviation >= threshold, then a load exactly 20 off will get flagged. 

The print runs only inside the if, so only flagged loads produce a line.

cherinefons@Mac foundation % python3 day8_loops.py
FLAG: 130 is 30 off target
FLAG: 75 is 25 off target
cherinefons@Mac foundation % 

EXERCISE 3
reading values until a sentinel stops you.

A sentinel is a special value that means "stop here" — not real data, just a marker for the end. Here the sentinel is None. You loop through a list and process each value, but the moment you hit None, you stop — even if there's more list after it.

This is where the for-vs-while judgment comes in, and the sheet wants you to choose and justify. Two honest ways to do it:

a for loop that breaks when it sees None, or
a while loop that keeps going until it hits None.

Start with the for+break version since you just learned break. Into day8_loops.py, below Exercise 2:

readings = [80, 85, 90, None, 100, 105]
for r in readings:
    if r is None:
        break
    print(r)

Two things to notice:

if r is None: — you test for None with is, not ==. (is None is the standard Python idiom; take it as the rule for now, the why comes later.)
when break fires at the None, everything after it (100, 105) is never printed — the sentinel cuts the list off.

PREDICTION:
80
85
90

... readings = [80, 85, 90, None, 100, 105]
... for r in readings:
...     if r is None:
...         break
...     print(r)
...     
80
85
90
>>> 

CONCLUSION: 80, 85, 90, are correct. Then None trips the break and 100, 105 never print. The sentinel cut the stream off exactly where you predicted. And you used is None correctly.

Now the judgment call the exercise is really about. You just did it with for+break. It could also be written as a while loop. The sheet asks: which did you choose, and why?

Here's the frame for deciding: for naturally walks a known collection start-to-finish; while is the honest choice when you're looping until some condition changes and you don't know the count in advance (like reading input from a user until they type "quit"). Here, since readings is a fixed list already sitting in front of you, for walking it (with break for the sentinel) is arguably the more natural fit — you have the collection.


Review Q1: for-with-break vs while — which did you choose for this, and why? (There's no single right answer; the reasoning is what's graded.)

Answer: I chose a for loop with break because the readings were already stored in a list, so it made sense to examine each value directly in order. When the loop reached the sentinel None, break stopped the loop immediately, preventing the later values from being processed. A while loop could also work, but it would require extra tracking, such as an index, so the for loop was simpler and clearer here.


EXERCISE 4
enumerate — when you need both the position and the value at once.

Yesterday, to get an index you used for i in range(len(xs)) and then looked up xs[i]. That works, but it's clumsy when you want both. enumerate hands you both directly, as a pair, each pass.

predict first:

exercises = ["squat", "bench", "deadlift"]
for i, name in enumerate(exercises):
    print(i, name)

The key mechanic: enumerate yields a pair each pass — the index and the value. for i, name in ... unpacks that pair into two variables at once: i gets the index, name gets the value. So pass 1 gives i=0, name="squat", and so on.

Predict exactly what prints (remember enumerate starts counting at 0), then run. 

PREDICTION:
0 squat
1 bench
2 deadlift

Correct.

Now the second half: enumerate can start counting from a different number. Humans often want 1-based labels. Predict, then run:

for i, name in enumerate(exercises, start=1):
    print(i, name)

start=1 tells enumerate to begin the count at 1 instead of 0. This is a cleaner fix for the off-by-one than the i + 1 trick you used yesterday — the counter itself starts where you want. Predict the three lines.

PREDICTION:
1 squat
2 bench
3 deadlift

Correct.
The thing to lock: enumerate yields a (index, value) pair each pass — that's what the for i, name two-variable unpacking is catching. If you'd written for x in enumerate(exercises), x would be the whole pair (0, "squat"), not just the value. That's the [predict] point the sheet flags.

Question: What does enumerate give you on each pass, and why does for i, name need two variables?
Answer: Enumerate gives you both the index and the item on each pass, so for i, name needs two variables to receive those two values separately.

EXERCISE 5
zip — walking two lists in parallel, pairing them up position by position.

enumerate paired an index with a value. zip pairs elements from two lists — first-with-first, second-with-second, and so on. Predict first:

names = ["squat", "bench", "deadlift"]
weights = [100, 80, 120]
for name, w in zip(names, weights):
    print(f"{name}: {w}kg")

The mechanic: zip(names, weights) yields a pair each pass — one element from each list, matched by position. for name, w unpacks that pair (same two-variable unpacking as enumerate). Pass 1: name="squat", w=100.

PREDICTION:
squat 100kg
bench 80kg
deadlift 120kg

After run:
>>> names = ["squat", "bench", "deadlift"]
... weights = [100, 80, 120]
... for name, w in zip(names, weights):
...     print(f"{name}: {w}kg")
...     
squat: 100kg
bench: 80kg
deadlift: 120kg
>>> 

now try:
names = ["squat", "bench", "deadlift", "row"]
weights = [100, 80]
for name, w in zip(names, weights):
    print(f"{name}: {w}kg")

Prediction:
squat: 100kg
bench: 80kg

run:

>>> names = ["squat", "bench", "deadlift", "row"]
... weights = [100, 80]
... for name, w in zip(names, weights):
...     print(f"{name}: {w}kg")
...     
squat: 100kg
bench: 80kg
>>> 

Here's the lesson — only two lines. zip stops at the shorter list. It paired squat/100 and bench/80, then ran out of weights and quit — "deadlift" and "row" are silently dropped. No error, no warning; the extra names just vanish.

That's the behavior to know, not guess: zip truncates to the shortest input. The danger is the silence — if your two lists are supposed to be the same length and aren't, zip won't tell you; it'll just quietly process fewer items. That's a bug-hiding trap, same family as the zip-drops and vols[-1]-wraparound cases you've been meeting.
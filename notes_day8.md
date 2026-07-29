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

next, type the same countdown, but leave out the n = n - 1 line:

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


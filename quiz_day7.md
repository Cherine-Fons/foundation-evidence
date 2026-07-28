**Day 7 End-of-Day Quiz**

1. Predict each, exact output: `list(range(4))` · `list(range(2, 11, 3))` · `len(range(50))` · a bare `range(4)` typed at `>>>`.

2. `xs = [10, 20, 30, 40, 50]`. Predict: `xs[0]` · `xs[-1]` · `xs[1:4]` · `xs[-2]`.

3. What's the difference between `for x in xs:` and `for i in range(len(xs)):`? Name one situation where you *must* use the second form.

4. Running total by hand: `counts = [2, 5, 1, 4]`, `total = 0`. Write `total` after each pass. Then: why must `total = 0` sit *outside* the loop — what breaks if it's the first line inside?

5. Given `vols = [800, 1000, 900, 1200]`, write from scratch — on paper, no references — the loop that builds `abs_diffs`, the list of day-over-day absolute differences. Then state: why does the loop start at `range(1, len(vols))` and not `range(0, ...)`? What goes wrong at index 0?

6. For the same `vols`, what does `vols[i] - vols[i-1]` compute when `i = 2`? Give the two elements and the result. Why does the percentage-change version keep the sign while the absolute-difference version drops it with `abs()`?

7. Off-by-one: `for week in range(3): print("Week", week)` prints what? Give two different one-line fixes so it reads Week 1, Week 2, Week 3.

8. Predict and explain the error type: `for x in [1,2,3]:` followed by a non-indented `print(x)`.

Take your time. Answers in one block when ready.


RESPONSES:

1. list(range(4))       output: [0, 1, 2, 3 ]
   list(range(2, 11, 3))    output: [2, 5, 8] 
   len(range(50))           output: 50
   range(4)           output: range(0, 4)

2. xs[0]        output: 10
   xs[-1]       output: 50
   xs[1:4]      output: [20, 30, 40]
   xs[-2]       output: 40

3. for x in xs:     gives me each value directly.
   for i in range(len(xs)):     gives you each index—0, 1, 2, ...—so you access the value with xs[i].
   We need the index form when the element’s position matters, such as changing the original list in place.

4. counts = [ 2, 5, 1, 4 ]
   total = 0

total = 0 must sit outside the loop because it should be initialized only once. Each pass then builds on the result from the previous pass. If we put it inside, Python resets total to 0 every time. Nothing accumulates. After the loop, total is only 4, the final item, rather than 12. The rule is: initialize the accumulator before the loop; update it inside the loop.

Start:        0
After adding 2:  2
After adding 5:  7
After adding 1:  8
After adding 4: 12

and if total = 0 sat inside the loop, the output would be:

2
5
1
4

5. 
vols = [800, 1000, 900, 1200]
abs_diffs = []
for i in range(1, len(vols)):
    diff = abs(vols[i] - vols[i - 1])
    abs_diffs.append(diff)
print(abs_diffs)

Why does the loop start at `range(1, len(vols))` and not `range(0, ...)`? 
ANS: len(volumes) is 4. So range(1, 4) produces 1, 2, 3. The loop starts at 1 because index 1 is the first position that actually has a previous element at index 0.
What goes wrong at index 0?
ANS: If the loop started at 0, the first calculation would be:
vols[0] - vols[-1]
In Python, index -1 means the last element of the list. So Python would compare 800 with 1200.

6. volumes[i]     = volumes[2] = 1050
   volumes[i - 1] = volumes[1] = 1100

result:
volumes[i] - volumes[i - 1]
1050 - 1100 = -50

The percentage-change calculation keeps the negative sign because it tells us the volume decreased by about 4.55%.
But the absolute-difference calculation drops the negative with abs(), because absolute difference measures only how far apart the two values are, not whether the volume went up or down.

7. for week in range(n): print("Week", week)

gives:
   
Week 0
Week 1
Week 2

Two fixes:
change print to: print("Week", week + 1), or
change the range: range(1, n + 1) so it produces 1, 2, 3

8. IndentationError: expected an indented block after 'for' statement


CORRECTIONS:

1. All four correct. range(2,11,3) → [2, 5, 8] (stops before 11, so no 11) — nailed. ✓

2. All four correct, including both negative indices. ✓

3. Right. One sharpening: your "must use the index form" example — "changing the original list in place" — is one valid case, but the sharper one from your own Exercise 4 is reaching a neighbor (vols[i-1]). Both are correct; the neighbor case is the one you actually built. ✓

4. Fully correct — 0, 2, 7, 8, 12, and a clean explanation of why inside-the-loop resets kill accumulation. Your "if inside" trace (2, 5, 1, 4) is exactly right. ✓

5. Loop is perfect, cold. The "why start at 1" is right. And you caught the subtle one: at index 0, vols[0] - vols[-1] would silently compare 800 to 1200 using Python's negative-wraparound — no crash, wrong answer. That's the dangerous kind of bug, and you spotted it without prompting. ✓✓

6. Method and reasoning fully correct — sign kept for direction, dropped for distance. One data slip: you wrote volumes[2] = 1050 and volumes[1] = 1100, but this question used vols = [800, 1000, 900, 1200], not the earlier [1000, 1100, 1050, 1200]. For these numbers: vols[2] = 900, vols[1] = 1000, so 900 - 1000 = -100. You pulled the values from the earlier session's list out of memory instead of reading the new one. The logic is flawless; just read the given list each time. Minor. ✓ (logic) / ⚠️ (wrong list)

7. Both correct. ✓

8. Correct error type. ✓
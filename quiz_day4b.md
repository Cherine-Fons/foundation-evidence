**DAY 4 QUIZ — Conditionals** Jul 24 testing material of Jul 23

Closed-book, from memory. No interpreter, no notes, no scrolling back. Traps and combination questions included by design. Write "blank" rather than guessing wildly.

**Section A — Booleans and comparison**

1. What *type* does `4 > 9` produce, and what does that tell you about where `if` gets its input?
2. Predict each: `5 == 5.0` · `"5" == 5` · `not (3 > 1)` · `True and False` · `False or True`
3. `2 < 5 < 4` — what does this give, and what does Python actually evaluate to get there?

**Section B — `=` vs `==`**

4. Explain the difference in one sentence each, and say what happens when you write `if x = 5:` — including *what kind* of error and why it happens before anything runs.

**Section C — The chain mechanism**

5. Someone writes `classify_intensity` with the branches in this order:
```
if pct >= 70:
    return "moderate"
elif pct > 85:
    return "heavy"
else:
    return "light"
```
What does `classify_intensity(95)` return? Is that correct? Explain what went wrong using the chain rule.

6. In that same broken function — does Python raise an error or warning? Why is that dangerous?

7. Is *every* `elif` unreachable? Give an example of an `elif` that IS reachable, and say what makes the difference.

**Section D — Combination (Days 3 + 4 together)**

8. Predict every line of output:
```
def check(n):
    if n > 10:
        return "big"
    else:
        print("small")

r = check(20)
print(r)
r = check(5)
print(r)
```

9. Using that same `check`: what happens if someone writes `print(check(5) + "!")`? Name the error and explain which branch caused it.

10. A function is supposed to answer a yes/no question. Why is `return None` on one path worse than `return False`, even though both are "not true"?

**Section E — Specification**

11. Your `can_promote` takes `current_rank` and `years_at_rank`. You originally wanted a rule using cumulative training time across all belts. Why couldn't that rule be implemented — and what's the general principle?

12. In `is_admissible(a, b)`, why does the exercise insist on test pairs that fail each condition *separately*? What could you miss otherwise?

**Section F — Reasoning**

13. `is_admissible` is written as `return (a + b) % 2 == 0 and a <= b` — no `if` anywhere. Explain why that works, and why wrapping it in `if ...: return True else: return False` would be circular.

14. Two functions both "show you" the word `"heavy"` when called. One returns it, one prints it. A caller writes `if classify(90) == "heavy":`. Which function makes that work, which breaks it, and what exactly does the broken one compare against?


MY ANSWERS:

section A:

1. <class 'bool'>, `if` gets its input from the value produced by an expression. So if 4>9: , python returns False and uses that as its condition
2. True, False, False, False, True
3. False python evaluates 2 < 5 then 5 < 4 

section B:

4. = puts a value into a variable while == compares two values. if x = 5: is asking Python to consume the result of an assignment as a condition. But assignment doesn't produce a bool or anything else and so this entry breaks before anything runs giving a SyntaxError.

section C:

5. moderate. Not correct. python never makes it to elif since the first branch in the chain is greater than or equal to 70 and python never needs to check elif.
6. not the same as a broken function. Python does and says nothing which is dangerous.
7. No. 

x = 3

if x >= 5:
    print("small")
elif x >= 2:
    print("smaller")


section D:

8. it displays the following but returns None:

         big
         small

9. c`heck(5)` runs first. Since `5 > 10` is false, the `else` branch is triggered and python displays small. But that branch does not return `small. `It reaches the end of the function and returns `None`. So python tries to evaluate None + "!" and we get TypeError since we have "NoneType" + "str"
10. Because `False` is a legitimate no answer, while `None` means the function failed to provide a yes/no answer at all.

section E:

11. The cumulative-time rule could not be implemented correctly because promotion eligibility depends on time spent at the current rank, not total time spent training. A function can only make a correct decision when its inputs contain enough information to distinguish every case that requires a different result?
12. if we only ever test pairs that fail both at once, we can't tell which condition is actually doing the work. A broken implementation could still pass our tests. Isolating failures is how we know each condition is live.

section F:

13. comparisons are expressions that evaluate to values, so `if` is optional.  It's just one thing we can do with a bool. The combined condition here is the answer.  Wrapping it in `if ...: return True else: return False `is asking "is this True? if so, return True" , which is circular.
14. the function that returns "heavy" makes the comparison work:

def classify(pct):
         return "heavy"

the function that only prints "heavy" breaks it:
def classify(pct):
         print("heavy")
the broken one is comparing None == "heavy"


MODEL FEEDBACK AND CORRECTIONS:

Strong quiz — twelve clean, two partial. Corrections from first principles, then the card.

Section A — all correct.

Q1: bool, and your framing is right — if never sees 4 or 9, only the bool the comparison produced. Q2: all five right. Q3: False, and you named the expansion correctly (2 < 5 and 5 < 4).

Section B — correct. = acts, == asks; assignment produces no value, so the line is ungrammatical and dies at parse time. Exact.

Section C

Q5 ✓ — "moderate", wrong, and your diagnosis is right: pct >= 70 swallows everything at or above 70, so the > 85 branch can never fire.

Q6 — substance right, wording garbled. The precise danger: Python raises nothing. No error, no warning, no complaint. The function runs "successfully" and returns a plausible-looking wrong answer. A test that only checks "does it crash" passes. That's what makes it worse than a crash — a crash tells you where to look.

Q7 — partial. Your example is correct and genuinely reachable (x = 3 fails >= 5, satisfies >= 2, prints). But you didn't answer the second half: what makes the difference. The principle: an elif is reachable when values exist that fail the first condition but satisfy the second — i.e. the second condition isn't a subset of the first. In the broken version, x > 10 sits entirely inside x > 5, so nothing survives to reach it. In yours, x >= 2 includes 2, 3, 4 — values x >= 5 rejects. Subset relation is the test. (Cosmetic: your labels are inverted — bigger x prints "small" — logic fine, naming confusing.)

Section D

Q8 — partial, and worth being precise about. You listed two output lines; there are three:

big      ← from print(r), the returned value
small    ← printed by the function itself during check(5)
None     ← from print(r), because check(5) returned nothing

That third line is real screen output, not a footnote. Your Q9 answer proves you understand the mechanism completely — this was an enumeration slip, not a concept gap. But when a question says "predict every line," count the lines.

Q9 ✓ — complete and correctly sequenced: small prints, None returns, None + "!" throws TypeError.

Q10 ✓ — "False is a legitimate no; None means no answer was produced." Exactly.

Section E

Q11 ✓ — and your general principle is the best sentence on the page: "A function can only make a correct decision when its inputs contain enough information to distinguish every case that requires a different result." Drop the question mark. That's a real engineering principle and you derived it.

Q12 ✓ — a broken implementation could pass tests that only fail both conditions at once. Isolation proves each condition is live.

Section F

Q13 ✓ — circular, exactly. Q14 ✓ — the printing version compares None == "heavy", which is False, so the branch never fires even though the word appeared on screen.

Result: no patch needed. Two enumeration/completeness slips, zero conceptual gaps (Q7, Q8). Conditionals are yours.


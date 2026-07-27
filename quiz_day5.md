Day 6, Monday Jul 27 — right on the amended schedule. Position confirmed: Days 1–5 complete, 34 commits, FA-1 controls from tomorrow. Today's sequence: Day-5 quiz → rebuild card → Week-1 exit check. Two tabs up as usual; no interpreter for the quiz.

**Day 5 quiz — closed book, all twelve, blanks written "blank":**

1. Your `plan_next_session` gets a difficulty it doesn't recognize. What does the function return, what appears at `>>>` for a bare call, and how do you make it visible?

2. Predict the full output:
```
def f(x):
    print(x * 2)

result = f(5)
print(result)
```

3. `sets = 1`, and your f-string reads `f"{sets} sets @ {weight}kg"`. What exactly prints, and what does that tell you about f-string output in general?

4. Predict: `f"2 + 3 = {2 + 3}"` — and say which part is frozen and which part runs.

5. In `format_set` you chose to *call* `classify_intensity` rather than copy its `if`/`elif` chain in. State the reasoning in one sentence.

6. Predict `c(30)`, then explain which branch is unreachable and why that's a bug even though nothing crashes:
```
def c(x):
    if x < 100:
        return "low"
    elif x < 50:
        return "very low"
    else:
        return "high"
```

7. `epley_1rm(100, 0)` returns `100.0` with no error. Name this failure mode and say why it's more dangerous than a traceback.

8. Predict each: `"3" * 4` · `3 * 4` · `"3" + "4"` · `"3" + 4`.

9. `weight = input("kg? ")` and the user types `80`. Predict what happens for `weight * 2`, then for `weight * 2.5` — and explain the difference.

10. `3 == 3.0` and `"3" == 3` — value of each, and why they differ.

11. Predict: `5 < 3 < 10` · `2 < 5 < 10`.

12. Two-part terminal check: (a) you're at `>>>` and type `python3 gym.py` — what happens? (b) a script is sitting at an `input()` prompt and you want out — what do you press?

Answer all twelve, then I correct in full.



ANSWERS:

**11/12.** Corrections:

**1 — right, tighten the wording.** The function *always* returns `None` when it falls off the end; `print()` doesn't cause that, it just reveals it. Bare call shows blank because `>>>` suppresses `None`.

**6 — answer right, half the question unanswered.** Your unreachable-logic is correct (every x < 50 is also < 100, so branch 1 always wins — first-True-stops). The missing half: why it's a bug when nothing crashes — the branch encodes an intention ("very low" exists as a category) that can never execute. The code silently lies about its own behavior. Same family as Q7: no traceback, wrong program.

**9 — substance right, name the rule precisely.** `str * int` is repetition; `str * float` is the TypeError — a repeat count must be a whole number. It's not "non-int × float" in general (`2 * 2.5` is fine); it's *string* × float.

**12b — miss.** `exit()` only works at `>>>`. A script blocked at `input()` will swallow `exit()` as the *string you typed* — it becomes the exercise name. The answer is **Ctrl+C**. You did this live on Friday; it didn't stick as a rule yet.

**Patch drill (2 min, predict first):** shell tab →

```
python3 day2_logline.py
```

At the name prompt type `exit()` and hit return — write your prediction of what happens before you do. Then re-run and Ctrl+C out at the prompt. Reconcile in one sentence.


CORRECTION:
My answer was wrong because exit() only exits the Python REPL at the >>> prompt. When a script is paused at input(), it treats exit() as ordinary text and stores it as the user’s response, so the program keeps running; we corrected this by pressing Ctrl+C, which interrupts and stops the script.
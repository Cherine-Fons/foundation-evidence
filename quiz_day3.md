Good call — you've got the runway and the material's fresh, so quizzing this afternoon while it's warm is legitimate. One thing worth being honest about, though, and then I'll build the quiz either way:

The reason we set quizzes for *next morning* was to test retention after sleep — a same-day quiz partly measures short-term echo rather than what stuck. So a quiz a few hours after learning will run a bit easier than a cold-morning one, and we should read the results with that grain of salt. That doesn't make it useless — it's still a real check, it'll still expose any genuine holes, and doing detailed corrections today is high-value. It just means: if you ace it this afternoon, that's good but not the same signal as acing it cold tomorrow.

My suggestion for the best of both: **do this afternoon's quiz now** as a "did today land" check with full corrections, *and* still take a short cold recall on Day 3 concepts tomorrow morning before Day 4 — not a full re-quiz, just three or four questions to confirm it survived the night. That way you get today's deep corrections *and* tomorrow's honest retention signal. Cheap, and it keeps the mechanism intact.

Either way — here's the **Day 3 quiz.** Closed-book, from memory, no interpreter, no scrolling up. Comprehensive, with traps and combination questions. Answer all, number them, then we correct in full detail from first principles.

**DAY 3 QUIZ — Functions**

**Section A — Anatomy.**
1. What are the four parts of a function header, in order? (Use `kg_to_lb(kg)` as your example.)
2. What does the keyword `return` do — where does the value go?
3. Why must the body of a function be indented?

**Section B — Predict the output.**
4. Given `def double(n): return n * 2`, what does `double(6)` give?
5. Given `def greet(name): return f"hi {name}"`, what does `greet("sam")` give?
6. Given `def add(a, b): return a + b`, what does `add(3, 4) + add(1, 1)` give? (Combination — two calls, then added.)

**Section C — return vs print (the big one).**
7. `def f(x): return x + 1` — what does `f(5) + 10` give?
8. `def g(x): print(x + 1)` — what does `g(5) + 10` give? Be specific: what prints, and what (if anything) breaks, and why.
9. In Q8, what *value* does `g(5)` hand back to the code that called it? What's that value called?

**Section D — Functions calling functions.**
10. You have `def volume(s, r, w): return s * r * w`. Write (from memory) a second function `total(s, r, w)` that returns volume × 2 by *calling* `volume` inside it. (You may write the code.)
11. If you define `total` but forget to define `volume` first, then call `total(2, 3, 4)` — what happens, and what's the error called?

**Section E — Hand-trace.**
12. Given:
```
def volume(s, r, w): return s * r * w
def session_line(ex, s, r, w): return f"{ex}: {volume(s, r, w)}"
```
Trace `session_line("squat", 3, 5, 100)` step by step: the four parameter bindings, the inner call, what volume returns, and the final string.

**Section F — Combination / reasoning.**
13. Two functions look almost identical: one uses `return`, one uses `print`. Both "show you" the number 7 when called. In one sentence each: why can only *one* of them be used inside another function's calculation, and which one?
14. `def mystery(x): x + 1` — note: no `return`, no `print`, just `x + 1` on the body line. What does `mystery(5)` give back when you call it? (Trap — think about what happens to a value that's computed but neither returned nor printed.)

QUIZ KEY:
Strong quiz — you're clearly solid on the core. Let me correct all 14 from first principles, marking each, then we drill the two spots that need it. This is your answer key.

**SECTION A**

**1. Four parts: def, name, parameter, colon.** ✅ Correct. All four, right order.

**2. "return defines what the function does, no output at this step. Value goes in the parameter parentheses after we call function."** ⚠️ **Half right, half tangled — this one needs cleaning up.** `return` doesn't "define what the function does" — the whole body does that. `return` specifically **hands a value back to the code that called the function.** And your second sentence mixed two different things: the *parameter parentheses* are where values go *in* when you call; `return` is about what comes *out*. So the precise version: **`return` sends a value back out of the function to whoever called it, so that value can be used in further computation.** The "no output/no print" instinct is right — return isn't print — but the wording conflated in and out. Mark **partially correct, re-state it.** (This matters because Q8/Q9 are the same concept.)

**3. Indentation: "so python understands this is a nesting and body is inside the function."** ✅ Correct in substance. Precisely: indentation is how Python knows which lines belong *inside* the function versus outside it. "Nesting" is the right instinct. Good.

**SECTION B**

**4. `double(6)` → 12.** ✅
**5. `greet("sam")` → `'hi sam'`.** ✅ (You wrote "Sam" capitalized — minor: the output is exactly what you passed, lowercase `sam`, since the function just drops the string in. `'hi sam'`. Trivial, but precision.)
**6. `add(3,4) + add(1,1)` → 9.** ✅ Correct — `7 + 2 = 9`. Nice on the combination: two function calls each return a number, then those numbers add. This is the "return gives usable values" idea in action.

**SECTION C — return vs print**

**7. `f(5) + 10` → 16.** ✅ `f(5)` returns 6, `6 + 10 = 16`. Correct.

**8. `g(5) + 10` → "typeerror. python returns none. print(x+1) runs first."** ✅ **Fully correct and well-sequenced.** `g(5)` prints 6, returns `None`, then `None + 10` throws `TypeError`. You got the order (print first, then the break) and the cause (None). This is the day's gate and you own it.

**9. What value does `g(5)` hand back, and what's it called?** You said "6 (don't know what it's called, printed value maybe)." ❌ **This is the one real miss, and it's important.** Trap alert: `g(5)` **prints** 6, but the value it **hands back** is **`None`** — not 6. The 6 goes to the *screen*; the value *returned to the code* is `None`. That's the whole distinction — what's printed and what's returned are different things, and here they're 6 (printed) versus None (returned). The name of that value is **`None`** (its type is `NoneType`). This is exactly why Q8 breaks: `g(5)` returns None, not 6. Mark **incorrect** — and this is your #1 patch target, because it's the crux of the entire day. Re-anchor: **print sends a value to the screen and returns None to the code.**

**SECTION D**

**10. Your `session_line` / `total`:** you wrote
```
def session_line(s, r, w):
    volume(sets, reps, weight)
    return f"{volume(sets, reps, weight) * 2}"
```
⚠️ **Partially correct — right idea, three issues.** The *concept* — call `volume` inside and use its result — is correct. But: (a) the question asked for a function named `total` that returns volume × 2 as a *number*, not a formatted string, so the f-string wrapper isn't needed (and it turns the number into a string); (b) **parameter-name mismatch** — your header uses `s, r, w` but inside you wrote `sets, reps, weight`, which don't exist → `NameError`. This is the exact bug you caught in yesterday's quiz (stored name must match used name); it crept back in. (c) the standalone `volume(sets, reps, weight)` line is the dead/discarded line again. The clean version: `def total(s, r, w): return volume(s, r, w) * 2` — matching names, no f-string, no dead line. Mark **partially correct, concept right, execution slipped on name-matching.** Good news: you *know* this bug, it's a slip not a gap.

**11. Forgot to define volume → NameError.** ✅ Correct. `NameError: name 'volume' is not defined`. The caller needs the callee to exist. 

**SECTION E**

**12. Hand-trace of `session_line("squat", 3, 5, 100)`** — attached photo. Reading it: bindings ex→squat, s→3, r→5, w→100; `volume(3,5,100)`; but your final line shows **`'squat: 1500'`**. ✅ **Correct!** `3 * 5 * 100 = 1500`, dropped into `f"{ex}: {volume(...)}"` → `'squat: 1500'`. The trace is right and matches. Well done — and this is a genuinely valuable skill you're demonstrating cleanly now.

**SECTION F**

**13. "only return can be used inside another function's calculation."** ✅ Correct, and it's the right answer — but the quiz asked *why*, in a sentence. The why: **only `return` hands back a usable value; `print` hands back `None`, which can't be computed with.** You named the *which*; make sure you can also say the *why* cold, because it's the same None concept as Q9. Mark **correct on the answer, attach the reason.**

**14. `def mystery(x): x + 1` — no return, no print. What does `mystery(5)` hand back?** You said "structure is wrong, must be an error." ❌ **Trap, and you fell in — but it's a great teaching miss.** It does **not** error. It runs perfectly fine — it computes `5 + 1 = 6`... and then **throws the 6 away**, because nothing captures or returns it. So `mystery(5)` hands back **`None`** (same as any function with no `return`). No error, no output, just silently returns None. This is the deepest version of the day's lesson: **a value that's computed but neither returned nor printed simply vanishes, and the function returns None by default.** It ties directly to Q9 — *any* function that doesn't explicitly `return` gives back None. Mark **incorrect** — and notice it's the *same root* as Q9.

---

**DIAGNOSIS**

Correct: 1(partial), 3, 4, 5, 6, 7, 8, 11, 12, 13. Miss/slip: 2 (wording), 9 (**real**), 10 (name-matching slip), 14 (**real**).

The pattern is crisp and it's a *single concept*: **Q9 and Q14 are the same miss — "what does a function hand back when it prints, or when it neither prints nor returns?" The answer is always `None`.** You've got the return-vs-print break itself (Q8 was perfect), but the specific fact "**print returns None**, and **no-return returns None**" hasn't fully locked. That's the patch target, and it's one idea, not two.

The other slip (Q10 name-matching) isn't a concept gap — you diagnosed that exact bug yourself yesterday — it's a fresh-code carefulness thing that reps will fix.

**The patch, ~5 min in the interpreter.** Type these, predicting each:

def g(x): print(x + 1)  one line way to write a function
def h(x): x + 1
now call g when x is 5
so we run:
result_g = g(5)

pred 1: what appears on the screen?  6
pred 2: what does result_g hold afterward? none

print(result_g) returns none
result_h = h(5)
print(result_h)

Watch: `g(5)` prints 6, but `result_g` is **None**. `h(5)` prints nothing, and `result_h` is **None**. Seeing `None` come back with your own eyes — *twice, from two different "no return" situations* — is the whole patch. When both print `None`, Q9 and Q14 are locked.

def mystery(x): x + 1
result_m = mystery(5)
print(result_m)

mystery(5) prints nothing (it computes 6 but neither prints nor returns it — the 6 just vanishes into thin air)
print(result_m) shows None (no return means the function hands back None by default)

Remember: A function hands back None unless it explicitly returns something. Whether it prints (like g) or does nothing with the value (like mystery), if there's no return, the caller gets None. Printing shows you a number on screen; it does not mean that number came back to your code.
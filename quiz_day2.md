Morning. Before the Day 3 card, here's your **Day 2 quiz** — as agreed: closed-book, from memory, no interpreter, no notes, no scrolling up. Comprehensive, with some traps and combination questions. Answer all of them, then we correct it together from first principles with a full answer key you keep.

Take your time. Write your answers however you like — just number them.

**DAY 2 QUIZ**

**Section A — Predict the output *and* the type.** For each, give both what prints and what type the result is (int, float, str, or an error):

1. `7 // 2`
2. `7.0 // 2`
3. `"ab" * 3`
4. `"7" + "2"`
5. `len("")`

**Section B — Strings and indexing.**

6. What does `"hello"[0]` give, and what does `"hello"[-1]` give? Why does `[-1]` do what it does?

**Section C — f-strings.**

7. What does this print?  `f"{2 + 3} apples"`
8. What does this print?  `f"{'2 + 3'} apples"`  (note the inner quotes around `2 + 3`)
9. In an f-string, what does the `:.1f` do in `{value:.1f}`?

**Section D — input() and conversions. (This is the heart of Day 2.)**

10. A program runs `x = input("num: ")` and the user types `5`. What is the *value* and *type* of `x`?
11. Given that `x` from Q10, what happens when you run `print(x * 3)`? Be specific about what you'd see.
12. How do you fix it so `x * 3` gives `15`?

**Section E — Errors (name the error type and the cause).**

13. `print("total: " + 45)` — what error, and why?
14. `name = 'farmer's carry'` — what error, and why?
15. `int("12.5")` — what happens, and why?

**Section F — Combination / reasoning.**

16. You write `weight = input("kg? ")` and then `print(weight * 2.5)`. Predict the error. Then: which conversion function fixes it — `int()` or `float()` — and why *that* one specifically and not the other?

17. Two-part: (a) What's the difference between a *value* and a *variable*? (b) If you write `v = 5 * 4`, then change nothing but type `v` again after reassigning one of the numbers it was built from — does `v` update on its own? Why or why not?


Good — you answered all 17 cold, and there's a lot right here. Let me correct it from first principles, question by question, marking each. Keep this as your answer key. I'll be precise about *why*, because the "why" is what makes it stick.

**SECTION A**

**1. `7 // 2` → 3.** ✅ Correct. Floor division, both inputs int, result is int `3`. (Full marks would also name the type: **int**.)

**2. `7.0 // 2` → 3.0.** ✅ Correct, and good — your "hmmm" hesitation still landed on the right answer. This is the trap you learned the hard way yesterday: `//` floors, but because one input is a **float** (`7.0`), the result is a **float** `3.0`, not an int. The type follows the ingredients.

**3. `"ab" * 3` → `ababab`.** ✅ Correct. But sharpen the language: `*` on a string isn't "multiplication," it's **repetition** — it repeats the string that many times. Result type is **str**. (Calling it "string with multiplication" is loose; the operator is repurposed for strings.)

**4. `"7" + "2"` → this is a trap and you half-fell in.** You wrote `72`. The output is the **string** `"72"` — with quotes, it's text, not the number 72. This is the exact distinction the whole day was about: `"7" + "2"` concatenates (glues) two strings into `"72"`; it does NOT add. If it were `7 + 2` (no quotes) you'd get the number `9`. Naming it "string with addition" is wrong on the operation — with strings, `+` is **concatenation**, not addition. Mark this one **partially correct**: right characters, wrong type and wrong operation name. This is your #1 thing to nail.

**5. `len("")` → you described what `len` does but didn't give the answer.** `len("")` = **0**. The string between the quotes is *empty* — zero characters — so its length is 0. Type is **int**. Always give the actual output, not just the definition. Mark **incomplete**.

**SECTION B**

**6. `"hello"[0]` → `h`, `"hello"[-1]` → `o`.** ✅ Both correct. And your reason for `[-1]` — "starts counting from the end" — is right. To be fully precise: positive indexes count from the front starting at **0** (`[0]` is the 1st character), and negative indexes count from the **end** starting at **-1** (`[-1]` is the last character). You had this exactly right in your notes yesterday, including catching your own earlier misconception. Solid.

**SECTION C**

**7. `f"{2 + 3} apples"` → `5 apples`.** ✅ Correct. Inside `{}`, Python **computes** `2 + 3` → `5`, then drops it into the text. Good.

**8. `f"{'2 + 3'} apples"` → you wrote `'5' apples`. Close, but not quite — this is a subtle one.** The inner content is `'2 + 3'` **in quotes**, which makes it a *string*, not an expression. So Python does NOT compute it — it drops the literal text in. The output is `2 + 3 apples` (the characters "2 + 3", no math, no quotes shown). Your answer `'5' apples` is wrong two ways: it computed (it shouldn't have, because of the inner quotes) and it showed quote marks (which don't print). This is the same lesson as Q4 — **quotes make Python treat something as literal text instead of computing it** — just hidden inside an f-string. Mark **incorrect**, and note it's the *same underlying rule* as #4. Worth really absorbing: quotes = "don't compute, this is text."

**9. `:.1f` → "format up to one decimal value."** ✅ Essentially correct. Precisely: it formats the number as a decimal (float) with exactly **1 digit after the decimal point**. So `3` becomes `3.0`, `3.14159` becomes `3.1`. Good.

**SECTION D**

**10. `x = input("num: ")`, user types 5 → value is `"5"`, type is... you said integer. Wrong — and this is THE key lesson of Day 2.** The value is `5` but the **type is str (string)**, NOT integer. `input()` **always** returns a string, no matter what the user types. Even though it *looks* like a number, `x` holds the text `"5"`. This is the single most important fact from yesterday, and it's the root of Q11, Q12, and Q16. Mark **incorrect** — and this is the one to burn in: **input() always gives you a string.**

**11. `print(x * 3)` → you wrote "error."** ✅ Correct that it errors — but let's be specific, because the specificity matters. Since `x` is the string `"5"`, `x * 3` is string *repetition*, not multiplication — so it actually would print `555` (the string "5" repeated three times), NOT an error! This is a genuine trap. `"5" * 3` = `"555"`. (Compare: `"5" + 3` *would* error, because you can't concatenate a string and an int.) So the honest answer: no error — it prints `555`, three fives glued together, because multiplying a string by an int repeats it. Mark **partially correct** — you sensed something was off, but the actual behavior is the repetition surprise. This ties directly back to Q3 (`"ab" * 3` → `ababab`).

**12. Fix → `x = int(input("x?"))` then `print(x * 3)`.** ✅ Correct. Wrapping in `int()` converts the string `"5"` to the number `5`, so `5 * 3` = `15`. Exactly right.

**SECTION E**

**13. `print("total: " + 45)` → you said "45 is a string, adding two strings."** Wrong reasoning — the opposite is true. 45 is **not** a string, it's an **int**. The error is `TypeError: can only concatenate str (not "int") to str`. The cause: `+` with a string on the left means concatenation, which only works string-to-string, but you gave it an int (45). So the problem is a string and a **non-string** being joined. Your answer got the situation backwards. Mark **incorrect on the reasoning** — the fix is `str(45)` or an f-string. Re-read your own line 65 from yesterday; you had the fix right, just describe the cause correctly.

**14. `name = 'farmer's carry'` → "quotes and quotations."** ✅ Right idea, needs precision. The error is `SyntaxError: unterminated string literal`. The cause: the string opens with `'`, and the apostrophe in `farmer's` is read as the *closing* quote — so Python thinks the string ends early and the rest is garbage. Fix: use double quotes outside (`"farmer's carry"`) or escape the apostrophe (`\'`). Mark **correct in spirit**, tighten the vocabulary.

**15. `int("12.5")` → "not an integer, it's a float."** ✅ Right instinct. Precisely: it throws `ValueError: invalid literal for int() with base 10: '12.5'`. The cause: `int()` can convert a *clean whole-number* string like `"12"`, but it chokes on a string containing a decimal point. (Note: it's a **ValueError**, not a TypeError — different error family.) Your notes yesterday nailed this. Mark **correct**.

**SECTION F**

**16. Two parts. (a) Predict the error — you didn't state it. (b) Which conversion fixes it and why.** The error is `TypeError: can't multiply sequence by non-int of type 'float'` — `weight` is the string from `input()`, and you can't multiply a string by 2.5. On the fix: you said **float**, "since decimals are floats" — ✅ **correct and correctly reasoned.** `float()` not `int()`, because a weight can be a decimal like 72.5, and `int()` would either reject it or chop off the decimal. Good reasoning. Mark **correct on the fix**, just remember to *name the error* too.

**17. (a) value vs variable, (b) does `v` auto-update.** Part (a): "value is fixed, variable can be assigned" — ✅ roughly right. A **value** is a piece of data (like `20`); a **variable** is a named box that holds a value. Part (b): you said "v updates on its own i think" — **incorrect**, and this is the Day 1 lesson that carries forward. `v = 5 * 4` computes `20` **once** and stores the number `20`. It does **not** remember the formula. If you change one of the original numbers, `v` stays `20` — it does NOT auto-update, because a variable holds a computed *value*, not a live formula. You'd have to re-run `v = ...` to recompute. This is exactly the `volume` staying `800` experiment from Day 1. Mark **incorrect** — and this one matters, so re-anchor it.

---

**SCORE AND DIAGNOSIS**

Fully correct: 1, 6, 7, 9, 12, 15, 16(fix). Partially/close: 2, 3, 5, 11, 14. **Genuinely wrong, and these are your patch targets: 4, 8, 10, 13, 17(b).**

Here's the pattern, and it's a *single* pattern, which is good news — it means one fix, not five:

**Every one of your misses is the same root confusion: string vs. number, and "compute vs. literal text."**
- Q4: `"7" + "2"` is `"72"` (text), not `72` (number)
- Q8: quotes inside an f-string = literal text, no computing
- Q10: `input()` gives a **string**, always
- Q13: 45 is a number, can't glue it to a string
- Q17b: a variable holds a computed value, not a live formula

These aren't five separate gaps — they're one idea seen from five angles: **Python treats "text that looks like a number" completely differently from an actual number, and quotes are the signal for which is which.** You *know* this — your notes prove it — but under cold-recall pressure it wobbled. That's exactly what the quiz is for: it found the soft spot.

**The 10-minute patch before Day 3:** open the interpreter and run these five, predicting each first:

"7" + "2" output "72" or '72' both strings
7 + 2   output 9
"5" * 3 output '555' since 5 is just text that looks like a number
5 * 3 output 15
type(input("type a number: ")) output is type a number:


IMPORTANT TABLE:

Here's the whole system in one place. 
**The `+` operator:**
- number `+` number → **adds**: `7 + 2` = `9`
- string `+` string → **glues (concatenates)**: `"7" + "2"` = `"72"`
- string `+` number → **ERROR** (can't glue text to a number): `"7" + 2` → TypeError

**The `*` operator:**
- number `*` number → **multiplies**: `5 * 3` = `15`
- string `*` number → **repeats**: `"5" * 3` = `"555"`
- string `*` string → **ERROR** (can't repeat text by text): `"5" * "3"` → TypeError


**Layer 1 — `input()` alone.** `input()` shows a prompt, waits, and hands back **whatever the user typed, always as a string.** Even if they type digits.

age = input("age: ")     # user types 30

Now `age` holds `"30"` — the string, not the number. That's the one fact that never changes: **input() → string, always.**

**Layer 2 — `input()` + `type()`, which proves Layer 1.** If you don't believe input gives a string, ask Python:

type(input("age: "))     # user types 30 → <class 'str'>

It says `str`, even though the user typed a number. That's the proof. 

**Layer 3 — `input()` + conversion + f-string, the full chain. Three steps in sequence:

weight = input("kg: ")        # step 1: get string, e.g. "20"
weight = float(weight)        # step 2: convert string → number, now 20.0
print(f"You lifted {weight} kg")   # step 3: drop the value into text

Or all in one line for steps 1–2: `weight = float(input("kg: "))`.

The logic of *why each step exists*:
- **input()** gets you text (that's all it can do)
- **int() or float()** turns that text into a number *if you need to do math on it* (int for whole numbers, float for decimals)
- **f-string** drops the value into a sentence for display — and inside `{}`, it shows the value; you can even compute there, like `{weight * 2}`


more questions:

**A.** User types `5`. What does each line give?

x = input("num: ")
print(type(x))


**B.** Same `x` (still the string from A). What does `print(x + x)` show?

**C.** Now:
```
x = int(input("num: "))    # user types 5
print(x + x)
```
What does `print(x + x)` show this time — and why is it different from B?

**D.** What does this print? `print(f"total: {3 + 4}")`

**E.** What does this print? `print(f"total: {'3 + 4'}")` (inner quotes — the trap from Q8)

Answer A–E. Wherever you hesitate is the exact spot we hammer before Day 3.


**A.** ✅ Right. `input("num: ")` shows the prompt `num:` and waits; `type(x)` gives `<class 'str'>`. And notice what you just confirmed with your own prediction: the user typed `5`, but the type is **str**. That's Q10 patched — you now expect `str`, not integer. Locked.

**B.** `x + x` where `x` is `"5"` → you said `55`. Right idea, small precision: the output is the **string** `"55"` — `"5" + "5"` glues two strings → `"55"` (text), not the number 55. The digits are right; just remember it's string concatenation producing text, because that's the whole point of B-versus-C. Mark **correct, tighten to "it's a string."**

**C.** ✅ Right, and your reasoning is exactly right: `int()` wrapped the input, so `x` is the *number* `5`, and `5 + 5` = `10` (actual addition). You even nailed *why* it differs from B: in B, `+` glued strings (`"55"`); in C, `+` added numbers (`10`). That B→C contrast — same `x + x`, totally different result depending on whether you converted — **is** the centerpiece of Day 2, and you just explained it cold. That's the one that matters most, and you have it.

**D.** ✅ `total: 7`. Inside `{}`, Python computes `3 + 4` → `7`. Correct.

**E.** The trap, and you fell in — but it's the *last* wobble, so let's kill it. You said `total: 34`. Look carefully: it's `{'3 + 4'}` — the `3 + 4` is **in quotes** inside the braces. Quotes mean "this is literal text, do NOT compute it." So Python doesn't add, doesn't glue — it just drops the characters `3 + 4` straight in. Output: **`total: 3 + 4`**. Your answer `34` assumed it concatenated `"3"` and `"4"`, but there's no `+` operation happening at all — the entire `'3 + 4'` is one frozen string, printed literally, spaces and plus sign included.

The rule, one more time, because this is the single thread through every miss you've had (Q4, Q8, and now E): **quotes = frozen literal text, Python does nothing to it.** No quotes = Python evaluates it.
**- {3 + 4} → no quotes → compute → `7`
**- {'3 + 4'} → quotes → literal text → `3 + 4`

Predict these two to seal it:
- `f"{'5' + '5'}"` → 55
- `f"{5 + 5}"` → 10

f"{'a' + 'b'}" → ab — two frozen strings, but the + outside the quotes runs and glues them ✅
f"{'a + b'}" → a + b — the whole thing inside one pair of quotes, frozen, printed literally ✅
f"{2 + 2}" → 4 — no quotes, numbers, computed ✅

Conditionals:

1. Boolean warm-up
Step 1 — where conditionals actually start:
Not with if. Comparisons stand alone and if is doing something different from what I'd assumed.
Arithmetic operators produce numbers, comparison operators produce booleans.

>>> 
>>> 2+3
5
>>> 3>5
False
>>> type(3>5)
<class 'bool'>
>>> 

Conclusion: 2 + 3 → 5, and type(5) would say int
            3 > 5 → False, and type(3 > 5) says bool


Prove the Storing part:
answer = 3 > 5
answer
type(answer)

Ans:
>>> answer= 3 > 5
>>> answer
False
>>> type(answer)
<class 'bool'>
>>> 

Step 2 — what if is actually for
You now have a type with two values. That's the whole input if was built to consume.
>>> if True:
...     print("ran")
...     
ran

>>> if False:
...     print("ran")
...     
>>> 

(nothing: a branch that doesn't run leaves no trace. No warning, no complaint, no output. Which means if you write a condition wrong, Python's response looks identical to the condition being legitimately false — a clean prompt either way.)

Step 3 — connect the two halves
CONSIDER THIS EXAMPLE:
    >>> x=7
>>> if x > 5:
...     print("big")
...     
big


but:

>>> x=2
>>> if x > 5:
...     print("big")
...     
>>> 
>>> 

Trace the order, because this is the mechanism: Python reaches if x > 5: and cannot decide anything yet — x > 5 isn't a value, it's an expression. So it evaluates it first. With x = 7 that expression collapses to True, and then if receives a bool and runs the block. With x = 2 the same expression collapses to False, and if skips. if never sees x. It only ever sees the bool the comparison produced.

That's why step 1 had to come first. if doesn't compare anything — comparison is a separate operation that happens before if gets involved. if is just the thing that consumes a bool and decides whether a block runs.

Step 4 — the other branch

>>> x=2
>>> if x > 5:
...     print("big")
... else:
...     print("small")
...     
small
>>> 
>>> x=7
>>> if x > 5:
...     print("big")
... else:
...     print("small")
...     
big
>>> 

Summary: 
1. Comparisons are expressions that evaluate to values, no if required
2. Those values have type bool, and bool has exactly two of them
3. True/False are capitalized literals; lowercase are just undefined names
4. if consumes a bool — it doesn't compare anything itself
5. A skipped branch is silent, no error, no trace
6. else is a peer of if, no condition, catches the False case


Starting over with Day 4:
EXERCISE 1:
RUN THE FOLLOWING:
1. 3 == 3.0             True
2. "3" == 3             False
3. True and False       False       (can't be True AND False at the same time)
4. not (1 < 2)          False
5. 1 < 2 < 3            True
6. 2 < 1 < 3            False

Reasoning: 
3 == 3.0 → True.  3 is an int, 3.0 is a float — different types — yet == says they're equal. So == compares numeric value. But "3" == 3 is False because a string and a number aren't comparable in value at all — one's text. So the rule isn't "same type required"; it's "same value, and text is never numerically equal to a number."

1 < 2 < 3 → True, 2 < 1 < 3 → False.   self-explanatory

Also:
True or False       True
False or False      False
not True            False

EXERCISE 2 classify_intensity(pct_1rm)

The function takes a percentage of my one-rep max and returns "light" (below 70), "moderate" (70–85), or "heavy" (above 85). We need to specify the boundaries. We will be building our first function with a conditional inside.

# boundaries closed on both ends: moderate = [70, 85]; 70 and 85 both return "moderate"
step 1 is the header: def, name, one parameter, colon
step 2 is the body: We need three branches, and Python's shape for that is if / elif / else. The mechanics: if takes a condition and a colon, then an indented block; elif (short for "else if") takes another condition and colon, for the case where the first was False; else takes no condition — it catches everything remaining.
ORDER MATTERS!

# boundaries closed on both ends: moderate = [70, 85]; 70 and 85 both return "moderate"
def classify_intensity(pct_1rm):
    if pct_1rm  >  85:
        return "heavy"
    elif pct_1rm  >=  70:
        return "moderate"
    else:
        return "light"

classify_intensity(85)      prediction 'moderate'   correct
classify_intensity(70)      prediction 'moderate'   correct
classify_intensity(90)      prediction 'heavy'      correct
classify_intensity(50)      prediction 'light'      correct

EXERCISE 3  can_promote(current_rank, years_at_rank)

comment: 
# white → eligible for blue at 2 years at white, blue → eligible for purple at 3 years at blue, purple → eligible for brown at 3 years at purple, brown → eligible for black at 2 years at brown.
At 2 years: white eligible for blue
At 3 years: blue eligible for purple
At 3 years: purple eligible for brown
At 2 years: brown eligible for black
Black is out of scope

improved comment:
# Belt-promotion eligibility, including boundary cases:
# White  → Blue:   eligible when years_at_rank >= 2
# Blue   → Purple: eligible when years_at_rank >= 3
# Purple → Brown:  eligible when years_at_rank >= 3
# Brown  → Black:  eligible when years_at_rank >= 2
# Black-belt progression is outside the scope of this function

def can_promote(current_rank, years_at_rank):
    if current_rank == "white" and  years_at_rank  >= 2:
        return True
    elif current_rank == "blue" and  years_at_rank  >= 3:
        return True
    elif current_rank == "purple" and  years_at_rank  >= 3:
        return True
    elif current_rank == "brown" and years_at_rank >= 2:
        return True
    else:
        return False

prove it:
can_promote("white", 2)     prediction: True
can_promote("white", 1)     prediction: False
can_promote("blue", 3)      prediction: True
can_promote("black", 10)    prediction: False

EXERCISE 4 is_admissible(a, b)      IMPORTANT FOR MY FLAGSHIP
Returns True if and only if two conditions both hold: a + b is even, and a <= b

first condition:
how to test whether a number is even? recall modulo operator
(a + b) % 2 == 0 — compute the remainder, compare it to zero, get a bool. That's the first condition.

second condition:
Is trivial by comparison: a <= b. And the function returns True only when both hold, which is what and is for.

Next is a design question. I could write this two ways:
Way 1 — an if/else chain like the last two functions: if both conditions hold, return True, else return False.

Way 2 — recognize that the conditions already produce a bool, and simply return that bool directly. No if at all. Something in the shape of return <condition> and <condition>.

Note:
Both are correct. Recall: comparisons are expressions that evaluate to values, no if required. if is optional — it's just one thing we can do with a bool. Here, the combined condition is the answer. Wrapping it in if X: return True else: return False is asking "is this True? if so, return True" — which is circular.

def is_admissible(a, b):
    return (a + b) % 2 == 0 and a <= b
 
 Note no if at all, because the combined condition already is the boolean answer. 

 I need to design six hand-tested pairs, at least two designed to fail each condition separately.
 There are four distinct outcomes possible, and good tests cover all of them (Testing each failure separately):

1. both conditions pass → True
2. the parity condition fails, but a <= b holds → False
3. a <= b fails, but parity holds → False
4. both fail → False


All six conditions are of the form is_admissible(a, b)
1. is_admissible(4, 6) returns True
2. is_admissible(7, 3) returns False
3. is_admissible(2, 7) returns False
4. is_admissible(5, 2) returns False
5. is_admissible(5, 5) returns True
6. is_admissible(0, 0) returns True
7. is_admissible(-2, 4)returns True 

Correct:
>>> def is_admissible(a, b):
...     return (a + b) % 2 == 0 and a <=b
...     
>>> is_admissible(4, 6)
True
>>> is_admissible(7, 3)
False
>>> is_admissible(2, 7)
False
>>> is_admissible(5, 2)
False
>>> is_admissible(5, 5)
True
>>> is_admissible(0, 0)
True
>>> is_admissible(-2, 4)
True
>>> 

EXERCISE 5 Bug Hunt

IMPORTANT: 
= is assignment. It's a command: put this value into this name. x = 3 means "make x hold 3." It doesn't ask a question, it doesn't produce True or False — it performs an action and produces no value at all.

== is comparison. It's a question: are these two equal? x == 3 produces a bool — True or False — and that bool is what if consumes.

BUG 1: if x = 3:         Repair: if x == 3 :
Based on the IMP note, if x = 3: is asking Python to consume the result of an assignment as a condition. But assignment doesn't produce a bool — it doesn't produce anything. So Python can't even make sense of the line's structure. Given that this breaks before anything runs, at the level of the line's grammar, we get a SyntaxError.

BUG 2: Construct an if/elif chain where the elif can never be reached because the first condition already covers it. Then explain why.

IMPORTANT NOTE: return only works INSIDE a function

x = 7
if x > 5:
    print("big")
elif x > 10:
    print("bigger")

PREDICTION: big

x = 3
if x > 5:
    print("big")
elif x > 10:
    print("bigger")

PREDICTION: nothing

x = 20
if x > 5:
    print("big")
elif x > 10:
    print("bigger")

    PREDICTION: big

    CONCLUSION: An unreachable branch is still a bug, even if the program does not crash. Python gives no error or warning, so the code appears to run normally while silently skipping part of the logic you wrote.

run to verify:
SyntaxError: invalid syntax
>>> 
>>> x = 7
>>> if x > 5:
...     print("big")
... elif x > 10:
...     print("bigger")
...     
big
>>> x = 3
>>> if x > 5:
...     print("big")
... elif x > 10:
...     print("bigger")
...     
>>> 
>>> 
>>> x = 20
>>> if x > 5:
...     print("big")
... elif x > 10:
...     print("bigger")
...     
big
>>> 
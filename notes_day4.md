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



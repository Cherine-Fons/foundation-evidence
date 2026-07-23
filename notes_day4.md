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

EXERCISE 2:



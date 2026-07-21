DAY 3 CARD — Functions I: def, parameters, return 

New concept, a function is defined with def, takes parameters (the values you pass in), and hands back a result with return. The shape is:
def name(parameter):
    return something  

(1) the line after def must be indented (Python uses indentation to know what's "inside" the function — 4 spaces, and VS Code does it for you when you end the def line with : and press Enter), and 
(2) return hands the value back to whoever called the function — it does not print anything.    

A function definition has exactly four parts, always in this order:

the keyword def — literally the word "def", which tells Python "I'm defining a function"
the name we're giving it — here, kg_to_lb
parentheses with the parameter inside — (kg) — the parameter is the name for "the value someone will hand in"
a colon : at the end of that line  

EXERCISE 1 FIRST FUNCTION: kg_to_lb(kg)
Task: Write a function that takes a weight in kg and returns pounds (kg × 2.2046). Define it in a .py file or the interpreter, then call it three times from the interpreter with three different values — like kg_to_lb(20). Calling means typing the function's name with a value in the parentheses; it hands you back the result.

def kg_to_lb(kg):
    return kg * 2.2046
call it

>>> def kg_to_lb(kg):
...     return kg * 2.2046
...     
>>> kg_to_lb(20)
44.092
>>> kg_to_lb(25)
55.115
>>> kg_to_lb(11.5)
25.3529
>>> 


EXERCISE 2 
def volume(sets, reps, weight):
    return sets * reps * weight


>> def volume(sets, reps, weight):
...     return sets * reps * weight
...     
>>> volume(5, 8, 20)
800
>>>     

session_line — a function that calls volume inside itself.
session_line(exercise, sets, reps, weight) takes four parameters — the exercise name plus the same three numbers. Its job is to return a formatted string (a training-log line), and crucially, it computes the volume part by calling volume rather than re-doing the multiplication itself.

def session_line(exercise, sets, reps, weight):
    volume(sets, reps, weight)
    return f"{exercise} volume: {volume(sets, reps, weight)}"

  then call 
  session_line("squats", 5, 8, 20)  
  output: 'squats volume: 800'

  EXERCISE 3
  The job: estimate a one-rep max from a weight and the reps you did. The formula is weight × (1 + reps/30)

 def epley_1rm(weight, reps):
    return weight * (1 + reps / 30).     group by order of operations 
>>> epley_1rm(405, 5)
472.50000000000006

(if we had done: return f"{weight * (1 + reps / 30):.1f}"  , output would have been: 472.5 )


EXERCISE 4: return vs print

Return is for using a value, print is for seeing one. This is why real functions almost always return — so their output can feed into other functions (exactly like session_line calling volume earlier, which only worked because volume returned its number rather than printing it)

whole lesson:
def f(x):
    return x + 1

def g(x):
    print(x + 1)

Now run and test:    
f(3) + 1 → 5. f(3) returned 4, handed it back, then + 1 made 5. The returned value was usable — you could keep computing with it. That's what return gives you: a value that flows onward.
g(2) + 1 → prints 3, then TypeError. Look carefully at the order of what happened:

g(2) ran and printed 3 on the screen (you see the 3 sitting there)
then it handed back None — because print displays but returns nothing
then Python tried None + 1 and choked: unsupported operand type(s) for +: 'NoneType' and 'int'

>>> f(3) + 1
5
>>> g(2) + 1
3
Traceback (most recent call last):
  File "<python-input-104>", line 1, in <module>
    g(2) + 1
    ~~~~~^~~
TypeError: unsupported operand type(s) for +: 'NoneType' and 'int'
>>> 

Reasoning: f(x) **returns** a value:
python
f(3)   # returns 4
4 + 1  # gives 5


g(x) only **prints** a value:
python
g(2)   # prints 3
But because `g()` has no `return`, Python automatically returns `None`. So Python then tries:
python
None + 1
That causes the `TypeError`.
The `3` appears before the error because `print(x + 1)` runs first.

EXERCISE 5 hand-trace on paper

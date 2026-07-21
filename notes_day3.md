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


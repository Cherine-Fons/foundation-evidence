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

kg = float(input("kg: "))



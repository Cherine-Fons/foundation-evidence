**Day 4 — None recall quiz**

Answer from memory, no interpreter, no notes. Five questions, write your answers in order. The card comes when you're done.

**Q1.** A function body runs to the end without ever hitting a `return` statement. What value does the caller receive?

**Q2.** Predict the output, both lines:
```
def greet(name): print("hello " + name)
r = greet("Cherine")
print(r)
```

**Q3.** What is the value of `x` after this line runs?
```
x = print("done")
```

**Q4.** This function has a `return` — a bare one, with nothing after it:
```
def stop(n):
    if n > 0:
        return
    return n
```
What comes back from `stop(5)`?

**Q5.** In one sentence: what is the difference between a function *showing* you a value and a function *handing back* a value?


ANSWER KEY
Q1- None
Q2- output is two lines: hello Cherine then None
Q3- x is None. done appeared on screen; that's not what got assigned
Q4- None. A bare return exits and hands back nothing
Q5- Showing = characters on screen, nothing handed back. Handing back = the value returns to your code

Notes:
Q1- print() displays a value, but it does not return that value. Its return value is always None. 
Python evaluates nested expressions from the inside outward. That single rule explains every example.
So type(print("x")) : Python first evaluates print("x") . This does two things: 
Displays x
retunrs None
then Python evaluates type(None)
which is <class 'NoneType'>

So type(print("x")) gives:
x
<class 'NoneType'>

Q2- print("done") + "!" 
Python first eval print("done") which displays : done
but returned value is always None
So Python tries to effectively calculate None + !
which gives an error because Python cannot concatenate None with a string.

To print done!, write:
print("done" + "!") or
print("done!")

So:
print("done") + "!"    # Tries to add "!" after print has returned None
print("done" + "!")    # Builds the string first, then prints it

Q3- len(print("hi"))
len(print("hi"))    # Print first, then incorrectly ask for len(None) (hi / len(None) / error)
print(len("hi"))    # Find the string's length first, then print 2

Q4- def greet(name):
    print("hello " + name)

r = greet("Cherine")            when this line runs, it gives hello Cherine
type(r)

But the function has no return statement. Python therefore supplies an implicit: return None
So the assignment becomes: r = None 
Therefore:
type(r) is <class 'NoneType'>


A FUNCTION THAT ONLY PRINTS:
def greet(name):
    print("hello " + name)
USAGE:
r = greet("Cherine")

RESULTS: 
Displayed: hello Cherine
Value stored in r: None

A FUNCTION THAT RETURNS A STRING:
def greet(name):
    return "hello " + name
Now:
  r = greet("Cherine")             
stores:
"hello Cherine"
Therefore:
type(r)
is:
<class 'str'>

So print() is for output to the screen.
return is for output from a function to the caller.

**Re-quiz — four questions.** 

**Q1.** Predict every line of output:

def total(a, b): print(a + b)

s = total(2, 3)
print(s + 1)

ANS:  5 
error since Nonetype + int

**Q2.** Using that same `greet`: what does `type(greet)` show, and what does `type(greet("Cherine"))` show? Why are they different?

def greet(name): print("hello " + name)

r = greet("Cherine")
type(r)

ANS: type(greet)  gives <class 'function'> and type(greet("Cherine")) calls the function first 
which returns None then type reports <class 'NoneType'>

**Q3.** Do these two hand back different things, or the same thing?

def f(): return
def g(): pass

ANS: bare return and pass both hand back None. No difference to the caller.


**Q4.** Someone writes `if greet("Cherine"):` expecting the branch to run when a greeting was produced. Explain why that's broken — without appealing to any rule about how `if` treats `None`.

greet("Cherine") returns None. A version that fails to greet anyone also returns None. Same value. Every time, in every case, no exceptions. So the if isn't broken because of some rule about how Python treats None in a condition. It's broken one level earlier: the value being tested never varies. Success and failure are indistinguishable from the return value, because the return value carries no information about what happened. Whatever if does with None, it does identically in both cases — so the branch you take has nothing to do with whether the greeting happened.
A test on a constant is not a test. That's the whole answer.



# Day 17 Warm-Up

1. What makes a .py file a module vs a script? Which one has top-level code that runs on import, and which should stay silent?
2. You have a class-free helpers.py. You import helpers at >>>, then edit a function. The running session still shows old behavior. One-line reason, and the fix.


1. A .py file is a module when another Python file imports it, and a script when you run it directly.

In your project:

read_edges.py    → module
helpers.py       → module
analyze_graph.py → script

The important part is that Python executes top-level statements when a file is imported. So if helpers.py contained:

print("hello")

at the top level, then merely doing:

import helpers

would print "hello".

That is why your imported modules, read_edges.py and helpers.py, should stay silent at the top level. They should mostly define functions that wait to be called and return results.

analyze_graph.py, on the other hand, is the script you deliberately run:

python analyze_graph.py

so it is appropriate for it to contain the coordinating calls and print() statements that produce the report.

The distinction to remember is:

Modules provide reusable functions and should not unexpectedly do work when imported; the script deliberately runs the workflow and produces output.

2. Reason: Python already loaded and cached helpers in the running interpreter, so editing the file on disk does not automatically replace the in-memory module.

Fix: exit and restart the REPL, then import it again:

>>> exit()
python3
>>> import helpers

Now Python loads the updated version.
----------------------------------------------------------------------------------------------------------------------------------------------------

# Day 17 — dataclasses. This is the first object-oriented tool of the phase, and it's the CPF's own Ch 6 content. Concept first, since classes are new territory.

So far your data has lived in loose pieces — a tuple (0, 1) for an edge, a dict {"ticker": "AAPL", ...} for a position. That works, but nothing bundles the data with a name and a shape. A class lets you define a new type — a template for objects that carry named fields together. A `dataclass` is Python's low-ceremony way to make one: you declare the fields, and Python generates the boilerplate (the constructor, the printing, etc.) for you.

The finance example from the Primer: a `Quote` — a market quote with a ticker, a bid price, an ask price, and a timestamp. Instead of juggling four loose variables or a dict, you bundle them into one Quote object.

Build it in a file. Create it:

code quote.py

(One word, quote.py, no space.) Then, the first two lines — the import and the decorator:
----------------------------------
from dataclasses import dataclass

@dataclass
class Quote:
----------------------------------
Walk it:

from dataclasses import dataclass — brings in the dataclass tool from Python's standard library. from X import Y pulls one specific name Y out of module X — a slightly different import form than the whole-module import helpers you know; here you grab just dataclass.
@dataclass — this is a decorator, a line starting with @ that sits directly above a class or function and modifies it. @dataclass tells Python "generate the standard boilerplate for this class." Take the @ syntax as given for now; the effect is what matters.
class Quote: — declares a new type named Quote. Class names use CapitalizedWords by convention (unlike functions/variables).

Type those three lines. Don't run yet — a class with no fields is incomplete. Tell me when they're in, and we add the four fields.
--------------------------------------------------------------------
Now the four fields — the named pieces of data every Quote carries. Indented inside the class, each field is name: type:

    ticker: str
    bid: float
    ask: float
    timestamp: str

Walk it:

# Each line declares a field: a name and its type. ticker: str means "every Quote has a ticker, which is a string." bid: float — a decimal price. And so on.

# The : type part is a type annotation — you're telling Python (and any reader) what kind of value each field holds. For a dataclass, these annotations are also what tells @dataclass which fields to generate the boilerplate for.

# They're indented one level (inside the class), and there's no = — you're declaring the shape, not assigning values yet. Values come when you create a Quote.

Type the four fields under class Quote:, save. **That's a complete dataclass now.**

Then test it in >>> — but this creates an instance (an actual Quote object), which is new. In the interpreter:

from quote import Quote
q = Quote("AAPL", 150.0, 150.2, "2026-08-08")
q

Walk the test:

from quote import Quote — pull the Quote class out of your quote.py file.
Quote("AAPL", 150.0, 150.2, "2026-08-08") — this creates a Quote object, passing the four values in field order (ticker, bid, ask, timestamp). @dataclass auto-generated the constructor that accepts these. q = stores the resulting object.
q on its own line — displays it.

Predict what q shows when displayed (dataclass auto-generates a readable form — think about what it'll look like). Run all three lines, show me.
--------------------------------------------------
>>> from quote import Quote
... q = Quote("AAPL", 150.0, 150.2, "2026-08-08")
... q
... 
Quote(ticker='AAPL', bid=150.0, ask=150.2, timestamp='2026-08-08')
>>> 
--------------------------------------------------
Quote(ticker='AAPL', bid=150.0, ask=150.2, timestamp='2026-08-08') — and that's the payoff. Notice what you got for free: a readable display showing every field with its name and value. You never wrote that. @dataclass auto-generated it (the __repr__), along with the constructor that accepted your four values in order. Compare to a plain class, where you'd hand-write both — that boilerplate is exactly what the decorator saves you.

# The thing to lock: a dataclass bundles named, typed fields into a new type, and the decorator generates the constructor and the readable representation automatically. Your q is now an object — one Quote, carrying four fields together, instead of four loose variables.

Now access individual fields — dot notation, like reaching into a module but for an object's data. Predict, then run:

q.ticker
q.bid
q.ask

q.ticker reaches the ticker field of the object q. Predict each ('AAPL', 150.0, 150.2), run, show me. Then we add a method — behavior that belongs to the class.

--------------------------------------------------
# PREDICTION:

>>> q.ticker
'AAPL'
>>> q.bid
150.0
>>> q.ask
150.2
>>> 
--------------------------------------------------
Correct — q.ticker → 'AAPL', q.bid → 150.0, q.ask → 150.2. Dot notation reaches each field of the object. Same dot you used to reach into a module (helpers.count_degrees), now reaching into an object's data.

Now the powerful part — **a method:** a function that lives inside the class and operates on the object's own data. A Quote has a bid and an ask; the mid-price (the midpoint) is a natural thing to compute from them. Instead of computing it outside, you give the class the ability to compute it itself.

Add this inside quote.py, indented at the same level as the fields (so it's part of the class), below the four fields:
-----------------------------------------
    def mid_price(self):
        return (self.bid + self.ask) / 2
-----------------------------------------
# Walk the new pieces:

`def mid_price(self):` — a method is just a def written inside the class. The first parameter, self, is special: it refers to the object the method is called on. Every method takes self first — it's how the method reaches the object's own fields.
`self.bid` and `self.ask` — inside the method, you reach the object's fields through self. self.bid means "this particular quote's bid." That's why self matters: it's the handle to the object's own data.
returns the average of bid and ask — the midpoint.

Type it, save. Then test — restart the interpreter first (you edited the file, so the old version is cached — the stale-import trap from Day 14):

exit()
python3
from quote import Quote
q = Quote("AAPL", 150.0, 150.2, "2026-08-08")
q.mid_price()

Note q.mid_price() — with parentheses, because it's a method call (unlike q.bid, a field, which has no parentheses). Predict what it returns (midpoint of 150.0 and 150.2), run, show me.
-------------------------------------------
>>> exit()
cherinefons@Mac foundation % python3
Python 3.14.6 (v3.14.6:c63aec69bd5, Jun 10 2026, 08:07:54) [Clang 21.0.0 (clang-2100.1.1.101)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> from quote import Quote
>>> q = Quote("AAPL", 150.0, 150.2, "2026-08-08")
>>> q.mid_price()
150.1
--------------------------------------------
# CONCLUSION

150.1 — the midpoint of 150.0 and 150.2, computed by the object on its own data. That's a method working: mid_price() reached into self.bid and self.ask and returned their average. The object doesn't just hold data now — it has behavior that belongs with it.

And notice the distinction you just used live: q.bid (field — no parentheses, it's stored data) vs q.mid_price() (method — parentheses, it's a computation). That's the field-vs-method difference, in your hands.
---------------------------------------------
# Last piece of Day 17 — a custom __str__ for a clean printed form. Right now printing q gives the full Quote(ticker='AAPL', ...) repr — fine for debugging, verbose for display. __str__ lets you define a concise human-readable string. Add inside the class, below mid_price:

    def __str__(self):
        return f"{self.ticker}: {self.bid}/{self.ask}"

Walk it:

__str__ is a special method (the double underscores mark it — "dunder"). Python calls it automatically when you print() an object. Defining it lets you control what printing shows.
It returns an f-string reaching the object's fields via self — here, AAPL: 150.0/150.2, a compact quote format.

Type it, save, restart, and test the difference:
---------------------------------------------
exit()
python3
from quote import Quote
q = Quote("AAPL", 150.0, 150.2, "2026-08-08")
print(q)
q
---------------------------------------------
Predict: print(q) uses your __str__ (concise), but q alone still shows the full repr. Two different forms, two purposes. Run, show me both:


>>> exit()
cherinefons@Mac foundation % python3
Python 3.14.6 (v3.14.6:c63aec69bd5, Jun 10 2026, 08:07:54) [Clang 21.0.0 (clang-2100.1.1.101)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> from quote import Quote
>>> q = Quote("AAPL", 150.0, 150.2, "2026-08-08")
>>> print(q)
AAPL: 150.0/150.2
>>> q
Quote(ticker='AAPL', bid=150.0, ask=150.2, timestamp='2026-08-08')
>>> 
------------------------------------------------
# CONCLUSION

There's the distinction, live on screen:

print(q) → AAPL: 150.0/150.2 — your custom __str__, the concise display form.
q alone → Quote(ticker='AAPL', bid=150.0, ask=150.2, timestamp='2026-08-08') — the auto-generated __repr__, the full debugging form.

**Two representations, two purposes.**
__str__ is what you define for humans reading output (print); __repr__ (which @dataclass gave you free) is the complete, unambiguous form for developers/debugging. Python picks __str__ when you print, __repr__ when you just evaluate the object. That's the Ch 6 Review Q2 distinction — and you just saw it rather than memorized it.

**That completes Day 17.** You built your first class: a Quote dataclass with four typed fields, a mid_price method operating on self, and a custom __str__ — the full "data plus behavior bundled into a type" package that CPF's Ch 6 is about, and the foundation for the Edge and Multigraph classes coming in a couple of days.
------------------------------------------------

# SIDE NOTE
__repr__ is the object's unambiguous, developer-facing representation — the string Python shows when you evaluate an object without printing it (like typing q alone at >>>), and it's meant to be complete and precise rather than pretty.

You just saw the contrast:

q alone → Quote(ticker='AAPL', bid=150.0, ask=150.2, timestamp='2026-08-08') — that's __repr__. Every field, labeled, exact.
print(q) → AAPL: 150.0/150.2 — that's __str__. Concise, for humans reading output.

The intended difference in purpose:

__repr__ answers "what is this object, exactly?" — for a developer debugging. The convention is that it should be detailed and, ideally, look like the code you'd type to recreate the object. Notice yours reads almost exactly like the Quote(...) call you'd write to make it — that's the ideal __repr__: unambiguous, reconstruction-like.
__str__ answers "how should this look to a person?" — for display, reports, user-facing output. Concise, readable, can drop detail.

Which one Python uses:

Type the object bare at >>>, or put it in a list, or when no __str__ exists → __repr__.
print(obj) or str(obj) → __str__ (and if you didn't define __str__, Python falls back to __repr__).
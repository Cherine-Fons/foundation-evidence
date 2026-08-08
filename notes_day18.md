# Day 18 — composition. Yesterday one class held data + behavior. Today: classes that contain other classes. This is composition — building bigger objects out of smaller ones — and it's how real models are structured.

The Primer's example, and it maps straight to your future Multigraph: a Position (a holding of some quantity of a ticker) and a Portfolio (a collection of positions). A portfolio has positions — that "has-a" relationship is composition.

Start with Position. Create the file:
---------------------------------------
code portfolio.py
---------------------------------------
First the import and the `Position` dataclass — a holding: a ticker, a quantity, and the price paid:

from dataclasses import dataclass

@dataclass
class Position:
    ticker: str
    quantity: int
    price: float
Same dataclass shape as Quote — decorator, class name, three typed fields. Type it (check indentation: import/decorator/class flush left, three fields at 4 spaces).

Then give Position a method — its market value at a given price (quantity × current price). Add inside the class, below the fields:

    def market_value(self, current_price):
        return self.quantity * current_price

Note this method takes self and a second parameter current_price — a method can accept arguments beyond self, same as any function. It reaches self.quantity (the object's own data) and multiplies by the passed-in current_price.

Type both, save. Then test in >>>:

from portfolio import Position
p = Position("AAPL", 10, 150.0)
p.market_value(155.0)

Predict what market_value(155.0) returns — 10 shares at 155.0. Run, show me.
---------------------------------------
cherinefons@Mac foundation % python3
Python 3.14.6 (v3.14.6:c63aec69bd5, Jun 10 2026, 08:07:54) [Clang 21.0.0 (clang-2100.1.1.101)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> from portfolio import Position
... p = Position("AAPL", 10, 150.0)
... p.market_value(155.0)
... 
1550.0
>>> 
---------------------------------------
# CONCLUSION

1550.0 — 10 shares × 155.0. The Position object computed its own market value from self.quantity and the passed-in price. First class of the day working.

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
_______________________________________

# Now the composition part — a Portfolio that contains Positions. This is the "has-a" relationship: a portfolio has a list of positions, and computes things across all of them.

In portfolio.py, below the Position class (flush left — a new top-level class), add:

@dataclass
class Portfolio:
    positions: list

Walk it:

Another @dataclass, flush left — a second class in the same file.
One field, positions: list — a Portfolio holds a list of Position objects. This is composition: the field's contents are other objects. A Portfolio has-a list of Positions.

Then give it a method to total the value across all positions, at a set of current prices. Add inside Portfolio (4 spaces):
---------------------------------------
    def total_value(self, prices):
        total = 0
        for pos in self.positions:
            total = total + pos.market_value(prices[pos.ticker])
        return total
---------------------------------------
Walk the method carefully — this is the rich part:

prices is a dict mapping ticker → current price (e.g. {"AAPL": 155.0}).
total = 0 — accumulator (your Week-2 pattern, back again).
for pos in self.positions: — loop over each Position object in the portfolio's list.
pos.market_value(prices[pos.ticker]) — for each position, call its own market_value method, passing the current price looked up by that position's ticker. So the Portfolio delegates to each Position's behavior. That delegation is the payoff of composition — the Portfolio doesn't recompute value; it asks each Position.
accumulate into total, return it.

Type it, save. Then predict before testing: two positions, at given prices — walk the total by hand. Tell me when it's typed and I'll give you the test call.
---------------------------------------

Now test it. In >>>, build a portfolio of two positions and total it at given prices:

from portfolio import Position, Portfolio
p1 = Position("AAPL", 10, 150.0)
p2 = Position("MSFT", 5, 400.0)
port = Portfolio([p1, p2])
prices = {"AAPL": 155.0, "MSFT": 410.0}
port.total_value(prices)

Walk it before running:

import both classes (Position, Portfolio — comma-separated).
make two Position objects.
Portfolio([p1, p2]) — create a portfolio, passing a list of the two positions as its positions field. Composition in action: the portfolio contains the position objects.
prices — a dict of current prices per ticker.
port.total_value(prices) — total across both positions.

Predict on paper first: AAPL is 10 × 155.0, MSFT is 5 × 410.0. Add them. What's the total?

Run it, show me your prediction and the result.

---------------------------------------
exit()
python3
from portfolio import Position, Portfolio
p1 = Position("AAPL", 10, 150.0)
p2 = Position("MSFT", 5, 400.0)
port = Portfolio([p1, p2])
prices = {"AAPL": 155.0, "MSFT": 410.0}
port.total_value(prices)
---------------------------------------
# INTERPRETER

cherinefons@Mac foundation % python3
Python 3.14.6 (v3.14.6:c63aec69bd5, Jun 10 2026, 08:07:54) [Clang 21.0.0 (clang-2100.1.1.101)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> from portfolio import Position, Portfolio
>>> p1 = Position("AAPL", 10, 150.0)
>>> p2 = Position("MSFT", 5, 400.0)
>>> port = Portfolio([p1, p2])
>>> prices = {"AAPL": 155.0, "MSFT": 410.0}
>>> port.total_value(prices)
3600.0
>>> 
----------------------------------------
# CONCLUSION

3600.0 — AAPL 10 × 155 = 1550, MSFT 5 × 410 = 2050, summed to 3600. The composition worked: the Portfolio looped its contained Position objects and delegated to each one's market_value. That delegation is the whole point — the Portfolio didn't recompute anything; it asked each Position to value itself.

That's composition, and it's the pattern behind your Multigraph in two days: a Multigraph will contain a collection of Edge objects and delegate to compute properties across them — structurally identical to Portfolio containing Positions.




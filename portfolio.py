from dataclasses import dataclass


@dataclass
class Position:
    ticker: str
    quantity: int
    price: float

    def market_value(self, current_price):
        return self.quantity * current_price    
    
@dataclass
class Portfolio:
    positions: list
    def total_value(self, prices):
        total = 0
        for pos in self.positions:
            total = total + pos.market_value(prices[pos.ticker])
        return total    
from dataclasses import dataclass

@dataclass
class Position:
    ticker: str
    quantity: int
    price: float
    
    def market_value(self, current_price):
        return self.quantity * current_price    
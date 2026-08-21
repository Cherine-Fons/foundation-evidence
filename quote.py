from dataclasses import dataclass


@dataclass
class Quote:
    ticker: str
    bid: float
    ask: float
    timestamp: str
    def mid_price(self):
        return (self.bid + self.ask) / 2
    def __str__(self):
        return f"{self.ticker}: {self.bid}/{self.ask}"
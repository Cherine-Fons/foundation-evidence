import pandas as pd


df = pd.DataFrame(
    {
        "date": ["2026-07-13", "2026-07-13", "2026-07-14", "2026-07-14"],
        "ticker": ["AAPL", "MSFT", "AAPL", "MSFT"],
        "price": [100.0, 200.0, 102.0, 205.0],
    }
)

wide = df.pivot(index="date", columns="ticker", values="price")

print(wide)
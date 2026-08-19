import pandas as pd

prices = pd.Series(
    [100.0, 102.0, 101.0],
    index=["2026-07-13", "2026-07-14", "2026-07-15"],
)

print(prices)
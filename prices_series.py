import pandas as pd

# Create a labeled pandas Series
prices = pd.Series(
    [100.0, 102.0, 101.0],
    index=["2026-07-13", "2026-07-14", "2026-07-15"],
)

print(prices)


# Create a DataFrame with two columns sharing the same date index
df = pd.DataFrame(
    {
        "price": [100.0, 102.0, 101.0],
        "volume": [1500, 1800, 1200],
    },
    index=["2026-07-13", "2026-07-14", "2026-07-15"],
)

print(df)


# Add a new return column using day-over-day fractional price change
df["return"] = df["price"].pct_change()

print(df)
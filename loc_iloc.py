import pandas as pd

df = pd.DataFrame(
    {
        "price": [100.0, 102.0, 101.0],
        "volume": [1500, 1800, 1200],
    },
    index=["2026-07-13", "2026-07-14", "2026-07-15"],
)

print("--- before sort ---")
print(df.loc["2026-07-15"])
print(df.iloc[2])

df = df.sort_values("price")

print("--- after sort by price ---")
print(df.loc["2026-07-15"])
print(df.iloc[2])
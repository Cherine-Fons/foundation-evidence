import pandas as pd

df = pd.DataFrame(
    {
        "sector": ["tech", "tech", "energy", "energy"],
        "return": [0.02, 0.04, -0.01, 0.03],
    }
)

print(df.groupby("sector")["return"].mean())
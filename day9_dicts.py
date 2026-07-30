pairs = [("AAPL", "tech"), ("XOM", "energy"), ("MSFT", "tech"), ("CVX", "energy"), ("NVDA", "tech")]
by_sector = {}
for ticker, sector in pairs:
    if sector not in by_sector:
        by_sector[sector] = [ticker]
    else:
        by_sector[sector].append(ticker)
print(by_sector)


foods = ["apple", "banana", "apple", "apple", "banana", "cherry"]
counts = {}
for food in foods:
    if food not in counts:
        counts[food] = 1
    else:
        counts[food] = counts[food] + 1
print(counts)


foods = {
    "apple": {"group": "fruit", "recent": [3, 4, 3]},
    "carrot": {"group": "vegetable", "recent": [2, 2]},
    "banana": {"group": "fruit", "recent": [5, 6, 5]},
}


# drop rule: if a food's combined quantity is 0, do not include it in the result
basket1 = {"apple": 3, "banana": 2, "cherry": 0}
basket2 = {"banana": 4, "cherry": 0, "date": 5}
combined = {}
for food, qty in basket1.items():
    if food not in combined:
        combined[food] = qty
    else:
        combined[food] = combined[food] + qty
for food, qty in basket2.items():
    if food not in combined:
        combined[food] = qty
    else:
        combined[food] = combined[food] + qty
result = {}
for food, qty in combined.items():
    if qty != 0:
        result[food] = qty
print(result)        
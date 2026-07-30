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

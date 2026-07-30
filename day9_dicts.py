pairs = [("AAPL", "tech"), ("XOM", "energy"), ("MSFT", "tech"), ("CVX", "energy"), ("NVDA", "tech")]
by_sector = {}
for ticker, sector in pairs:
    if sector not in by_sector:
        by_sector[sector] = [ticker]
    else:
        by_sector[sector].append(ticker)
print(by_sector)
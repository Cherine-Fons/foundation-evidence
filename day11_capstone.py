positions = [
    {"ticker": "AAPL", "quantity": 10, "price": 150},
    {"ticker": "MSFT", "quantity": 5, "price": 400},
    {"ticker": "NVDA", "quantity": 8, "price": 120},
]
def total_value(positions):
    total = 0
    for p in positions:
        total = total + p["quantity"] * p["price"]
    return total
print(total_value(positions))

def above_threshold(positions, threshold):
    result = []
    for p in positions:
        value = p["quantity"] * p["price"]
        if value > threshold:
            result.append(p["ticker"])
    return result

print(above_threshold(positions, 1500))
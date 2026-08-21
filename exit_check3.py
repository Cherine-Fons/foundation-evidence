import numpy as np

# Task 1 — vectorize a loop
# Original loop:
# prices = np.array([100.0, 102.0, 101.0, 105.0, 103.0])
# result = []
# for i in range(len(prices)):
#     result.append(prices[i] * 1.05)

prices = np.array([100.0, 102.0, 101.0, 105.0, 103.0])

result = prices * 1.05

print(result)

# Prediction / expected output:
# [105.   107.1  106.05 110.25 108.15]


# Task 2 — broadcasting
# (a) (4, 3) + (3,) → broadcasts, result shape (4, 3)
# (b) (4, 3) + (4,) → ValueError
# (c) (4, 1) + (1, 3) → broadcasts, result shape (4, 3)

a = np.ones((4, 3))
b1 = np.array([1, 2, 3])

print((a + b1).shape)

# This would raise ValueError because (4, 3) and (4,) do not broadcast:
# b2 = np.array([1, 2, 3, 4])
# print(a + b2)

c1 = np.ones((4, 1))
c2 = np.ones((1, 3))

print((c1 + c2).shape)

# Expected output:
# (4, 3)
# (4, 3)


# Task 3 — boolean-mask selection
returns = np.array([0.02, -0.01, 0.0, -0.03, 0.015, -0.008])

negative_returns = returns[returns < 0]

print(negative_returns)

# Prediction / expected output:
# [-0.01  -0.03  -0.008]


# Task 4 — axis reasoning
# Given a (3, 4) array: 3 assets, 4 days.
# We want one average return per asset.
# The named axis disappears, so axis=1 removes the 4-day dimension.

data = np.array([
    [0.01, 0.02, 0.03, 0.04],
    [0.05, 0.06, 0.07, 0.08],
    [0.09, 0.10, 0.11, 0.12]
])

average_per_asset = data.mean(axis=1)

print(average_per_asset)
print(average_per_asset.shape)

# Expected output:
# [0.025 0.065 0.105]
# (3,)
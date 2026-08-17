import matplotlib.pyplot as plt

asset_a = [0.012, -0.008, 0.0, 0.021, -0.015, 0.006, 0.009, -0.004, 0.011, -0.002]
asset_b = [0.010, -0.006, 0.002, 0.018, -0.012, 0.008, 0.007, -0.003, 0.013, 0.000]

fig, ax = plt.subplots()

ax.scatter(asset_a, asset_b)

ax.set_title("Asset A vs Asset B returns")
ax.set_xlabel("Asset A return")
ax.set_ylabel("Asset B return")

fig.savefig("artifacts/returns_scatter.png")

plt.show()

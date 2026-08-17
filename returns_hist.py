import matplotlib.pyplot as plt

returns = [0.012, -0.008, 0.0, 0.021, -0.015, 0.006, 0.009, -0.004, 0.011, -0.002]

fig, ax = plt.subplots()

ax.hist(returns)
ax.axvline(0, color="red", linestyle="--")

fig.savefig("artifacts/returns_hist.png")

ax.set_title("Distribution of returns")
ax.set_xlabel("Return")
ax.set_ylabel("Frequency")

plt.show()
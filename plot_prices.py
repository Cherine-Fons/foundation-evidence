import matplotlib.pyplot as plt

prices = [100, 102, 101, 104, 103]
days = [1, 2, 3, 4, 5]

fig, ax = plt.subplots()

ax.plot(days, prices)

ax.set_title("Price over 5 days")
ax.set_xlabel("Day")
ax.set_ylabel("Price")

fig.savefig("artifacts/prices.png")

plt.show()
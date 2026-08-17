import matplotlib.pyplot as plt

days = [1, 2, 3, 4, 5, 6]
prices = [100, 102, 101, 104, 103, 105]
returns = [0.0, 0.02, -0.0098, 0.0297, -0.0096, 0.0194]

fig, (ax_top, ax_bottom) = plt.subplots(2, 1, sharex=True)

ax_top.plot(days, prices)
ax_top.set_title("Prices and returns")
ax_top.set_ylabel("Price")

ax_bottom.plot(days, returns)
ax_bottom.set_ylabel("Return")
ax_bottom.set_xlabel("Day")

fig.savefig("artifacts/two_panel.png")

plt.show()

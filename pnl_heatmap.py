import numpy as np
import matplotlib.pyplot as plt

from pricing import black_scholes

# Set Values
K = 105
r = 0.05
T = 1

purchase_price = 8.02

contracts = int(input("Number of contracts: "))
contract_multiplier = 100

# Grid
stock_prices = np.arange(80, 121, 2)

volatilities = np.arange(0.10, 0.41, 0.02)


# Profit and Loss
pnl_prices = []

for stock in stock_prices:

    row = []

    for vol in volatilities:

        call, put, d1, d2 = black_scholes(stock, K, r, vol, T)

        pnl = ((call - purchase_price) * contracts * contract_multiplier)

        row.append(pnl)

    pnl_prices.append(row)

pnl_prices = np.array(pnl_prices)

# Plotting
heatmap = plt.imshow(pnl_prices, extent=[volatilities[0], volatilities[-1], stock_prices[0], stock_prices[-1]], aspect="auto", origin="lower", cmap="RdYlGn") # Red=losses, Green=profits

# Break-even contour
contour = plt.contour(volatilities, stock_prices, pnl_prices, levels=[0], colors="black", linewidths=2)

plt.clabel(contour, fmt="Break-even", fontsize=10)

plt.colorbar(heatmap, label="Position P&L ($)")

plt.xticks(volatilities[::2], [f"{v:.0%}" for v in volatilities[::2]])

plt.xlabel("Implied Volatility")
plt.ylabel("Underlying Stock Price ($)")
plt.title("Black-Scholes Call Option Position P&L")

plt.tight_layout()

plt.savefig("position_pnl_heatmap.png", dpi=300)

plt.show()
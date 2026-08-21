import numpy as np
from pricing import black_scholes
import matplotlib.pyplot as plt

# Fixed Black-Scholes inputs
K = 105
r = 0.05
T = 1

# Stock prices: $80 → $120
stock_prices = np.arange(80, 121, 2)

# Volatility: 10% → 40%
volatilities = np.arange(0.10, 0.41, 0.02)

# Store call prices
call_prices = []

# Calculate every combination
for stock in stock_prices:

    row = []

    for vol in volatilities:
        call, put, d1, d2 = black_scholes(stock, K, r, vol, T)
        row.append(call)

    call_prices.append(row)

# Convert list into NumPy array
call_prices = np.array(call_prices)

# Heatmap
plt.imshow(call_prices, extent=[volatilities[0], volatilities[-1], stock_prices[0], stock_prices[-1]], aspect="auto", origin="lower")

# Color Scale
plt.colorbar(label="Call Option Price")

# Labels
plt.xlabel("Volatility")
plt.ylabel("Stock Price")
plt.title("Black-Scholes Call Price Sensitivity")

# Volatility display as percentages
plt.xticks(volatilities[::2], [f"{v:.0%}" for v in volatilities[::2]])

plt.savefig("call_heatmap.png")
plt.show()
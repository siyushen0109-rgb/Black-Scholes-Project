import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

from pricing import black_scholes
from greeks import calculate_greeks

def validate_inputs(S, K, r, sigma, T):

    if S <= 0:
        raise ValueError("Stock price must be positive.")

    if K <= 0:
        raise ValueError("Strike price must be positive.")

    if sigma <= 0:
        raise ValueError("Volatility must be positive.")

    if T <= 0:
        raise ValueError("Time to expiry must be positive.")

# Test function

S = float(input("Stock Price: "))
K = float(input("Strike Price: "))
r = float(input("Risk-Free Rate (%): ")) / 100
sigma = float(input("Volatility (%): ")) / 100
T = float(input("Time to Expiry (years): "))

validate_inputs(S, K, r, sigma, T)

call, put, d1, d2 = black_scholes(S, K, r, sigma, T)
call_delta, put_delta, gamma, vega, theta_call, rho_call = calculate_greeks(S, K, r, sigma, T, d1, d2)

# P&L Calculation
purchase_price = call
current_price = float(input("Enter current option price: "))
contracts = int(input("Enter number of contracts: "))

contract_multiplier = 100

pnl_per_option = current_price - purchase_price

total_pnl = (pnl_per_option * contracts * contract_multiplier)

print()
print("P&L")
print("-" * 40)
print(f"Purchase Price:  ${purchase_price:.2f}")
print(f"Current Price:   ${current_price:.2f}")
print(f"P&L per option:  ${pnl_per_option:.2f}")
print(f"Contracts:       {contracts}")
print(f"Total P&L:       ${total_pnl:.2f}")

print()
print("=" * 40)
print("       BLACK-SCHOLES OPTION PRICER")
print("=" * 40)

print()
print("OPTION PRICES")
print("-" * 40)
print(f"Call Price: ${call:.2f}")
print(f"Put Price: ${put:.2f}")

print()
print("GREEKS")
print("-" * 40)
print(f"Call Delta: {call_delta:.4f}")
print(f"Put Delta:  {put_delta:.4f}")
print(f"Gamma:      {gamma:.4f}")
print(f"Vega:       {vega:.2f}")
print(f"Call Theta: {theta_call:.4f}")
print(f"Call Rho:   {rho_call:.2f}")

print("=" * 40)

# Sensitivity Code

stock_prices = np.arange(80, 121, 1)

call_prices = []
put_prices = []

for stock_price in stock_prices:
    call, put, d1, d2 = black_scholes(stock_price, K, r, sigma, T)

    call_prices.append(call)
    put_prices.append(put)

# Plotting
plt.plot(stock_prices, call_prices, label="Call")
plt.plot(stock_prices, put_prices, label ="Put")

plt.xlabel("Stock Price")
plt.ylabel("Call Price")
plt.title("Call Price vs Stock Price")

plt.legend()
plt.grid()

plt.savefig("call_price_graph.png")
plt.show()

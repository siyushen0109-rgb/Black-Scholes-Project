import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from pricing import black_scholes
from greeks import calculate_greeks
from implied_volatility import implied_volatility

# --------------------------------------------------
# Heading
# --------------------------------------------------

st.set_page_config(
    page_title="Black-Scholes Option Pricer",
    page_icon="📈",
    layout="wide"
)

st.title("Black-Scholes Option Pricer")
st.caption(
    "Interactive option valuation, Greeks, implied volatility, "
    "scenario analysis, and position risk."
)

# --------------------------------------------------
# Inputs
# --------------------------------------------------

option_type = st.selectbox(
    "Option Type",
    ["Call", "Put"]
)

st.caption(f"Selected position: {option_type}")

col1, col2 = st.columns(2)

with col1:
    stock_price = st.slider(
        "Stock Price",
        min_value=50.0,
        max_value=150.0,
        value=100.0,
        step=1.0
    )

    strike_price = st.slider(
        "Strike Price",
        min_value=50.0,
        max_value=150.0,
        value=105.0,
        step=1.0
    )

    volatility = st.slider(
        "Volatility (%)",
        min_value=0.10,
        max_value=0.40,
        value=0.20,
        step=0.01
    )

with col2:
    risk_free_rate = st.slider(
        "Risk-Free Rate",
        min_value=0.0,
        max_value=0.10,
        value=0.05,
        step=0.01
    )

    T = st.slider(
        "Time to Expiration",
        min_value=0.1,
        max_value=2.0,
        value=1.0,
        step=0.1
    )

    purchase_price = st.number_input(
        "Purchase Price",
        min_value=0.01,
        value=8.02,
        step=0.01
    )

contracts = st.number_input(
    "Number of Contracts",
    min_value=1,
    value=10,
    step=1
)

contract_multiplier = 100

# --------------------------------------------------
# Option Valution
# --------------------------------------------------

call, put, d1, d2 = black_scholes(
    stock_price,
    strike_price,
    risk_free_rate,
    volatility,
    T
)

if option_type == "Call":
    option_price = call
else:
    option_price = put

st.divider()
st.subheader("Option Valuation")

market_price = st.number_input(
    "Market Option Price",
    min_value=0.01,
    value=10.00,
    step=0.01
)

iv = implied_volatility(
    market_price=market_price,
    S=stock_price,
    K=strike_price,
    r=risk_free_rate,
    T=T,
    option_type=option_type
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Call Price", f"${call:.2f}")

with col2:
    st.metric("Put Price", f"${put:.2f}")

with col3:
    if iv is not None:
        st.metric("Implied Volatility", f"{iv:.2%}")
    else:
        st.metric("Implied Volatility", "N/A")

# --------------------------------------------------
# Current Greeks
# --------------------------------------------------

(
    call_delta,
    put_delta,
    gamma,
    vega,
    theta_call,
    theta_put,
    rho_call,
    rho_put
) = calculate_greeks(
    stock_price,
    strike_price,
    risk_free_rate,
    volatility,
    T,
    d1,
    d2
)

if option_type == "Call":
    selected_delta = call_delta
    selected_theta = theta_call
    selected_rho = rho_call
else:
    selected_delta = put_delta
    selected_theta = theta_put
    selected_rho = rho_put

st.subheader(f"{option_type} Greeks")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Delta", f"{selected_delta:.4f}")

with col2:
    st.metric("Gamma", f"{gamma:.4f}")

with col3:
    st.metric("Vega", f"{vega:.2f}")

col1, col2 = st.columns(2)

with col1:
    st.metric("Theta", f"{selected_theta:.4f}")

with col2:
    st.metric("Rho", f"{selected_rho:.2f}")


# --------------------------------------------------
# Scenario Analysis
# --------------------------------------------------

st.divider()
st.subheader("Scenario Analysis")

col1, col2 = st.columns(2)

with col1:
    scenario_stock_price = st.number_input(
        "Scenario Stock Price",
        min_value=1.0,
        value=stock_price,
        step=1.0
    )

with col2:
    scenario_volatility = st.number_input(
        "Scenario Volatility (%)",
        min_value=0.01,
        max_value=1.00,
        value=volatility,
        step=0.01
    )

scenario_call, scenario_put, scenario_d1, scenario_d2 = black_scholes(
    scenario_stock_price,
    strike_price,
    risk_free_rate,
    scenario_volatility,
    T
)

if option_type == "Call":
    scenario_option_price = scenario_call
else:
    scenario_option_price = scenario_put


# --------------------------------------------------
# Current vs Scenario Price
# --------------------------------------------------

st.markdown("#### Option Price Comparison")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        f"Current {option_type} Price",
        f"${option_price:.2f}"
    )

with col2:
    st.metric(
        f"Scenario {option_type} Price",
        f"${scenario_option_price:.2f}",
        delta=f"${scenario_option_price - option_price:.2f}"
    )


# --------------------------------------------------
# Scenario Greeks
# --------------------------------------------------

(
    scenario_call_delta,
    scenario_put_delta,
    scenario_gamma,
    scenario_vega,
    scenario_theta_call,
    scenario_theta_put,
    scenario_rho_call,
    scenario_rho_put
) = calculate_greeks(
    scenario_stock_price,
    strike_price,
    risk_free_rate,
    scenario_volatility,
    T,
    scenario_d1,
    scenario_d2
)

if option_type == "Call":
    scenario_selected_delta = scenario_call_delta
    scenario_selected_theta = scenario_theta_call
    scenario_selected_rho = scenario_rho_call
else:
    scenario_selected_delta = scenario_put_delta
    scenario_selected_theta = scenario_theta_put
    scenario_selected_rho = scenario_rho_put


# --------------------------------------------------
# Current vs Scenario Greeks
# --------------------------------------------------

st.markdown("#### Greeks Comparison")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Current Delta",
        f"{selected_delta:.4f}"
    )
    st.metric(
        "Current Gamma",
        f"{gamma:.4f}"
    )
    st.metric(
        "Current Vega",
        f"{vega:.2f}"
    )
    st.metric(
        "Current Theta",
        f"{selected_theta:.4f}"
    )
    st.metric(
        "Current Rho",
        f"{selected_rho:.2f}"
    )

with col2:
    st.metric(
        "Scenario Delta",
        f"{scenario_selected_delta:.4f}"
    )
    st.metric(
        "Scenario Gamma",
        f"{scenario_gamma:.4f}"
    )
    st.metric(
        "Scenario Vega",
        f"{scenario_vega:.2f}"
    )
    st.metric(
        "Scenario Theta",
        f"{scenario_selected_theta:.4f}"
    )
    st.metric(
        "Scenario Rho",
        f"{scenario_selected_rho:.2f}"
    )


# --------------------------------------------------
# Current vs Scenario Position P&L
# --------------------------------------------------

current_pnl = (
    (option_price - purchase_price)
    * contracts
    * contract_multiplier
)

scenario_pnl = (
    (scenario_option_price - purchase_price)
    * contracts
    * contract_multiplier
)

st.markdown("#### Position P&L")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Current Position P&L",
        f"${current_pnl:,.2f}"
    )

with col2:
    st.metric(
        "Scenario Position P&L",
        f"${scenario_pnl:,.2f}",
        delta=f"${scenario_pnl - current_pnl:,.2f}"
    )


# --------------------------------------------------
# Scenario Ranges
# --------------------------------------------------

stock_prices = np.arange(
    stock_price - 20,
    stock_price + 21,
    2
)

volatilities = np.arange(
    max(0.05, volatility - 0.15),
    min(0.60, volatility + 0.16),
    0.02
)


# --------------------------------------------------
# Position P&L Grid
# --------------------------------------------------

pnl_prices = []

for stock in stock_prices:
    row = []

    for vol in volatilities:
        (
            heatmap_call,
            heatmap_put,
            heatmap_d1,
            heatmap_d2
        ) = black_scholes(
            stock,
            strike_price,
            risk_free_rate,
            vol,
            T
        )

        if option_type == "Call":
            heatmap_option_price = heatmap_call
        else:
            heatmap_option_price = heatmap_put

        pnl = (
            (heatmap_option_price - purchase_price)
            * contracts
            * contract_multiplier
        )

        row.append(pnl)

    pnl_prices.append(row)

pnl_prices = np.array(pnl_prices)


# --------------------------------------------------
# Position P&L Heatmap
# --------------------------------------------------

st.subheader("Position P&L Heatmap")

fig, ax = plt.subplots()

heatmap = ax.imshow(
    pnl_prices,
    extent=[
        volatilities[0],
        volatilities[-1],
        stock_prices[0],
        stock_prices[-1]
    ],
    origin="lower",
    aspect="auto",
    cmap="RdYlGn"
)

# Current position marker
ax.scatter(
    volatility,
    stock_price,
    marker="o",
    s=80,
    edgecolors="black",
    facecolors="white",
    label="Current"
)

# Scenario position marker
ax.scatter(
    scenario_volatility,
    scenario_stock_price,
    marker="X",
    s=100,
    edgecolors="black",
    label="Scenario"
)

ax.legend()

# Break-even line
if np.min(pnl_prices) <= 0 <= np.max(pnl_prices):
    contour = ax.contour(
        volatilities,
        stock_prices,
        pnl_prices,
        levels=[0],
        colors="black",
        linewidths=2
    )

    ax.clabel(
        contour,
        fmt="Break-even",
        fontsize=10
    )

# Labels
ax.set_xlabel("Implied Volatility")
ax.set_ylabel("Stock Price ($)")
ax.set_title(
    f"Black-Scholes {option_type} Option Position P&L"
)

fig.colorbar(
    heatmap,
    ax=ax,
    label="Position P&L ($)"
)

st.pyplot(fig)

plt.close(fig)
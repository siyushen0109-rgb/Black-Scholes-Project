import numpy as np

from pricing import black_scholes
from greeks import calculate_greeks

def implied_volatility(
    market_price,
    S,
    K,
    r,
    T,
    option_type,
    initial_guess=0.20,
    tolerance=1e-6,
    max_iterations=100
):

    discounted_strike = K * np.exp(-r * T)

    if option_type == "Call":
        lower_bound = max(0, S - discounted_strike)
        upper_bound = S
    else:
        lower_bound = max(0, discounted_strike - S)
        upper_bound = discounted_strike

    if market_price < lower_bound or market_price > upper_bound:
        return None

    sigma = initial_guess

    for _ in range(max_iterations):

        # Calculate option price using sigma
        call, put, d1, d2 = black_scholes(
            S,
            K,
            r,
            sigma,
            T
        )

        if option_type == "Call":
            model_price = call
        else:
            model_price = put

        # Calculate pricing error
        price_error = model_price - market_price

        # Are we close enough?
        if abs(price_error) < tolerance:
            return sigma

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
            S,
            K,
            r,
            sigma,
            T,
            d1,
            d2
        )

        if abs(vega) < 1e-8:
            return None

        sigma = sigma - price_error / vega

        if sigma <= 0:
            return None

    return None
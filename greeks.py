import numpy as np
from scipy.stats import norm


def calculate_greeks(S, K, r, sigma, T, d1, d2):
    # Delta
    call_delta = norm.cdf(d1)
    put_delta = norm.cdf(d1) - 1

    # Gamma
    gamma = norm.pdf(d1) / (
        S * sigma * np.sqrt(T)
    )

    # Vega
    vega = (
        S
        * norm.pdf(d1)
        * np.sqrt(T)
    )

    # Theta
    common_theta_term = (
        -S
        * norm.pdf(d1)
        * sigma
        / (2 * np.sqrt(T))
    )

    theta_call = (
        common_theta_term
        - r
        * K
        * np.exp(-r * T)
        * norm.cdf(d2)
    )

    theta_put = (
        common_theta_term
        + r
        * K
        * np.exp(-r * T)
        * norm.cdf(-d2)
    )

    # Rho
    rho_call = (
        K
        * T
        * np.exp(-r * T)
        * norm.cdf(d2)
    )

    rho_put = (
        -K
        * T
        * np.exp(-r * T)
        * norm.cdf(-d2)
    )

    return (
        call_delta,
        put_delta,
        gamma,
        vega,
        theta_call,
        theta_put,
        rho_call,
        rho_put,
    )
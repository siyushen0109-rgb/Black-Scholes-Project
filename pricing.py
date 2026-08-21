import numpy as np
from scipy.stats import norm


def black_scholes(S, K, r, sigma, T):
    # d1
    d1 = (
        np.log(S / K)
        + (r + 0.5 * sigma**2) * T
    ) / (sigma * np.sqrt(T))

    # d2
    d2 = d1 - sigma * np.sqrt(T)

    # Call price
    call_price = (
        S * norm.cdf(d1)
        - K * np.exp(-r * T) * norm.cdf(d2)
    )

    # Put price
    put_price = (
        K * np.exp(-r * T) * norm.cdf(-d2)
        - S * norm.cdf(-d1)
    )

    return call_price, put_price, d1, d2

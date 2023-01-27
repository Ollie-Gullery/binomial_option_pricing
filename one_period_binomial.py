import numpy as np


def one_period_binomial(S0, u, d, K, r, option_type='c'):
    Su, Sd = S0 * u, S0*d
    if option_type == 'c':
        Cu = max(Su - K, 0)
        Cd = max(Sd - K, 0)
    elif option_type == 'p':
        Cu = max(K - Su, 0)
        Cd = max(K - Sd, 0)
    q = (np.exp(r) - d) / (u - d)  # risk neutral probability

    option_price = (Cu * q + Cd * (1 - q)) / np.exp(r)
    return option_price

import numpy as np

# Binomial Option Pricing for European Call Option

# Initializing Parameters
S0 = 120
K = 120
T = 1  # Time to maturity in years
r = 0.04
N = 3  # number of time steps
u = 1.2
d = 1 / u  # We make d the reciprocal of u to ensure we have a balanced tree
option_type = 'C'



def binomial_tree(K, T, S0, r, N, u, d, option_type='C'):
    # Calculating Discount Rate
    dt = T / N  # timestep
    discount_rate = np.exp(-r * dt)  # e^-rt

    # Calculating Risk Neutral Probability
    q = (np.exp(r * dt) - d) / (u - d)

    # Initialising asset price at maturity
    S = np.zeros(N + 1)

    S[0] = S0 * d ** N  # If we think of our vector in terms of (i, j) this is position (N, 0)

    for j in range(1, N + 1):  # We reverse our way through the tree from (N,0) to (N,1) etc.
        S[j] = S[
                   j - 1] * u / d  # This gives us the array 'S' which contains values for the vector at the end of
        # the binomial tree

    # array of payoff at maturity
    C = np.zeros(N + 1)
    for j in range(0, N + 1):
        C[j] = max(0, S[j] - K)  # payoff for call option

    # discount payoff back through tree
    for i in np.arange(N, 0, -1):
        for j in range(0, i): # discount back i periods
            expected_value_option = (q * C[j + 1] + (1 - q) * C[j])
            C[j] = discount_rate * expected_value_option

    return C[0]

print(binomial_tree(K, T, S0, r, N, u, d, option_type='C'))

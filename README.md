# binomial_option_pricing
Attempts of implementing binomial option model learned in investment theory class into python, starting of with one period binomial mode then for binomial model with multiple periods.

# One-Period Binomial Model
#### Parameters / Variables
```python
S0 = 120 # Inital Stock Price
K = 120 # Strike Price
T = 1  # Time to maturity in years
r = 0.04 # Risk free rate
N = 3  # number of time steps for multiple period model
u = 1.2 # up factor
d = 1 / u  # down factor - We make d the reciprocal of u to ensure we have a balanced tree
option_type = 'C'
```
We can begin by finding the formula for the price of a call option through its stock price **S0** where **Su** is `S0 * up factor` and **Sd** is `S0 * down factor`.

We can then find the probability `q (risk netural probability)` of the stock going up which and use `1-q` to find the probability of the stock going down similar to the expected value of the call option. We can then find the payoff through the express `payoff = max(Su-K, 0)` where `Cu` and `Cd` are the payoffs for up or down. Due to the *law of no arbitrage* we can discount this payoff by `e^rt` or `e^r` (as t = 1) to find the current Call price.

Formula for initial Call price:

$$ S0 = \frac{q*Su + (1-q)*Sd}{1 + r} $$

We can rearrange to find `q`:

$$ S0 = \frac{S0(qu - qd + d)}{1 + r} $$

`S0` cancels out such that:

$$ 1 = \frac{qu - qd + d}{1 + r} $$

Finally we can find the `risk neutral probability q` through:

$$ q = \frac{(1 + r) - d}{u - d} $$

## Python Implementation for One-Period Binomial Option Pricing
```python
import numpy as np

def one_period_binomial(S0, u, d, K, r, option_type='c'):
    Su = S0 * u
    Sd = S0*d 
    if option_type == 'c':
        Cu = max(Su - K, 0) # Payoff Cu
        Cd = max(Sd - K, 0) # Payoff Cd
    elif option_type == 'p':
        Cu = max(K - Su, 0) # Payoff Cu
        Cd = max(K - Sd, 0) # Payoff Cd
    q = (np.exp(r) - d) / (u - d)  # risk neutral probability equation

    option_price = (Cu * q + Cd * (1 - q)) / np.exp(r) # discount back one period e^r
    return option_price

```

# Multiple - Period Binomial Pricing for Call Option

For a three period binomial model in one year we can vectorise our tree in terms of `(i, j)` :


<img width="300" alt="image" src="https://user-images.githubusercontent.com/115392875/215066749-9299f135-4be1-4ca1-b178-4d1971b5ae00.png">

Through drawing out the tree, you notice that you can represent u and using i and j: `u^j` and `d^(i-j)`. You can use this to find stock prices at maturity

## Python Implementation Multiple Period 

#### Calculating Constants
```python
def multi_period_binomial_tree(K, T, S0, r, N, u, d, option_type='C'):
    # Calculating Discount Rate
    dt = T / N  # timestep
    discount_rate = np.exp(-r * dt)  # e^-rt
    
    # Calculating Risk Neutral Probability
    q = (np.exp(r * dt) - d) / (u - d)
```
#### Finding Stock Prices at Maturity (period N)
```python
S = np.zeros(N + 1)

    S[0] = S0 * d ** N  # If we think of our vector in terms of (i, j) this is position (N, 0)

    for j in range(1, N + 1):  # We reverse our way through the tree from (N,0) to (N,1) etc.
        S[j] = S[
                   j - 1] * u / d  # This gives us the array 'S' which contains values for the vector 
                   # at the end of the binomial tree (where i = N)
        
```

#### Finding Payoff at Maturity (period i = N)
```python
    # array of payoff at maturity
    C = np.zeros(N + 1)
    for j in range(0, N + 1):
        C[j] = max(0, S[j] - K)  # payoff for call option
```
#### Discounting Payoff Back
```python
    # discount payoff back through tree
    for i in np.arange(N, 0, -1):
        for j in range(0, i):  # discount back i periods
            expected_value_option = (q * C[j + 1] + (1 - q) * C[j])
            C[j] = discount_rate * expected_value_option

    return C[0]
```
#### Calling our Function
```python
multi_period_binomial_tree(K, T, S0, r, N, u, d, option_type='C')
```
Libraries used: `numpy`

## Potential Enhancements / Future Projects
* Pricing American Options
* Accounting for dividend paying stocks
* Creating replicating portfolio with position in the underlying asset and the risk free bond
 

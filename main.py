import math
from scipy.stats import norm

def call(S0, X, T, r, sigma):
    d1 = (math.log(S0 / X) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * (math.sqrt(T))

    call_price = (S0 * norm.cdf(d1)) - X * math.exp(-r * T) * norm.cdf(d2)
    return call_price

def put(S0, X, T, r, sigma):
    d1 = (math.log(S0 / X) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    
    put_price = (X * math.exp(-r * T) * norm.cdf(-d2)) - (S0 * norm.cdf(-d1))
    return put_price

S0 = 100  # Spot price of the asset
X = 100   # Strike price
T = 1     # Time to expiration (in years)
r = 0.05  # Risk-free interest rate
sigma = 0.2 # Volatility (20%)

if sigma <= 0:
    raise ValueError("Volatility has to be greater than 0.")

call_price = call(S0, X, T, r, sigma)
put_price = put(S0, X, T, r, sigma)

print(f"Call Option Price: {call_price:.2f}")
print(f"Put Option Price: {put_price:.2f}")
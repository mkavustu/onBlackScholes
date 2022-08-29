# This script calculates the value of a call option using Black-Scholes-Merton Model by sweeping volatility.
# Useful for checking whether a certain (premium, vt) pair exists for given X, r & t

import plotly.graph_objects as go
import numpy as np
from scipy.stats import norm


r_f = 0.04                  #annual interest rate
t = 0.1589041095890411      #time to expiration in years
S = 276.35 #price of non-dividend paying stock
vt = np.linspace(0.001, 2, 100)   #annual standard deviation of stock price, in percentage
X = 175                     #exercise price

C = np.zeros((len(vt)))

for k in range(0, len(vt)):     #this loop calculates the option premium using BlackScholes model for non-dividends
    d1 = (np.log(S / X) + (r_f + pow(vt[k], 2) / 2) * t) / (vt[k] * np.sqrt(t))

    d2 = d1 - vt[k]*np.sqrt(t)

    C[k] = norm.cdf(d1)*S - X*np.exp(-r_f*t)*norm.cdf(d2)

fig = go.Figure(data=[go.Scatter(y = C, x = vt)])       #made the mistake of using graph_objects for scatter, express is probably easier

fig.update_layout(title='Volatility vs Option Price & current stock price for K = ',
                    xaxis_title='Volatility',
                    yaxis_title='Current Price ($)', width = 1000
                  )

fig.show()
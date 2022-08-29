# This script calculates the value of a call option using Black-Scholes-Merton Model.
#     interest rate is kept constant, while volatility and underlying price is swept

import plotly.graph_objects as go
import numpy as np
from scipy.stats import norm

r_f = 0.00                  # annual interest rate
t = 0.25                    # time to expiration in years
# S = 100                     # price of non-dividend paying stock
S = np.linspace(80, 120, 100)  # price of non-dividend paying stock
# S = np.linspace(0.8, 1.2, 100) # price of non-dividend paying stock
vt = np.linspace(0.001, 2, 50)   # annual standard deviation of stock price, in percentage
X = 100                     # exercise price
# X = 1                     # exercise price

C = np.zeros((len(S), len(vt)))

for i in range(0,len(S)):
    for k in range(0, len(vt)):
        d1 = (np.log(S[i] / X) + (r_f + pow(vt[k], 2) / 2) * t) / (vt[k] * np.sqrt(t))

        d2 = d1 - vt[k]*np.sqrt(t)

        C[i][k] = norm.cdf(d1)*S[i] - X*np.exp(-r_f*t)*norm.cdf(d2)

fig = go.Figure(data=[go.Surface(z=C, x=vt, y=S)])

fig.update_layout(title='Call Premium vs Volatility & Stock Price for K = $' + str(X) + ', t = ' + str(t), autosize=False,
                    scene = dict(xaxis_title='Volatility',
                                 yaxis_title='Current Price ($)',
                                 zaxis_title='Option Price ($)'),
                  width=800, height=800,
                  margin=dict(l=65, r=50, b=65, t=90))

name = 'eye = (x:2, y:2, z:0.1)'
camera = dict(
    eye=dict(x=-2, y=-2, z=1)
)

fig.update_layout(scene_camera=camera)

fig.show()
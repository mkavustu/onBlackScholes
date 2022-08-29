# This script calculates and plots the volatility of a call
#   option for different values of stock price and call price

import plotly.graph_objects as go
import numpy as np
from scipy.stats import norm
import BS

r_f = 0.05                  #annual interest rate
t = np.linspace(0.1, 4, 20)                    #time to expiration in years
S = 200                    #price of non-dividend paying stock
#vt = np.linspace(0.001, 1, 50)   #annual standard deviation of stock price, in percentage
C = 10    #price of the call option
X = np.linspace(100, 400, 20)
e = 0.001                   #error target for Newton Rhapson


vt = np.zeros((len(t),len(X)))

for i in range(0,len(t)):
    for k in range(0, len(X)):

        vt[i][k] = BS.find_vt(0.5, S, C, r_f, t[i], X[k], e, 100)

#vt[1][1] = BS.find_vt(0.5, S[1], C[1], r_f, t, X, e, 100)

fig = go.Figure(data=[go.Surface(z=vt, x=t, y=X)])

fig.update_layout(title='Volatility vs Option Price & current stock price for K = ' + str(X), autosize=False,
                    scene = dict(xaxis_title='Time to expire (years)',
                                 yaxis_title='Strike Price ($)',
                                 zaxis_title='Volatility (%)'),
                  width=800, height=800,
                  margin=dict(l=65, r=50, b=65, t=90))

name = 'eye = (x:2, y:2, z:0.1)'
camera = dict(
    eye=dict(x=-2, y=-2, z=1)
)

fig.update_layout(scene_camera=camera)

fig.show()


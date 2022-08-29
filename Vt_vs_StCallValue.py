# This script calculates and plots the volatility of a call
#   option for different values of stock price and call price

import plotly.graph_objects as go
import numpy as np
from scipy.stats import norm
import BS

r_f = 0.05                  #annual interest rate
t = 0.25                    #time to expiration in years
#S = 100                     #price of non-dividend paying stock
S = np.linspace(80, 120, 50) #price of non-dividend paying stock
#vt = np.linspace(0.001, 1, 50)   #annual standard deviation of stock price, in percentage
C = np.linspace(0, 20, 50)    #price of the call option
X = 100
e = 0.001                   #error target for Newton Rhapson


vt = np.zeros((len(S),len(C)))

for i in range(0,len(S)):
    for k in range(0, len(C)):

        vt[i][k] = BS.find_vt(0.5, S[i], C[k], r_f, t, X, e, 10)

#vt[1][1] = BS.find_vt(0.5, S[1], C[1], r_f, t, X, e, 100)

fig = go.Figure(data=[go.Surface(z=vt, x=C, y=S)])

fig.update_layout(title='Volatility vs Option Price & current stock price for K = $' + str(X), autosize=False,
                    scene = dict(xaxis_title='Option Price ($)',
                                 yaxis_title='Stock Price ($)',
                                 zaxis_title='Volatility'),
                  width=800, height=800,
                  margin=dict(l=65, r=50, b=65, t=90))

name = 'eye = (x:2, y:2, z:0.1)'
camera = dict(
    eye=dict(x=-2, y=-2, z=1)
)

fig.update_layout(scene_camera=camera)

fig.show()


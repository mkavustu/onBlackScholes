# A module with useful functions relating to Black Scholes model


import numpy as np
import plotly.graph_objects as go
from scipy.stats import norm


def find_vt(vt_0, S, C, r_f, t, X, e, i):
    # recursively calculates the implied volatility for given premium, price, strike, r & t
    # pick a vt value
    # put it in black scholes model
    # calculate vega at each point
    # Apply newton-rhapson method until error < e
    # return IV

    # print("i " + str(i)) # for debugging
    vt = vt_0

    if vt == 0:  # here to avoid divide by zero error in the upcoming calculations
        return 0

    # print("volatility " + str(vt)) # for debugging
    d1 = (np.log(S/X)+(r_f + pow(vt, 2)/2)*t)/(vt*np.sqrt(t))
    vega = S*np.sqrt(t)*norm.cdf(d1)

    # print("vega " + str(vega)) # for debugging

    d2 = d1 - vt*np.sqrt(t)
    C_n = norm.cdf(d1) * S - X * np.exp(-r_f * t) * norm.cdf(d2)

    # print("error "+str(abs(C_n-C))) # for debugging

    if np.abs(C_n-C) > e and i > 1:         # go inside if error is greater than e and available depth for recursion
        # vt_1 = abs(vt_0 - (C_n-C)/vega)
        if vt_0 - (C_n-C)/vega < 0:         # needed since volatility cannot be less than 0
            vt_1 = vt_0/10
        else:
            vt_1 = vt_0 - (C_n - C) / vega  # newton-rhapson

        if vt_0 < pow(10, -50) and vt_1 < pow(10, -50):   # added to avoid oscillation, might not be needed really.
            return 0
        vt_0 = find_vt(vt_1, S, C, r_f, t, X, e, i-1)    # keep going until parent if is false or i is out of bounds

    return vt_0


def plot_vt(smin, smax, X, r_f, vtmax, t):  # plot call option premium vs volatility and stock price

    # r_f = 0.00  # annual interest rate
    # t = 0.25  # time to expiration in years
    # S = 100                     # price of non-dividend paying stock
    S = np.linspace(smin, smax, 100) # price of non-dividend paying stock
    vt = np.linspace(0.001, vtmax, 50)  # annual standard deviation of stock price, in percentage
    # X = 100  # exercise price
    # S = np.linspace(min(1, abs(X-sk*X)), sk*X, 50)  # price of non-dividend paying stock
    # X = 1                     # exercise price

    C = np.zeros((len(S), len(vt)))

    for i in range(0, len(S)):
        for k in range(0, len(vt)):
            d1 = (np.log(S[i] / X) + (r_f + pow(vt[k], 2) / 2) * t) / (vt[k] * np.sqrt(t))

            d2 = d1 - vt[k] * np.sqrt(t)

            C[i][k] = norm.cdf(d1) * S[i] - X * np.exp(-r_f * t) * norm.cdf(d2)

    fig = go.Figure(data=[go.Surface(z=C, x=vt, y=S)])

    fig.update_layout(title='Call Premium vs Volatility & Stock Price for K = $' + str(X) + ', t = ' + str(t),
                      autosize=False,
                      scene=dict(xaxis_title='Volatility',
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

def plot_vtvt(S, X, r_f, vtmax, tmax):  # plot call option premium vs volatility and time

    # r_f = 0.00  # annual interest rate
    # t = 0.25  # time to expiration in years
    # S = 100                     # price of non-dividend paying stock
    # S = np.linspace(smin, smax, 100) # price of non-dividend paying stock
    vt = np.linspace(0.001, vtmax, 50)  # annual standard deviation of stock price, in percentage
    # X = 100  # exercise price
    # S = np.linspace(min(1, abs(X-sk*X)), sk*X, 50)  # price of non-dividend paying stock
    # X = 1                     # exercise price
    t = np.linspace(0.01, tmax, 50)    #time to expiry

    C = np.zeros((len(t), len(vt)))

    for i in range(0, len(t)):
        for k in range(0, len(vt)):
            d1 = (np.log(S / X) + (r_f + pow(vt[k], 2) / 2) * t[i]) / (vt[k] * np.sqrt(t[i]))

            d2 = d1 - vt[k] * np.sqrt(t[i])

            C[i][k] = norm.cdf(d1) * S - X * np.exp(-r_f * t[i]) * norm.cdf(d2)

    fig = go.Figure(data=[go.Surface(z=C, x=vt, y=t)])

    fig.update_layout(title='Call Premium vs Volatility & Maturity for K = '+'&#36;' + str(X) + ', '+'S = '+ '&#36;' + str(S),
                      autosize=False,
                      scene=dict(xaxis_title='Volatility',
                                 yaxis_title='Maturity (years)',
                                 zaxis_title='Option Price ($)'),
                      width=800, height=800,
                      margin=dict(l=65, r=50, b=65, t=90))

    name = 'eye = (x:2, y:2, z:0.1)'
    camera = dict(
        eye=dict(x=-2, y=-2, z=1)
    )

    fig.update_layout(scene_camera=camera)

    fig.show()


def sweep_vt(S, X, vtmax, t, r_f):
    # This script calculates the value of a call option using Black-Scholes-Merton Model by sweeping volatility, and
       # then plots the result on 2D graph
    # Useful for quickly checking whether a (premium, vt) pair exists for given S, X, r_f & t

    # r_f = 0.04  # annual interest rate
    # t = 0.1589041095890411  # time to expiration in years
    # S = 276.35  # price of non-dividend paying stock
    vt = np.linspace(0.001, vtmax, 100)  # annual standard deviation of stock price, in percentage
    # X = 175  # exercise price

    C = np.zeros((len(vt)))

    for k in range(0, len(vt)):  # this loop calculates the option premium using BlackScholes model for non-dividends
        d1 = (np.log(S / X) + (r_f + pow(vt[k], 2) / 2) * t) / (vt[k] * np.sqrt(t))

        d2 = d1 - vt[k] * np.sqrt(t)

        C[k] = norm.cdf(d1) * S - X * np.exp(-r_f * t) * norm.cdf(d2)

    fig = go.Figure(
        data=[go.Scatter(y=C, x=vt)])  # made the mistake of using graph_objects for scatter, express is probably easier

    fig.update_layout(title='Option Price vs Volatility for S = &#36;' + str(S) + ', K = &#36;' + str(X) + ', t = ' + str(t) + ' years,' + ' r = ' + str(r_f),
                      xaxis_title='Volatility',
                      yaxis_title='Premium ($)', width=1000
                      )
    fig.show()
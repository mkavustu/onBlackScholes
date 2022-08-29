# Calculates the implied volatility across strike prices for a given maturity and plots on a 2D scatter graph.
# trading data is pulled live from yahoo finance API, which means there could potentially be obsolete/incorrect price
#   information for particular options, producing nonsensical results, sometimes even depending on the hour of the day.
# Implied volatility for deep in the money options might "behave" erratically though it is reasonable since the price of
#   deep in the money options are insensitive to lower volatility which doesn't make it easy for Newton-Rahpson.
#   Planning to modify the calculation for deep in the money options in the future to address this.

# Next step is to bring together different maturities to plot IV surface for a given stock.


from yahoo_fin import options as op
from yahoo_fin import stock_info as si
import yahoo_fin_fncs as yh

import plotly.graph_objects as go
from datetime import date
import numpy as np
import BS

ticker = 'MSFT'         # stock ticker
expirationDates = op.get_expiration_dates(ticker)  # get the expiration dates for the ticker's options
callData = op.get_calls(ticker, expirationDates[6])  # get call data for this particular expiration date

a = yh.parsedate(expirationDates[6])    # get the date in list format

d0 = date.today()
d1 = date(a[2], a[0], a[1])
delta = d1 - d0                         # calculate the number of days remaining till maturity

time2exp = delta.days/365               # days to maturity to years to maturity
# print(time2exp) # for debugging

dataShape = callData.shape

r_f = 0.025                      # annual interest rate
t = time2exp                    # time to expiration in years
S = si.get_live_price(ticker)   # price of non-dividend paying stock
# vt = np.linspace(0.001, 1, 50) # annual standard deviation of stock price, in percentage
# C = np.linspace(0, 20, 50)     # price of the call option
C = callData.loc[:, 'Ask']      # price for the options, can use 'Bid' or 'Last Price' if wished
# X = 100
X = callData.loc[:, 'Strike']
e = 0.000001                   # error target for Newton-Raphson method

api_IV = callData.loc[:, 'Implied Volatility'].values

p = np.zeros(len(api_IV))

for i in range(0, len(p)):
    p[i] = float(api_IV[i].split('%',1)[0])/100

vt0 = 1                         # initial value for IV
vt = np.zeros(len(C))

for k in range(0, len(C)):

    vt[k] = BS.find_vt(vt0, S, C[k], r_f, t, X[k], e, 200)  # calculate IV
    # v0 = vt[k] # use the previous result as initial value for the next data point

fig = go.Figure(data=[go.Scatter(y=vt, x=X, name='Calculated IV')])  # plot IV vs strike price

fig.update_layout(title='Implied Volatility of ' + ticker + '. Expiration: ' + expirationDates[6],
                  xaxis_title='Strike Price ($)', yaxis_title='Implied Volatility', width=1000
                  )



fig.add_trace(go.Scatter(y=p, x=X,
        mode="lines",
        line=go.scatter.Line(color="red"),
        showlegend=True, name='Database IV')
)

fig.show()

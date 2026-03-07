import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

symbol = input("symbol:")

data = yf.download(symbol, start="2015-01-01")

if len(data) < 2000:
    raise Exception("dataset too small")

data.to_csv(symbol+"_data.csv")

returns = data["Close"].pct_change().dropna()

years = len(data)/252
cagr = (data["Close"].iloc[-1]/data["Close"].iloc[0])**(1/years)-1

vol = returns.std()*np.sqrt(252)

cum=(1+returns).cumprod()
peak=cum.cummax()
dd=(cum-peak)/peak
max_dd=dd.min()

plt.figure()
plt.plot(data.index,data["Close"])
plt.title(symbol+" price")
plt.savefig(symbol+"_chart.png")

report=f"""
{symbol} report

CAGR:{cagr:.2%}
Volatility:{vol:.2%}
MaxDrawdown:{max_dd:.2%}
"""

open(symbol+"_report.md","w").write(report)

print("done")

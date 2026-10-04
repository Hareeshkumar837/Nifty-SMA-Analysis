import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1.Data
nifty = yf.download("^NSEI",period='6mo')
nifty.columns = nifty.columns.droplevel(1)

print(nifty.shape)
print(nifty.head())

nifty['SMA20']= nifty['Close'].rolling(window=20).mean()

print(nifty.tail())

nifty['Signal'] = np.where(nifty['Close']>nifty['SMA20'],1,0)

new_nifty = nifty[['Close','SMA20','Signal']]
print(new_nifty.tail(10))

print(new_nifty.describe())
print(new_nifty[new_nifty['Signal']==1])

print(new_nifty['Signal'].sum())
print(new_nifty['Signal'].value_counts())

# 2.Baseline & Strategy Math
new_nifty['Positions'] = new_nifty['Signal'].diff()

new_nifty['Market_ret'] = new_nifty['Close'].pct_change()
new_nifty["Strategy_ret"] = new_nifty['Market_ret']*new_nifty['Signal'].shift(1)
cumulative_market = (1+new_nifty['Market_ret']).cumprod()
cumulative_strategy = (1+new_nifty["Strategy_ret"]).cumprod()
print(f"Buy and hold returns {(cumulative_market.iloc[-1]-1)*100:.2f}%")
print(f"Bot trading return {(cumulative_strategy.iloc[-1]-1)*100:.2f}%")

sma_windows =[5,10,15,20,30,40]
print("SMA strategy optimization")
print(f"Buy and hold returns {(cumulative_market.iloc[-1]-1)*100:.2f}%")

# 3.Optimization
for window in sma_windows:
    new_nifty[f'SMA{window}'] = new_nifty['Close'].rolling(window=window).mean()

    new_nifty['Temp_signal'] = np.where(new_nifty['Close']>new_nifty[f'SMA{window}'],1,0)

    new_nifty['Temp_stra_ret'] = new_nifty['Market_ret']*new_nifty['Temp_signal'].shift(1)

    temp_cumulative = (1+new_nifty['Temp_stra_ret']).cumprod()
    print(f"{window}-Day SMA Return:{(temp_cumulative.iloc[-1]-1)*100:.2f}%")


# 4.Visualization
plt.figure(figsize=(12,6))
plt.plot(new_nifty.index,new_nifty['Close'],label='Nifty 50 Close', color='blue',alpha=0.6)
plt.plot(new_nifty.index,new_nifty['SMA20'],label='20-day SMA', color='orange',linewidth=0.6)
plt.plot(new_nifty[new_nifty['Positions']==1].index,new_nifty['Close'][new_nifty['Positions']==1],
         '^',markersize=10,color='green',label='Buy')
plt.plot(new_nifty[new_nifty['Positions']==-1].index,new_nifty['Close'][new_nifty['Positions']==-1],
         'v',markersize=10,color='red',label='Sell')
plt.title("Nifty50: SMA Strategy with Buy/Sell Signals" )
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend()
plt.grid(True)
plt.show()


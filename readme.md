# Quantitative Trading Backtester: Nifty 50

A Python-based algorithmic trading pipeline that backtests Moving Average (SMA) crossover strategies against the Nifty 50 index. 

## Features
* **Live Data Ingestion:** Automates historical data pulls via `yfinance`.
* **Look-Ahead Bias Prevention:** Uses `.shift(1)` to accurately model 24-hour trade execution delays.
* **Compound Growth Modeling:** Utilizes pandas `.cumprod()` to calculate true portfolio growth.
* **Algorithmic Optimization:** Built-in iteration loop tests multiple SMA timeframes (5, 10, 15, 20, 30, 40 days) in milliseconds to identify mathematically superior strategies.
* **Visual Diagnostics:** Maps exact entry (buy) and exit (sell) coordinates over dynamic price charts using Matplotlib to analyze whipsaw effects in sideways markets.

## Technologies Used
* Python
* Pandas (Data manipulation & financial logic)
* NumPy (Vectorized signal generation)
* Matplotlib (Trade plotting)
* yfinance (Market data API)
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

# Load Microsoft stock data for 6 months
msft = yf.Ticker('MSFT').history(period='6mo')

# Daily return count
msft['Daily Return'] = msft['Close'].pct_change()

# 7-d average rolling
msft['Rolling Avg (7d)'] = msft['Close'].rolling(window=7).mean()

# 14-d volatility
msft['Volatility (14d)'] = msft['Daily Return'].rolling(window=14).std()

# Sharp price change (>+-5%)
msft['Growth Spike'] = msft['Daily Return'].abs() > 0.05

# Mean and median profitability
print(f"Mean: {msft['Daily Return'].mean()*100:.3f}%, Median: {msft['Daily Return'].median()*100:.3f}%")

# Dates of lagest drop and growth
print(f"Largest drop: {msft['Daily Return'].idxmin().date()}, Largest growth: {msft['Daily Return'].idxmax().date()}")

# Sharp price change days
print(f"Spike days: {msft['Growth Spike'].sum()}")

# Most volume month
msft.index = pd.to_datetime(msft.index)
most_volume_month = msft['Volume'].resample('M').sum().idxmax()
print(f"Most volume month: {most_volume_month.strftime('%B')}")

# Chart of closing price and 7-day moving average
plt.figure(figsize=(7.5, 3.5))
plt.plot(msft['Close'], label="Close Price")
plt.plot(msft['Rolling Avg (7d)'], label="7-Day SMA", linestyle="--")
plt.title("MSFT Stock Price & 7-Day Moving Average")
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("msft_stock_price_&_7-day_moving_average.png")

# Chart of daily profitability
plt.figure(figsize=(7.5, 3.5))
plt.bar(msft.index, msft['Daily Return'] * 100, label="Daily Return")
plt.title("MSFT Daily Return")
plt.xlabel("Date")
plt.ylabel("Return (%)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("msft_daily_return.png")

# Chart of volatility in 14 days
plt.figure(figsize=(7.5, 3.5))
plt.plot(msft['Volatility (14d)'], label="Volatility (14d)", color='tab:red')
plt.title("MSFT Volatility (14d)")
plt.xlabel("Date")
plt.ylabel("Volatility (Std of Daily Return)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("msft_volatility_14d.png")

# Chart of profitability on days of spikes
spikes = msft.loc[msft['Growth Spike'], 'Daily Return']
plt.figure(figsize=(7.5, 3.5))
plt.bar(spikes.index, spikes * 100, label="Spikes Return", color='tab:purple')
plt.title("MSFT Spike Days Return")
plt.xlabel("Date")
plt.ylabel("Return (%)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("msft_spike_days_return.png")

# Chart of trading volume and volatility on a single chart with two axes
plt.figure(figsize=(7.5, 3.5))
ax1 = plt.gca()
ax1.plot(msft['Volume'], label="Volume", color='tab:blue')
ax1.set_ylabel("Volume", color='tab:blue')
ax1.tick_params(axis='y', labelcolor='tab:blue')

ax2 = ax1.twinx()
ax2.plot(msft['Volatility (14d)'], label="Volatility (14d)", color='tab:orange', linestyle="--")
ax2.set_ylabel("Volatility (14d)", color='tab:orange')
ax2.tick_params(axis='y', labelcolor='tab:orange')

plt.title("MSFT Volume & Volatility (14d)")
plt.xlabel("Date")
plt.grid(True)
plt.tight_layout()
plt.savefig("msft_volume_&_volatility_14d.png")

# Displaying graphs
plt.show()

# Save df to CSV-file
msft.to_csv("microsoft.csv", index=False)

# https://www.youtube.com/watch?v=PuZY9q-aKLw&t=327s

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas_datareader import data as pdr
import datetime as dt
import os
import requests

import yfinance as yf
yf.pdr_override()

# from sklearn.preprocessing import MinMaxScaler
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Dense, Dropout, LSTM

os.environ["TIINGO_API_KEY"] = "c18a43200a4dde2d36f4a4986bd03bb70d92fd4d"

# Define the stock symbol and the date range
symbol = 'AAPL'

# Define the Tiingo API endpoint for 5-minute data
url = f'https://api.tiingo.com/iex/{symbol}/prices'

# Define the API parameters including the date range
params = {
    'startDate': "2023-08-1",
    'endDate': "2023-09-1",
    'resampleFreq': '5min',
}

# Add your Tiingo API token to the headers
headers = {
    'Authorization': f'Token {os.environ["TIINGO_API_KEY"]}',
}

# Make the API request
response = requests.get(url, params=params, headers=headers)

# Parse the JSON response into a DataFrame
data = response.json()
df = pd.DataFrame(data)

# EMAs
df['EMA_5'] = df['close'].ewm(span=5, adjust=False).mean()
df['EMA_50'] = df['close'].ewm(span=50, adjust=False).mean()
df['EMA_100'] = df['close'].ewm(span=100, adjust=False).mean()
df['EMA_200'] = df['close'].ewm(span=200, adjust=False).mean()

# macd
df['ema_short'] = df['close'].ewm(span=12, adjust=False).mean()
df['ema_long'] = df['close'].ewm(span=26, adjust=False).mean()

# Calculate the MACD line as the difference between the short-term and long-term EMA
df['macd'] = df['ema_short'] - df['ema_long']

# Define the signal line period (e.g., 9 periods)
signal_period = 9

# Calculate the signal line as the EMA of the MACD line
df['signal'] = df['macd'].ewm(span=9, adjust=False).mean()




# Create a figure and multiple subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

# Plot the original 'close' price, EMAs, and RSI in the top subplot
ax1.plot(df['date'], df['close'], label='Close Price', color='blue')
ax1.plot(df['date'], df['EMA_5'], label='EMA 5', color='orange')
ax1.plot(df['date'], df['EMA_50'], label='EMA 50', color='red')
ax1.plot(df['date'], df['EMA_100'], label='EMA 100', color='green')
ax1.plot(df['date'], df['EMA_200'], label='EMA 200', color='yellow')
ax1.set_ylabel('Price')
ax1.legend()

# Plot the MACD and signal line in the middle subplot
ax2.plot(df['date'], df['macd'], label='MACD', color='red')
ax2.plot(df['date'], df['signal'], label='Signal Line', color='purple')
ax2.set_ylabel('MACD')
ax2.legend()

# Reduce the number of x-axis ticks and labels as shown in previous responses
num_ticks = 3  # Adjust this number to your preference
step = len(df) // num_ticks
xticks = df['date'][::step]

# Set the x-axis ticks and labels for all subplots
ax1.set_xticks(xticks)

# Customize the layout and title
ax1.set_xlabel('Date')
ax1.set_title(f"{symbol} Stock")

# Ensure tight layout
plt.tight_layout()

# Display the plot
plt.show()

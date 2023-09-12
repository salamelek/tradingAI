import pandas as pd
import os
import requests


def getDf(symbol, start, end, period):
    os.environ["TIINGO_API_KEY"] = "c18a43200a4dde2d36f4a4986bd03bb70d92fd4d"

    # Define the Tiingo API endpoint for 5-minute data
    url = f'https://api.tiingo.com/iex/{symbol}/prices'

    # Define the API parameters including the date range
    params = {
        'startDate': start,
        'endDate': end,
        'resampleFreq': period
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

    # RSI
    # Define the period for RSI calculation (e.g., 14 periods)
    rsi_period = 14
    # Calculate the price changes (daily close price - previous day's close price)
    df['price_change'] = df['close'].diff()
    # Calculate the gain and loss for each day
    df['gain'] = df['price_change'].apply(lambda x: x if x > 0 else 0)
    df['loss'] = df['price_change'].apply(lambda x: -x if x < 0 else 0)
    # Calculate the average gain and average loss over the RSI period
    df['avg_gain'] = df['gain'].rolling(window=rsi_period).mean()
    df['avg_loss'] = df['loss'].rolling(window=rsi_period).mean()
    # Calculate the relative strength (RS) and RSI
    df['rs'] = df['avg_gain'] / df['avg_loss']
    df['rsi'] = 100 - (100 / (1 + df['rs']))

    return df

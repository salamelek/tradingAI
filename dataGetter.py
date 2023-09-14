import pandas as pd
import os
import requests


def getDf(symbol, start, end, period):
    print("Getting data...")
    os.environ["TIINGO_API_KEY"] = "c18a43200a4dde2d36f4a4986bd03bb70d92fd4d"

    # Define the Tiingo API endpoint for 5-minute data
    url = f"https://api.tiingo.com/iex/{symbol}/prices"

    # Define the API parameters including the date range
    params = {
        "startDate": start,
        "endDate": end,
        "resampleFreq": period
    }

    # Add your Tiingo API token to the headers
    headers = {
        "Authorization": f"Token {os.environ['TIINGO_API_KEY']}",
    }

    # Make the API request
    response = requests.get(url, params=params, headers=headers)

    # Parse the JSON response into a DataFrame
    data = response.json()
    df = pd.DataFrame(data)

    # drop useless data
    df = df.drop('open', axis=1)
    df = df.drop('high', axis=1)
    df = df.drop('low', axis=1)

    # EMAs
    df["EMA_5"] = df["close"].ewm(span=5, adjust=False).mean()
    df["EMA_50"] = df["close"].ewm(span=50, adjust=False).mean()
    df["EMA_100"] = df["close"].ewm(span=100, adjust=False).mean()
    df["EMA_200"] = df["close"].ewm(span=200, adjust=False).mean()
    # now their slopes
    df['EMA_5_SLOPE'] = df['EMA_5'].diff()
    df['EMA_50_SLOPE'] = df['EMA_50'].diff()
    df['EMA_100_SLOPE'] = df['EMA_100'].diff()
    df['EMA_200_SLOPE'] = df['EMA_200'].diff()
    # The first row of 'EMA_Slope' will be NaN, so you might want to fill it with 0 or another appropriate value
    # df['EMA_5_SLOPE'].fillna(0, inplace=True)

    # macd
    df["ema_short"] = df["close"].ewm(span=12, adjust=False).mean()
    df["ema_long"] = df["close"].ewm(span=26, adjust=False).mean()
    df["macd"] = df["ema_short"] - df["ema_long"]
    df["macd_signal"] = df["macd"].ewm(span=9, adjust=False).mean()
    # slopes
    df['macd_slope'] = df['macd'].diff()
    df['macd_signal_slope'] = df['macd_signal'].diff()
    # distance
    df["macd_distance"] = df["macd"] - df["macd_signal"]


    # RSI
    # Calculate the price changes (daily close price - previous day's close price)
    df["price_change"] = df["close"].diff()
    # Calculate the gain and loss for each day
    df["gain"] = df["price_change"].apply(lambda x: x if x > 0 else 0)
    df["loss"] = df["price_change"].apply(lambda x: -x if x < 0 else 0)
    # Calculate the average gain and average loss over the RSI period
    df["avg_gain"] = df["gain"].rolling(window=14).mean()
    df["avg_loss"] = df["loss"].rolling(window=14).mean()
    # Calculate the relative strength (RS) and RSI
    df["rs"] = df["avg_gain"] / df["avg_loss"]
    df["rsi"] = 100 - (100 / (1 + df["rs"]))

    print("Done!\n")

    return df

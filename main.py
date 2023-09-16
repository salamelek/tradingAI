import os
import requests
import pandas as pd


# get data
def getData(stock, start, end, timeFrame):
    print("Getting data...")

    os.environ["TIINGO_API_KEY"] = "c18a43200a4dde2d36f4a4986bd03bb70d92fd4d"

    url = f"https://api.tiingo.com/iex/{stock}/prices"
    params = {
        "startDate": start,
        "endDate": end,
        "resampleFreq": timeFrame
    }
    headers = {
        "Authorization": f"Token {os.environ['TIINGO_API_KEY']}",
    }

    response = requests.get(url, params=params, headers=headers)

    # Parse the JSON response into a DataFrame
    data = response.json()
    df = pd.DataFrame(data)

    # calculate emas
    df["ema5"] = df["close"].ewm(span=5, adjust=False).mean()
    df["ema50"] = df["close"].ewm(span=50, adjust=False).mean()
    df["ema100"] = df["close"].ewm(span=100, adjust=False).mean()
    df["ema200"] = df["close"].ewm(span=200, adjust=False).mean()

    # calculate macd
    df["ema_short"] = df["close"].ewm(span=12, adjust=False).mean()
    df["ema_long"] = df["close"].ewm(span=26, adjust=False).mean()
    df["macd"] = df["ema_short"] - df["ema_long"]
    df["macd_signal"] = df["macd"].ewm(span=9, adjust=False).mean()

    # calculate rsi
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

    return df


print(getData("NVDA", "2023-05-1", "2023-06-1", "5min"))

# normalize data (FROM 0 TO 1)

# learn to make a reinforcement q-learn algorythm
# try sine indicator

# plot results

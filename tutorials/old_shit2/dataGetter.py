import yfinance as yf
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import csv

# TODO add also the ema of the indicators to get past values
# TODO get better values
# TODO make this module more modular (can choose sign, timeframe and shit)

stocks = [
    "AAPL",
    # "NVDA",
    # "TSLA",
    # "CNHI",
    # "ABNB",
    # "AMZN",
    # "AMD",
    # "PFE",
    # "SIRI",
    # "T",
    # "F",
    # "VST",
    # "WFC",
    # "LNC",
    # "ALLY",
    # "INTC",
    # "TLRY",
    # "CSCO",
    # "APLE",
    # "PLTR",
    # "BAC",
    # "LBRT",
    # "AUR",
    # "GLPI",
    # "FNF"
]


def ADX(data: pd.DataFrame, period: int):
    """
    Computes the ADX indicator.
    """

    df = data.copy()
    alpha = 1 / period

    # TR
    df['H-L'] = df['high'] - df['low']
    df['H-C'] = np.abs(df['high'] - df['close'].shift(1))
    df['L-C'] = np.abs(df['low'] - df['close'].shift(1))
    df['TR'] = df[['H-L', 'H-C', 'L-C']].max(axis=1)
    del df['H-L'], df['H-C'], df['L-C']

    # ATR
    df['ATR'] = df['TR'].ewm(alpha=alpha, adjust=False).mean()

    # +-DX
    df['H-pH'] = df['high'] - df['high'].shift(1)
    df['pL-L'] = df['low'].shift(1) - df['low']
    df['+DX'] = np.where(
        (df['H-pH'] > df['pL-L']) & (df['H-pH'] > 0),
        df['H-pH'],
        0.0
    )
    df['-DX'] = np.where(
        (df['H-pH'] < df['pL-L']) & (df['pL-L'] > 0),
        df['pL-L'],
        0.0
    )
    del df['H-pH'], df['pL-L']

    # +- DMI
    df['S+DM'] = df['+DX'].ewm(alpha=alpha, adjust=False).mean()
    df['S-DM'] = df['-DX'].ewm(alpha=alpha, adjust=False).mean()
    df['+DMI'] = (df['S+DM'] / df['ATR']) * 100
    df['-DMI'] = (df['S-DM'] / df['ATR']) * 100
    del df['S+DM'], df['S-DM']

    # ADX
    df['DX'] = (np.abs(df['+DMI'] - df['-DMI']) / (df['+DMI'] + df['-DMI'])) * 100
    df['adx'] = df['DX'].ewm(alpha=alpha, adjust=False).mean()

    del df['DX'], df['ATR'], df['TR'], df['-DX'], df['+DX'], df['+DMI'], df['-DMI']

    return df


def calculate_mad(arr):
    # use this shit because pandas .mad() is deprecated :(
    return np.mean(np.abs(arr - np.mean(arr)))


# Commodity Channel Index
def CCI(df, nDays):
    df['TP'] = (df['high'] + df['low'] + df['close']) / 3
    df['sma'] = df['TP'].rolling(nDays).mean()
    df['mad'] = df['TP'].rolling(nDays).apply(calculate_mad)
    df['cci'] = (df['TP'] - df['sma']) / (0.015 * df['mad'])

    del df['TP'], df['sma'], df['mad']

    return df


def getYfData():
    print("Getting train df...")

    df = yf.download(stocks[0], interval="5m", start="2023-08-01", end="2023-09-01")

    pd.options.display.max_columns = None
    pd.options.display.max_rows = None

    df = df.drop(["Open", "Adj Close"], axis=1)
    df = df.rename(columns={'Close': 'close', "High": "high", "Low": "low", "Volume": "volume"})

    # calculate indicators
    # rsi
    # Calculate the price changes (daily close price - previous day's close price)
    rsiPeriod = 14
    df["price_change"] = df["close"].diff()
    # Calculate the gain and loss for each day
    df["gain"] = df["price_change"].apply(lambda x: x if x > 0 else 0)
    df["loss"] = df["price_change"].apply(lambda x: -x if x < 0 else 0)
    # Calculate the average gain and average loss over the RSI period
    df["avg_gain"] = df["gain"].rolling(window=rsiPeriod).mean()
    df["avg_loss"] = df["loss"].rolling(window=rsiPeriod).mean()
    # Calculate the relative strength (RS) and RSI
    df["rs"] = df["avg_gain"] / df["avg_loss"]
    df["rsi"] = 100 - (100 / (1 + df["rs"]))
    # cleanup
    df = df.drop(["rs", "avg_loss", "avg_gain", "loss", "gain", "price_change"], axis=1)

    # adx
    adxPeriod = 14
    df = ADX(df, adxPeriod)

    # cci
    cciPeriod = 20
    df = CCI(df, cciPeriod)

    # drop Nan rows
    df = df.dropna()

    # add indexes
    df['index'] = range(len(df))

    print()

    return df


def getCsvData():
    # https://www.binance.com/en/landing/data

    df = pd.read_csv('../../tradingData/BTCUSDT/BTCUSDT-5m-2022-11.csv', header=None, usecols=[0, 1, 2, 3, 4])
    df.columns = ["startTime", "open", "high", "low", "close"]




df = getYfData()[0]
plt.plot(df["close"])
plt.show()
#
# print(df["high"])
#
# print("\n\n\n\n\n")
#
# print(min(df[(df["high"] > 188) & (df["index"] > 1700)]["index"]))

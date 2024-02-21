import copy

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt


def calculate_mad(arr):
    # use this shit because pandas .mad() is deprecated :(
    return np.mean(np.abs(arr - np.mean(arr)))


def getRSI(df, period):
    df["price_change"] = df["close"].diff()
    # Calculate the gain and loss for each day
    df["gain"] = df["price_change"].apply(lambda x: x if x > 0 else 0)
    df["loss"] = df["price_change"].apply(lambda x: -x if x < 0 else 0)
    # Calculate the average gain and average loss over the RSI period
    df["avg_gain"] = df["gain"].rolling(window=period).mean()
    df["avg_loss"] = df["loss"].rolling(window=period).mean()
    # Calculate the relative strength (RS) and RSI
    df["rs"] = df["avg_gain"] / df["avg_loss"]
    df["rsi"] = 100 - (100 / (1 + df["rs"]))
    # cleanup
    return df.drop(["rs", "avg_loss", "avg_gain", "loss", "gain", "price_change"], axis=1)


def getADX(df, period):
    """
    Computes the ADX indicator.
    """

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


def getCCI(df, period):
    df['TP'] = (df['high'] + df['low'] + df['close']) / 3
    df['sma'] = df['TP'].rolling(period).mean()
    df['mad'] = df['TP'].rolling(period).apply(calculate_mad)
    df['cci'] = (df['TP'] - df['sma']) / (0.015 * df['mad'])

    del df['TP'], df['sma'], df['mad']

    return df


def setCoords(df):
    """
    THis will set the coords to the "old" 5 points for each indicator

    :param df:
    :return:
    """

    # adx, cci, rsi
    bufferPoint = [[], [], []]

    bufferLen = 5
    for i in range(bufferLen):
        bufferPoint[0].append(df["adx"][i])
        bufferPoint[1].append(df["cci"][i])
        bufferPoint[2].append(df["rsi"][i])

    coords = [np.nan, np.nan, np.nan, np.nan, np.nan]

    for j in range(bufferLen, len(df["close"])):
        flatList = []
        for lst in bufferPoint:
            for sub in lst:
                flatList.append(sub)

        coords.append(copy.deepcopy(flatList))

        bufferPoint[0].pop(0)
        bufferPoint[1].pop(0)
        bufferPoint[2].pop(0)

        bufferPoint[0].append(df["adx"][j])
        bufferPoint[1].append(df["cci"][j])
        bufferPoint[2].append(df["rsi"][j])

    df["coords"] = coords

    df = df.drop(index=range(5))

    df = df.reset_index(drop=True)

    return df


def getSwissDataDf(filePath=""):
    print("Calculating all the labeledDf coords...")

    df = pd.read_csv(filePath, usecols=[1, 2, 3, 4], header=None, skiprows=1, names=["open", "high", "low", "close"])
    # df = pd.read_csv(fileString)

    df["open"] = df["open"].astype(float)
    df["high"] = df["high"].astype(float)
    df["low"] = df["low"].astype(float)
    df["close"] = df["close"].astype(float)

    # here calculate all the necessary indicators and calculate coords
    df = getADX(df, 14)
    df = getCCI(df, 20)
    df = getRSI(df, 14)

    df = df.dropna()
    df = df.reset_index(drop=True)

    df = setCoords(df)

    print("Done!")

    return df

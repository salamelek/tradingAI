import json
import math
import random
import numpy as np

from qLearning_v1.dataGetter import getData
from qLearning_v1.loadingBar import progressBar

data = getData()


slTp = 0.2
cumulativeProfit = 0
balance = 100
investmentSize = 0.1
commissionFee = 0.01
netProfit = 0
buyCounter, sellCounter, holdCounter = 0, 0, 0


def getAction(point):
    distList = []
    with open('adx_cci_rsi_5min.json') as json_file:
        data = json.load(json_file)

    for buyPoint in data["bullish"]:
        dist = (((buyPoint[0] - point[0]) ** 2) + ((buyPoint[1] - point[1]) ** 2) + ((buyPoint[2] - point[2]) ** 2))
        distList.append((dist, "buy"))

    for sellPoint in data["bearish"]:
        dist = (((sellPoint[0] - point[0]) ** 2) + ((sellPoint[1] - point[1]) ** 2) + ((sellPoint[2] - point[2]) ** 2))
        distList.append((dist, "sell"))

    for holdPoint in data["ranging"]:
        dist = (((holdPoint[0] - point[0]) ** 2) + ((holdPoint[1] - point[1]) ** 2) + ((holdPoint[2] - point[2]) ** 2))
        distList.append((dist, "hold"))

    k = int(math.sqrt(len(distList)))
    if len(distList) % 2 == k % 2 == 0:
        # if they are both even, add 1 to k
        k += 1

    sortedDistList = sorted(distList, key=lambda x: x[0])
    firstKNearPoints = sortedDistList[:k]

    labelsList = []
    for nearPoint in firstKNearPoints:
        labelsList.append(nearPoint[1])

    action = max(set(labelsList), key=labelsList.count)

    return action


def calcPosition(df, entryPrice, slTp, currentPos):
    try:
        highExitIndex = min(df[(df["high"] > (entryPrice + entryPrice * slTp)) & (df["index"] > currentPos)]["index"])
    except ValueError:
        highExitIndex = np.inf

    try:
        lowExitIndex = min(df[(df["low"] < (entryPrice - entryPrice * slTp)) & (df["index"] > currentPos)]["index"])
    except ValueError:
        lowExitIndex = np.inf

    if highExitIndex == lowExitIndex == np.inf:
        return None, None

    if highExitIndex < lowExitIndex:
        # the position concluded above
        exitPrice = entryPrice + entryPrice * slTp

    elif lowExitIndex < highExitIndex:
        # the position concluded below
        exitPrice = entryPrice - entryPrice * slTp

    else:
        # a candle that goes from +1% to -1%
        # randomly selects an option
        exitPrice = entryPrice + (entryPrice * slTp * random.choice([1, -1]))

    candlesToExit = min(highExitIndex, lowExitIndex) - currentPos

    return exitPrice, candlesToExit


candlesNum = len(data)
for i in range(candlesNum):
    tradeProfit = 0

    action = getAction([data["adx"][i], data["cci"][i], data["rsi"][i]])

    entryPrice = data["open"][i]
    exitPrice, candlesToExit = calcPosition(data, entryPrice, slTp, i)

    if action == "buy":
        try:
            tradeProfit = (exitPrice - entryPrice) / entryPrice
            buyCounter += 1
        except TypeError:
            pass

    elif action == "sell":
        try:
            tradeProfit = (entryPrice - exitPrice) / entryPrice
            sellCounter += 1
        except TypeError:
            pass

    else:
        holdCounter += 1

    cumulativeProfit += tradeProfit
    netProfit = tradeProfit * ((balance * investmentSize) - (balance * investmentSize * commissionFee))
    balance += netProfit

    progressBar(i + 1, candlesNum, f"Backtesting:")


print(cumulativeProfit)
print(netProfit)
print(f"Buys: {buyCounter}, Sells: {sellCounter}, Holds: {holdCounter}")

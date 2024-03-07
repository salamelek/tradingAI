"""
a data point (dp) is a vector/a tuple

use such data points that are not influenced by price, but by trend
    ~~> use slopes / price changes

the distance of two data points goes from 0 to potentially infinity
    I need to NORMALISE IT

or, instead of normalising it, I could just take the k closest points
the only problem then is to determine the quality of those points
"""

import csv
import numpy as np
import matplotlib.pyplot as plt

from binanceDataReader import getCryptoDf


def getDataPoints(filePath, skipNullRows=True):
    print("Getting dataPoints from csv... ", end="")

    dataPoints = []

    with open(filePath, "r") as csvFile:
        csvReader = csv.reader(csvFile)
        # skip first row
        next(csvReader)
        # time, Open, High, Low, Close, Volume
        for row in csvReader:
            if float(row[5]) == 0 and skipNullRows:
                # skip "empty" rows
                continue

            # difference between close and open price
            diffOC = float(row[4]) - float(row[1])

            # difference between high and low
            diffHL = float(row[2]) - float(row[3])

            # volume
            vol = float(row[5])

            dataPoints.append((diffOC, vol))

    print("Done!")

    return dataPoints


def displayDataPoints(dataPoints):
    xValues = []
    yValues = []

    for i in range(len(dataPoints)):
        xValues.append(i)
        yValues.append(dataPoints[i])

    plt.plot(xValues, yValues)
    ax = plt.gca()
    ax.yaxis.set_major_locator(plt.MaxNLocator(10))  # Adjust the locator as needed

    plt.axhline(y=0, color="black", linestyle='-')
    plt.grid(True)
    plt.show()


def euclideanDistance(dp1, dp2):
    distance = 0

    for i in range(len(dp1)):
        distance += (dp1[i] - dp2[i]) ** 2

    return np.sqrt(distance)


def compareGroups(g1, g2):
    totDistance = 0

    for i in range(len(g1)):
        totDistance += euclideanDistance(g1[i], g2[i])

    return np.sqrt(totDistance)


def appendDistToDict(avgDistDict, avgDist, index, k):
    """
    handles storing the best values and its indexes

    :param avgDistDict:
    :param avgDist:
    :param index:
    :param k:
    :return:
    """

    if len(avgDistDict) < k:
        avgDistDict[avgDist] = index
        return avgDistDict

    # sort the dict in reverse (greatest to lowest)
    avgDistDict = dict(sorted(avgDistDict.items(), reverse=True))

    # change the first element since it's the greatest distance
    prevWorse = list(avgDistDict.keys())[0]
    if avgDist < prevWorse:
        avgDistDict.pop(prevWorse)
        avgDistDict[avgDist] = index

    return avgDistDict


def getPrediction(dataPoints, dpIndex, groupSize, k):
    """
    here a group is a tuple of dataPoints.
    index 0 is at index 0 and so on

    returns the closest groups and their indexes
    {distance: index}

    :param dataPoints:
    :param dpIndex:     index of the original group
    :param groupSize:
    :param k:
    :return:
    """

    bestDistDict = {}

    # create currentGroup
    currentGroup = []
    for i in range(groupSize):
        currentGroup.append(dataPoints[dpIndex + i])

    # loop through every possible group
    for i in range(len(dataPoints) - groupSize):
        if i == dpIndex:
            # we don't care about the same group
            continue

        tmpGroup = []
        for j in range(groupSize):
            tmpGroup.append(dataPoints[i + j])

        averageDistance = compareGroups(currentGroup, tmpGroup)

        # append the best average distances to a dict long k
        bestDistDict = appendDistToDict(bestDistDict, averageDistance, i, k)

    return bestDistDict


def weightFunction(x, n=1/4):
    """
    this function is based on e^-kx
    n is a real positive number
    when n increases, the "severity" of the distance increases too

    :param n:
    :param x:
    :return:
    """

    if x < 0:
        raise Exception("given distance mustn't be negative!")

    if n < 0:
        raise Exception("n must be positive!")

    return np.e ** (n * x * -1)


def analisePredictionDictShit(dataPoints, dpIndex, groupSize, k, pDict, distThreshold):
    originalDirection = dataPoints[dpIndex + groupSize][0]

    counter = 1
    weightedAvgDirectionTot = 0
    for key in pDict.keys():
        weightedAvgDirectionTot += weightFunction(key)

        counter += 1

    # TODO instead of checking only the next direction, check the following trend

    weightedAvgDirection = weightedAvgDirectionTot / k

    # if the average weighted distance is shit, don't consider it and hold
    # FIXME something seriously wrong with the weight system (negative dist etc)
    if weightedAvgDirection > distThreshold:
        # dont consider the value
        return None

    sameDirection = True
    if originalDirection * weightedAvgDirection < 0:
        sameDirection = False

    # print()
    # print(f"Price direction after original group:   {originalDirection}")
    # print(f"Non-weighted average direction:         {avgDirection}")
    # print(f"Direction difference:                   {avgDirection - originalDirection}")
    # print(f"Same direction:                         {sameDirection}")

    return sameDirection


def analisePredictionDict(pDict, ohlc, dpIndex):
    originIndex = dpIndex + groupSize

    directions = {"original": ohlc[originIndex]["close"] - ohlc[originIndex]["open"], "predicted": []}
    for key in pDict.keys:
        predictIndex = pDict[key]
        predictDist = key

        directions["predicted"].append(ohlc[predictIndex]["close"] - ohlc[predictIndex]["open"])

    return directions


if __name__ == '__main__':
    # dataPoints = getDataPoints(
    #     "../forexData/EURUSD_Candlestick_15_M_BID_01.01.2022-01.01.2023.csv",
    #     skipNullRows=False
    # )

    # cryptoDF = getCryptoDf("../cryptoData/MERGED-ETHUSDT-15m-20-22.csv")
    cryptoDF = getCryptoDf("../cryptoData/ETHUSDT-15m-2020-01.csv")

    dataPoints = []
    for row in cryptoDF["coords"]:
        dataPoints.append((row[0], row[1], row[2]))


    dpIndex = 0
    groupSize = 5
    k = 3
    distThreshold = 7

    correctCount = 0
    skipped = 0

    print("started predicting")

    for i in range(1000):
        print(i)
        predictionDict = getPrediction(dataPoints, i, groupSize, k)

        if list(predictionDict.keys())[0] > distThreshold:
            continue

        print(predictionDict)
        displayDataPoints(dataPoints)

        # res = analisePredictionDict(dataPoints, i, groupSize, k, predictionDict, distThreshold)
        #
        # if res is None:
        #     skipped += 1
        #     continue
        #
        # if res:
        #     correctCount += 1
        #
        # print(f"{(round(correctCount / (i + 1 - skipped) * 100, 2))}%     | {correctCount} / {i + 1} | {res} | skipped: {skipped}")

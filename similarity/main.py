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
            diff = float(row[4]) - float(row[1])

            # volume
            vol = float(row[5])

            dataPoints.append((diff, vol))

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


def analisePredictionDict(dataPoints, dpIndex, groupSize, k, pDict):
    originalDirection = dataPoints[dpIndex + groupSize][0]
    # print()

    counter = 1
    avgDirectionTot = 0
    for key in pDict.keys():
        value = key
        index = pDict[key]
        # print(f"Price direction prediction {counter}: {dataPoints[index + groupSize][0]}")
        avgDirectionTot += dataPoints[index + groupSize][0]

        counter += 1

    avgDirection = avgDirectionTot / k

    # TODO weighted average (best points are more valuable)

    sameDirection = True
    if originalDirection * avgDirection < 0:
        sameDirection = False

    # print()
    # print(f"Price direction after original group:   {originalDirection}")
    # print(f"Non-weighted average direction:         {avgDirection}")
    # print(f"Direction difference:                   {avgDirection - originalDirection}")
    # print(f"Same direction:                         {sameDirection}")

    return sameDirection


if __name__ == '__main__':
    dataPoints = getDataPoints(
        "../forexData/EURUSD_Candlestick_15_M_BID_01.01.2022-01.01.2023.csv",
        skipNullRows=True
    )
    dpIndex = 0
    groupSize = 5
    k = 3

    displayDataPoints(dataPoints)

    correctCount = 0
    for i in range(500):
        predictionDict = getPrediction(dataPoints, i, groupSize, k)
        res = analisePredictionDict(dataPoints, i, groupSize, k, predictionDict)

        if res:
            correctCount += 1

        print(f"{(round(correctCount / (i + 1) * 100, 2))}%     | {correctCount} / {i + 1} | {res}")

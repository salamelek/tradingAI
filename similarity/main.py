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


class colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    RESET = '\033[0m'  # Reset to default color


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

            # dataPoints.append((diffOC, vol, diffHL))
            dataPoints.append((diffOC, vol))
            # dataPoints.append((diffOC,))

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


def weightFunction(x):
    """
    this function is based on e^-kx
    n is a real positive number
    when n increases, the "severity" of the distance increases too

    :param x:
    :return:
    """

    if x < 0:
        raise Exception("given distance mustn't be negative!")

    if n < 0:
        raise Exception("n mustn't be negative!")

    return np.e ** (n * x * -1)


def analisePredictionDict(predictionDict):
    """
    analyses the given prediction dictionary
    returns the weighted average value

    weighted average:
    sum(value1 * weight1, value2 * weight2, ...) / sum(weight1, weight2, ...)
    value:  next price change
    weight: weight function of the distance

    returns 0 if the weighted average does not meet the quota (lethal company reference)

    :param predictionDict:
    :return:
    """

    sumWeightedValues = 0
    sumWeights = 0

    for dist in predictionDict.keys():
        index = predictionDict[dist]
        weight = weightFunction(dist)
        value = dataPoints[index + groupSize][0]    # index [0] is the change open-close

        sumWeightedValues += value * weight
        sumWeights += weight

    weightedAverage = sumWeightedValues / sumWeights

    if abs(weightedAverage) < threshold:
        return 0

    return weightedAverage


if __name__ == '__main__':
    dataPoints = getDataPoints("../forexData/EURUSD_Candlestick_15_M_BID_01.01.2022-01.01.2023.csv")
    dpIndex = 0
    groupSize = 3
    k = 5
    n = 1
    threshold = 0.0001

    correctCount = 0
    skipped = 0
    for i in range(20000):
        predictionDict = getPrediction(dataPoints, i, groupSize, k)
        predictedNextValue = analisePredictionDict(predictionDict)

        realNextValue = dataPoints[i + groupSize][0]

        if predictedNextValue * realNextValue < 0:
            # if they are not the same direction
            correctCount += 1
            print(f"{colors.GREEN}{(correctCount / (i + 1 - skipped)) * 100:.2f}% correct     {correctCount}/{i + 1 - skipped}    | {i+1}{colors.RESET}")
        elif predictedNextValue * realNextValue > 0:
            # they are the same direction
            print(f"{colors.RED}{(correctCount / (i + 1 - skipped)) * 100:.2f}% incorrect   {correctCount}/{i + 1 - skipped}    | {i+1}{colors.RESET}")
        else:
            # they did not meet the threshold
            skipped += 1

            if i + 1 - skipped == 0:
                print(f"{colors.YELLOW}NaN% skipped     {correctCount}/{i + 1 - skipped}    | {i+1}{colors.RESET}")

            else:
                print(f"{colors.YELLOW}{(correctCount / (i + 1 - skipped)) * 100:.2f}% skipped     {correctCount}/{i + 1 - skipped}    | {i+1}{colors.RESET}")

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


def getDataPoints(filePath):
    print("Getting dataPoints from csv... ", end="")

    dataPoints = []

    with open(filePath, "r") as csvFile:
        csvReader = csv.reader(csvFile)
        # skip first row
        next(csvReader)
        # time, Open, High, Low, Close, Volume
        for row in csvReader:
            if float(row[5]) == 0:
                # skip "empty" rows
                continue

            # difference between close and open price
            dataPoints.append(float(row[4]) - float(row[1]))

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


def getPrediction(dataPoints, dpIndex, groupSize, k):
    """
    here a group is a tuple of dataPoints.
    index 0 is at index 0 and so on

    :param dataPoints:
    :param dpIndex:
    :param groupSize:
    :param k:
    :return:
    """

    # create currentGroup
    currentGroup = []
    for i in range(groupSize):
        currentGroup.append(dataPoints[dpIndex + i])

    for i in range(len(dataPoints) - groupSize):
        if i == dpIndex:
            continue

        tmpGroup = []
        for j in range(groupSize):
            tmpGroup.append(dataPoints[i + j])

        averageDistance = compareGroups(currentGroup, tmpGroup)
        # TODO store best distances etc



if __name__ == '__main__':
    dataPoints = getDataPoints("../forexData/EURUSD_Candlestick_15_M_BID_01.01.2022-01.01.2023.csv")



    displayDataPoints(dataPoints)

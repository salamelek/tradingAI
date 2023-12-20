"""
BASIC GOAL
    The goal of this program is to say what action should have been taken given the price action and specific time
    So basically I want the program to say "long" when the price is about to go up
    and I want it to say "short" when the price is about to go down

    Since this program should be quite picky, I hope I won't have to rely on another program that refines the choices of this one.

DETECT A SLOPE:
    THINKING
    to detect a nice slope and thus the beginning of it, I need some key parameters:
        1) xMin: the min time that has to pass from the beginning of the slope to the end of it
        2) xMax: the max time that can pass from the beginning of the slope to the end of it
        3) yMin: the min change in price that has to happen for a slope to be considered
        4) mMax: the max inclination that the slope can have (we don't want to consider those instant cliffs)
        5) chopMax: the max amount of chope that we allow a slope to have
            But how do I detect chop?
                1) average distance from line
                2) area between price and line

    THE MATH MUST GET MATHING
        x: time
        y: price
        A: open position
        N1, N2, ..., NK: all the values between A and B
        B: close position

        1) Bx - Ax >= xMin
        2) Bx - Ax <= xMax
        3) By - Ay >= yMin
        4) (By - Ay) / (Bx - Ax) <= mMax
        5.1) sum(dist(line, N1), dist(line, N2), ..., dist(line, NK)) / K
        5.2) ??? idk I don't want to implement that

OPTIMISATION
    I could check for each kline all the following xMax - xMin klines, but this would be slow
    Instead, I think it would be quicker to first eliminate all the values that do not meet certain conditions
    and then refine the search. E.g.: first eliminate the values that can't reach yMin within xMax, then calculate the chop
"""

import numpy as np
import matplotlib.pyplot as plt

from KNN_v1.loadingBar import loadingBar
from binanceDataReader import getCryptoDf


"""
THE MAIN PARAMETERS

xMin    [int]   : number of minimum klines for a slope
xMax    [int]   : number of maximum klines for a slope
yMin    [float] : the minimum change in % (0.11 = 11%)
mMax    [int]   : the maximum allowed slope of a slope
chopMax [float] : the maximum allowed chop (1 seems about good?)
"""
xMin = 5
xMax = 100
yMin = 0.05
# TODO maybe rethink how to measure this thing here
mMax = 2
chopMax = 3

# klineFile = "labeledDf-GC15min-01-09-23 00:00:00.json"
klineFile = "ETHUSDT-15m-2020.csv"


def getDf():
    # let's load the data that we stole
    # return pd.read_json(f"klineData/{klineFile}")
    return getCryptoDf()


def plot(df, slopes):
    # plot the price
    df["close"].plot(color="black")

    # plot the slopes
    for key in slopes.keys():
        Ax = slopes[key]["xStart"]
        Ay = slopes[key]["yStart"]
        Bx = slopes[key]["xEnd"]
        By = slopes[key]["yEnd"]

        plt.plot([Ax, Bx], [Ay, By], linestyle="dashed", marker='x')

    plt.grid()
    plt.show()


def getDistanceOfPointFromLine(xPoint, yPoint, x1, y1, x2, y2):
    """
    Returns the distance of the point x0 y0 to the line defined by the two points

    :param xPoint: X coord of the point
    :param yPoint: Y coord of the point
    :param x1: X coord of the first point defining the line
    :param y1: Y coord of the first point defining the line
    :param x2: X coord of the second point defining the line
    :param y2: Y coord of the second point defining the line
    :return:
    """

    a = np.abs((y2 - y1) * xPoint + (x1 - x2) * yPoint - x1 * y2 + x2 * y1)
    b = np.sqrt((y2 - y1) ** 2 + (x1 - x2) ** 2)
    distance = a / b

    return distance


def getChopOfSeries(series):
    """
    x: time
    y: price
    A: open position
    N1, N2, ..., NK: all the values between A and B
    B: close position

    5.1) sum(dist(line, N1), dist(line, N2), ..., dist(line, NK)) / K

    the series must be at least 3 long, since
    series[0] and series[-1] are not considered in the average

    :param series:
    :return:
    """

    # just make sure that it's a list
    series = list(series)

    if len(series) < 3:
        print(series)
        raise Exception("No enough values in series!")

    totChop = 0

    x1 = 0
    y1 = series[x1]
    x2 = len(series) - 1
    y2 = series[x2]

    for i in range(len(series[1:-1])):
        xPoint = i + 1
        yPoint = series[xPoint]
        totChop += getDistanceOfPointFromLine(xPoint, yPoint, x1, y1, x2, y2)

    return totChop / len(series[1:-1])


def getSlopesTheSlowWay(df, xMin, xMax, yMin, mMax, chopMax):
    """
    x: time
    y: price
    A: open position
    N1, N2, ..., NK: all the values between A and B
    B: close position

    1) Bx - Ax >= xMin
    2) Bx - Ax <= xMax
    3) By - Ay >= yMin
    4) (By - Ay) / (Bx - Ax) <= mMax
    5.1) sum(dist(line, N1), dist(line, N2), ..., dist(line, NK)) / K

    :param df:
    :param xMin:
    :param xMax:
    :param yMin:
    :param mMax:
    :param chopMax:
    :return:
    """

    slopesDict = {}

    for Ax in range(len(df["close"]) - xMax):
        for Bx in range(Ax + xMin, Ax + xMax):
            # let's check each condition in the inverse way, to speed things up
            # xMin and xMax are taken care of by the specified range

            Ay = df["close"][Ax]
            By = df["close"][Bx]

            # yMin (remember that its in %)
            # it's abs because it's good in both directions
            yChange = abs((By - Ay) / Ay)
            if yChange < yMin:
                continue

            # mMax
            if (By - Ay) / (Bx - Ax) > mMax:
                continue

            # chop3
            chop = getChopOfSeries(df["close"][Ax:Bx + 1])
            if chop > chopMax:
                continue

            # if the code arrives here, it means that we got a slope :D
            slopesDict[Ax] = {
                "xStart": Ax,
                "xEnd": Bx,
                "yStart": Ay,
                "yEnd": By,
                "yChange": yChange,
                "chop": chop
            }

        loadingBar(Ax + 1, len(df.index) - xMax, f"Getting slopes (got {len(slopesDict.keys())}): ")

    return slopesDict


def getLabeledData(df, slopes):
    """
    This function takes the dataFrame alongside the slopes dict and labels each kline in the dataframe
    Hold: 0
    Sell: -1
    Buy: 1
    The key of the dict is the index of the kline

    :param df:
    :param slopes:
    :return:
    """

    labels = []

    for i in range(len(df["close"])):
        # check if there is a slope starting at time i
        if i not in slopes.keys():
            labels.append(0)
            continue

        # check if the slope is rising or falling
        if slopes[i]["yStart"] > slopes[i]["yEnd"]:
            labels.append(-1)

        else:
            labels.append(1)

    df["label"] = labels
    # do NOT drop rows with same coords!

    return df


if __name__ == '__main__':
    df = getDf()

    slopes = getSlopesTheSlowWay(df, xMin, xMax, yMin, mMax, chopMax)

    # export the labeled data
    labeledDf = getLabeledData(df, slopes)
    df.to_json(rf'./labeled_data/autoLabeledDf-{klineFile}')

    plot(df, slopes)

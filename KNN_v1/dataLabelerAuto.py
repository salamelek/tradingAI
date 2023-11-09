"""
1) data from a dict
2) check at which point it was optimal to buy/sell/hold
    2.1) since this will be algorithmic, I need a concrete way of telling if a trade is good or bad. I will measure it in profit %.
    2.2) Parameters required to define a "good" slope:
        xMin: min num of Klines
        xMax: max num of klines
        yMin: min difference in price
        chop: max tolerated "choppiness" (~~> standard deviation) NOT TRUE! it's not std
            2.2.1) First draw a line from the first point to the last.
            2.2.2) calculate the distance for each point to the line
            2.2.3) average those distances
    2.3)
        - from kline a, check points in the range [a + xMin, a + xMax]
        - for each kline check, check also y
        - if y > yMin, then check also the std from a to the current kline
        - if std([a, cKline]) < chop, then store a as a good slope point
        - continue to do this until end dof check klines, then procede to the next kline, b
3) label that point
    Since I don't know the timestamps, I'll have to derive them myself.
    Since I know the start kline, current kline and kline time, i can calculate the current kline's timestamp
    Data example:
        timestamp of start of slope: [coords, close, x, y, std, label]

        GC15min = {
            19-09-23 13:00:00: {
                "coords": [adx0, adx1, ..., rsi4],
                "close": 1924.65,
                "label": "s",
                "duration": 7,
                "priceChange": -3.6,
                "std": 1.2
            },
            19-09-23 13:15:00: {
                "coords": [adx0, adx1, ..., rsi4],
                "close": 1920.52,
                "label": "h",
                "duration": None,
                "priceChange": None,
                "std": None
            },
            . . .
        }
"""

import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from loadingBar import progressBar


xMin = 2
xMax = 96
# the difference in price
yMin = 5
# FIXME try to find a better choppiness function, because this one is shit
"""
maybe instead of calculating the distance from the line, do the following:
    if the line goes up, only calculate the distance of the values beneath it
    if the line goes down, only calculate the distance of the values above it
"""
chopMax = 0.01


with open("GC15min-01-01-23 00:00:00.json", "r") as jsonFile:
    klines = json.load(jsonFile)

df = pd.DataFrame.from_dict(klines, orient='index')
df.columns = ['close', 'coords']
df.insert(0, "timestamp", df.index)
df.reset_index(drop=True, inplace=True)

# fill buffer to speed things up
checkList = []
for i in range(xMax):
    checkList.append(df["close"][i + 1])


def getDistanceOfPointFromLine(x0, y0, x1, y1, x2, y2):
    """
    :param x0:
    :param y0:
    :param x1:
    :param y1:
    :param x2:
    :param y2:
    :return:
    """
    a = np.abs(((x2 - x1) * (y1 - y0)) - ((x1 - x0) * (y2 - y1)))
    b = np.sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))
    return a / b


def getChopOfSeries(series):
    if len(series) < 2:
        raise Exception("No enough values in series.")

    distances = []
    for i in range(len(series)):
        x1 = 0
        y1 = series[x1]
        x2 = len(series) - 1
        y2 = series[x2]
        xa = i
        ya = series[xa]

        v1 = (x2 - x1, y2 - y1)  # Vector 1
        v2 = (x2 - xa, y2 - ya)  # Vector 2
        xp = v1[0] * v2[1] - v1[1] * v2[0]  # Cross product (magnitude)

        rising = series[-1] - series[0] >= 0
        above = xp < 0

        # if the point is below and the series is rising
        if not above and rising:
            print('below')
            distances.append(getDistanceOfPointFromLine(i, series[i], 0, series[0], len(series) - 1, series[-1]))

        if not above and not rising:
            distances.append(0)

        # if the point is above and the series is falling
        if above and not rising:
            print('above')
            distances.append(getDistanceOfPointFromLine(i, series[i], 0, series[0], len(series) - 1, series[-1]))

        if above and rising:
            distances.append(0)

    print(distances)
    return np.mean(distances)


print(getChopOfSeries([0, -0.5, 1]))
exit()


niceValues = []
for i in range(xMax, len(df.index) - xMax):
    for j in range(xMin, xMax + 1):
        y = np.abs(df["close"][i] - df["close"][i + j])
        chop = getChopOfSeries(checkList[:j])

        if y > yMin and chop < chopMax:
            niceValues.append({"startKline": i, "targetKline": (i + j), "x": j, "y": y, "chop": chop})

    # update buffer
    checkList.pop(0)
    checkList.append(df["close"][i])

    progressBar(i + 1, len(df.index) - xMax, f"Getting niceValues: ")

print()

# filter out niceValues so only the best answer for each kline remains
bestValues = []
dictGroup = [niceValues[0]]
for i in range(len(niceValues) - 1):
    currDict = niceValues[i]
    nextDict = niceValues[i + 1]

    if currDict["startKline"] == nextDict["startKline"]:
        dictGroup.append(nextDict)

    else:
        bestValues.append(max(dictGroup, key=lambda x: x['y']))
        dictGroup = [nextDict]

# print(niceValues)
# print(bestValues)

# plot price
df.plot(color="black")

# plot lines
for point in bestValues:
    xA = point["startKline"]
    xB = point["targetKline"]

    yA = df["close"][xA]
    yB = df["close"][xB]

    plt.plot([xA, xB], [yA, yB], linestyle="dashed", marker='x', label='Line AB')

plt.grid()
plt.show()

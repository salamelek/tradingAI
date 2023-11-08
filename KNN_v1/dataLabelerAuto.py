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


xMin = 2
xMax = 5
yMin = 0.01
chop = 5


with open("GC15min-01-01-23 00:00:00.json", "r") as jsonFile:
    klines = json.load(jsonFile)

df = pd.DataFrame.from_dict(klines, orient='index')
df.columns = ['close', 'coords']
df.insert(0, "timestamp", df.index)
df.reset_index(drop=True, inplace=True)

# fill buffer to speed things up
checkList = []
for i in range(xMax):
    checkList.append(df["close"][i])


def getDistanceOfPointFromLine(p0, p1, p2):
    """
    :param p0: the point that we care about
    :param p1: point 1 that defines the line
    :param p2: point 2 that defines the line
    :return:
    """

    return np.abs((p2[0] - p1[0]) * (p1[1] - p0[1]) - (p1[0] - p0[0]) * (p2[1] - p1[1])) / np.sqrt(((p2[0] - p1[0]) ** 2) + ((p2[1] - p1[1]) ** 2))


def getAvgDistFromLine(series):
    if len(series) < 2:
        raise Exception("No enough values in series.")

    distances = []
    for i in range(len(series) - 1):
        distances.append(getDistanceOfPointFromLine((i, series[i]), (0, series[0]), (len(series), series[-1])))

    return np.average(distances)


for i in range(xMax, len(df.index)):
    # FIXME figure this shit out
    print(i, checkList)
    for j in range(xMin, xMax + 1):
        print(j, checkList[j:i + 1], checkList[j:i])
        # print(i, checkList[j:i + 1], getAvgDistFromLine(checkList[:j]))

    # update buffer
    checkList.pop(0)
    checkList.append(df["close"][i])


df.plot()
plt.grid()
plt.show()

"""
This program will use labeled data to guess on new data.
It will draw a chart of the given price action with indicators on where to open a position
"""

import time
import pandas as pd
import matplotlib.pyplot as plt

from KNN_v1.loadingBar import loadingBar

# k number of closest points
k = 3
# threshold for dividing the space
startT = 50
# by how much will the threshold increase each iteration
tk = 20

labeledDf = pd.read_json("labeled_data/autoLabeledDf-GC15min-01-01-23 00:00:00.json")
newDf = pd.read_json("klineData/df-GC15min-27-11-23 00:00:00.json")

"""
Try setting (0, 0) around the point of interest and shift every other point accordingly.
Then take in consideration only the points that are somewhat close to the center

1) shift every point accordingly
2) select a threshold t
3) calculate the distance of each point that is within t
4) check if there are enough values (if not, go to 2, if yes continue)
5) sort the values and get the first k
"""

startTime = time.time()


def inCircle(coords, t):
    if (
            (coords[0] ** 2) +
            (coords[1] ** 2) +
            (coords[2] ** 2) +
            (coords[3] ** 2) +
            (coords[4] ** 2) +
            (coords[5] ** 2) +
            (coords[6] ** 2) +
            (coords[7] ** 2) +
            (coords[8] ** 2) +
            (coords[9] ** 2) +
            (coords[10] ** 2) +
            (coords[11] ** 2) +
            (coords[12] ** 2) +
            (coords[13] ** 2) +
            (coords[14] ** 2)
    ) > (t ** 2):
        return False

    else:
        return True


def inSquare(coords, t):
    for coord in coords:
        if abs(coord) > t:
            return False

    return True


def getCenteredCoords(point, coords):
    centeredCoords = []
    for i in range(len(coords)):
        centeredCoords.append(coords[i] - point[i])

    return centeredCoords


predictedLabels = []

# for each point in the new dataframe
for i in range(len(newDf["coords"])):
    distList = []
    t = startT

    while len(distList) < k:
        # reset it each time, so it doesn't get overwritten each time t increases
        distList = []

        # for each labeled coordinate
        for j in range(len(labeledDf["coords"])):
            # shift every point
            centeredLabeledCoords = getCenteredCoords(newDf["coords"][i], labeledDf["coords"][j])

            # if the point is not in the threshold range, don't bother with it
            if not inSquare(centeredLabeledCoords, t):
                continue

            if not inCircle(centeredLabeledCoords, t):
                continue

            # now that the point is in the threshold, deal with it
            dist = 0

            for x in centeredLabeledCoords:
                dist += x ** 2

            distList.append((dist, labeledDf["label"][j]))

        loadingBar(i + 1, len(newDf["coords"]), f"Calculating distances: ", f"| elapsed: {round(time.time() -  startTime, 2)}s")

        t += tk

    sortedDistList = sorted(distList, key=lambda x: x[0])
    firstKNP = sortedDistList[:k]
    predictedLabel = int(round(sum(x[1] for x in firstKNP) / k, 0))
    predictedLabels.append(predictedLabel)

print()

# print(f"k={k} t={startT}, tk={tk} | time: {round(time.time() - startTime, 2)}s")
# print(predictedLabels)

longX = []
longY = []
shortX = []
shortY = []
for i in range(len(predictedLabels)):
    if predictedLabels[i] == 1:
        longX.append(i)
        longY.append(newDf["close"][i])
    elif predictedLabels[i] == -1:
        shortX.append(i)
        shortY.append(newDf["close"][i])

# plot
newDf["close"].plot()

plt.scatter(longX, longY, color='green', label='Long Positions')
plt.scatter(shortX, shortY, color='red', label='Short Positions')

plt.grid()
plt.show()

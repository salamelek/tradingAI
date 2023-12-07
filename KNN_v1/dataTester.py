"""
This program will use labeled data to guess on new data.
It will draw a chart of the given price action with indicators on where to open a position
"""

import time

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from KNN_v1.loadingBar import loadingBar


k = 1


labeledDf = pd.read_json("labeled_data/autoLabeledDf-GC15min-01-01-23 00:00:00.json")
newDf = pd.read_json("klineData/df-GC15min-27-11-23 00:00:00.json")


# for each point in the new df calculate the closest k neighbours
counter = 1
guessedLabels = []

# TODO
"""
Try setting (0, 0) around the point of interest and shift every other point accordingly.
Then take in consideration only the points that are somewhat close to the center

1) shift every point accordingly
2) select a threshold t
3) calculate the distance of each point that is within t
4) check if there are enough values (if not, go to 2, if yes continue)
5) sort the values and get the first k
"""
for i in range(len(newDf["coords"])):
    coords = newDf["coords"][i]

    # shift every point
    centeredLabeledDf = labeledDf["coords"] - coords


# TODO

for coords in newDf["coords"]:
    distList = []
    for i in range(len(labeledDf["coords"])):
        distList.append((sum((labeledDf["coords"][i][j] - coords[j]) ** 2 for j in range(15)), labeledDf["label"][i]))

    sortedDistList = sorted(distList, key=lambda x: x[0])
    closestKNP = sortedDistList[:k]

    labelsSum = 0
    for closePoint in closestKNP:
        labelsSum += closePoint[1]
    labelsAvg = labelsSum / k

    if abs(labelsAvg) <= 0.5:
        guessedLabels.append(0)

    elif labelsAvg > 0.5:
        guessedLabels.append(1)

    elif labelsAvg < 0.5:
        guessedLabels.append(-1)

    loadingBar(counter + 1, len(newDf.index), f"Calculating distances...")
    counter += 1

print()

longX = []
longY = []
shortX = []
shortY = []
for i in range(len(guessedLabels)):
    # print(f"{i}: {guessedLabels[i]}")
    if guessedLabels[i] == 1:
        longX.append(i)
        longY.append(newDf["close"][i])
    elif guessedLabels[i] == -1:
        shortX.append(i)
        shortY.append(newDf["close"][i])

# plot
newDf["close"].plot()

plt.scatter(longX, longY, color='green', label='Long Positions')
plt.scatter(shortX, shortY, color='red', label='Short Positions')

plt.grid()
plt.show()

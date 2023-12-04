"""
This program will use labeled data to guess on new data.
It will draw a chart of the given price action with indicators on where to open a position
"""

import pandas as pd
import matplotlib.pyplot as plt

from KNN_v1.loadingBar import progressBar


k = 1


labeledDf = pd.read_json("labeled_data/autoLabeledDf-GC15min-01-01-23 00:00:00.json")
newDf = pd.read_json("klineData/df-GC15min-27-11-23 00:00:00.json")


# for each point in the new df calculate the closest k neighbours
counter = 1
guessedLabels = []
for coords in newDf["coords"]:
    distList = []
    for i in range(len(labeledDf["coords"])):
        distList.append((sum((labeledDf["coords"][i][j] - coords[j]) ** 2 for j in range(15)), labeledDf["label"][i]))

    sortedDistList = sorted(distList, key=lambda x: x[0])
    closestKNP = sortedDistList[:k]

    # find the most common label
    holdCount, shortCount, longCount = 0, 0, 0
    for closePoint in closestKNP:
        if closePoint[1] == 0:
            holdCount += 1
        elif closePoint[1] == 1:
            longCount += 1
        elif closePoint[1] == -1:
            shortCount += 1

    if holdCount >= shortCount and holdCount >= longCount:
        guessedLabels.append(0)

    elif shortCount > holdCount and shortCount > longCount:
        guessedLabels.append(-1)

    elif longCount > shortCount and longCount > holdCount:
        guessedLabels.append(1)

    progressBar(counter, len(newDf.index), f"Calculating distances...")
    counter += 1

print()

longX = []
longY = []
shortX = []
shortY = []
for i in range(len(guessedLabels)):
    print(f"{i}: {guessedLabels[i]}")
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

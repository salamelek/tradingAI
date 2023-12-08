"""
This program will use labeled data to guess on new data.
It will draw a chart of the given price action with indicators on where to open a position
"""

import time
import pandas as pd
import matplotlib.pyplot as plt

from KNN_v1.loadingBar import loadingBar

# k number of closest points
k = 2
# threshold for dividing the space
startT = 10
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


def isInThreshold(coords, t):
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

    while len(distList) <= k:
        # for each labeled coordinate
        for j in range(len(labeledDf["coords"])):
            # shift every point
            centeredLabeledCoords = getCenteredCoords(newDf["coords"][i], labeledDf["coords"][j])

            # if the point is not in the threshold range, don't bother with it
            if not isInThreshold(centeredLabeledCoords, t):
                continue

            # now that the point is in the threshold, deal with it
            dist = 0

            for x in centeredLabeledCoords:
                dist += x ** 2

            distList.append((dist, labeledDf["label"][j]))

        loadingBar(i + 1, len(newDf["coords"]), f"Calculating distances [t={t}]: ")

        t += tk
    # FIXME when changing t or tk, there is a different amount of distances in sortedDistList
    # FIXME actually that is normal since less t means less values. I now have to check if all the values are the minimal ones
    # FIXME probably because i am checking in a square instead of a circle so some points in angles are categorised as closer than just outside the side
    sortedDistList = sorted(distList, key=lambda x: x[0])
    firstKNP = sortedDistList[:k]
    predictedLabel = int(round(sum(x[1] for x in firstKNP) / k, 0))
    predictedLabels.append(predictedLabel)

print()

print(f"k={k} t={startT}, tk={tk} | time: {round(time.time() - startTime, 2)}s")
print(predictedLabels)
print(sortedDistList)

longX = []
longY = []
shortX = []
shortY = []
for i in range(len(predictedLabels)):
    # print(f"{i}: {guessedLabels[i]}")
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

"""
k=2 t=20, tk=20 | time: 16.72s
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
[(1560.93324425, 0), (1736.4370342599996, 0), (1864.810694750001, 0), (2226.407562150001, 0), (2266.23956334, 0), (2342.5752988, 0), (2399.0681147600008, 0), (2463.0607758300007, 0), (2555.183875920001, 0), (2770.1634953700013, 0), (2775.4271140300016, 1), (2913.4264036200007, 0), (2934.4878987200004, 0), (3043.7280350100013, 0), (3206.5341237800017, 0), (3252.8954416600004, 0), (3309.445838440001, 0), (3643.9131585600003, 0), (3646.6008845100005, 0), (3660.0820776199994, 0), (3810.0912887100003, 0), (3867.582724090001, 0), (3878.9405082900003, 0), (3966.9512762199993, 0), (4088.935439680001, 0), (6467.103815209999, 0), (6475.763823190002, 0), (7717.934936270002, 0)]
k=2 t=10, tk=20 | time: 18.99s
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
[(1560.93324425, 0), TUKAJ MANJKA             (1864.810694750001, 0), TUKAJ MANJKA            (2266.23956334, 0), (2342.5752988, 0), TUKAJ MANJKA              TUKAJ MANJKA              TUKAJ MANJKA          (2770.1634953700013, 0), (2775.4271140300016, 1), TUKAJ MANJKA             TUKAJ MANJKA             (3043.7280350100013, 0), TUKAJ MANJKA             TUKAJ MANJKA             (3309.445838440001, 0), TUKAJ MANJKA             (3646.6008845100005, 0), TUKAJ MANJKA             (3810.0912887100003, 0), TUKAJ MANJKA            (3878.9405082900003, 0) TUKAJ MANJKA             TUKAJ MANJKA             TUKAJ MANJKA             TUKAJ MANJKA             TUKAJ MANJKA             ]

"""

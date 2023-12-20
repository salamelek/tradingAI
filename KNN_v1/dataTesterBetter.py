import math
import copy
import pandas as pd
import matplotlib.pyplot as plt

from binanceDataReader import getCryptoDf
from loadingBar import loadingBar


quadSize = 100
k = 3

quadrants = {}


def getDistance(p1, p2):
    # we are assuming that p1 and p2 have the same number of coords
    distSquared = 0

    for i in range(len(p1)):
        distSquared += (p1[i] - p2[i]) ** 2

    return math.sqrt(distSquared)


class Quadrant:
    def __init__(self, pIndexes, coords):
        # store the indexes of the points so the label is easily accessible
        self.pIndexes = pIndexes
        self.coords = coords

    def getKNN(self, point, k):
        # work with a deepcopy to not get ducked in the grass
        pIndexes = copy.deepcopy(self.pIndexes)

        # if len(pIndexes) < k:
        #     # TODO widen the quadrant
        #     pass

        # calculate knn
        distDict = {}

        for index in self.pIndexes:
            p = labeledDf["coords"][index]
            dist = getDistance(p, point)
            distDict[dist] = index

        firstKSortedKeys = sorted(distDict.keys())[:k]

        # if distDict[firstKSortedKeys[-1]] > quadSize / 2:
        #     # TODO i think quadSize / 2 is correct..
        #     pass

        knnIndexes = []

        for sortedIndex in firstKSortedKeys:
            knnIndexes.append(distDict[sortedIndex])

        return knnIndexes


def getQuadCoordsOfPoint(point):
    quadCoords = []
    for coord in point:
        quadCoords.append(coord // quadSize)

    return tuple(quadCoords)


# get the labeled points
print("Fetching data... ")
labeledDf = pd.read_json("labeled_data/autoLabeledDf-MERGED-ETHUSDT-15m-2020.json")
newDf = getCryptoDf("/2023-data/MERGED-ETHUSDT-15m-23.csv")
print("Done!")

# place the points in the appropriate quadrant
print("Placing the data points into quadrants... ")
for pIndex in labeledDf.index:
    quadCoords = getQuadCoordsOfPoint(labeledDf["coords"][pIndex])

    try:
        quadrants[quadCoords].pIndexes.append(pIndex)
    except KeyError:
        newQuad = Quadrant(pIndexes=[], coords=quadCoords)
        newQuad.pIndexes.append(pIndex)
        quadrants[quadCoords] = newQuad


print("Done!")

print("\nresult of placing points:")
print("quadrants: ", len(quadrants.keys()))
print("points:    ", len(labeledDf["coords"]))

predictedLabels = []

# now check every point
for i in range(len(newDf["coords"])):
    point = newDf["coords"][i]
    quadCoords = getQuadCoordsOfPoint(point)

    try:
        quad = quadrants[quadCoords]
    except KeyError:
        # there are no points in the quadrant, aka the quadrant does not exist
        # create the empty quadrant
        quad = Quadrant([], quadCoords)
        quadrants[quadCoords] = quad

    knnIndexes = quad.getKNN(point, k)
    knnLabels = []

    for index in knnIndexes:
        knnLabels.append(labeledDf["label"][index])

    predictedLabel = int(round(sum(knnLabels) / k, 0))
    predictedLabels.append(predictedLabel)

    loadingBar(i + 1, len(newDf["coords"]), f"Calculating distances: ")


print()

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

plt.scatter(longX, longY, color='green')
plt.scatter(shortX, shortY, color='red')

plt.grid()
plt.show()

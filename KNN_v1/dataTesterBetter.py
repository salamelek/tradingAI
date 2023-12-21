import math
import copy
import pandas as pd
import matplotlib.pyplot as plt

from binanceDataReader import getCryptoDf
from loadingBar import loadingBar


quadSize = 90
k = 5

quadrants = {}


# get the labeled points
print("Fetching data... ")

# labeledDf = pd.read_json("labeled_data/autoLabeledDf-MERGED-ETHUSDT-15m-2020.json") # 2yrs 15m data
labeledDf = pd.read_json("labeled_data/autoLabeledDf-ETHUSDT-3m-2023-10.json")

# newDf = getCryptoDf("/2023-data/MERGED-ETHUSDT-15m-23.csv")
newDf = getCryptoDf("/3m-data/ETHUSDT-3m-2023-11.csv")

print("Done!")


class Quadrant:
    def __init__(self, pIndexes, coords):
        # store the indexes of the points so the label is easily accessible
        self.pIndexes = pIndexes
        self.coords = coords

    def getKNN(self, point, k):
        # work with a deepcopy to not get ducked in the grass
        pIndexes = copy.deepcopy(self.pIndexes)
        quadsLvl = 0
        circleCheck = False

        while not circleCheck:
            # FIXME idk if this works
            while len(pIndexes) < k:
                quadsLvl += 1
                nextQuads = getNextQuads(quadsLvl, self)

                for quad in nextQuads:
                    pIndexes += quadrants[quad].pIndexes

            # calculate knn
            distDict = {}

            for index in pIndexes:
                p = labeledDf["coords"][index]
                dist = getDistance(p, point)
                distDict[dist] = index

            firstKSortedKeys = sorted(distDict.keys())
            firstKSortedKeys = firstKSortedKeys[:k]

            # print(f"max distance: {distDict[firstKSortedKeys[-1]]}\n quadSize / 2: {(quadSize / 2) + (quadsLvl * quadSize)}")

            if firstKSortedKeys[-1] <= (quadSize / 2) + (quadsLvl * quadSize):
                # TODO i think quadSize / 2 is correct..
                circleCheck = True

            else:
                quadsLvl += 1

        knnIndexes = []

        for sortedIndex in firstKSortedKeys:
            knnIndexes.append(distDict[sortedIndex])

        return knnIndexes


def getQuadCoordsOfPoint(point):
    quadCoords = []
    for coord in point:
        quadCoords.append(coord // quadSize)

    return tuple(quadCoords)


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


def getDistance(p1, p2):
    # we are assuming that p1 and p2 have the same number of coords
    if len(p1) != len(p2):
        raise Exception("P1 and P2 have not the same len of coords!!!")

    distSquared = 0

    for i in range(len(p1)):
        distSquared += (p1[i] - p2[i]) ** 2

    return math.sqrt(distSquared)


def isOnCorrectLevel(startQuadCoords, quadCoords, quadLevel):
    # check if at least one difference of coordinates is equal to quadLevel
    for i in range(len(startQuadCoords)):
        if abs(startQuadCoords[i] - quadCoords[i]) == quadLevel:
            return True

    return False


def getNextQuads(quadLevel, startQuad):
    """
    This must return a list of ONLY the quadrants at the specified level

    :param quadLevel:
    :param startQuad:
    :return:
    """

    startQuadCoords = startQuad.coords
    nextQuadsCoords = []
    """
    now append to nextQuadCoords all the possible ± quadLevel permutations (?)
    so if I have 2D and the start quad is (1, 1), then I have to append the following:
        +: (2, 1), (1, 2), (2, 2)
        -: (0, 1), (1, 0), (0, 0)
        ±: (2, 0)
        ∓: (0, 2)
    the number of quadrants, when the number of dimensions is d adn quadLevel >= 1:
        (2 * quadLevel + 1)^d - (2 * quadLevel - 1)^d
    lets try for 2D, quadLevel = 2:
        Base quadrant: (0, 0)
        +: ( 2,  0), ( 2,  1), ( 0,  2), ( 1,  2), ( 2,  2)
        -: (-2,  0), (-2, -1), ( 0, -2), (-1, -2), (-2, -2)
        ±: (-1,  2), (-2,  2), (-2,  1)
        ∓: ( 1, -2), ( 2, -2), ( 2, -1)
        
    The above stuff is waaay to hard for me to do 
    so i will just loop through all the quadrants and see which ones are good
    """

    # for each quadrant in quadrants
    for k in quadrants.keys():
        quadCoords = quadrants[k].coords

        if isOnCorrectLevel(startQuadCoords, quadCoords, quadLevel):
            nextQuadsCoords.append(quadCoords)

    return nextQuadsCoords


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

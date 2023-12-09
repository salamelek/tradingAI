import matplotlib.pyplot as plt


# k number of closest points
k = 2
# threshold for dividing the space
startT = 10
# by how much will the threshold increase each iteration
tk = 20


newCoords = {
    "close": [10, 11, 9],
    "coords": [(0, 0), (1, 1), (2, 1)]
}
labeledCoords = {
    "coords": [(1, 2), (2, 1), (3, 4)],
    "label": [1, 1, 1]
}


def isInThreshold(coords, t):
    if ((coords[0] ** 2) + (coords[1] ** 2)) > (t ** 2):
        return False

    # for coord in coords:
        # if abs(coord) > t:
        #     return False
    else:
        return True


def getCenteredCoords(point, coords):
    centeredCoords = []
    for i in range(len(coords)):
        centeredCoords.append(coords[i] - point[i])

    return centeredCoords


predictedLabels = []

# for each point in the new dataframe
for i in range(len(newCoords["coords"])):
    distList = []
    t = startT

    while len(distList) <= k:
        # for each labeled coordinate
        for j in range(len(labeledCoords["coords"])):
            # shift every point
            centeredLabeledCoords = getCenteredCoords(newCoords["coords"][i], labeledCoords["coords"][j])

            # if the point is not in the threshold range, don't bother with it
            if not isInThreshold(centeredLabeledCoords, t):
                continue

            # now that the point is in the threshold, deal with it
            dist = 0

            for x in centeredLabeledCoords:
                dist += x ** 2

            distList.append((dist, labeledCoords["label"][j]))

        t += tk
    # FIXME when changing t or tk, there is a different amount of distances in sortedDistList
    # FIXME actually that is normal since less t means less values. I now have to check if all the values are the minimal ones
    # FIXME probably because i am checking in a square instead of a circle so some points in angles are categorised as closer than just outside the side
    sortedDistList = sorted(distList, key=lambda x: x[0])
    firstKNP = sortedDistList[:k]
    predictedLabel = int(round(sum(x[1] for x in firstKNP) / k, 0))
    predictedLabels.append(predictedLabel)

print()

print(f"k={k} t={startT}, tk={tk}")
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
        longY.append(newCoords["close"][i])
    elif predictedLabels[i] == -1:
        shortX.append(i)
        shortY.append(newCoords["close"][i])

# plot
plt.plot(newCoords["close"])

plt.scatter(longX, longY, color='green', label='Long Positions')
plt.scatter(shortX, shortY, color='red', label='Short Positions')

plt.grid()
plt.show()

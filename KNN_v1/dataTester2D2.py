import math
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
    "coords": [(1, 2), (2, 1), (-1, -1), (0.7, 0.4)],
    "label": [1, 1, 1]
}


def getDist(point):
    return math.sqrt(point[0] ** 2 + point[1] ** 2)


for point in labeledCoords["coords"]:
    print(f"{point}: {round(getDist(point), 2)}")

# plot

coordsX = []
coordsY = []

for coord in labeledCoords["coords"]:
    coordsX.append(coord[0])
    coordsY.append(coord[1])

fig, ax = plt.subplots()

plt.axhline(y=0, color='k')
plt.axvline(x=0, color='k')

plt.scatter(coordsX, coordsY, color='red', label='Short Positions')

plt.grid()
plt.gca().set_aspect('equal')
plt.show()

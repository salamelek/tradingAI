import json
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


k = 3
wantedIndex = -1


with open('labeled_data/2023-10-23-15min-adx-cci-rsi-5-test1.json') as jsonFile:
    data = json.load(jsonFile)


# convert to usable dict
trainDict = {
    "x1": [],
    "x2": [],
    "x3": [],
    "x4": [],
    "x5": [],
    "x6": [],
    "x7": [],
    "x8": [],
    "x9": [],
    "x10": [],
    "x11": [],
    "x12": [],
    "x13": [],
    "x14": [],
    "x15": [],
    "label": []
}
for key in data.keys():
    for triplet in data[key]:
        # i don't careeeeeeeeeeeee
        trainDict["x1"].append(triplet[0][0])
        trainDict["x2"].append(triplet[0][1])
        trainDict["x3"].append(triplet[0][2])
        trainDict["x4"].append(triplet[0][3])
        trainDict["x5"].append(triplet[0][4])
        trainDict["x6"].append(triplet[1][0])
        trainDict["x7"].append(triplet[1][1])
        trainDict["x8"].append(triplet[1][2])
        trainDict["x9"].append(triplet[1][3])
        trainDict["x10"].append(triplet[1][4])
        trainDict["x11"].append(triplet[2][0])
        trainDict["x12"].append(triplet[2][1])
        trainDict["x13"].append(triplet[2][2])
        trainDict["x14"].append(triplet[2][3])
        trainDict["x15"].append(triplet[2][4])
        trainDict["label"].append(key)


trainData = pd.DataFrame(trainDict)
randomRow = 755  # random.randint(0, len(trainData))
testPoint = trainData.iloc[randomRow].tolist()
trainData.drop(randomRow)
testPointLabel = testPoint.pop(-1)

# create a list of all length
distList = []
for i in range(len(trainData)):
    # euclidean distance (its in 15 dimensions, and yet I still call it euclidean?)
    dist = (
            (trainData["x1"][i] - testPoint[0]) ** 2 +
            (trainData["x2"][i] - testPoint[1]) ** 2 +
            (trainData["x3"][i] - testPoint[2]) ** 2 +
            (trainData["x4"][i] - testPoint[3]) ** 2 +
            (trainData["x5"][i] - testPoint[4]) ** 2 +
            (trainData["x6"][i] - testPoint[5]) ** 2 +
            (trainData["x7"][i] - testPoint[6]) ** 2 +
            (trainData["x8"][i] - testPoint[7]) ** 2 +
            (trainData["x9"][i] - testPoint[8]) ** 2 +
            (trainData["x10"][i] - testPoint[9]) ** 2 +
            (trainData["x11"][i] - testPoint[10]) ** 2 +
            (trainData["x12"][i] - testPoint[11]) ** 2 +
            (trainData["x13"][i] - testPoint[12]) ** 2 +
            (trainData["x14"][i] - testPoint[13]) ** 2 +
            (trainData["x15"][i] - testPoint[14]) ** 2
    )

    # maybe exponential distance?
    # dist = some_magic_here

    distList.append((dist, i))

# Sort by the distance
sortedDistList = sorted(distList, key=lambda x: x[0])

# get the first k nearest points
firstKNearPoints = sortedDistList[:k]

# count labels
labelsList = []
for nearPoint in firstKNearPoints:
    labelsList.append(trainData.loc[[nearPoint[1]]]["label"].item())

guessedOutcome = max(set(labelsList), key=labelsList.count)


# now show the results
print(f"True label: {testPointLabel}\nGuessed label: {guessedOutcome}")

# if testPointLabel == "h":
#     exit()

# plot everything

bullishADX, bullishCCI, bullishRSI = [], [], []
bearishADX, bearishCCI, bearishRSI = [], [], []
rangingADX, rangingCCI, rangingRSI = [], [], []

for triplet in data["l"]:
    bullishADX.append(triplet[0][wantedIndex])
    bullishCCI.append(triplet[1][wantedIndex])
    bullishRSI.append(triplet[2][wantedIndex])

for triplet in data["s"]:
    bearishADX.append(triplet[0][wantedIndex])
    bearishCCI.append(triplet[1][wantedIndex])
    bearishRSI.append(triplet[2][wantedIndex])

for triplet in data["h"]:
    rangingADX.append(triplet[0][wantedIndex])
    rangingCCI.append(triplet[1][wantedIndex])
    rangingRSI.append(triplet[2][wantedIndex])

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(bullishADX, bullishCCI, bullishRSI, c='g', marker='o', label="Bullish")
ax.scatter(bearishADX, bearishCCI, bearishRSI, c='r', marker='o', label="Bearish")
ax.scatter(rangingADX, rangingCCI, rangingRSI, c='y', marker='o', label="Ranging")
ax.scatter(testPoint[4], testPoint[9], testPoint[14], c='blue', marker="o", label="Test Point")

ax.set_xlabel("ADX")
ax.set_ylabel("CCI")
ax.set_zlabel("RSI")

plt.title('Training trading data')
plt.show()

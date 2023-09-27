# My first approach to KNN

import random
import pandas as pd
import math

# get some labeled data
# for now I will use a 2D coordinate system (The label will be the quadrant number)
trainDict = {"x": [], "y": [], "label": []}

for i in range(100):
	trainDict["x"].append(random.randint(-100, 100))
	trainDict["y"].append(random.randint(-100, 100))

	if trainDict["x"][i] >= 0 and trainDict["y"][i] >= 0:
		trainDict["label"].append(1)

	if trainDict["x"][i] < 0 <= trainDict["y"][i]:
		trainDict["label"].append(2)

	if trainDict["x"][i] < 0 and trainDict["y"][i] < 0:
		trainDict["label"].append(3)

	if trainDict["x"][i] >= 0 > trainDict["y"][i]:
		trainDict["label"].append(4)

trainData = pd.DataFrame(trainDict)

# get some new data
testPoint = (20, 20)

# try to label it accordingly to the old data

k = 9

# now get the k-nearest neighbours in such a way that is not trash
# instead of using c = sqrt(a**2 + b**2) just use c = a**2 + b**2

# create a list of all length
distList = []
for i in range(len(trainDict["x"])):
	dist = ((trainDict["x"][i] - testPoint[0]) ** 2 + (trainDict["y"][i] - testPoint[1]) ** 2)
	distList.append((dist, i))

sortedDistList = sorted(distList, key=lambda x: x[0])
firstKNearPoints = sortedDistList[:k]

labelsList = []
for nearPoint in firstKNearPoints:
	labelsList.append(trainData.loc[[nearPoint[1]]]["label"].item())

print(max(set(labelsList), key=labelsList.count))

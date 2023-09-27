# My first approach to KNN

import random
import pandas as pd


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
print(trainData)


# get some new data
testPoint = (3, 55)


# try to label it accordingly to the old data

k = 9

# now get the k-nearest neighbours in such a way that is not trash

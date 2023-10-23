import matplotlib.pyplot as plt
import json


wantedIndex = 4


with open('labeled_data/2023-10-23-15min-adx-cci-rsi-5-test1.json') as json_file:
	trainData = json.load(json_file)

bullishADX, bullishCCI, bullishRSI = [], [], []
bearishADX, bearishCCI, bearishRSI = [], [], []
rangingADX, rangingCCI, rangingRSI = [], [], []

for triplet in trainData["l"]:
	bullishADX.append(triplet[0][wantedIndex])
	bullishCCI.append(triplet[1][wantedIndex])
	bullishRSI.append(triplet[2][wantedIndex])

for triplet in trainData["s"]:
	bearishADX.append(triplet[0][wantedIndex])
	bearishCCI.append(triplet[1][wantedIndex])
	bearishRSI.append(triplet[2][wantedIndex])

for triplet in trainData["h"]:
	rangingADX.append(triplet[0][wantedIndex])
	rangingCCI.append(triplet[1][wantedIndex])
	rangingRSI.append(triplet[2][wantedIndex])

# Create a 3D scatter plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(bullishADX, bullishCCI, bullishRSI, c='g', marker='o', label="Bullish")
ax.scatter(bearishADX, bearishCCI, bearishRSI, c='r', marker='o', label="Bearish")
ax.scatter(rangingADX, rangingCCI, rangingRSI, c='y', marker='o', label="Ranging")

ax.set_xlabel("ADX")
ax.set_ylabel("CCI")
ax.set_zlabel("RSI")

plt.title('Training trading data')
plt.show()

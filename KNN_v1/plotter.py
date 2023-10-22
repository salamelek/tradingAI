import matplotlib.pyplot as plt
import json


with open('labeled_data/2023-10-22-15min-adx-cci-rsi-buffer_5_1st-test.json') as json_file:
	trainData = json.load(json_file)

bullishADX, bullishCCI, bullishRSI = [], [], []
bearishADX, bearishCCI, bearishRSI = [], [], []
rangingADX, rangingCCI, rangingRSI = [], [], []

for triplet in trainData["l"]:
	print(triplet)
	bullishADX.append(triplet[0][0])
	bullishCCI.append(triplet[1][0])
	bullishRSI.append(triplet[2][0])

for triplet in trainData["s"]:
	bearishADX.append(triplet[0][0])
	bearishCCI.append(triplet[1][0])
	bearishRSI.append(triplet[2][0])

for triplet in trainData["h"]:
	rangingADX.append(triplet[0][0])
	rangingCCI.append(triplet[1][0])
	rangingRSI.append(triplet[2][0])

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

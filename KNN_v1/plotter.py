import matplotlib.pyplot as plt
import json


with open('data_5m.json') as json_file:
	trainData = json.load(json_file)

bullishADX, bullishCCI, bullishRSI = [], [], []
bearishADX, bearishCCI, bearishRSI = [], [], []
rangingADX, rangingCCI, rangingRSI = [], [], []

for triplet in trainData["bullish"]:
	bullishADX.append(triplet[0])
	bullishCCI.append(triplet[1])
	bullishRSI.append(triplet[2])

for triplet in trainData["bearish"]:
	bearishADX.append(triplet[0])
	bearishCCI.append(triplet[1])
	bearishRSI.append(triplet[2])

for triplet in trainData["ranging"]:
	rangingADX.append(triplet[0])
	rangingCCI.append(triplet[1])
	rangingRSI.append(triplet[2])

# Create a 3D scatter plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(bullishADX, bullishCCI, bullishRSI, c='g', marker='o', label="Bullish")
ax.scatter(bearishADX, bearishCCI, bearishRSI, c='r', marker='o', label="Bearish")
ax.scatter(rangingADX, rangingCCI, rangingRSI, c='y', marker='o', label="Bullish")

ax.set_xlabel("ADX")
ax.set_ylabel("CCI")
ax.set_zlabel("RSI")

plt.title('Training trading data')
plt.show()

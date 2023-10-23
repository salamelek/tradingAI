import matplotlib.pyplot as plt
import json

# trying to see the differences in time I guess?


with open('labeled_data/2023-10-23-15min-adx-cci-rsi-5-test1.json') as json_file:
	trainData = json.load(json_file)

bullish0, bullish1, bullish2 = [], [], []
bearish0, bearish1, bearish2 = [], [], []
ranging0, ranging1, ranging2 = [], [], []

for triplet in trainData["l"]:
	bullish0.append(triplet[1][-1])
	bullish1.append(triplet[1][-2])
	bullish2.append(triplet[1][-3])

for triplet in trainData["s"]:
	bearish0.append(triplet[1][-1])
	bearish1.append(triplet[1][-2])
	bearish2.append(triplet[1][-3])

for triplet in trainData["h"]:
	ranging0.append(triplet[1][-1])
	ranging1.append(triplet[1][-2])
	ranging2.append(triplet[1][-3])

# Create a 3D scatter plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(bullish0, bullish1, bullish2, c='g', marker='o', label="Bullish")
ax.scatter(bearish0, bearish1, bearish2, c='r', marker='o', label="Bearish")
# ax.scatter(ranging0, ranging1, ranging2, c='y', marker='o', label="Ranging")

ax.set_xlabel("0")
ax.set_ylabel("1")
ax.set_zlabel("2")

plt.title('Training trading data')
plt.show()

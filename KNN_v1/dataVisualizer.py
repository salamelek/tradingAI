import json

import matplotlib as plt
import json


with open("labeled_data/autoLabeled-GC15min-01-01-23 00:00:00.json", "r") as jsonFile:
    labeledDict = json.load(jsonFile)


bullishADX, bullishCCI, bullishRSI = [], [], []
bearishADX, bearishCCI, bearishRSI = [], [], []
rangingADX, rangingCCI, rangingRSI = [], [], []

# TODO here I realise it would be really damn cool to write the label in the original file :|
for coord in labeledDict


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(bullishADX, bullishCCI, bullishRSI, c='green', marker='o', label="Bullish")
ax.scatter(bearishADX, bearishCCI, bearishRSI, c='red', marker='o', label="Bearish")
ax.scatter(rangingADX, rangingCCI, rangingRSI, c='yellow', marker='o', label="Ranging")

ax.set_xlabel("ADX")
ax.set_ylabel("CCI")
ax.set_zlabel("RSI")

plt.show()

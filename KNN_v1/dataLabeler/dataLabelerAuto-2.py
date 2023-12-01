import matplotlib.pyplot as plt
import pandas as pd
import json

with open("GC15min-01-01-23 00:00:00.json", "r") as jsonFile:
    klines = json.load(jsonFile)

df = pd.DataFrame.from_dict(klines, orient='index')
df.columns = ['close', 'coords']
df.insert(0, "timestamp", df.index)
df.reset_index(drop=True, inplace=True)

# get niceValues from json file
with open("niceValues.json", "r") as jsonFile:
    niceValues = json.load(jsonFile)

"""
niceValues are all the positions between xMin and xax that have at least yMin of %change

I split the dataLabeler in two files so the first one that does the heavy work just fills a dict
So this one, the second, can use the already processed data so i won't have to do that every time

Now i only need to find the optimal 
"""

# filter out niceValues so only the best answer for each kline remains
# FIXME this appears to be not working
bestValues = []
dictGroup = [niceValues[0]]
for i in range(len(niceValues) - 1):
    currDict = niceValues[i]
    nextDict = niceValues[i + 1]

    if currDict["startKline"] == nextDict["startKline"]:
        dictGroup.append(nextDict)

    else:
        bestValues.append(max(dictGroup, key=lambda x: x['y']))
        dictGroup = [nextDict]

# print(niceValues)
# print(bestValues)

# plot price
df.plot(color="black")

# plot lines
for point in bestValues:
    xA = point["startKline"]
    xB = point["targetKline"]

    yA = df["close"][xA]
    yB = df["close"][xB]

    plt.plot([xA, xB], [yA, yB], linestyle="dashed", marker='x', label='Line AB')

plt.grid()
plt.show()

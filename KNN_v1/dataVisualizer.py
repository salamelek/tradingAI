import pandas as pd
import matplotlib.pyplot as plt


# labeledDf = pd.read_json("labeled_data/autoLabeledDf-GC15min-01-01-23 00:00:00.json")
# df = pd.read_json("labeled_data/autoLabeledDf-MERGED-ETHUSDT-15m-2020.json")
# df = pd.read_json("labeled_data/autoLabeledDf-ETHUSDT-3m-2023-10.json")
df = pd.read_json("labeled_data/autoLabeledDf-EURUSD_Candlestick_15_M_BID_01.01.2022-01.01.2023.json")


ranging = df.loc[df['label'] == 0]
bearish = df.loc[df['label'] == -1]
bullish = df.loc[df['label'] == 1]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

a = 0
b = 5
c = 10
ax.scatter(bullish["coords"].apply(lambda x: x[a]), bullish["coords"].apply(lambda x: x[b]), bullish["coords"].apply(lambda x: x[c]), c='g', marker='o', label="Bullish")
ax.scatter(bearish["coords"].apply(lambda x: x[a]), bearish["coords"].apply(lambda x: x[b]), bearish["coords"].apply(lambda x: x[c]), c='r', marker='o', label="Bearish")
# ax.scatter(ranging["coords"].apply(lambda x: x[a]), ranging["coords"].apply(lambda x: x[b]), ranging["coords"].apply(lambda x: x[c]), c='y', marker='o', label="Ranging")

ax.set_xlabel("ADX")
ax.set_ylabel("CCI")
ax.set_zlabel("RSI")

print("ranging", len(ranging))
print("bullish", len(bullish))
print("bearish", len(bearish))

plt.show()

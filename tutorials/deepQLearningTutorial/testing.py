import pandas as pd

df = pd.read_csv('../../qLearning_v1/tradingData/BTCUSDT/BTCUSDT-5m-2022-11.csv', header=None, usecols=[0, 1, 2, 3, 4])
df.columns = ["startTime", "open", "high", "low", "close"]

print(df)

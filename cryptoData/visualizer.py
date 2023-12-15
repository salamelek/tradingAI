import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("MERGED-ETHUSDT-15m-20-22.csv") # , usecols=[1, 2, 3, 4], header=None, names=["open", "high", "low", "close"])

df = df.dropna()
df = df.reset_index(drop=True)

df["close"].plot()
plt.show()

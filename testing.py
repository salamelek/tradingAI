import numpy as np
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
from dataGetter import getDf


df = getDf("NVDA", "2023-08-1", "2023-09-1", "5min")

trainData = pd.DataFrame(
    {
        "ema_5_slope": df["EMA_5_SLOPE"],
        "ema_50_slope": df["EMA_50_SLOPE"],
        "ema_100_slope": df["EMA_100_SLOPE"],
        "ema_200_slope": df["EMA_200_SLOPE"],
        "macd_slope": df["macd_slope"],
        "macd_signal_slope": df["macd_signal_slope"],
        "macd_distance": 0,
        "rsi": df["rsi"]
    }
)

# print(trainData)

minValue = -100
maxValue = 100
normalized_df = (trainData - minValue) / (maxValue - minValue)

# Check the result
# print(normalized_values)
# print(normalizedTrainData)

print(normalized_df.loc[4, 'ema_50_slope'].item())

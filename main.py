# https://www.youtube.com/watch?v=PuZY9q-aKLw&t=327s

from dataGetter import getDf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM

df = getDf("NVDA", "2023-08-1", "2023-09-1", "5min")


# plot(df)


# format the data for the AI input
# use z-score normalization

# must be a df row of all the inputs
# ema 5, 50, 100, 200 slope, macd slope and signal slope, macd distance, rsi
# get the useful data

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

# TODO calculate the macd distance

# normalize the df
# TODO normalize the RSI separately, since the slopes are usually between -10 and 10, while the RSI is 0-100
# this normalizes everything between 0 and 1
minValue = -100
maxValue = 100
normalized_df = (trainData - minValue) / (maxValue - minValue)

xTrain = []
yTrain = []

trimNValues = 200

for index, row in normalized_df.iterrows():
    if trimNValues < float(index) < (len(df.index) - 1):
        # append inputs
        xTrain.append(list(row))
        # append the future slope of the EMA 5
        # TODO should not train with some data that is in xtrain (will be lazy)
        yTrain.append(normalized_df.loc[index + 1, 'ema_50_slope'].item())


# Convert training data to np arrays
xTrain, yTrain = np.array(xTrain), np.array(yTrain)
xTrain = np.reshape(xTrain, (xTrain.shape[0], xTrain.shape[1], 1))

# build the model
model = Sequential()

model.add(LSTM(units=50, return_sequences=True, input_shape=(8, 1)))
model.add(Dropout(0.2))
model.add(LSTM(units=50, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(units=50, return_sequences=False))
model.add(Dropout(0.2))
model.add(Dense(units=1))

model.compile(optimizer="adam", loss="mean_squared_error")
model.fit(xTrain, yTrain, epochs=5, batch_size=32)


prediction = model.predict(xTrain)

print(prediction)

unNormalizedPrediction = prediction * (maxValue - minValue) + minValue
unNormalizedPrediction = unNormalizedPrediction.flatten()

plt.plot(unNormalizedPrediction)
plt.show()

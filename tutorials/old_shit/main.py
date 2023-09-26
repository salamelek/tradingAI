# https://www.youtube.com/watch?v=PuZY9q-aKLw&t=327s

from dataGetter import getDf
from dataPlotter import plot, plotPredictionResults, comparePredictionWithTrainData

import pandas as pd
import numpy as np

import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM

df = getDf("NVDA", "2023-01-1", "2023-04-1", "5min")

# print(df.loc[1422, 'EMA_5_SLOPE'].item())
# print(df.loc[1659, 'EMA_5_SLOPE'].item())
# plot(df)
# exit()

# must be a df row of all the inputs
# ema 5, 50, 100, 200 slope, macd slope and signal slope, macd distance, rsi
# get the useful df

trainData = pd.DataFrame(
    {
        "ema_5_slope": df["EMA_5_SLOPE"],
        "ema_50_slope": df["EMA_50_SLOPE"],
        "ema_100_slope": df["EMA_100_SLOPE"],
        "ema_200_slope": df["EMA_200_SLOPE"],
        "macd_slope": df["macd_slope"],
        "macd_signal_slope": df["macd_signal_slope"],
        "macd_distance": df["macd_distance"],
        # normalize the rsi in the range -5, 5
        "rsi": ((df["rsi"] - 50) / 5)
    }
)

# remove any ema5 slope value that is more than 10 or less than -10
# df = df.drop(df[abs(df['EMA_5_SLOPE']) > 10].index)
# remove invalid values
df.dropna()
# reset index to avoid holes
df = df.reset_index(drop=True)

# normalize the df
# this normalizes everything between 0 and 1
# min and max values are dummies to set the max and min, so everything gets normalized normally
minValue = -10
maxValue = 10
normalizedTrainData = (trainData - minValue) / (maxValue - minValue)


xTrain = []
yTrain = []

trimNValues = 200

print(len(normalizedTrainData.index))
print(df.loc[[1422]])
print(normalizedTrainData.max())

for index, row in normalizedTrainData.iterrows():
    if trimNValues < float(index) < (len(df.index) - 1):
        # append inputs
        xTrain.append(list(row))
        # The train df should be growth %
        closePrice = df.loc[index, 'close'].item()
        nextClose = df.loc[index + 1, 'close'].item()
        yTrain.append((nextClose - closePrice) / closePrice)

# print(len(yTrain))          # 1693
# print(len(xTrain))          # 1693
# print(len(df["close"]))     # 1895


print(yTrain[1220])


# Convert training df to np arrays
xTrain, yTrain = np.array(xTrain), np.array(yTrain)
# I don't think I have to reshape this, so it's commented out
# xTrain = np.reshape(xTrain, (xTrain.shape[0], xTrain.shape[1], 1))

# build the model
model = Sequential()

model.add(LSTM(units=50, return_sequences=True, input_shape=(8, 1)))
model.add(Dropout(0.2))
model.add(LSTM(units=50, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(units=50, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(units=30, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(units=10, return_sequences=False))
model.add(Dropout(0.2))
model.add(Dense(units=1))


def custom_mse(y_true, y_pred):
    # Calculate the squared differences between true and predicted values
    squared_diff = tf.pow((y_true - y_pred), 2)

    # Calculate the mean of the squared differences
    mse = tf.reduce_mean(squared_diff)

    return mse


model.compile(optimizer="adam", loss=custom_mse)
model.fit(xTrain, yTrain, epochs=25, batch_size=32)

prediction = model.predict(xTrain).flatten()


# plotPredictionResults(list(df["close"]), prediction, trimNValues)
comparePredictionWithTrainData(prediction, yTrain)

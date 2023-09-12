# https://www.youtube.com/watch?v=PuZY9q-aKLw&t=327s

from dataGetter import getDf
from dataPlotter import plot

# from sklearn.preprocessing import MinMaxScaler
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Dense, Dropout, LSTM


df = getDf("NVDA", "2023-08-1", "2023-09-1", "5min")

plot(df)


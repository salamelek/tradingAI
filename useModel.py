import torch as t
from myQLearningPack import DeepQNetwork, calcPosition
from dataGetter import getData
import numpy as np
import matplotlib.pyplot as plt
from loadingBar import progressBar


lr = 0
nActions = 3
inputDims = [3]

model = DeepQNetwork(lr, nActions=nActions, inputDims=inputDims, fc1Dims=256, fc2Dims=256)
model.load_state_dict(t.load("savedModels/firstTimeWithFees.pth"))

print("Getting data...")
trainData = getData()
print("Done!\n")

# Set the model to evaluation mode (important if using layers like Dropout)
model.eval()

slTp = 0.01

cumulativeProfit = 0
balance = 100
investmentSize = 0.01
commissionFee = 0.01

cumProfits = []


# Forward pass (inference) to get predictions
totRowsNum = len(trainData.index)
with t.no_grad():
    for i in range(totRowsNum):
        prediction = model(t.tensor(np.array([trainData["rsi"][i], trainData["adx"][i], trainData["cci"][i]]), dtype=t.float32))
        action = t.argmax(prediction).item()

        # trading logic
        entryPrice = trainData["open"][i]
        exitPrice, candlesToExit = calcPosition(trainData, entryPrice, slTp, i)

        if action == 0:
            # buy
            try:
                tradeProfit = (exitPrice - entryPrice) / entryPrice
            except TypeError:
                # no enough data to continue
                pass
        elif action == 1:
            # sell
            try:
                tradeProfit = (entryPrice - exitPrice) / entryPrice
            except TypeError:
                # no enough data to continue
                pass

        # hold
        elif action == 2:
            # add some reward to maybe get some hold action?
            # self.reward += 1
            # it's commented out since I will apply commissions
            tradeProfit = 0

        cumulativeProfit += tradeProfit
        grossProfit = tradeProfit * (balance * investmentSize)
        netProfit = grossProfit - (balance * investmentSize * commissionFee)
        balance += netProfit

        cumProfits.append(cumulativeProfit)

        # print something
        progressBar(i + 1, totRowsNum, "Calculating...")

    print()
    print(balance)

    plt.plot(cumProfits)
    plt.show()

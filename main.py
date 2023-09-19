from myQLearningPack import Agent, TradingEnv
from dataGetter import getData
from loadingBar import progressBar

import matplotlib.pyplot as plt

import torch


if __name__ == '__main__':
    print("Getting data...")
    trainData = getData()
    print("Done!\n")

    env = TradingEnv(trainData=trainData, startBalance=100, commissionFee=0.01, investmentSize=1.0, slTp=0.01)
    agent = Agent(gamma=0.99, epsilon=1.0, batchSize=64, nActions=3, inputDims=[3], epsMin=0.01, lr=0.001)

    retries = 1
    totRowsNum = len(trainData.index)

    for i in range(retries):
        counter = 0
        done = False
        observation = env.reset()
        cumulativeProfitValues, tradeProfitValues, actions = [], [], []

        while not done:
            action = agent.chooseAction(observation)
            observation_, reward, done, info = env.step(action)

            agent.storeTransition(observation, action, reward, observation_, done)

            agent.learn()

            # log stuff
            cumulativeProfitValues.append(info["cumulativeProfit"])
            tradeProfitValues.append(info["tradeProfit"])
            actions.append(info["action"])

            observation = observation_
            counter += 1

            # print something
            progressBar(counter + 1, totRowsNum, "Training progress:")

        plt.plot(cumulativeProfitValues)
        plt.show()

    # save agent
    torch.save(agent.model.state_dict(), "savedModels/testModel.pth")


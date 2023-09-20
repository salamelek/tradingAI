from myQLearningPack import Agent, TradingEnv
from dataGetter import getData
from loadingBar import progressBar

import matplotlib.pyplot as plt

import torch


if __name__ == '__main__':
    print("Getting data...")
    trainData = getData()
    print("Done!\n")

    env = TradingEnv(trainData=trainData, startBalance=100, commissionFee=0.0025, investmentSize=1.0, slTp=0.01)
    agent = Agent(gamma=0.99, epsilon=1.0, batchSize=64, nActions=3, inputDims=[3], epsMin=0.01, lr=0.001)

    listCumProfits = []
    retries = 5

    for i in range(retries):
        totRowsNum = len(trainData.index)
        counter = 0
        done = False
        observation = env.reset()
        cumulativeProfitValues, tradeProfitValues, positions, rewards = [], [], [], []

        while not done:
            action = agent.chooseAction(observation)
            observation_, reward, done, info = env.step(action)

            agent.storeTransition(observation, action, reward, observation_, done)

            agent.learn()

            # log stuff
            cumulativeProfitValues.append(info["cumulativeProfit"])
            tradeProfitValues.append(info["tradeProfit"])
            positions.append(info["position"])
            rewards.append(reward)

            observation = observation_
            counter += 1

            # print something
            progressBar(counter + 2, totRowsNum, "Training progress:")

        listCumProfits.append(cumulativeProfitValues)

    print()
    print(f"End balance: {info['balance']}")
    print(f"Number buys: {(info['counts'][0])}")
    print(f"Number sells: {(info['counts'][1])}")
    print(f"Number holds: {(info['counts'][2])}")

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 10), sharex="all")

    # Plot the original 'close' price, EMAs, and RSI in the top subplot
    ax1.plot(listCumProfits[retries - 1], label='Cum. profits', color='blue')
    ax1.set_ylabel('Cum. profits')
    ax1.grid()

    ax2.plot(rewards, label="rewards", color="black")
    ax2.set_ylabel('Rewards')
    ax2.grid()

    plt.tight_layout()
    plt.show()

    # save agent
    if input("Do you want to save this model? [y/n]:\n") != "n":
        fileName = input("Enter the file name: ")
        torch.save(agent.model.state_dict(), f"savedModels/{fileName}.pth")
        print("File saved!")


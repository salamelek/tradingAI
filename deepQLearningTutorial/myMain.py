from myQLearningPack import Agent, TradingEnv
from dataGetter import getTrainData
import numpy as np


if __name__ == '__main__':
    env = TradingEnv(startBalance=100, endPadding=10, commissionFee=0.01, investmentSize=1.0, slTp=0.01)
    agent = Agent(gamma=0.99, epsilon=1.0, batchSize=64, nActions=3, epsMin=0.01, inputDims=[3], lr=0.001)
    scores, epsHistory = [], []

    # each episode has its own dataframe
    # put dataframes in the episodes lis
    # each episode is 1month of data
    # each symbol will add 1 month
    episodes = getTrainData()

    for i in range(len(episodes)):
        score = 0
        done = False
        observation = env.reset(trainData=episodes[i])

        while not done:
            action = agent.chooseAction(observation)
            observation_, reward, done, info = env.step(action)
            score += reward
            agent.storeTransition(observation, action, reward, observation_, done)
            agent.learn()
            observation = observation_

            profit = info["profit"]

        scores.append(score)
        epsHistory.append(agent.epsilon)

        avgScore = np.mean(scores[-100:])

        print(f"episode {i + 1}/{len(episodes)}:\n"
              f"score: {score}, avg score: {avgScore}, epsilon: {agent.epsilon}\n"
              f"Total profit: {profit}\n"
              )

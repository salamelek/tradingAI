from myQLearningPack import Agent, TradingEnv
from dataGetter import getData

if __name__ == '__main__':
    trainData = getData()

    env = TradingEnv(trainData=trainData, startBalance=100, commissionFee=0.01, investmentSize=1.0, slTp=0.01)
    agent = Agent(gamma=0.99, epsilon=1.0, batchSize=64, nActions=3, inputDims=[3], epsMin=0.01, lr=0.001)

    done = False
    observation = env.reset()

    while not done:
        action = agent.chooseAction(observation)
        observation_, reward, done, info = env.step(action)

        agent.storeTransition(observation, action, reward, observation_, done)

        agent.learn()

        observation = observation_

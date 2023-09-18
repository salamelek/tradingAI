import gym
from myQLearningPack import Agent
import numpy as np

if __name__ == '__main__':
    env = gym.make("LunarLander-v2")
    agent = Agent(gamma=0.99, epsilon=1.0, batchSize=64, nActions=4, epsMin=0.01, inputDims=[8], lr=0.001)
    scores, epsHistory = [], []
    nGames = 1

    for i in range(nGames):
        score = 0
        done = False
        observation, info = env.reset()

        while not done:
            action = agent.chooseAction(observation)
            observation_, reward, done, done2, info = env.step(action)
            score += reward
            agent.storeTransition(observation, action, reward, observation_, done)
            agent.learn()
            observation = observation_

        scores.append(score)
        epsHistory.append(agent.epsilon)

        avgScore = np.mean(scores[-100:])

        print(f"episode {i}: score: {score}, avg score: {avgScore}, epsilon: {agent.epsilon}")

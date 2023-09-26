# idk where this tutorial will take me, I just want to learn how to deep q networks ;-;
# https://www.youtube.com/watch?v=wc-FxNENg9U


import torch as t
import torch.nn as nn
import torch.nn.functional as f
import torch.optim as optim

import numpy as np
import random

from gym import spaces
import gym


t.autograd.set_detect_anomaly(True)


def calcPosition(df, entryPrice, slTp, currentPos):
    try:
        highExitIndex = min(df[(df["high"] > (entryPrice + entryPrice * slTp)) & (df["index"] > currentPos)]["index"])
    except ValueError:
        highExitIndex = np.inf

    try:
        lowExitIndex = min(df[(df["low"] < (entryPrice - entryPrice * slTp)) & (df["index"] > currentPos)]["index"])
    except ValueError:
        lowExitIndex = np.inf

    if highExitIndex == lowExitIndex == np.inf:
        return None, None

    if highExitIndex < lowExitIndex:
        # the position concluded above
        exitPrice = entryPrice + entryPrice * slTp

    elif lowExitIndex < highExitIndex:
        # the position concluded below
        exitPrice = entryPrice - entryPrice * slTp

    else:
        # a candle that goes from +1% to -1%
        # randomly selects an option
        exitPrice = entryPrice + (entryPrice * slTp * random.choice([1, -1]))

    candlesToExit = min(highExitIndex, lowExitIndex) - currentPos

    return exitPrice, candlesToExit


class DeepQNetwork(nn.Module):
    def __init__(self, lr, inputDims, fc1Dims, fc2Dims, fc3Dims, nActions):
        super(DeepQNetwork, self).__init__()

        self.inputDims = inputDims
        self.fc1Dims = fc1Dims
        self.fc2Dims = fc2Dims
        self.fc3Dims = fc3Dims
        self.nActions = nActions

        # the input layer and the first hidden layer (3 and 256 neurons respectively)
        self.fc1 = nn.Linear(*self.inputDims, self.fc1Dims)
        # first and second hidden layer (256 neurons)
        self.fc2 = nn.Linear(self.fc1Dims, self.fc2Dims)
        # second and third hidden layer (256 neurons)
        self.fc3 = nn.Linear(self.fc2Dims, self.fc3Dims)
        # the output of the deep NN (neural network)
        self.fc4 = nn.Linear(self.fc3Dims, self.nActions)

        self.optimiser = optim.Adam(self.parameters(), lr=lr)
        self.loss = nn.MSELoss()
        # try using a GPU
        print("Trying to use GPU..")
        if t.cuda.is_available():
            print("Successfully using GPU!\n")
            self.device = t.device("cuda")
        else:
            print("Nope, using CPU\n")
            self.device = t.device("cpu")
        self.to(self.device)

    # forward propagation
    def forward(self, state):
        # first layer gets the state
        x = f.relu(self.fc1(state))
        # second layer gets the output of the first layer
        x = f.relu(self.fc2(x))
        # third layer gets the output of the second layer
        x = f.relu(self.fc3(x))
        # action is the last layer. No relu function, because we don't want values out of 0-1 range (08:00)
        actions = self.fc4(x)

        return actions


class Agent:
    def __init__(self, gamma, epsilon, lr, inputDims, batchSize, nActions, maxMemSize=100000, epsMin=0.01, epsDec=5e-4):
        self.gamma = gamma                                  # determines the weighting of future rewards
        self.epsilon = epsilon                              # How much time does the agent use for exploring vs taking the best known action
        self.lr = lr                                        # Learning rate, to pass into our neural network (?idk what it does?)
        self.epsMin = epsMin                                # Minimum value of epsilon
        self.epsDec = epsDec                                # Epsilon decrement
        self.inputDims = inputDims                          # Input dimension
        self.actionSpace = [i for i in range(nActions)]     # nActions represented as ints (easier to randomly pick one)
        self.maxMemSize = maxMemSize                        # maximum memory allocated
        self.batchSize = batchSize                          # Batches of memories (???)
        self.memCounter = 0                                 # keep track of the position of the first available memory to store the agent's memory

        # in the tutorial it's called qEval instead of model
        self.model = DeepQNetwork(self.lr, nActions=nActions, inputDims=inputDims, fc1Dims=256, fc2Dims=256, fc3Dims=256)

        # store memories
        self.stateMemory = np.zeros((self.maxMemSize, *inputDims), dtype=np.float32)  # always specify the datatype so there is no loss of info
        self.newStateMemory = np.zeros((self.maxMemSize, *inputDims), dtype=np.float32)
        self.actionMemory = np.zeros(self.maxMemSize, dtype=np.int32)
        self.rewardMemory = np.zeros(self.maxMemSize, dtype=np.float32)
        self.terminalMemory = np.zeros(self.maxMemSize, dtype=np.bool_)

    def storeTransition(self, state, action, reward, state_, done):
        index = self.memCounter % self.maxMemSize  # this magically finds where to store the memory
        self.stateMemory[index] = state
        self.newStateMemory[index] = state_
        self.rewardMemory[index] = reward
        self.actionMemory[index] = action
        self.terminalMemory[index] = done

        self.memCounter += 1

    def chooseAction(self, observation):
        # if a random number 0-1 is greater than epsilon, it will take the best known action
        if np.random.random() > self.epsilon:
            # Convert the list of NumPy arrays to a single NumPy array
            state_np = np.array([observation])
            # Convert the NumPy array to a PyTorch tensor
            state = t.tensor(state_np, dtype=t.float32).to(self.model.device)

            actions = self.model.forward(state)
            action = t.argmax(actions).item()
            # TODO is this a good approach? Is this considering the global possible range? I don't know anything ;-;
            # TODO instead of choosing one of three actions, use the first output to determine buy, sell or hold, the second one for the take profit and the third one for the stop loss
            # TODO probably will have to also enlarge the network and optimise epsilon, lr and stuff
            # put the actions values between -1 and 1
            # actions = t.tanh(actions)
            # actionArray = tuple(actions)

        else:
            action = np.random.choice(self.actionSpace)
            # TODO instead of a random number in the action space it has to spit out 3 random numbers
            # actionArray = tuple(np.random.uniform(-1, 1, size=3))

        return action

    # 21:45
    def learn(self):
        # if the memory isn't full, don't bother learning, just do random stuff
        if self.memCounter < self.batchSize:
            return

        self.model.optimiser.zero_grad()

        maxMem = min(self.memCounter, self.maxMemSize)
        batch = np.random.choice(maxMem, self.batchSize, replace=False)

        batchIndex = np.arange(self.batchSize, dtype=np.int32)

        stateBatch = t.tensor(self.stateMemory[batch]).to(self.model.device)
        newStateBatch = t.tensor(self.newStateMemory[batch]).to(self.model.device)
        rewardBatch = t.tensor(self.rewardMemory[batch]).to(self.model.device)
        terminalBatch = t.tensor(self.terminalMemory[batch]).to(self.model.device)

        actionBatch = self.actionMemory[batch]

        # select maximal nActions
        qEval = self.model.forward(stateBatch)[batchIndex, actionBatch]
        qNext = self.model.forward(newStateBatch)
        qNext[terminalBatch] = 0.0

        qTarget = rewardBatch + self.gamma * t.max(qNext, dim=1)[0]

        loss = self.model.loss(qTarget, qEval).to(self.model.device)
        loss.backward()
        self.model.optimiser.step()

        # decrease epsilon
        self.epsilon = self.epsilon - self.epsDec if self.epsilon > self.epsMin else self.epsMin


class TradingEnv(gym.Env):
    """
    Tutorial at https://youtu.be/uKnjGn8fF70
    """

    def __init__(self, startBalance, commissionFee, investmentSize, slTp, trainData):
        super(TradingEnv, self).__init__()
        # these things will be initialised in reset()
        self.done = False
        self.reward = 0
        self.counter = 0
        self.observation = None
        self.tradeProfit = 0
        self.cumulativeProfit = 0
        self.trainData = trainData
        self.buyCount, self.sellCount, self.holdCount = 0, 0, 0

        # money stuff
        self.startBalance = startBalance
        self.balance = self.startBalance
        self.commissionFee = commissionFee
        self.investmentSize = investmentSize    # investment is in % of the current balance
        self.slTp = slTp

        # buy, sell, hold
        self.action_space = spaces.Discrete(3)
        # rsi, adx, cci
        self.observation_space = spaces.Box(low=-300, high=300, shape=(3,), dtype=np.float32)

    def reset(self, seed=None, options=None, **kwargs):
        # since I will not be using episodes, all things are initialised in the __init__() function
        # IMPORTANT if I end up implementing episodes again, INITIALISE THINGS ON RESET HERE
        self.done = False
        self.counter = 0
        self.cumulativeProfit = 0
        self.balance = self.startBalance
        self.buyCount, self.sellCount, self.holdCount = 0, 0, 0

        self.observation = np.array([
            self.trainData["adx"][self.counter],
            self.trainData["cci"][self.counter],
            self.trainData["ema5Slope"][self.counter],
            self.trainData["ema50Slope"][self.counter],
            self.trainData["rsi"][self.counter],
        ])

        return self.observation

    def step(self, action):
        # stuff to reset each step
        self.tradeProfit = 0
        self.reward = 0
        # start balance is reset every time, so I can train it based on net profit
        self.balance = self.startBalance

        # trading logic
        entryPrice = self.trainData["open"][self.counter]
        exitPrice, candlesToExit = calcPosition(self.trainData, entryPrice, self.slTp, self.counter)

        if action == 0:
            # buy
            self.buyCount += 1
            try:
                self.tradeProfit = (exitPrice - entryPrice) / entryPrice
            except TypeError:
                # no enough data to continue
                pass
        elif action == 1:
            # sell
            self.sellCount += 1
            try:
                self.tradeProfit = (entryPrice - exitPrice) / entryPrice
            except TypeError:
                # no enough data to continue
                pass

        # hold
        elif action == 2:
            # hold
            self.holdCount += 1
            self.reward += -0.1
            # have to reset this so it doesn't penalize hold
            candlesToExit = 0

        # count the money
        self.cumulativeProfit += self.tradeProfit
        netProfit = self.tradeProfit * ((self.balance * self.investmentSize) - (self.balance * self.investmentSize * self.commissionFee))
        self.balance += netProfit

        # set the next observation
        self.counter += 1

        self.observation = np.array([
            self.trainData["adx"][self.counter],
            self.trainData["cci"][self.counter],
            self.trainData["ema5Slope"][self.counter],
            self.trainData["ema50Slope"][self.counter],
            self.trainData["rsi"][self.counter],
        ])

        # set reward
        # self.reward += candlesToExit / netProfit
        if candlesToExit is not None:
            # if the candles are below 100, the reward will still be positive
            # its cubed so the sign is preserved and the extremes are much better / worse
            self.reward += netProfit - (candlesToExit / 100)

        else:
            # I'm not even sure if the netProfit exists if there are no candlesToExit
            self.reward += netProfit

        # check if it's done
        if self.balance < 0.0:
            print(f"\nDone because of balance: {self.balance}\n")
            # when it blows the account
            self.done = True

        if self.counter >= max(self.trainData["index"]):
            print(f"\nDone because of ending bars: {max(self.trainData['index'])}\n")
            # when there are no more candles
            self.done = True

        # write some info
        info = {
            "cumulativeProfit": self.cumulativeProfit,
            "tradeProfit": self.tradeProfit,
            # set the counter to -1 because the action happened that time
            "position": (action, self.counter - 1),
            "balance": self.balance,
            "counts": (self.buyCount, self.sellCount, self.holdCount)
        }

        return self.observation, self.reward, self.done, info

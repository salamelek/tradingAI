# idk where this tutorial will take me, I just want to learn how to deep q networks ;-;
# https://www.youtube.com/watch?v=wc-FxNENg9U


import torch as t
import torch.nn as nn
import torch.nn.functional as f
import torch.optim as optim

import numpy as np

from gym import spaces
import gym


class DeepQNetwork(nn.Module):
    def __init__(self, lr, inputDims, fc1Dims, fc2Dims, nActions):
        super(DeepQNetwork, self).__init__()

        self.inputDims = inputDims
        self.fc1Dims = fc1Dims
        self.fc2Dims = fc2Dims
        self.nActions = nActions

        # first linear layer of inputs (?)
        self.fc1 = nn.Linear(*self.inputDims, self.fc1Dims)
        # second linear layer (?)
        self.fc2 = nn.Linear(self.fc1Dims, self.fc2Dims)
        # the output of the deep NN (neural network)
        self.fc3 = nn.Linear(self.fc2Dims, self.nActions)

        self.optimiser = optim.Adam(self.parameters(), lr=lr)
        self.loss = nn.MSELoss()
        # try using a GPU
        print("Trying to use GPU..")
        if t.cuda.is_available():
            print("Successfully using GPU!")
            self.device = t.device("cuda:0")
        else:
            print("Nope, using cpu")
            self.device = t.device("cpu")
        self.to(self.device)

    # forward propagation
    def forward(self, state):
        # first layer gets the state
        x = f.relu(self.fc1(state))
        # second layer gets the output of the first layer
        x = f.relu(self.fc2(x))
        # action is the last layer. No relu function, because we don't want values out of 0-1 range (08:00)
        actions = self.fc3(x)

        return actions


class Agent:
    def __init__(self, gamma, epsilon, lr, inputDims, batchSize, nActions, maxMemSize=100000, epsMin=0.01, epsDec=5e-4):
        self.gamma = gamma  # determines the weighting of future rewards
        self.epsilon = epsilon  # How much time does the agent use for exploring vs taking the best known action
        self.lr = lr  # Learning rate, to pass into our neural network (?idk what it does?)
        self.epsMin = epsMin  # I think this is the minimum value of epsilon
        self.epsDec = epsDec  # I think this is the value by which epsilon is decremented
        self.inputDims = inputDims  # I guess the dimension of the input?
        self.actionSpace = [i for i in range(nActions)]  # actions represented as ints (easier to randomly pick one)
        self.maxMemSize = maxMemSize  # maximum memory allocated
        self.batchSize = batchSize  # Batches of memories (???)
        self.memCounter = 0  # keep track of the position of the first available memory to store the agent's memory

        self.qEval = DeepQNetwork(self.lr, nActions=nActions, inputDims=inputDims, fc1Dims=256, fc2Dims=256)

        # store memories
        self.stateMemory = np.zeros((self.maxMemSize, *inputDims),
                                    dtype=np.float32)  # always specify the datatype so there is no loss of info
        self.newStateMemory = np.zeros((self.maxMemSize, *inputDims), dtype=np.float32)
        self.actionMemory = np.zeros(self.maxMemSize, dtype=np.int32)
        self.rewardMemory = np.zeros(self.maxMemSize, dtype=np.float32)
        self.terminalMemory = np.zeros(self.maxMemSize,
                                       dtype=np.bool_)  # Idk why its bool_ and not bool maybe here should be bool_ but I have no clue

    def storeTransition(self, state, action, reward, state_, done):
        index = self.memCounter % self.maxMemSize  # this magically finds where to store the memory
        self.stateMemory[index] = state
        self.newStateMemory[index] = state_
        self.rewardMemory[index] = reward
        self.actionMemory[index] = action
        self.terminalMemory[index] = done

        self.memCounter += 1

    def chooseAction(self, observation):
        # if a random number is greater than epsilon, it will take the best known action
        if np.random.random() > self.epsilon:

            # Convert the list of NumPy arrays to a single NumPy array
            state_np = np.array([observation])
            # Convert the NumPy array to a PyTorch tensor
            state = t.tensor(state_np, dtype=t.float32).to(self.qEval.device)

            actions = self.qEval.forward(state)
            action = t.argmax(actions).item()

        else:
            action = np.random.choice(self.actionSpace)

        return action

    # 21:45
    def learn(self):
        # if the memory isn't full, don't bother learning, just do random stuff
        if self.memCounter < self.batchSize:
            return

        self.qEval.optimiser.zero_grad()

        maxMem = min(self.memCounter, self.maxMemSize)
        batch = np.random.choice(maxMem, self.batchSize, replace=False)

        batchIndex = np.arange(self.batchSize, dtype=np.int32)

        stateBatch = t.tensor(self.stateMemory[batch]).to(self.qEval.device)
        newStateBatch = t.tensor(self.newStateMemory[batch]).to(self.qEval.device)
        rewardBatch = t.tensor(self.rewardMemory[batch]).to(self.qEval.device)
        terminalBatch = t.tensor(self.terminalMemory[batch]).to(self.qEval.device)

        actionBatch = self.actionMemory[batch]

        # select maximal actions
        qEval = self.qEval.forward(stateBatch)[batchIndex, actionBatch]
        qNext = self.qEval.forward(newStateBatch)
        qNext[terminalBatch] = 0.0

        qTarget = rewardBatch + self.gamma * t.max(qNext, dim=1)[0]

        loss = self.qEval.loss(qTarget, qEval).to(self.qEval.device)
        loss.backward()
        self.qEval.optimiser.step()

        # decrease epsilon
        self.epsilon = self.epsilon - self.epsDec if self.epsilon > self.epsMin else self.epsMin


class TradingEnv(gym.Env):
    """
    Tutorial at https://youtu.be/uKnjGn8fF70
    """

    def __init__(self, startBalance, endPadding, commissionFee):
        super(TradingEnv, self).__init__()
        # these things will be initialised in reset()
        self.trainData = None
        self.cci = None
        self.adx = None
        self.rsi = None
        self.done = None
        self.reward = None
        self.counter = None
        self.balance = None
        self.trainData = None
        self.observation = None
        self.endPadding = endPadding
        # starting amount of $
        self.startBalance = startBalance
        self.commissionFee = commissionFee

        # buy, sell, hold
        self.action_space = spaces.Discrete(3)
        # rsi, adx, cci
        self.observation_space = spaces.Box(low=-300, high=300, shape=(3,), dtype=np.float32)

    def reset(self, trainData, seed=None, options=None):
        # "initialise" things here
        self.counter = 0
        self.reward = 0
        self.done = False
        self.trainData = trainData
        self.balance = self.startBalance

        self.rsi = self.trainData["rsi"][self.counter]
        self.adx = self.trainData["adx"][self.counter]
        self.cci = self.trainData["cci"][self.counter]

        self.observation = np.array([self.rsi, self.adx, self.cci])

        return self.observation

    def step(self, action):
        # here goes each timeframe action
        # here goes also all the logic of the trades

        self.counter += 1

        # when it blows the account
        if self.balance <= 0.0:
            self.done = True

        # when there are no more candles
        if self.counter >= (len(self.trainData.index) - self.endPadding):
            self.done = True

        # set the observation
        self.rsi = self.trainData["rsi"][self.counter]
        self.adx = self.trainData["adx"][self.counter]
        self.cci = self.trainData["cci"][self.counter]

        self.observation = np.array([self.rsi, self.adx, self.cci])

        # calculate reward
        if self.done:
            # profit% * 10 + counter, so it encourages to live
            # TODO could add a punishment for every candle that passed between placed order and fulfilled, to encourage fast positions
            self.reward = profits * 10 + self.counter

        info = {"earnings": "yes maybe i should implement this so i can see"}

        return self.observation, self.reward, self.done, info

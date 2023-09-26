def step(self, action):
    # 1) simulate action
    # sl : tp = 1
    # 1% sl tp
    entryPrice = self.trainData["close"][self.counter]
    self.profit = 0

    # buy
    if action == 0:
        tp = entryPrice + (self.slTp * entryPrice)
        sl = entryPrice - (self.slTp * entryPrice)

        try:
            closestHighIndex = min(
                self.trainData[(self.trainData["high"] >= tp) & (self.trainData["index"] > self.counter)]["index"])
        except ValueError:
            closestHighIndex = np.inf
        try:
            closestLowIndex = min(
                self.trainData[(self.trainData["low"] <= sl) & (self.trainData["index"] > self.counter)]["index"])
        except ValueError:
            closestLowIndex = np.inf

        self.profit = (self.balance * self.investmentSize) * self.slTp

        # profit
        if closestLowIndex > closestHighIndex:
            self.cumulativeProfit += self.profit
            self.balance += self.profit

        # loss
        elif closestLowIndex < closestHighIndex:
            self.cumulativeProfit -= self.profit
            self.balance -= self.profit

    # sell
    elif action == 1:
        tp = entryPrice - (self.slTp * entryPrice)
        sl = entryPrice + (self.slTp * entryPrice)

        try:
            closestHighIndex = min(
                self.trainData[(self.trainData["high"] >= sl) & (self.trainData["index"] > self.counter)]["index"])
        except ValueError:
            closestHighIndex = np.inf
        try:
            closestLowIndex = min(
                self.trainData[(self.trainData["low"] <= tp) & (self.trainData["index"] > self.counter)]["index"])
        except ValueError:
            closestLowIndex = np.inf

        self.profit = (self.balance * self.investmentSize) * self.slTp

        # profit
        if closestLowIndex < closestHighIndex:
            self.cumulativeProfit += self.profit
            self.balance += self.profit

        # loss
        elif closestLowIndex > closestHighIndex:
            self.cumulativeProfit -= self.profit
            self.balance -= self.profit

    # hold
    elif action == 2:
        pass

    else:
        print("Wtf")
        exit()

    # 2) check if it's done
    # when it blows the account
    if self.balance <= 10.0:
        self.done = True

    # when there are no more candles
    if self.counter >= (len(self.trainData.index) - self.endPadding):
        self.done = True

    # 3) calculate reward
    # profit% * 10 + counter, so it encourages to live
    # TODO could add a punishment for every candle that passed between placed order and fulfilled, to encourage fast positions
    self.reward = self.profit

    # 4) update the observation

    self.counter += 1
    # set the observation
    self.rsi = self.trainData["rsi"][self.counter]
    self.adx = self.trainData["adx"][self.counter]
    self.cci = self.trainData["cci"][self.counter]

    self.observation = np.array([self.rsi, self.adx, self.cci])

    info = {
        "balance": self.balance,
        "profit": self.profit,
        "action": action
    }

    return self.observation, self.reward, self.done, info
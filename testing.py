tradeProfit = 0.01
balance = 100
investmentSize = 0.01
commissionFee = 0.01

netProfit = tradeProfit * ((balance * investmentSize) - (balance * investmentSize * commissionFee))

print(netProfit)

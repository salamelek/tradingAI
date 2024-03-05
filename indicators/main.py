import csv

import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle


class Indicator:
    pass


class Chart:
    """
    Holds all the kline data (open, close, high, low, volume)
    BUT NOT THE INDICATORS (I want those to be applied later)
    """

    def __init__(
            self,
            ochlv: list,
            indicators: list,
            positions: list,
            bearishColor="red",
            bullishColor="green",
            rangingColor="yellow",
            lineHeight=0.00002,
            hlWidth=0.1
    ):
        self.ochlv = ochlv  # ochlv = open close high low volume ({"open": 3...}, {...})
        self.indicators = indicators
        self.bearishColor = bearishColor
        self.bullishColor = bullishColor
        self.rangingColor = rangingColor
        self.lineHeight = lineHeight
        self.hlWidth = hlWidth

    def addIndicator(self):
        pass

    def removeIndicator(self):
        pass

    def plot(self):
        print("Plotting...")

        fig, ax = plt.subplots(1)
        bullish = []
        bearish = []
        ranging = []

        for index in range(len(self.ochlv)):
            kline = self.ochlv[index]

            coords = (index, kline["open"])             # (index, openPrice)
            width = 1                                   # 1, because each index is large 1
            height = kline["close"] - kline["open"]     # closePrice - openPrice

            coordsHl = (((index + 0.5) - self.hlWidth / 2), kline["low"])
            heightHl = kline["high"] - kline["low"]

            if height > 0:
                bullish.append(Rectangle(coords, width, height))
                bullish.append(Rectangle(coordsHl, self.hlWidth, heightHl))
            elif height < 0:
                bearish.append(Rectangle(coords, width, height))
                bearish.append(Rectangle(coordsHl, self.hlWidth, heightHl))
            else:
                ranging.append(Rectangle(coords, width, self.lineHeight))

        ax.add_collection(PatchCollection(bullish, edgecolor="none", facecolor=self.bullishColor))
        ax.add_collection(PatchCollection(bearish, edgecolor="none", facecolor=self.bearishColor))
        ax.add_collection(PatchCollection(ranging, edgecolor="none", facecolor=self.rangingColor))

        ax.errorbar(0, 0)

        plt.grid(True)
        plt.show()


class Pivot:
    def __init__(self, timeInterval, threshold):
        self.timeInterval = timeInterval
        self.threshold = threshold


def readCsv(filePath):
    print("Reading csv file...", end="")

    dataPoints = []

    with open(filePath, "r") as csvFile:
        csvReader = csv.reader(csvFile)
        # skip first row
        next(csvReader)
        # time, Open, High, Low, Close, Volume
        for row in csvReader:
            if float(row[5]) == 0 and skipRows:
                # skip "empty" rows
                continue

            kline = {
                "open": float(row[1]),
                "close": float(row[4]),
                "high": float(row[2]),
                "low": float(row[3]),
                "volume": float(row[5])
            }

            dataPoints.append(kline)

    print("Done!")

    return dataPoints


if __name__ == '__main__':
    skipRows = False

    a = readCsv("../forexData/EURUSD_Candlestick_15_M_BID_01.01.2022-01.01.2023.csv")
    chart = Chart(a, [], [])
    chart.plot()

import csv
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle

import pandas as pd
from binanceDataReader import getCryptoDf


class Indicator:
    def __init__(self, timeFrame):
        self.timeFrame = timeFrame

    def calculateIndicator(self, klines, index):
        raise Exception("Someone did not override this function smh")


class SupportResistence(Indicator):
    def __init__(self, timeFrame, threshold):
        super().__init__(timeFrame)
        self.threshold = threshold

    def calculateIndicator(self, klines, index):
        """
        To find a support/resistance level we have to check for a few things...

        Reminder: s/r levels work best at larger timeframes (actual company shares buyers)

        An s/r level will be present if:
            - a drastic move gets stopped (and reversed)
            - a level is rejected multiple times
            - a level acts as both support and resistance

        :param klines: the chart's klines
        :param index: index at which we want to know the value
        :return:
        """
        pass


class Position:
    def __init__(self, index, direction, value, tp, sl):
        self.index = index              # index of the kline
        self.direction = direction      # long / short
        self.value = value              # value in €
        self.tp = tp                    # take profit
        self.sl = sl                    # stop loss


class Chart:
    """
    Holds all the kline data (open, close, high, low, volume)
    the indicators and positions will be held in a list to be displayed
    """

    def __init__(
            self,
            klines: list,
            indicators: list,
            extraSeries: list,
            positions: list,
            bearishColor="red",
            bullishColor="green",
            rangingColor="yellow",
            lineHeight=0.00002,
            hlWidth=0.1
    ):
        self.klines = klines  # klines = open close high low volume ({"open": 3...}, {...})
        self.indicators = indicators
        self.bearishColor = bearishColor
        self.bullishColor = bullishColor
        self.rangingColor = rangingColor
        self.lineHeight = lineHeight
        self.hlWidth = hlWidth
        self.extraSeries = extraSeries

    def addIndicator(self):
        pass

    def removeIndicator(self):
        pass

    def calculateProfits(self):
        """
        loops through each position and calculates the profit and other stats

        :return:
        """
        pass

    def plot(self):
        print("Plotting...")

        fig = plt.figure()
        gs = fig.add_gridspec(2, 1, hspace=0, height_ratios=[3, 1])
        axs = gs.subplots(sharex=True)
        bullish = []
        bearish = []
        ranging = []

        for index in range(len(self.klines)):
            kline = self.klines[index]

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

        axs[0].add_collection(PatchCollection(bullish, edgecolor="none", facecolor=self.bullishColor))
        axs[0].add_collection(PatchCollection(bearish, edgecolor="none", facecolor=self.bearishColor))
        axs[0].add_collection(PatchCollection(ranging, edgecolor="none", facecolor=self.rangingColor))

        axs[0].errorbar(0, 0)

        # plot volume
        axs[1].plot(range(len(self.klines)), [kline["volume"] for kline in self.klines])

        # plot given extra series
        for series in self.extraSeries:
            axs[0].plot(range(len(series)), series)

        for ax in axs:
            ax.label_outer()

        plt.tight_layout()

        axs[0].grid(True)
        axs[1].grid(True)
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

    klines = readCsv("../forexData/EURUSD_Candlestick_15_M_BID_01.01.2022-01.01.2023.csv")
    chart = Chart(klines, [], [], [])
    chart.plot()

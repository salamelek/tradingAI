import csv
import numpy as np
import matplotlib.pyplot as plt


class DataPoint:
    def __init__(self, open, close, high, low, volume, duration, time=0):
        self.open = open
        self.close = close
        self.high = high
        self.low = low
        self.volume = volume
        self.duration = duration
        self.time = time

        self.coords = [open, close, high, low, volume]

    def cosineSimilarity(self, other):
        dotProduct = self.dotProduct(other)
        distA = self.euclideanNorm()
        distB = other.euclideanNorm()

        return dotProduct / (distA * distB)

    def dotProduct(self, other):
        dotProduct = 0

        for i in range(len(self.coords)):
            dotProduct += (self.coords[i] * other.coords[i])

        return dotProduct

    def euclideanNorm(self):
        euclideanNorm = 0

        for coord in self.coords:
            euclideanNorm += (coord * coord)

        return np.sqrt(euclideanNorm)


class Chart:
    def __init__(self, dataPoints, pair, timeInterval):
        self.dataPoints = dataPoints
        self.numOfDataPoints = len(dataPoints)
        self.pair = pair
        self.timeInterval = timeInterval

    def display(self):
        print("Displaying chart... ", end="")

        xValues = []
        yValues = []

        # Assuming self.dataPoints is a list of data points
        for i in range(self.numOfDataPoints):
            xValues.append(i)
            yValues.append(self.dataPoints[i].open)

        plt.plot(xValues, yValues)
        ax = plt.gca()
        ax.yaxis.set_major_locator(plt.MaxNLocator(10))  # Adjust the locator as needed

        plt.grid(True)
        plt.show()

        print("Done!")

    def size(self):
        return len(self.dataPoints)


class DpGroup:
    """
    A dataPoint group is a group of data points
    The index of the groups goes from 0 to chart.size - group.size
    the index 0 of a Group is at the last index of the chart (reversed)
    the index 0 of a dataPoint in the group is the first one from the left (normal)
    """

    def __init__(self, chart, size, index):
        self.size = size
        self.dataPoints = []

        for i in range(size):
            self.dataPoints.append(chart.dataPoints[-1 - i - index])

    def similarTo(self, other):
        total = 0

        for i in range(self.size):
            total += self.dataPoints[i].cosineSimilarity(other.dataPoints[i])

        return total / self.size


class Prediction:
    def __init__(self, groupSize, k):
        self.valuesCounter = 0
        self.largestValues = []
        self.largestIndexes = []
        self.k = k
        self.groupSize = groupSize

    def __str__(self):
        return f"""
PREDICTION DATA:
    Group size:         {self.groupSize}
    Number of nn (k):   {self.k}
    Values:             {self.largestValues}
    Indexes:            {self.largestIndexes}
        """

    def addThisValue(self, value, index):
        if self.valuesCounter < self.k:
            self.largestValues.append(value)
            self.largestIndexes.append(index)

            self.valuesCounter += 1
            return

        greatestBufferValue = -1
        bufferIndex = -1

        for i in range(len(self.largestValues)):
            tmpValue = self.largestValues[i]

            if value > tmpValue > greatestBufferValue:
                greatestBufferValue = tmpValue
                bufferIndex = i

        if bufferIndex < 0:
            self.valuesCounter += 1
            return

        self.largestValues[bufferIndex] = value
        self.largestIndexes[bufferIndex] = self.valuesCounter

        self.valuesCounter += 1

    def getPrediction(self):
        """
        returns the predicted direction:
            direction > 0: price will go up
            direction < 0: price will go down
            direction = 0: price will stay still

        the value of direction will be between -1 and 1, the absolute value of which will
        give the probability that that direction is right

        :return:
        """

        direction = 0

        valuesDict = {}
        for i in range(len(self.largestValues)):
            valuesDict[self.largestValues[i]] = self.largestIndexes[i]

        sortedKeys = sorted(valuesDict, reverse=True)

        for key in sortedKeys:
            # check where the price goes

        return direction


def getChart(filePath, pair, timeInterval):
    print("Creating chart from csv file... ", end="")

    dataPoints = []

    with open(filePath, "r") as csvFile:
        csvReader = csv.reader(csvFile)
        # skip first row
        next(csvReader)
        for row in csvReader:
            if float(row[5]) == 0:
                # skip "empty" rows
                continue

            # time, Open, High, Low, Close, Volume
            dp = DataPoint(float(row[1]), float(row[4]), float(row[2]), float(row[3]), float(row[5]), timeInterval)
            dataPoints.append(dp)

    print("Done!")

    return Chart(dataPoints, pair, timeInterval)


def getPrediction(chart, groupSize, k):
    prediction = Prediction(groupSize, k)
    currentGroup = DpGroup(chart, groupSize, 0)

    for i in range(1, chart.size() - groupSize):
        diff = currentGroup.similarTo(DpGroup(chart, groupSize, i))
        prediction.addThisValue(diff, i)

    return prediction


if __name__ == '__main__':
    chart = getChart("../forexData/EURUSD_Candlestick_15_M_BID_01.01.2022-01.01.2023.csv", "EURUSD", 15 * 60)
    prediction = getPrediction(chart, 10, 10)

    print(prediction)

    # chart.display()

    print(prediction.getPrediction())

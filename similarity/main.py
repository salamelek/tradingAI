import csv
import numpy as np
import matplotlib.pyplot as plt


class DataPoint:
    def __init__(self, coords):
        self.coords = coords

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

    def __str__(self):
        return f"Chart of length {self.numOfDataPoints} of {self.pair}."

    def display(self):
        print("Displaying chart... ", end="")

        xValues = []
        yValues = []

        # Assuming self.dataPoints is a list of data points
        for i in range(self.numOfDataPoints):
            xValues.append(i)
            yValues.append(self.dataPoints[i].coords[0])

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
    the index 0 of a dataPoint in the group is the last one from left to right (reversed too)

    chart:       a b c d e f
    dp index:    0 1 2 3 4 5
    group2:     |a,b|c,d|e,f|
    dp index:    1 0 1 0 1 0
    group index:  2   1   0
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
    def __init__(self, groupSize, k, index):
        self.valuesCounter = 0
        self.largestValues = []
        self.largestIndexes = []
        self.k = k
        self.groupSize = groupSize
        self.index = index

    def __str__(self):
        return f"""
PREDICTION DATA:
    Group size:             {self.groupSize}
    Number of nn (k):       {self.k}
    Values:                 {self.largestValues}
    Indexes:                {self.largestIndexes}
    Predicted direction:    {self.getPrediction()}
    Target index:           {self.index}
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

        # TODO here im only checking close values, but i should check every value

        directions = []

        valuesDict = {}
        for i in range(len(self.largestValues)):
            valuesDict[self.largestValues[i]] = self.largestIndexes[i]

        sortedKeys = sorted(valuesDict, reverse=True)

        for key in sortedKeys:
            # check where does the price go
            lastValueIndex = valuesDict[key]
            nextValueIndex = lastValueIndex + 1

            lastValue = chart.dataPoints[lastValueIndex]
            nextValue = chart.dataPoints[nextValueIndex]

            if lastValue.coords[0] > nextValue.coords[0]:
                directions.append(-1)
            elif lastValue.coords[0] < nextValue.coords[0]:
                directions.append(1)

        return sum(directions) / len(directions)


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
            # FIXME when using only 1D, every point is the same
            dp = DataPoint([float(row[4])])
            dataPoints.append(dp)

    print("Done!")

    return Chart(dataPoints, pair, timeInterval)


def getPrediction(chart, groupSize, k, dpIndex):
    index = chart.size() - dpIndex

    prediction = Prediction(groupSize, k, dpIndex)
    currentGroup = DpGroup(chart, groupSize, index)

    for i in range(0, chart.size() - groupSize):
        if i == index:
            continue

        diff = currentGroup.similarTo(DpGroup(chart, groupSize, i))
        prediction.addThisValue(diff, i)

    return prediction


if __name__ == '__main__':
    chart = getChart("../forexData/EURUSD_Candlestick_15_M_BID_01.01.2022-01.01.2023.csv", "EURUSD", 15 * 60)
    prediction = getPrediction(chart, 10, 5, 1000)

    # print(chart)
    # print(prediction)
    # chart.display()

    p1 = DataPoint([1])
    p2 = DataPoint([1])
    p3 = DataPoint([10])

    print(p1.cosineSimilarity(p2))
    print(p1.cosineSimilarity(p3))
    print()
    print(p1.dotProduct(p2))
    print(p1.dotProduct(p3))

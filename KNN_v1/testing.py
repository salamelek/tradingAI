import copy

someList = [[1, 2, 3], [1, 3, 9]]
someDict = {"a": [], "b": []}

someDict["a"].append(copy.deepcopy(someList))
print(someDict)

someList[0].pop(0)
someList[0].append(4)

someDict["b"].append(copy.deepcopy(someList))

print(someDict)

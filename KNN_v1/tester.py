# this module will attempt to read the screen to get the prices from any site

import pyautogui
import pytesseract
from pynput import keyboard
import json
import math

# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Set the region to capture (left, top, width, height)
# IMPORTANT the resolution should be quite high, so take the screenshot at like 200% zoom
# ADXRegion = (407, 943, 120, 40)
# CCIRegion = (359, 1048, 120, 40)
# RSIRegion = (361, 1191, 120, 40)
ADXRegion = (2091, 949, 120, 40)
CCIRegion = (2045, 1047, 120, 40)
RSIRegion = (2042, 1174, 120, 40)

print("Data getter running")


point = []


def getTestPoint():
    try:
        extractedADX = float(pytesseract.image_to_string(pyautogui.screenshot(region=ADXRegion)))
        extractedCCI = float(pytesseract.image_to_string(pyautogui.screenshot(region=CCIRegion)))
        extractedRSI = float(pytesseract.image_to_string(pyautogui.screenshot(region=RSIRegion)))

        testPoint = [extractedADX, extractedCCI, extractedRSI]

        print(extractedADX, extractedCCI, extractedRSI)

        return testPoint

    except ValueError:
        print("Could not read well :/")
        return None


def getAction(point):
    distList = []
    with open('adx_cci_rsi_5min.json') as json_file:
        data = json.load(json_file)

    for buyPoint in data["bullish"]:
        dist = (((buyPoint[0] - point[0]) ** 2) + ((buyPoint[1] - point[1]) ** 2) + ((buyPoint[2] - point[2]) ** 2))
        distList.append((dist, "buy"))

    for sellPoint in data["bearish"]:
        dist = (((sellPoint[0] - point[0]) ** 2) + ((sellPoint[1] - point[1]) ** 2) + ((sellPoint[2] - point[2]) ** 2))
        distList.append((dist, "sell"))

    for holdPoint in data["ranging"]:
        dist = (((holdPoint[0] - point[0]) ** 2) + ((holdPoint[1] - point[1]) ** 2) + ((holdPoint[2] - point[2]) ** 2))
        distList.append((dist, "hold"))

    k = int(math.sqrt(len(distList)))
    if len(distList) % 2 == k % 2 == 0:
        # if they are both even, add 1 to k
        k += 1

    sortedDistList = sorted(distList, key=lambda x: x[0])
    firstKNearPoints = sortedDistList[:k]

    labelsList = []
    for nearPoint in firstKNearPoints:
        labelsList.append(nearPoint[1])

    action = max(set(labelsList), key=labelsList.count)

    return action


def onPress(key):
    try:
        if key.char == "t":
            point = getTestPoint()
            if point:
                print(f"Should {getAction(point)}!")

    except AttributeError:
        # Key is not a printable character
        if key == keyboard.Key.esc:
            return False


# Set up the keyboard listener
with keyboard.Listener(on_press=onPress) as listener:
    listener.join()




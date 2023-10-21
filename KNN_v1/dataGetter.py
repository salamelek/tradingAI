# this module will attempt to read the screen to get the prices from any site

import pyautogui
import pytesseract
from pynput import keyboard
import json

# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Set the region to capture (left, top, width, height)
# IMPORTANT the resolution should be quite high, so take the screenshot at like 200% zoom
# windows
# ADXRegion = (407, 943, 120, 40)
# CCIRegion = (359, 1048, 120, 40)
# RSIRegion = (361, 1191, 120, 40)
# ubuntu
ADXRegion = (2091, 949, 120, 40)
CCIRegion = (2045, 1047, 120, 40)
RSIRegion = (2042, 1174, 120, 40)

with open('labeled_data/adx_cci_rsi_5min.json') as json_file:
    data = json.load(json_file)

print("Data getter running")


def on_s():
    try:
        extractedADX = float(pytesseract.image_to_string(pyautogui.screenshot(region=ADXRegion)))
        extractedCCI = float(pytesseract.image_to_string(pyautogui.screenshot(region=CCIRegion)))
        extractedRSI = float(pytesseract.image_to_string(pyautogui.screenshot(region=RSIRegion)))

        data["bearish"].append([extractedADX, extractedCCI, extractedRSI])

        print(extractedADX, extractedCCI, extractedRSI)

    except ValueError:
        print("Could not read well :/")


def on_h():
    try:
        extractedADX = float(pytesseract.image_to_string(pyautogui.screenshot(region=ADXRegion)))
        extractedCCI = float(pytesseract.image_to_string(pyautogui.screenshot(region=CCIRegion)))
        extractedRSI = float(pytesseract.image_to_string(pyautogui.screenshot(region=RSIRegion)))

        data["ranging"].append([extractedADX, extractedCCI, extractedRSI])

        print(extractedADX, extractedCCI, extractedRSI)

    except ValueError:
        print("Could not read well :/")


def on_l():
    try:
        extractedADX = float(pytesseract.image_to_string(pyautogui.screenshot(region=ADXRegion)))
        extractedCCI = float(pytesseract.image_to_string(pyautogui.screenshot(region=CCIRegion)))
        extractedRSI = float(pytesseract.image_to_string(pyautogui.screenshot(region=RSIRegion)))

        data["bullish"].append([extractedADX, extractedCCI, extractedRSI])

        print(extractedADX, extractedCCI, extractedRSI)

    except ValueError:
        print("Could not read well :/")


def onPress(key):
    try:
        if key.char == "s":
            on_s()
        elif key.char == "h":
            on_h()
        elif key.char == "l":
            on_l()

    except AttributeError:
        # Key is not a printable character
        if key == keyboard.Key.esc:
            return False


# Set up the keyboard listener
with keyboard.Listener(on_press=onPress) as listener:
    listener.join()

with open("labeled_data/adx_cci_rsi_5min.json", 'w') as json_file:
    json.dump(data, json_file)

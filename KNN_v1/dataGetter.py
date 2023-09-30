# this module will attempt to read the screen to get the prices from any site

import pyautogui
import pytesseract
import keyboard
import json

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Set the region to capture (left, top, width, height)
# IMPORTANT the resolution should be quite high, so take the screenshot at like 200% zoom
ADXRegion = (407, 943, 120, 40)
CCIRegion = (359, 1048, 120, 40)
RSIRegion = (361, 1191, 120, 40)

with open('data_5m.json') as json_file:
	data = json.load(json_file)

print("Running")


def on_s(e):
	try:
		extractedADX = float(pytesseract.image_to_string(pyautogui.screenshot(region=ADXRegion)))
		extractedCCI = float(pytesseract.image_to_string(pyautogui.screenshot(region=CCIRegion)))
		extractedRSI = float(pytesseract.image_to_string(pyautogui.screenshot(region=RSIRegion)))

		data["bearish"].append([extractedADX, extractedCCI, extractedRSI])

		print("Done!")

	except ValueError:
		print("Could not read well :/")


def on_h(e):
	try:
		extractedADX = float(pytesseract.image_to_string(pyautogui.screenshot(region=ADXRegion)))
		extractedCCI = float(pytesseract.image_to_string(pyautogui.screenshot(region=CCIRegion)))
		extractedRSI = float(pytesseract.image_to_string(pyautogui.screenshot(region=RSIRegion)))

		data["ranging"].append([extractedADX, extractedCCI, extractedRSI])

		print("Done!")

	except ValueError:
		print("Could not read well :/")


def on_l(e):
	try:
		extractedADX = float(pytesseract.image_to_string(pyautogui.screenshot(region=ADXRegion)))
		extractedCCI = float(pytesseract.image_to_string(pyautogui.screenshot(region=CCIRegion)))
		extractedRSI = float(pytesseract.image_to_string(pyautogui.screenshot(region=RSIRegion)))

		data["bullish"].append([extractedADX, extractedCCI, extractedRSI])

		print("Done!")

	except ValueError:
		print("Could not read well :/")


# short
keyboard.on_press_key('s', on_s)
# hold
keyboard.on_press_key('h', on_h)
# long
keyboard.on_press_key('l', on_l)

# Keep the program running
keyboard.wait('esc')  # Program will exit when the Escape key is pressed

with open("data_5m.json", 'w') as json_file:
	json.dump(data, json_file)

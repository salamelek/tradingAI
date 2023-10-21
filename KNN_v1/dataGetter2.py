from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import time
import json
from datetime import date


pressInterval = 0.2     # how many seconds to wait between clicks
running = True


timeFrame = "15min"
indicators = "adx-cci-rsi"


bufferLen = 5
bufferPoint = [[], [], []]


data = {
    "h": [],
    "l": [],
    "s": []
}

# load a dict from a json file
# with open('labeled_data/adx_cci_rsi_5min.json') as jsonFile:
#     data = json.load(jsonFile)


def getDriver(url):
    options = webdriver.FirefoxOptions()
    options.headless = False
    driver = webdriver.Firefox(options=options)

    driver.get(url)

    try:
        """
        Attempts to connect to the given URL
        It will also try to access nested iframes to get the HTML of the chart and thus its values
        """

        partial_id = "tvc_frame_"
        parent_iframe = driver.find_element(By.XPATH, f'//iframe[contains(@id, "{partial_id}")]')
        driver.switch_to.frame(parent_iframe)
        partial_src = "https://tvc-invdn-com.investing.com/web/1.12.34/index60-prod.html"
        iframe = driver.find_element(By.XPATH, f'//iframe[contains(@src, "{partial_src}")]')
        driver.switch_to.frame(iframe)
        partial_src = "https://tvc-invdn-com.investing.com/web/1.12.34/static/tv-chart"
        iframe = driver.find_element(By.XPATH, f'//iframe[contains(@src, "{partial_src}")]')

        # Switch to the third iframe
        driver.switch_to.frame(iframe)

        return driver

        # driver.page_source    # <-- get the raw HTML

    except Exception as e:
        print(f"An error occurred: \n\n{e}\n\n")
        exit()


def getIndicatorsValue():
    """
    ================================
    IMPORTANT:
    Set the ADX indicator to #FF0000
    Set the CCI indicator to #808000
    Set the RSI indicator to #800080
    these are the defaults, so it should work without touching anything
    ================================

    :return:
    """

    class_name = "pane-legend-item-value"

    adxColor = "rgb(255, 0, 0)"
    cciColor = "rgb(128, 128, 0)"
    rsiColor = "rgb(128, 0, 128)"

    adxSelector = f".{class_name}[style*='color: {adxColor}']"
    cciSelector = f".{class_name}[style*='color: {cciColor}']"
    rsiSelector = f".{class_name}[style*='color: {rsiColor}']"

    adxValue = driver.find_element(By.CSS_SELECTOR, adxSelector).text
    cciValue = driver.find_element(By.CSS_SELECTOR, cciSelector).text
    rsiValue = driver.find_element(By.CSS_SELECTOR, rsiSelector).text

    return adxValue, cciValue, rsiValue


def moveByN(n):
    # since we are tabbed in the terminal, we have to send the arrow press via selenium

    for i in range(abs(n)):
        if n > 0:
            # -->
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ARROW_RIGHT)

        elif n < 0:
            # -->
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ARROW_LEFT)

        else:
            # shouldn't be needed but who cares
            break

        time.sleep(pressInterval)


def fillBuffer():
    print("Filling buffer...")

    for i in range(bufferLen):
        adx, cci, rsi = getIndicatorsValue()

        bufferPoint[0].append(adx)
        bufferPoint[1].append(cci)
        bufferPoint[2].append(rsi)

        moveByN(1)

    print("Done!\n")


def deleteLast():
    print("deleted")


def labelKline(label):
    bufferPoint[0].pop(0)
    bufferPoint[1].pop(0)
    bufferPoint[2].pop(0)

    adx, cci, rsi = getIndicatorsValue()

    bufferPoint[0].append(adx)
    bufferPoint[1].append(cci)
    bufferPoint[2].append(rsi)

    # add the point to the data dict
    data[label].append(bufferPoint)

    # print a super cool message

    if label == "l":
        msg = "\033[32m" + "\033[1m" + "LONG" + "\033[0m"
    elif label == "s":
        msg = "\033[31m" + "\033[1m" + "SHORT" + "\033[0m"
    elif label == "h":
        msg = "\033[33m" + "\033[1m" + "HOLD" + "\033[0m"
    else:
        msg = ""

    print(f"Stored kline as {msg}.")


if __name__ == '__main__':
    """
    The user sets a starting point and the program asks the user in what category does every kline should go. 
    This option seems much better in every way, so i dont even know why did i consider the 1st one.
        
    The three categories for each kline are long, short and hold. I need to select any of them with a click of a button.
    Since i cant click any character while on the browser, i will use the terminal window to write b, s and h commands. 
    This has the added advantage that the program will wait the user input.
    
    The labeling of data:
        Label as buy and sell only large spikes, don't cherrypick every kline
        
    Structure of the data:
        data = {
            [
                [1, 2, 3, 4, 5],    # adx
                [2, 3, 4, 5, 6],    # cci
                [3, 4, 5, 6, 7]     # rsi
            ]: "l"
        }
        
        each point is a 2D list. Each sublist is a list of timeframes for each indicator.
    """

    driver = getDriver("https://www.investing.com/charts/futures-charts")

    print("""
DATA LOGGER SETUP

1) Set all the wanted indicators
2) Check the indicators color just in case
3) Set the mouse on the wanted "central" candle
4) Alt-tab to this window (the mouse must remain on the chart!!!!) 
5) Press any key to continue...
    	""")
    input()

    fillBuffer()

    while running:
        currInput = input("Choose action (l, s, h, del, stop): ").lower()

        if currInput in ["l", "s", "h"]:
            labelKline(currInput)
            moveByN(1)

        elif currInput == "del":
            deleteLast()

        elif currInput == "stop":
            running = False

        else:
            print("Invalid input!\nThe possible inputs are the following: l, s, h, del, stop")

        print()

    # write all the data in a json file
    newFileName = str(date.today())

    with open(f"labeled_data/{newFileName}-{timeFrame}-{indicators}-buffer_{bufferLen}.json", 'w') as json_file:
        json.dump(data, json_file)

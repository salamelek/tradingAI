"""
This will (should) label each kline automatically
It will run in two phases:
1) Getting all the klines
2) Identifying the slopes

1) connect to a chart or get data from a dict
    1.1) Data needed is at least close prices and timestamps of klines
2) check at which point it was optimal to buy/sell/hold
    2.1) since this will be algorithmic, I need a concrete way of telling if a trade is good or bad. I will measure it in profit %.
    2.2) Parameters required to define a "good" slope:
        xMin: min num of Klines
        xMax: max num of klines
        yMin: min difference in price
        chop: max tolerated "choppiness" (~~> standard deviation)
            standardDeviation = sqrt(((data[0] - avg(data))² + (data[1] - avg(data))² + ... + (data[len(data) - 1] - avg(data))²) / len(data)
            standardDeviation = dataFrame.std()
    2.3)
        - fill the necessary buffer
        - from kline a, check points in the range [a + xMin, a + xMax]
        - for each kline check, check also y
        - if y > yMin, then check also the std from a to the current kline
        - if std([a, cKline]) < chop, then store a as a good slope point
        - continue to do this until end dof check klines, then procede to the next kline, b
3) label that point
    Since I don't know the timestamps, I'll have to derive them myself.
    Since I know the start kline, current kline and kline time, i can calculate the current kline's timestamp
    Data example:
        timestamp of start of slope: [x, y, std, label]

        GC15min = {
            19-09-23 13:00:00: {
                "coords": [adx0, adx1, ..., rsi4],
                "close": 1924.65,
                "label": "s",
                "duration": 7,
                "priceChange": -3.6,
                "std": 1.2
            },
            19-09-23 13:15:00: {
                "coords": [adx0, adx1, ..., rsi4],
                "close": 1920.52,
                "label": "h",
                "duration": None,
                "priceChange": None,
                "std": None
            },
        }
"""


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import time
import json
import copy
from datetime import datetime

pressInterval = 0.3
xMin = 3
xMax = 50
datetime_str = "01-01-23 00:00:00"
timeIncrement = 15 * 60
wantedNumOfKlines = 1000

running = True

bufferLen = 5
# close, adx, cci, rsi
bufferPoint = [[], [], [], []]

# unix timestamp (seconds) format
datetime_object = datetime.strptime(datetime_str, '%d-%m-%y %H:%M:%S')
startTime = int(datetime.timestamp(datetime_object))
print(f"Starting date: {datetime_object}\nUnix seconds: {startTime}")

# load a dict from a json file
# with open('labeled_data/adx_cci_rsi_5min.json') as jsonFile:
#     data = json.load(jsonFile)


def getDriver(url):
    options = webdriver.FirefoxOptions()
    options.headless = False
    myDriver = webdriver.Firefox(options=options)

    myDriver.get(url)

    try:
        """
        Attempts to connect to the given URL
        It will also try to access nested iframes to get the HTML of the chart and thus its values
        """

        partial_id = "tvc_frame_"
        parent_iframe = myDriver.find_element(By.XPATH, f'//iframe[contains(@id, "{partial_id}")]')
        myDriver.switch_to.frame(parent_iframe)
        partial_src = "https://tvc-invdn-com.investing.com/web/1.12.34/index60-prod.html"
        iframe = myDriver.find_element(By.XPATH, f'//iframe[contains(@src, "{partial_src}")]')
        myDriver.switch_to.frame(iframe)
        partial_src = "https://tvc-invdn-com.investing.com/web/1.12.34/static/tv-chart"
        iframe = myDriver.find_element(By.XPATH, f'//iframe[contains(@src, "{partial_src}")]')

        # Switch to the third iframe
        myDriver.switch_to.frame(iframe)

        return myDriver

        # driver.page_source    # <-- get the raw HTML

    except Exception as e:
        print(f"An error occurred: \n\n{e}\n\n")
        exit()


def getKline():
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

    closeColor = "rgb(91, 26, 19)"
    adxColor = "rgb(255, 0, 0)"
    cciColor = "rgb(128, 128, 0)"
    rsiColor = "rgb(128, 0, 128)"

    adxSelector = f".{class_name}[style*='color: {adxColor}']"
    cciSelector = f".{class_name}[style*='color: {cciColor}']"
    rsiSelector = f".{class_name}[style*='color: {rsiColor}']"

    adxValue = float(driver.find_element(By.CSS_SELECTOR, adxSelector).text)
    cciValue = float(driver.find_element(By.CSS_SELECTOR, cciSelector).text)
    rsiValue = float(driver.find_element(By.CSS_SELECTOR, rsiSelector).text)

    # Find the span element with the "C" value and then
    # Navigate to the next sibling span element for the price
    element_with_c = driver.find_element(By.XPATH, '//span[@class="pane-legend-item-value-title pane-legend-line pane-legend-item-value-title__main" and text()="C"]')
    price_element = element_with_c.find_element(By.XPATH, './following-sibling::span[@class="pane-legend-item-value pane-legend-line pane-legend-item-value__main"]')
    closeValue = float(price_element.text)

    return closeValue, adxValue, cciValue, rsiValue


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
        close, adx, cci, rsi = getKline()

        bufferPoint[0].append(close)
        bufferPoint[1].append(adx)
        bufferPoint[2].append(cci)
        bufferPoint[3].append(rsi)

        moveByN(1)

    print("Done!\n")


def logKline(sTime):
    bufferPoint[0].pop(0)
    bufferPoint[1].pop(0)
    bufferPoint[2].pop(0)
    bufferPoint[3].pop(0)

    close, adx, cci, rsi = getKline()

    bufferPoint[0].append(close)
    bufferPoint[1].append(adx)
    bufferPoint[2].append(cci)
    bufferPoint[3].append(rsi)

    # add the point to the data dict
    # the buffer point must be copied to avoid references to the same buffer point
    # data[label].append(copy.deepcopy(bufferPoint))
    klines[strTime] = {"coords": bufferPoint[1] + bufferPoint[2] + bufferPoint[3], "close": bufferPoint[0][-1]}


if __name__ == '__main__':
    driver = getDriver("https://www.investing.com/charts/futures-charts")

    # wait for user to ready things up
    input()

    fillBuffer()
    startTime += (bufferLen * timeIncrement)

    klines = {}
    lastTime = startTime

    # while running:
    for i in range(wantedNumOfKlines):
        # get kline (close, adx, cci, rsi)
        strTime = datetime.utcfromtimestamp(lastTime + 3600).strftime("%d-%m-%y %H:%M:%S")

        logKline(strTime)
        moveByN(1)

        lastTime += timeIncrement

    with open(f"GC15min.json", 'w') as json_file:
        json.dump(klines, json_file)

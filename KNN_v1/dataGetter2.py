from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Path to the GeckoDriver executable (update this with your driver path)
geckodriver_path = '/path/to/geckodriver'

# Create a new instance of the Firefox driver
options = webdriver.FirefoxOptions()
options.headless = False
driver = webdriver.Firefox(options=options)

# Replace 'https://example.com' with the URL you want to access
url = "https://www.investing.com/charts/futures-charts"
driver.get(url)
time.sleep(10)

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

    # driver.page_source    # <-- get the raw HTML

except Exception as e:
    print(f"An error occurred: \n\n{e}\n\n")
    exit()


# print(driver.page_source)

if __name__ == '__main__':
    # wait for the user to set all the indicators and the wanted future

    """
    Option 1:
        The user selects the starting kline, the program logs it and by navigating using the arrows will also log the previous n klines
    
    Option 2:
        The user sets a starting point and the program asks the user in what category does every kline should go. 
        This option seems much better in every way, so i dont even know why did i consider the 1st one.
        
    The three categories for each kline are buy, sell and hold. I need to select any of them with a click of a button.
    Since i cant click any character while on the browser, maybe i can use buttons like shift, enter and such or just select a window that is not the browser.
    """

    # navigate the chart using arrows left and right

    pass

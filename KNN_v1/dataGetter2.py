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

retries = 10

for i in range(retries):
    try:
        """
        Attempts to connect to the given URL
        It will also try to access nested iframes to get the HTML of the chart and thus its values
        """

        partial_src = "https://tvc4.investing.com/init.php"
        parent_iframe = driver.find_element(By.XPATH, f'//iframe[contains(@src, "{partial_src}")]')
        driver.switch_to.frame(parent_iframe)
        partial_src = "https://tvc-invdn-com.investing.com/web/1.12.34/index60-prod.html"
        iframe = driver.find_element(By.XPATH, f'//iframe[contains(@src, "{partial_src}")]')
        driver.switch_to.frame(iframe)
        partial_src = "https://tvc-invdn-com.investing.com/web/1.12.34/static/tv-chart"
        iframe = driver.find_element(By.XPATH, f'//iframe[contains(@src, "{partial_src}")]')

        # Switch to the third iframe
        driver.switch_to.frame(iframe)

        # driver.page_source    # <-- get the raw HTML

        break

    except Exception as e:
        print(f"An error occurred: \n\n{e}\n\n... Retrying ({i + 1 / retries})")
        time.sleep(10)

for i in range(10):
    print(driver.page_source)

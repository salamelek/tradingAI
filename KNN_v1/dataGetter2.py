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

try:
    driver.get(url)

    time.sleep(10)

    # Find the parent iframe by a partial match on its src attribute
    partial_src = "https://tvc4.investing.com/init.php"
    parent_iframe = driver.find_element(By.XPATH, f'//iframe[contains(@src, "{partial_src}")]')

    # Switch to the parent iframe
    driver.switch_to.frame(parent_iframe)

    # Find the second iframe by a partial match on its src attribute
    partial_src = "https://tvc-invdn-com.investing.com/web/1.12.34/index60-prod.html"
    iframe = driver.find_element(By.XPATH, f'//iframe[contains(@src, "{partial_src}")]')

    # Switch to the second iframe
    driver.switch_to.frame(iframe)

    partial_src = "https://tvc-invdn-com.investing.com/web/1.12.34/static/tv-chart"
    iframe = driver.find_element(By.XPATH, f'//iframe[contains(@src, "{partial_src}")]')

    # Switch to the third iframe
    driver.switch_to.frame(iframe)

    # Now you are inside the third iframe, and you can access its content
    iframe_content = driver.page_source

    # You can now work with the content of the second iframe
    print(iframe_content)


except Exception as e:
    print(f"An error occurred: {e}")

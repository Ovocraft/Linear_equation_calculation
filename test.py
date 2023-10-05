from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

hub_url = "http://localhost:4444/wd/hub"

chrome_options = Options()

driver = webdriver.Remote(
    command_executor=hub_url,
    options=chrome_options
)

driver.get("http://localhost:8000")

element = driver.find_element(By.NAME, "some_element")
element.send_keys("some text")
element.send_keys(Keys.RETURN)

driver.quit()

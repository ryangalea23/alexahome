from selenium import webdriver
import os

def capture_screenshot(url, file_path):
    # Set up headless Chrome browser
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(executable_path='/path/to/chromedriver', options=options)

    # Open the URL
    driver.get(url)

    # Capture and save the screenshot
    driver.save_screenshot(file_path)

    # Close the browser
    driver.quit()

# Example Usage
url = "http://goicon.com"
file_path = "screenshot.png"
capture_screenshot(url, file_path)

from flask import Flask, request, send_file
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
from io import BytesIO
#from dotenv import load_dotenv
#load_dotenv('.env.development')


app = Flask(__name__)
def page_has_loaded(driver):
    return driver.execute_script("return document.readyState;") == "complete"

def capture_screenshot(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")

    service = Service(executable_path=os.environ.get("CHROMEDRIVER_PATH"))
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_window_size(1920, 1080)  # Set the desired window size
    driver.get(url)

    # Save the screenshot to an in-memory file
    try:
        time.sleep(10)
        #WebDriverWait(driver, timeout=10).until(page_has_loaded)
    finally:
        screenshot = BytesIO()
        screenshot.write(driver.get_screenshot_as_png())
        screenshot.seek(0)

    driver.quit()

    return screenshot

@app.route('/screenshot', methods=['GET'])
def screenshot():
    url = request.args.get('url')
    if not url:
        return "No URL provided", 400

    screenshot = capture_screenshot(url)

    return send_file(screenshot, mimetype='image/png')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

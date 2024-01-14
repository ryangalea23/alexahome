from flask import Flask, request, send_file
from selenium import webdriver
import os
from io import BytesIO

app = Flask(__name__)

def capture_screenshot(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=options)

    driver.get(url)

    # Save the screenshot to an in-memory file
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
    app.run(host='0.0.0.0', port=port)

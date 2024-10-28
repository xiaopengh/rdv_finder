import os
import time
import random
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from PIL import Image

def setup_driver():
    """
    Setup the Chrome Web Driver with random user agent and window size
    Web Driver is set to run with headless mode disabled by default
    The driver uses Chrome as the browser
    """
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0",
    ]
    window_sizes = ["1920x1080", "1366x768", "1280x720"]

    options = Options()
    options.add_argument(f'user-agent={random.choice(user_agents)}')
    options.add_argument(f'--window-size={random.choice(window_sizes)}')
    # options.add_argument('--headless')  # Run in headless mode if required

    driver = webdriver.Chrome(options=options)
    return driver

def human_delay(min_seconds=1, max_seconds=3):
    time.sleep(random.uniform(min_seconds, max_seconds))

def human_scroll(driver):
    scroll_pause_time = random.uniform(0.5, 1.5)
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def human_typing(element, text, min_delay=0.05, max_delay=0.2):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(min_delay, max_delay))

def get_html(url):
    """
    Get the HTML content of a webpage using Selenium
    Web Driver waits for the page to load completely with a timeout of 20 seconds
    The function also mimics human behavior by waiting a random time
    """
    driver = setup_driver()
    try:
        driver.get(url)
        # Wait 10 seconds so that the content can be fully loaded
        wait = WebDriverWait(driver, 20)
        wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        # Mimicking human behavior by waiting a random time
        human_delay()
        html = driver.page_source
    finally:
        driver.quit()
    return html

def get_captcha_naive(html, id):
    """
    id: ID of the captcha image element
    html: HTML content of the webpage
    """
    soup = BeautifulSoup(html, 'html.parser')
    captcha_element = soup.find(id=id)
    pretty_html = soup.prettify()
    captcha_url = captcha_element['src']
    captcha_url = captcha_url[5:]
    image_response = requests.get(captcha_url)
    if image_response.status_code == 200:
        with open("downloaded_image.png", "wb") as file:
            file.write(image_response.content)
        print("Image saved as downloaded_image.png")
    else:
        print("Failed to download the image")

def get_screenshot(url, scroll_pos=0):
    """
    url: URL of the webpage
    scroll_pos: Scroll position of the webpage
    """
    driver = setup_driver()
    scroll_speed = 1000
    try:
        driver.get(url)
        # Wait 10 seconds so that the content can be fully loaded
        wait = WebDriverWait(driver, 20)
        wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        # Mimicking human behavior by waiting a random time
        human_delay()
        # Get the window size
        window_size = driver.get_window_size()
        width = window_size['width']
        height = window_size['height']
        # Scroll to the specified position
        driver.execute_script(f"window.scrollTo(0, {scroll_pos});")
        driver.save_screenshot("screenshot.png")
        print("Screenshot saved as screenshot.png")
    finally:
        driver.quit()
    return width, height
import os
import time
import requests
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from PIL import Image
from io import BytesIO
from datetime import datetime
from colorama import Fore, Style, init

# Path to your WebDriver executable
webdriver_path = 'C:/Users/milanszilveszter/Documents/chromedriver.exe'  # Replace with your actual path
save_dir = 'truck_images_2'
os.makedirs(save_dir, exist_ok=True)

WEBCAM_URLS = [ 
    "https://webcams2.asfinag.at/webcamviewer/SingleScreenServlet/?user=webcamstartseite&wcsid=A014_000,070_1_00082441&ssid=1d48c33c-c318-424b-90c8-36da44e2322b&token=IyMjIzM4OCMzMTYjYXRERSNpbmZvI2ZhbHNlI05vdFVzZWQjMTA4MTkyMTI5NQ",
    "https://webcams2.asfinag.at/webcamviewer/SingleScreenServlet/?user=webcamstartseite&wcsid=A014_000,070_2_00082444&ssid=382e63c1-8d99-49dc-ad43-df7af264b60e&token=IyMjIzM4OCMzMTYjYXRERSNpbmZvI2ZhbHNlI05vdFVzZWQjMTA4MTkyMTI5NQ",
    "https://webcams2.asfinag.at/webcamviewer/SingleScreenServlet/?user=webcamstartseite&wcsid=A014_000,200_2_00082447&ssid=da2bc319-0521-4766-b2c6-8fa706fde855&token=IyMjIzM4OCMzMTYjYXRERSNpbmZvI2ZhbHNlI05vdFVzZWQjMTA4MTkyMTI5NQ",
    "https://webcams2.asfinag.at/webcamviewer/SingleScreenServlet/?user=webcamstartseite&wcsid=A014_000,490_0_00082458&ssid=c4bb34d8-690d-43a5-9e6d-699c2c47782b&token=IyMjIzM4OCMzMTYjYXRERSNpbmZvI2ZhbHNlI05vdFVzZWQjMTA4MTkyMTI5NQ",
    "https://webcams2.asfinag.at/webcamviewer/SingleScreenServlet/?user=webcamstartseite&wcsid=A014_024,350_0_00082470&ssid=6c65b61f-dc9d-4eea-bc48-2a0341d7b54c&token=IyMjIzM4OCMzMTYjYXRERSNpbmZvI2ZhbHNlI05vdFVzZWQjMTA4MTkyMTI5NQ",
    "https://webcams2.asfinag.at/webcamviewer/SingleScreenServlet/?user=webcamstartseite&wcsid=A014_024,350_Q_00082467&ssid=bbad3b43-3263-439e-ad2e-005c01bd8745&token=IyMjIzM4OCMzMTYjYXRERSNpbmZvI2ZhbHNlI05vdFVzZWQjMTA4MTkyMTI5NQ",
    "https://webcams2.asfinag.at/webcamviewer/SingleScreenServlet/?user=webcamstartseite&wcsid=S016_044,100_0_00082486&ssid=fb77c13c-c7ef-43c9-9d31-dba431217a79&token=IyMjIzM4OCMzMTYjYXRERSNpbmZvI2ZhbHNlI05vdFVzZWQjMTA4MTkyMTI5NQ",
    "https://webcams2.asfinag.at/webcamviewer/SingleScreenServlet/?user=webcamstartseite&wcsid=A012_135,430_0_00082436&ssid=22c49859-9300-429c-ad03-12e46a8e9fad&token=IyMjIzM4OCMzMTYjYXRERSNpbmZvI2ZhbHNlI05vdFVzZWQjMTA4MTkyMTI5NQ",
    "https://webcams2.asfinag.at/webcamviewer/SingleScreenServlet/?user=webcamstartseite&wcsid=A012_103,340_2_00092628&ssid=0ff2da18-9de3-415b-a450-d5200ff2362e&token=IyMjIzM4OCMzMTYjYXRERSNpbmZvI2ZhbHNlI05vdFVzZWQjMTA4MTkyMTI5NQ",
    "https://webcams2.asfinag.at/webcamviewer/SingleScreenServlet/?user=webcamstartseite&wcsid=A012_103,340_1_00092625&ssid=1576f63f-bcdf-4ad0-9cb4-0312e361ca2e&token=IyMjIzM4OCMzMTYjYXRERSNpbmZvI2ZhbHNlI05vdFVzZWQjMTA4MTkyMTI5NQ",
    "https://webcams2.asfinag.at/webcamviewer/SingleScreenServlet/?user=webcamstartseite&wcsid=A012_095,750_0_00082425&ssid=62d09e8b-9337-4a1d-9123-341874ee5d12&token=IyMjIzM4OCMzMTYjYXRERSNpbmZvI2ZhbHNlI05vdFVzZWQjMTA4MTkyMTI5NQ",
    "https://webcams2.asfinag.at/webcamviewer/SingleScreenServlet/?user=webcamstartseite&wcsid=A013_034,025_1_00112518&ssid=a0290e70-930c-4f99-a5fb-47c822d85c54&token=IyMjIzM4OCMzMTYjYXRERSNpbmZvI2ZhbHNlI05vdFVzZWQjMTA4MTkyMTI5NQ",
    "https://webcams2.asfinag.at/webcamviewer/SingleScreenServlet/?user=webcamstartseite&wcsid=A008_000,550_2_00012745&ssid=351ec7e8-28f9-4a72-99a8-a1c48350fa51&token=IyMjIzM4OCMzMTYjYXRERSNpbmZvI2ZhbHNlI05vdFVzZWQjMTA4MTkyMTI5NQ"
]

# Initialize Selenium WebDriver
service = Service(webdriver_path)
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run in headless mode (no browser window)
options.add_argument('--enable-gpu')
driver = webdriver.Chrome(service=service, options=options)

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create a console handler
ch = logging.StreamHandler()

# Define log format
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(ch)

# Define colorful logging functions
def log_info(message):
    logger.info(f"{Fore.CYAN}{message}{Style.RESET_ALL}")

def log_success(message):
    logger.info(f"{Fore.GREEN}{message}{Style.RESET_ALL}")

def log_warning(message):
    logger.warning(f"{Fore.YELLOW}{message}{Style.RESET_ALL}")

def log_error(message):
    logger.error(f"{Fore.RED}{message}{Style.RESET_ALL}")

def log_debug(message):
    logger.debug(f"{Fore.MAGENTA}{message}{Style.RESET_ALL}")

def download_image(webcam_url, driver, index):
    try:
        # Shorten the URL for logging
        short_url = f"Webcam {index + 1}"

        # Open the webcam page
        log_info(f"Processing {short_url}...")
        driver.get(webcam_url)
        
        # Wait for the page to load
        time.sleep(3)

        # Find the image element
        img_element = driver.find_element(By.TAG_NAME, 'img')

        # Get the image URL
        img_url = img_element.get_attribute('src')
        log_debug(f"Image URL found for {short_url}")

        # Download the image
        img_response = requests.get(img_url)
        img_response.raise_for_status()

        # Verify that the content is an image and save it
        content_type = img_response.headers.get('Content-Type', '')
        if 'image' in content_type:
            # Save the image with the current timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S") + f"_{datetime.now().microsecond // 1000:03d}"
            image_filename = f"webcam_image_{timestamp}.jpg"
            full_path = os.path.join(save_dir, image_filename)
            img = Image.open(BytesIO(img_response.content))
            img.save(full_path)
            log_success(f"Image saved for {short_url} at {full_path}")
        else:
            log_warning(f"Downloaded content for {short_url} is not an image. Content-Type: {content_type}")

    except Exception as e:
        log_error(f"An error occurred while processing {short_url}: {e}")

try:
    # Infinite loop to download images every 15 minutes
    while True:
        for index, webcam_url in enumerate(WEBCAM_URLS):
            download_image(webcam_url, driver, index)
        
        # Sleep for 15 minutes (900 seconds)
        log_info("Waiting for 15 minutes before the next download...")
        time.sleep(900)  # 15 minutes

except KeyboardInterrupt:
    log_warning("Stopping the webcam downloader...")

finally:
    driver.quit()
    log_info("Web driver closed.")

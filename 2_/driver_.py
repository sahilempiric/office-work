import os.path
import zipfile

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager



def driver_options():
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--autoplay-policy=no-user-gesture-required')
    options.add_argument('--start-maximized')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--disable-blink-features")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--enable-javascript")
    options.add_argument("--disable-notifications")
    options.add_argument("disable-infobars")
    options.add_argument('--no-proxy-server')
    
    options.add_argument('--disable-gpu')
    options.add_argument("--disable-popup-blocking")
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("--disable-web-security")
    options.add_argument("--allow-running-insecure-content")
    options.add_experimental_option('useAutomationExtension', True)
    options.add_experimental_option("excludeSwitches", [
        "enable-logging",
        "enable-automation",
        "ignore-certificate-errors",
        "safebrowsing-disable-download-protection",
        "safebrowsing-disable-auto-update",
        "disable-client-side-phishing-detection"])
    # options.add_argument('--user-data-dir=./profiles/')
    # options.add_argument(f"--profile-directory={profile_dir}")
    prefs = {"credentials_enable_service": True,
             "profile.password_manager_enabled": True}
    options.add_experimental_option("prefs", prefs)
    # options.add_extension(os.path.join(BASE_DIR, "store/cyberghost.crx"))

    return options


def get_driver():
    
    options = driver_options()
    # service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    return driver

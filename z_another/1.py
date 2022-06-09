import time,  requests, string
from random import randint
import random
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
import threading, queue
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager

# user_v = '7PLwk9zH36H68SK4nwiTgFNW'
# pass_v = 'SoWr1BBWKh5s3KoEt8fZrFjT'

with open('cred.txt', 'r') as f:
    for line in f.readlines():
        user_v, pass_v = line.split(' ')

def generateUser():
	#generates random username and password
	username = names.get_first_name()
	username += ''.join(str(randint(0,9))for i in range(randint(5,20)))
	password = ''.join(random.choice(string.ascii_letters+string.digits) for i in range(randint(10,20)))

	return username, password


def gets( PROXY):
    try:

        # desired_capabilities = webdriver.DesiredCapabilities.CHROME.copy()
        # desired_capabilities['proxy'] = {
        #    "httpProxy":PROXY,
        #    "ftpProxy":PROXY,
        #    "sslProxy":PROXY,
        #     "proxyType":"MANUAL",
        #     "noProxy":[],
        #     "class": "org.openqa.selenium.Proxy",
        #     "autodetect": False
        # }
        opt = {'proxy':
        {
            'https':f'socks5://{user_v}:{pass_v}@{PROXY}',
            'no_proxy':'localhost,127.0.0.1,dev_server:8080'}
        }

        software_names = [SoftwareName.CHROME.value]
        operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]   

        user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)

        useragent = user_agent_rotator.get_random_user_agent()

        options = webdriver.ChromeOptions() 

        # options.add_extension("CyberGhost_VPN.crx")#crx file path
        options.add_argument('--no-sandbox')
        options.add_argument('--autoplay-policy=no-user-gesture-required')
        options.add_argument('--start-maximized')    
        options.add_argument('--single-process')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--disable-blink-features")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--enable-javascript")
        options.add_argument("--disable-notifications")
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument("--enable-popup-blocking")
        options.add_argument("--incognito")
        options.add_argument("start-maximized")
        options.add_argument("--disable-blink-features")
        options.add_argument("--disable-blink-features")
        options.add_argument("--disable-blink-features=AutomationControlled")

        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option("excludeSwitches", [
            "enable-logging",
            "enable-automation",
            "ignore-certificate-errors",
            "safebrowsing-disable-download-protection",
            "safebrowsing-disable-auto-update",
            "disable-client-side-phishing-detection"])
        options.add_argument("disable-infobars")

        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options,)
        stealth(driver,
            languages=["en-US", "en"],
            user_agent=useragent,
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )
        

q = queue.Queue()

def find_email_veri(driver):
    scrolling_px = 500
    for i in range(2):
        driver.execute_script(f"window.scrollTo(0, {scrolling_px})")
        k = 0
        scrolling_px+=500

        
        while True:
            if k<= 5:
                try:
                    driver.find_element_by_xpath("//a[contains(text(), 'Verify your Reddit email address')]").click()
                    print('got email')
                    break

                except:
                    time.sleep(10)

                    k = k+1

with open('proxy.txt', 'r') as f:
    for line in f.readlines():
        q.put(line)

def main(proxy):
    loop_bool = True
    while loop_bool:
        try:
            proxy = proxy
            gets_return = gets(user, passw, proxy)
            if gets_return:
                loop_bool = False
                return True
        except:
            continue
n = int(input("Enter the number of accounts: "))
q_s = 3
# q_s = 2


my_tr = []

if q_s>=n:

    for _ in range(n):
        prx = q.get()
        t = threading.Thread(target=main, args=(prx,))
        t.start()
        my_tr.append(t)

    for t in my_tr:
        t.join()

else:
    m = int(n/q_s)

    for _ in range(m):
        for _ in range(q_s):
            prx = q.get()
            t = threading.Thread(target=main, args=(prx,))
            t.start()
            my_tr.append(t)

        for t in my_tr:
            t.join()

        with q.mutex:
            q.queue.clear()

        with open('proxy.txt', 'r') as f:
            for line in f.readlines():
                q.put(line)

        my_tr.clear()
           
        time.sleep(randint(3600, 4680))


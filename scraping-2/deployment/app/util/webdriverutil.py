from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from configparser import ConfigParser
from time import sleep

config = ConfigParser()
config.read("./config.ini")

environment = config['DEFAULT']['ENVIRONMENT']

def __create_webdriver():
    if environment == 'DEVELOPMENT':
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
        )
    elif environment == 'PRODUCTION':
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
    
        # Handle: urllib3.exceptions.MaxRetryError
        sleep(3)
        driver = webdriver.Remote(
            command_executor='http://chrome:4444/wd/hub',
            options=chrome_options
        )
    else:
        raise Exception(f'unknown environment {environment} in config ini')

    secret = ConfigParser()
    secret.read('./secret.ini')

    email = secret['DEFAULT']['email']
    password = secret['DEFAULT']['password']

    driver.get('https://stockbit.com/login')
    driver.find_element(by=By.XPATH, value="//input[@id='username']").send_keys(email)
    driver.find_element(by=By.XPATH, value="//input[@id='password']").send_keys(password)
    driver.find_element(by=By.XPATH, value="//button[@id='email-login-button']").click()
    
    # Handle: after __create_driver(), immediately do driver.get(), the page won't change
    sleep(1)
    
    return driver

def get_webdriver():
    global driver
    try:
        driver
    except NameError:
        driver = __create_webdriver()
    
    return driver

# it takes time for webdriver.Remote()
if environment == 'PRODUCTION':
    get_webdriver()
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import threading
from configparser import ConfigParser

from time import sleep

config = ConfigParser()
config.read("./config.ini")

if config['DEFAULT']['ENVIRONMENT'] == 'DEVELOPMENT':
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
    )
elif config['DEFAULT']['ENVIRONMENT'] == 'PRODUCTION':
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

def scrape(symbol: str):
    driver.get(f'https://stockbit.com/symbol/{symbol}')
    
    while True:
        date_elements = driver.find_elements(by=By.XPATH, value="//a[@color='#B5B5B5']")
        
        # Handle: IndexError: list index out of range
        if len(date_elements) != 0:
            break
        
    # Handle: All arrays must be of the same length
    comment_elements = driver.find_elements(by=By.XPATH, value="//p[@color='#333333' and @style='word-wrap:break-word']")
    
    dates = [date_element.text for date_element in date_elements]
    comments = [comment_element.text for comment_element in comment_elements]
    
    # print(f'{symbol} dates {len(dates)} comments {len(comments)}')
    # print(dates[-1], comments[-1])
    
    return dates, comments

def __populate_db():
    global db 
    
    db = pd.DataFrame()
    symbols = [
        'ICBP', 'CPIN', 'INDF', 'MYOR', 'CMRY', 'GOOD', 'MLBI',
        'PANI', 'JPFA', 'AALI', 'ULTJ', 'FAPA', 'SMAR', 'SSMS',
        'STAA', 'STTP', 'ROTI', 'LSIP', 'TLDN', 'SIMP', 'PALM',
        'CLEO', 'DSNG', 'ADES', 'WMPP', 'TBLA', 'CPRO', 'SGRO', 'BISI',
        'FISH', 'PSGO', 'JARR', 'DLTA', 'MGRO', 'ANJT', 'BWPT', 'KEJU', 
        'TRGU', 'CAMP', 'WMUU', 'MAIN', 'CEKA', 'CSRA', 'AISA', 'HOKI'
    ]
    
    for symbol in symbols:
        dates, comments = scrape(symbol)
        
        df_c = pd.DataFrame(data={'date': dates, 'comment': comments, 'symbol': symbol})
        
        db = pd.concat([db, df_c])
    
    # scrape daily.
    scrape_daily = threading.Timer(interval=3600*24, function=__populate_db)
    scrape_daily.start()

__populate_db()

def get_db(symbol: str):
    return db.loc[db['symbol'] == symbol]
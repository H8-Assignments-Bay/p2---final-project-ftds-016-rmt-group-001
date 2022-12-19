from util.webdriverutil import get_webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
import pandas as pd
import numpy as np
from util.cacheutil import get_cache, set_cache

# import threading

def __get_comments(driver: WebDriver, symbol: str, end_at: int):
    driver.get(f'https://stockbit.com/symbol/{symbol}')
    
    while True:
        # if not logged in
        # date_elements = driver.find_elements(by=By.XPATH, value="//a[@color='#B5B5B5']")
        # if logged in
        date_elements = driver.find_elements(by=By.XPATH, value="//div[@class='stream-date']")
        
        # Handle: IndexError: list index out of range
        if len(date_elements) != 0:
            break
        
    while True:
        if len(date_elements) < end_at:
            driver.execute_script("window.scrollBy(0,document.body.scrollHeight)", "")
            date_elements = driver.find_elements(by=By.XPATH, value="//div[@class='stream-date']")
        else:
            break
        
    # Handle: All arrays must be of the same length
    # if not logged in
    # comment_elements = driver.find_elements(by=By.XPATH, value="//p[@color='#333333' and @style='word-wrap:break-word']")
    # if logged in
    comment_elements = driver.find_elements(by=By.CLASS_NAME, value="stream-text-single")
        
    dates = []
    comments = []
        
    for index, (date_element, comment_element) in enumerate(zip(date_elements, comment_elements)):
        # Handle: StaleElementReferenceException or ''
        if index == len(date_elements) - 1:
            break
        
        dates.append(date_element.text)
        comments.append(comment_element.text)
    
    # print(f'{symbol} dates {len(dates)} comments {len(comments)}')
    # print(dates[-1], comments[-1])
    
    return pd.DataFrame(data={ 'date': dates, 'comment': comments})

# def __populate_db():
#     global db 
    
#     db = pd.DataFrame()
#     if config['DEFAULT']['ENVIRONMENT'] == 'DEVELOPMENT':
#         symbols = [
#             'ICBP', 'CPIN', 'INDF', 'MYOR', 'CMRY', 'GOOD', 'MLBI',
#         ]
#     elif config['DEFAULT']['ENVIRONMENT'] == 'PRODUCTION':
#         symbols = [
#             'ICBP', 'CPIN', 'INDF', 'MYOR', 'CMRY', 'GOOD', 'MLBI',
#             'PANI', 'JPFA', 'AALI', 'ULTJ', 'FAPA', 'SMAR', 'SSMS',
#             'STAA', 'STTP', 'ROTI', 'LSIP', 'TLDN', 'SIMP', 'PALM',
#             'CLEO', 'DSNG', 'ADES', 'WMPP', 'TBLA', 'CPRO', 'SGRO', 'BISI',
#             'FISH', 'PSGO', 'JARR', 'DLTA', 'MGRO', 'ANJT', 'BWPT', 'KEJU', 
#             'TRGU', 'CAMP', 'WMUU', 'MAIN', 'CEKA', 'CSRA', 'AISA', 'HOKI'
#         ]
    
#     for symbol in symbols:
#         dates, comments = scrape(symbol)
        
#         df_c = pd.DataFrame(data={'date': dates, 'comment': comments, 'symbol': symbol})
        
#         db = pd.concat([db, df_c])
    
#     # scrape daily.
#     scrape_daily = threading.Timer(interval=3600*24, function=__populate_db)
#     scrape_daily.start()

# __populate_db()

# TODO: Not Spam/Spam Model
def __predict_spam(comments: pd.DataFrame):
    return np.random.randint(0,2, comments.shape[0])

# TODO: Rule-based Filter
def __predict_subject(comments: pd.DataFrame):
    return np.random.randint(0,2,comments.shape[0])

# TODO: Neutral/Negative/Positive Model
def __predict_sentiment(comments: pd.DataFrame):
    return np.random.randint(0,3,comments.shape[0])

def __do_predict_chain(driver: WebDriver, symbol: str, end_at: int):
    comments = __get_comments(driver=driver, symbol=symbol, end_at=end_at)
    
    comments['label 2'] = __predict_spam(comments)
    
    comments.loc[comments['label 2'] == 0, 'subject'] = __predict_subject(comments[comments['label 2'] == 0])
    
    comments.loc[comments['subject'] == True, 'label 1'] = __predict_sentiment(comments[comments['subject'] == True])
    
    set_cache(symbol, comments)
    
    return comments

def get_sentiment(symbol: str, start_from: int, end_at: int):
    driver = get_webdriver()
    
    comments = get_cache(symbol)
    
    # end_at - 1 because we drop 1 row to handle StaleElementReferenceException or ''
    if comments is None or len(comments) < end_at - 1:
        comments = __do_predict_chain(driver=driver, symbol=symbol, end_at=end_at)
        
    comments = comments[start_from:end_at]
        
    return {
        'neutral': len(comments[comments['label 1'] == 0]),
        'negative': len(comments[comments['label 1'] == 1]),
        'positive': len(comments[comments['label 1'] == 2]),
        'comments': comments[[ 'date', 'comment', 'label 2', 'subject', 'label 1']].to_dict(orient="records")
    }
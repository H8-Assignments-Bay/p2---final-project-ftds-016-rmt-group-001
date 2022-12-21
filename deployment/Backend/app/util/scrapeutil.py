from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
import pandas as pd

def get_comments(driver: WebDriver, symbol: str, end_at: int):
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
    
    return pd.DataFrame(data={ 'date': dates, 'comment': comments})
from util.webdriverutil import get_webdriver
from util.cacheutil import get_cache, set_cache
from util.scrapeutil import get_comments
from util.spamutil import predict_spam
from util.ruleutil import predict_subject
from util.sentimentutil import predict_sentiment
from selenium.webdriver.chrome.webdriver import WebDriver

def __do_predict_chain(driver: WebDriver, symbol: str, end_at: int):
    comments = get_comments(driver=driver, symbol=symbol, end_at=end_at)
    
    comments['label 2'] = predict_spam(comments)
    
    comments.loc[comments['label 2'] == 0, 'subject'] = predict_subject(comments[comments['label 2'] == 0])
    comments['subject'].fillna(value="", inplace=True)
    
    comments.loc[comments['subject'] == True, 'label 1'] = predict_sentiment(comments[comments['subject'] == True])
    comments['label 1'].fillna(value="", inplace=True)
    
    return comments

def predict_or_get_sentiment(symbol: str, start_from: int, end_at: int):
    driver = get_webdriver()
    
    comments = get_cache(symbol)
    
    # end_at - 1 because we drop 1 row to handle StaleElementReferenceException or ''
    if comments is None or len(comments) < end_at - 1:
        comments = __do_predict_chain(driver=driver, symbol=symbol, end_at=end_at)
        
    set_cache(symbol, comments)
        
    comments = comments[start_from:end_at]
        
    return {
        'neutral': len(comments[comments['label 1'] == 0]),
        'negative': len(comments[comments['label 1'] == 1]),
        'positive': len(comments[comments['label 1'] == 2]),
        'comments': comments[[ 'date', 'comment', 'label 2', 'subject', 'label 1']].to_dict(orient="records")
    }
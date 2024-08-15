import time
import sys
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

from scraper import scrape_stock_data
from scraper import scrape_articles 
from scraper import scrape_text

from model import analyze

BRIGHT_CYAN = '\033[96m'
BRIGHT_MAGENTA = '\033[95m'
RESET = '\033[0m' # called to return to standard terminal text color

# Usage is on ONE stock
def womptrompolis(ticker):
    options = Options()
    options.headless = True

    # Initialize Driver
    driver = driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=options,
    )
    driver.set_window_size(1000, 1000)

    # Store the information:
    ret = [] # Ticker: [Articles, Scores]
    all_articles = {}   # Title of Article: URL

    # Omit quantitative data because available through yahoo_fin lib

    # Articles
    articles = scrape_articles(ticker)

    # Text from each of them
    text = ""
    for title in articles:
        text += scrape_text(articles[title])
    
    # Analyze text + record
    score = analyze(text)
    ret.append(score)
    ret.append(articles)


    # Close the driver
    driver.quit()
    print(ret)
    return ret



tsla = "TSLA"
five_tickers = "AMZN AAPL GOOGL MSFT TSLA" # Change later
# womptrompolis(tsla)
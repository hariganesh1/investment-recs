import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests

## Scraping Function

def scrape_stock_data(driver, ticker):
    # print("data")
    # print(ticker)
    # Set up URL with Driver
    url = f'https://finance.yahoo.com/quote/{ticker}'
    driver.get(url)

    price_selector = f'fin-streamer[data-symbol="{ticker}"][data-field="regularMarketPreviousClose"]'
    price_element = driver.find_element(By.CSS_SELECTOR, price_selector)
    market_price = price_element.get_attribute("data-value")

    open_selector = f'fin-streamer[data-symbol="{ticker}"][data-field="regularMarketOpen"]'
    open_element = driver.find_element(By.CSS_SELECTOR, open_selector)
    market_open = open_element.get_attribute("data-value")

    range_selector = f'fin-streamer[data-symbol="{ticker}"][data-field="regularMarketDayRange"]'
    range_element = driver.find_element(By.CSS_SELECTOR, range_selector)
    day_range = range_element.get_attribute("data-value")

    # Add info to dictionary with stocks 
    stockInfo = {'ticker' : ticker}
    stockInfo['market_price (previous close)'] = market_price
    stockInfo['market_open'] = market_open
    stockInfo['day_range'] = day_range

    # Use this to predict w/RNN

    return stockInfo

# print(scrape_stock_data(webdriver.Chrome(ChromeDriverManager().install()), "AAPL"))
## Helper method to get the top URLs and related to the stock from yahoo finance
def scrape_articles(ticker): 
    # print("urls")
    # print(ticker)
    # Set up URL with BeautifulSoup
    url = f'https://finance.yahoo.com/quote/{ticker}'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Get all the articles pertaining to the stock
    links = soup.find_all("a", class_="subtle-link fin-size-small thumb yf-13p9sh2")

    articles = {}
    urls = []
    titles = []
    index = 0
    websites = True

    while websites and index < len(links): # Retrieves the first five links
        link = links[index]
        index += 1
        url = link["href"] # Retrieves URLs; they're marked with href
        title = link["title"] # Retrieves the title of the article
        if "a.beap.gemini.yahoo" in url:
            websites = False
        else:
            urls.append(url)
            titles.append(title)
            articles[title] = url

    return articles

## Scrape the text from the first five URLs from the ticker's website
def scrape_text(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    paras = soup.find_all("p")
    text = ''
    for para in paras:
        text += para.get_text()
    
    return text





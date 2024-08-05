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

    market_price = driver.find_element(By.CSS_SELECTOR, f'fin-streamer[data-symbol={ticker}][data-field="regularMarketPreviousClose"]')\
        .get_attribute("data-value")

    market_open = driver.find_element(By.CSS_SELECTOR, f'fin-streamer[data-symbol={ticker}][data-field="regularMarketOpen"]')\
        .get_attribute("data-value")

    day_range = driver.find_element(By.CSS_SELECTOR, f'fin-streamer[data-symbol={ticker}][data-field="regularMarketDayRange"]')\
        .get_attribute("data-value")

    # Add info to dictionary with stocks 
    stockInfo = {'ticker' : ticker}
    stockInfo['market_price (previous close)'] = market_price
    stockInfo['market_open'] = market_open
    stockInfo['day_range'] = day_range

    # Use this to predict w/RNN

    return stockInfo

## Helper method to get the top 5 URLs related to the stock from yahoo finance
def scrape_urls(ticker): 
    # print("urls")
    # print(ticker)
    # Set up URL with BeautifulSoup
    url = f'https://finance.yahoo.com/quote/{ticker}'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Get all the articles pertaining to the stock
    links = soup.find_all("a", class_="subtle-link fin-size-small thumb yf-13p9sh2")

    urls = []
    
    index = 0
    websites = True
    '''index < 5 and''' 
    while websites and index < len(links): # Retrieves the first five links
        link = links[index]
        index += 1
        url = link["href"] # Retrieves URLs; they're marked with href
        if "a.beap.gemini.yahoo" in url:
            websites = False
        else:
            urls.append(url)

    return urls

## Scrape the text from the first five URLs from the ticker's website
def scrape_text(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    paras = soup.find_all("p")
    text = ''
    for para in paras:
        text += para.get_text()
    
    return text





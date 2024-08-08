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
## Driver Code. Input from Cmd Line. 

if (len(sys.argv) <= 1):
    print("Input Ticket Symbol To Extract!")
    print("Eg. Correct Usage: python main.py NVDA AAPL AMZN for Nvidia, Apple, and Amazon respectively")
    sys.exit(2)
ticker = sys.argv[1]

# Options
options = Options()
options.headless = True

# Initialize driver with website
# url = f'https://finance.yahoo.com/quote/{ticker_symbol}'

driver = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install()),
    options=options,
)
driver.set_window_size(1000, 1000)

# Function for the frontend stuff

def get_data():
    return scrape_stock_data(driver, ticker)

stock_data = [] # List of stock data dictionaries
scoreDict = {} # Scores of each URL
articles = {} # Title of Article -> URL
all_urls = []

for ticker in sys.argv[1:]:
    stock_data.append(scrape_stock_data(driver, ticker))
    urls = scrape_articles(ticker)
    text = ""
    for title in urls.keys():
        text += scrape_text(urls[title])
    all_urls.append(urls)

    score = analyze(text) # Preprocesses, records sentiment
    scoreDict[ticker] = score



print("stock data scraper: \n")
for data in stock_data:
    print(data)
print("stock scores: ")
for score in scoreDict:
    print("stock: ", score, "corresponding score: ", scoreDict[score])

driver.quit()


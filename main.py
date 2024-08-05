import time
import sys
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

from scraper import scrape_stock_data
from scraper import scrape_urls 
from scraper import scrape_text

from old_model import analyze
# from old_model import analyze_without_preprocess
## Driver Code. Input from Cmd Line. 

start_time = time.time()


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

stock_data = [] # List of stock data dictionaries
urls_array = [] # List of all the URLs listed in the Yahoo Finance Quote website
scoreDict = {}

for ticker in sys.argv[1:]:
    stock_data.append(scrape_stock_data(driver, ticker))
    urls = scrape_urls(ticker)
    text = ""
    for url in urls:
        text += scrape_text(url)
    urls_array.append(urls)

    filename = f'{ticker}_url_text.txt'
    f = open(filename, "w") # Opens a new file & writes 
    f.write(text)
    f.close()
    score = analyze(text) # Preprocesses, records sentiment
    scoreDict[ticker] = score


    # f_all_text = open("all_text.txt", "a") # Append to the file
    # f_all_text.write(text)
    # f_all_text.close()



print("stock data scraper: \n")
for data in stock_data:
    print(data)
# print("stock urls scraper: \n")
# for urls in urls_array:
#     for url in urls:
#         print(url)
# print('\n')
print("stock scores: ")
for score in scoreDict:
    print("stock: ", score, "corresponding score: ", scoreDict[score])

driver.quit()


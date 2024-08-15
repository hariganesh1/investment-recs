from flask import Flask, render_template, request, jsonify
from yahoo_fin.stock_info import get_data
from datetime import datetime
from scraper import scrape_articles
from scraper import scrape_text
from sentiment import get_sentiment


app = Flask(__name__)





def process_input(ticker):
    # Quantitative Data
    data = get_data(ticker)
    recent = data.iloc[-1]
    open = round(recent["open"], 2)
    close = round(recent["close"], 2)
    ret = f"{ticker}\n"
    ret += f"The most recent open price (today if it's after 4:30 PM EST or yesterday's if before then) is ${open}.\n"
    ret += f"The most recent close price (today if it's after 4:30 PM EST or yesterday's if before then) is ${close}.\n"

    articles = scrape_articles(ticker)

    # Maybe do sentiment of EACH article but that takes a while
    ret += f"This is the most recent news about {ticker}:\n"
    urls = []
    text = ""
    for article in articles:
        ret += f"Article: \"{article}\" --> URL: {articles[article]}\n"
        urls.append(articles[article])
    for url in urls:
        text += scrape_text(url)
    ret += "This is the sentiment analysis of the news:\n"
    ret += get_sentiment(ticker, text)

    return ret

@app.route('/', methods=['GET', 'POST'])

def index():
    ticker = None
    if request.method == 'POST':
        ticker = request.form.get('stock')
        articles = scrape_articles(ticker)
    articles = scrape_articles(ticker)
    return render_template('index.html')

@app.route('/process', methods=['POST'])

def process():
    input = request.form.get("stock")
    # Get stocks and then process them
    # Each stock is one word in the input separated by a space so get the process_input for each stock and return the jsonified result
    
    result = ""
    for stock in input.split(", "):
        result += process_input(stock)
        result += "\n"
        result += "\n"
    
    return jsonify(result=result)



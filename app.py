from flask import Flask, render_template, request, jsonify
from yahoo_fin.stock_info import get_data
from datetime import datetime
import pytz


# from main import get_data

app = Flask(__name__)



# Format of this can be like:
# AAPL

# - (either today's if it's after 5pm in ur time OR yday's) open price: $xx
# - (either today's if it's after 5pm in ur time OR yday's) close price: $xx
# - Here are the articles listed on yahoo finance: {article titles w/url's embedded in them}
# - NLTK's thoughts on their sentiment 




def process_input(ticker):
    # Write python script that get's current time and check's if it's after 5pm
    now = datetime.now(pytz.utc)
    est = pytz.timezone("US/Eastern")
    now = now.astimezone(est)
    now = now.strftime("%H:%M:%S")
    print(now)
    data = get_data(ticker)
    recent = data.iloc[-1]
    open = recent["open"]
    close = recent["close"]
    ret += f"{ticker}\n"
    ret += f"The most recent open price (today if it's after 4:30 PM EST or yesterday's if before then) is {open}.\n"
    ret += f"The most recent close price (today if it's after 4:30 PM EST or yesterday's if before then) is {close}.\n"

    ret = "This is the stock data for " + ticker + "\n"
    ret += f"Most recent open price: {open}.\n Most recent close price: {close}."
    return ret

@app.route('/')

def index():
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
    
    # result = ""
    # stock = ""
    # for letter in input:
    #     if stock != " ":
    #         stock += letter
    #     else:
    #         result += process_input(stock)
    
    return jsonify(result=result)



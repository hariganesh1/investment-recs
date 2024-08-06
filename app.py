from flask import Flask, render_template, request, jsonify
from yahoo_fin.stock_info import get_data


# from main import get_data

app = Flask(__name__)


def process_input(ticker):
    data = get_data(ticker)
    recent = data.iloc[-1]
    open = recent["open"]
    close = recent["close"]
    ret = "This is the stock data for " + ticker + "\n"
    ret += f"Most recent open price: {open}.\n Most recent close price: {close}."
    return ret

@app.route('/')

def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])

def process():
    input = request.form.get("stock")
    result = process_input(input)
    return jsonify(result=result)
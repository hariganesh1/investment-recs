from flask import Flask, render_template, request, jsonify
from yahoo_fin.stock_info import get_data


# from main import get_data

app = Flask(__name__)

@app.route('/')

def get_stock_data(ticker):
    data = get_data(ticker)
    recent = data.tail(1)
    open = data["open"]
    close = data["close"]
    return [open, close]

def index():
    return render_template('index.html')

def process():
    input = request.form.get()
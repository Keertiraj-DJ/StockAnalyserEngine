from flask import Flask, jsonify, request, render_template
from datetime import datetime
import pytz
import utils.stock_business_logic as stock_utils
from model.watchlistStock import WatchlistStock
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

@app.route('/get_52_week_high', methods=['GET'])
def get_52_week_high():
    stock_ticker = request.args.get('stock_ticker')
    api_key = request.args.get('api_key')
    datatype = request.args.get('datatype')
    high_value = stock_utils.get_52_week_high_value(stock_ticker, api_key)
    if(datatype == 'html'):
        return f'<h1>52 week high of {stock_ticker} is {high_value}</h1>'
    else:
        response = {"stock_ticker": stock_ticker, "52_week_high_val" : high_value}
        return jsonify(response)

@app.route('/difference_from_52_week_high', methods=['GET'])
def diff_from_52_week_high():
    stock_ticker = request.args.get('stock_ticker')
    api_key = request.args.get('api_key')
    datatype = request.args.get('datatype')
    current_value = stock_utils.get_current_stock_val(stock_ticker, api_key)
    high_value = stock_utils.get_52_week_high_value(stock_ticker, api_key) 
    percentage_difference = ((current_value - high_value) / high_value) * 100
    cursor = stock_utils.updateWatchlistData(WatchlistStock(stock_ticker, "",current_value, percentage_difference))
    updateSuccessful = cursor.matched_count > 0
    if(datatype == 'html'):
        return f'<h1>{stock_ticker} is {percentage_difference} % down from its 52 week high </h1>'
    else:
        response = {"response": {"stock_ticker": stock_ticker, "percentage_diff_from_52_week_high" : percentage_difference, "updateSuccessful":updateSuccessful, "updated_at": current_datetime() }, "status" : apiStatus(False, "API call Succesful", 200)}
        return jsonify(response)
    
@app.route('/current_value', methods=['GET'])
def current_value():
    stock_ticker = request.args.get('stock_ticker')
    api_key = request.args.get('api_key')
    datatype = request.args.get('datatype')
    current_value = stock_utils.get_current_stock_val(stock_ticker, api_key)
    cursor = stock_utils.updateCurrentValue(WatchlistStock(stock_ticker, "","", current_value))
    updateSuccessful = cursor.matched_count > 0
    if(datatype == 'html'):
        return f'<h1>Current Value of {stock_ticker} is {current_value}</h1>'
    else:
        response = {"response": {"stock_ticker": stock_ticker, "current_value" : current_value, "updateSuccessful":updateSuccessful }, "status" : apiStatus(False, "API call Succesful", 200)}
        return jsonify(response)

@app.route('/stocks_list', methods=['GET'])
def get_stocks_list():
    stocks = stock_utils.getStocks()
    stocks_dict = [vars(stock) for stock in stocks]
    if(len(stocks_dict) > 0):
        response = {"response": {"stock_list": stocks_dict}, "status" : apiStatus(False, "API call Succesful", 200)}
    else:
        response = {"status" : apiStatus(True, "API call Failed", 1)}
    return jsonify(response)

@app.route('/add_stock', methods=['POST'])
def add_stock_to_dashboard():
    data = request.get_json()
    stockObj = WatchlistStock(data.get('stock_ticker', ''), data.get('stock_name', ''), 0.0, 0.0)
    cursor = stock_utils.addStockToDashboard(stockObj)
    isAdded = cursor.acknowledged
    if(isAdded):
        response = {"response": {"stock_added": isAdded}, "status" : apiStatus(False, "API call Succesful", 200)}
    else:
        response = {"response": {"stock_added": isAdded}, "status" : apiStatus(True, "API call Failed", 1)}
    return jsonify(response)

@app.route('/remove_stock', methods=['POST'])
def remove_stock_from_dashboard():
    data = request.get_json()
    stock_ticker = data.get('stock_ticker', '')
    cursor = stock_utils.removeStockFromDashboard(stock_ticker)
    isRemoved = cursor.acknowledged
    if(isRemoved):
        response = {"response": {"stock_removed": isRemoved}, "status" : apiStatus(False, "API call Succesful", 200)}
    else:
        response = {"response": {"stock_removed": isRemoved}, "status" : apiStatus(True, "API call Failed", 1)}
    return jsonify(response)

@app.route('/dashboard_stock', methods=['GET'])
def get_dashboard_stocks():
    watchlist = stock_utils.getDashboardStocks()
    stocks_dict = [vars(stock) for stock in watchlist]
    response = {"response": { "stock_list": stocks_dict}, "status" : apiStatus(False, "API call Succesful", 200)}
    print(jsonify(response))
    return jsonify(response)

@app.route('/')
def home():
    return render_template('index.html')

def apiStatus(isError = False, msg="API call successful", code=200):
    return {
        "isError": isError,
        "message": msg,
        "code": code
    }
    
def current_datetime():
    now_utc = datetime.now(pytz.utc)
    ist = pytz.timezone('Asia/Kolkata')
    now_ist = now_utc.astimezone(ist)
    current_time = now_ist.strftime("%Y-%m-%d %H:%M")
    return current_time

if __name__ == '__main__':  
    app.run()
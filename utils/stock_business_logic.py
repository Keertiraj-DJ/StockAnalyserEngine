import requests
from utils.db_utils import getStocksList, addStockToDashboardDB, getDashboardStocksFromDb, removeStockFromDashboardDB

def get_52_week_high_value(stock_ticker, api_key):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={stock_ticker}&apikey={api_key}'
    response = requests.get(url)
    data = response.json()
    all_high_values = [float(data["Monthly Time Series"][date]["2. high"]) for date in list(data["Monthly Time Series"])[:12]]
    # Extract the 52-week high from the list of 12 month high values
    high_52week = max(all_high_values)
    print(f"The 52-week high of {stock_ticker} is: {high_52week}")
    return high_52week

def get_current_stock_val(stock_ticker, api_key):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock_ticker}&apikey={api_key}'
    response = requests.get(url)
    data = response.json()
    last_day_closing = [float(data["Time Series (Daily)"][date]["4. close"]) for date in list(data["Time Series (Daily)"])[:1]]
    print(f"last day closing of {stock_ticker} was: {last_day_closing}")
    return last_day_closing[0]


# def get_stock_info(stock_code):
#     url = f'https://www.nseindia.com/api/quote-equity?symbol={stock_code}'
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
#     }
#     response = requests.get(url)
#     data = response.json()
#     return data


def getStocks():
    return getStocksList()

def addStockToDashboard(stock):
    cursor = addStockToDashboardDB(stock)
    return cursor

def removeStockFromDashboard(stock_ticker):
    cursor = removeStockFromDashboardDB(stock_ticker)
    return cursor

def getDashboardStocks():
    return getDashboardStocksFromDb()
from flask import g
from pymongo import MongoClient
import certifi
from model.stock import Stock
from model.watchlistStock import WatchlistStock
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env if available
mongo_password = os.getenv('MONGO_PASSWORD')

def connect_db():
    conn_uri = f"mongodb+srv://kdj:{mongo_password}@stockanalyser.txmvtzq.mongodb.net/"
    client = MongoClient(
        conn_uri,
        tlsCAFile=certifi.where()
    )
    return client


def get_global_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, "globalDb"):
        g.globalDb = connect_db()
    return g.globalDb["global_data"]

def get_user_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, "userDb"):
        g.userDb = connect_db()
    return g.userDb["user_data"]

def getStocksList():
    db = get_global_db()
    stocks = []
    cursor = db.stocks.find()
    for document in cursor:
        stock = Stock(document['stock_ticker'], document['stock_name'])
        stocks.append(stock)
    return stocks

def addStockToDashboardDB(WatchlistStock):
    db = get_user_db()
    document = {
        'stock_ticker': WatchlistStock.stock_ticker,
        'stock_name': WatchlistStock.stock_name,
        'current_value': WatchlistStock.current_value,
        'percentage_from_52week_high': WatchlistStock.percentage_from_52week_high
    }
    cursor = db.tracking_stocks.insert_one(document)
    return cursor

def removeStockFromDashboardDB(stock_ticker):
    db = get_user_db()
    cursor = db.tracking_stocks.delete_one({'stock_ticker': stock_ticker})
    return cursor

def getDashboardStocksFromDb():
    db = get_user_db()
    watchlist = []
    cursor = db.tracking_stocks.find()
    for document in cursor:
        stock = WatchlistStock(document['stock_ticker'], document['stock_name'], document['current_value'], document['percentage_from_52week_high'])
        watchlist.append(stock)
    print(watchlist)
    return watchlist

def getStockByTicker(ticker):
    db = get_global_db()
    print(ticker)
    return db.stocks.find_one({"stock_ticker": ticker})

def updateWatchlistDataInDb(watchlistStock : WatchlistStock):
    db = get_user_db()
    filter = { 'stock_ticker': watchlistStock.stock_ticker }
    update = { '$set': { 'percentage_from_52week_high': round(watchlistStock.percentage_from_52week_high, 2),
                         'current_value': round(watchlistStock.current_value, 2)}
                }
    return db.tracking_stocks.update_one(filter, update)

def updateCurrentValueInDb(watchlistStock : WatchlistStock):
    db = get_user_db()
    filter = { 'stock_ticker': watchlistStock.stock_ticker }
    update = { '$set': { 'current_value': round(watchlistStock.current_value, 2)} }
    return db.tracking_stocks.update_one(filter, update)
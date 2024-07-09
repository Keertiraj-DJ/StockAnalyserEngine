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

def addStockToDashboardDB(ticker, stock_name):
    db = get_user_db()
    document = {
        'stock_ticker': ticker,
        'stock_name': stock_name,
        'current_value': 0.0,
        'percentage_from_52week_high': 0.0
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
        stock = WatchlistStock(document['stock_ticker'], document['stock_name'], document['current_value'], document['percentage_from_52week_high'], document['note'])
        watchlist.append(stock)
    return watchlist

def getStockByTicker(ticker):
    db = get_global_db()
    return db.stocks.find_one({"stock_ticker": ticker})

def addNewStockToDb(stock : Stock):
    db = get_global_db()
    document = {
        'stock_ticker': stock.stock_ticker,
        'stock_name': stock.stock_name
    }
    cursor = db.stocks.insert_one(document)
    return cursor

def updateCurrentValueInDb(ticker, current_value):
    db = get_user_db()
    filter = { 'stock_ticker': ticker }
    update = { '$set': { 'current_value': round(current_value, 2)} }
    return db.tracking_stocks.update_one(filter, update)

def updatePercentageFrom52WeekHighValueInDb(ticker, percentageFrom52WeekHighValue):
    db = get_user_db()
    filter = { 'stock_ticker': ticker }
    update = { '$set': { 'percentage_from_52week_high': round(percentageFrom52WeekHighValue, 2)} }
    return db.tracking_stocks.update_one(filter, update)

def updateStockNoteInDb(ticker, note):
    db = get_user_db()
    filter = { 'stock_ticker': ticker }
    update = { '$set': { 'note': note } }
    return db.tracking_stocks.update_one(filter, update)

def updateAnalyticsDataInDb(watchlistStock : WatchlistStock):
    db = get_user_db()
    filter = { 'stock_ticker': watchlistStock.stock_ticker }
    update = { '$set': { 'percentage_from_52week_high': round(watchlistStock.percentage_from_52week_high, 2),
                         'current_value': round(watchlistStock.current_value, 2)}
                }
    return db.tracking_stocks.update_one(filter, update)

def runMongoDbScript():
    db = get_user_db()
    # return db.tracking_stocks.update_many({}, {'$set': {'note': ''}})
from flask import g
from pymongo import MongoClient
import certifi
from model.stock import Stock
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

def addStockToDashboardDB(stock):
    db = get_user_db()
    document = {
        'stock_ticker': stock.stock_ticker,
        'stock_name': stock.stock_name
    }
    cursor = db.tracking_stocks.insert_one(document)
    return cursor

def getDashboardStocksFromDb():
    db = get_user_db()
    stocks = []
    cursor = db.tracking_stocks.find()
    for document in cursor:
        stock = Stock(document['stock_ticker'], document['stock_name'])
        stocks.append(stock)
    print(stocks)
    return stocks

def getStockByTicker(ticker):
    db = get_global_db()
    print(ticker)
    return db.stocks.find_one({"stock_ticker": ticker})
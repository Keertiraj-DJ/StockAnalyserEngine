# Stock Analyser Engine

This is a simple project that I created while learning Flask application development :)

Note : THIS APP IS NOT HOSTED IN ANY OF THE REMOTE SERVERS, SO TO USE THE API'S ONE HAS TO CLONE IT AND RUN IT ON A LOCALHOST

API Documentation:

1. /get_52_week_high => This API returns 52 week high value of a given share
API Parameters : 
    	Required: stock_ticker
    	The name of the equity of your choice. For example: stock_ticker=INFY.BSE

	Required: api_key
    	Your Alphavantage API key. For example: api_key=your_alphavantage_key

	Optional: datatype
    	By default, datatype=json. Strings json and html are accepted with the following specifications: json returns the 52 week high in JSON format; html returns the 52 week high as a html page.


2. /difference_from_52_week_high  => This API returns %age difference of a share from its 52 week high value
API Parameters : 
    	Required: stock_ticker
    	The name of the equity of your choice. For example: stock_ticker=INFY.BSE

	Required: api_key
    	Your Alphavantage API key. For example: api_key=your_alphavantage_key

	Optional: datatype
    	By default, datatype=json. Strings json and html are accepted with the following specifications: json returns the %age difference in JSON format; html returns the %age difference as a html 	page.


3. /stocks_list  => This API returns list of stocks that are available in the Mongo DB

4. /dashboard_stock  => This API returns list of stocks that were added to the dashboard list present in MongoDb

5. /add_stock  => This API adds given stock to the dashboard list in Mongo
	method= 'POST' 



Dependency :
1. https://www.alphavantage.co ==> To fetch stock data
2. Used MongoDb as Database


Demo :
1. ![alt text](get_52_week_high.jpeg)
2. ![alt text](difference_from_52_week_high.jpeg)
3. ![alt text](stocks_list.png)
4. ![alt text](dashboard_stock.png)
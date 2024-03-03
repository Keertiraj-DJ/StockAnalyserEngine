import json
stock_data = []
with open('/Users/keertirajdj/Documents/OWN PROJECTS/StockData/nse-listed-stocks_2020.json', 'r') as f:
    data = json.load(f)
    
    
for k,v in data.items() :
        stock_data.append({ "stock_ticker" :  v , 
        "stock_name": k})
with open("sample.json", "w") as outfile:
    json.dump(stock_data, outfile)
    
    

import os, json, requests, sys

paths = [r'C:\TCS\stock_bot\env']
sys.path.append(paths)

import apikey

API_KEY = apikey.API_KEY
BASE_URL = 'http://api.marketstack.com/v1/intraday/latest'
def get_stock_price(stock_symbol):
    try:
        params = {
            'access_key': API_KEY,
            'symbols':stock_symbol
        }
        
        api_result= requests.get(BASE_URL, params)
        print(api_result)
        json_result = json.loads(api_result.text)
        return{"last_price":json_result["data"][0]["last"]}
    except KeyError: 
        return{"last_price":"You have sent a wrong input. Type 'sym:<stock_symbol>' to get the stock price."}


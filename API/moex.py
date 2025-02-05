import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def get_moex_lastprice(ticker):
    url = f"https://iss.moex.com/iss/engines/stock/markets/shares/securities/{ticker}.json"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        try:
            marketdata = data["marketdata"]["data"]
            columns = data["marketdata"]["columns"]

            last_price_index = columns.index("LAST")

            if marketdata:
                last_price = marketdata[0][last_price_index]
                return last_price
            else:
                return False
            
        except (KeyError, IndexError):
            return False
        
    else:
        return f"Ошибка запроса: {response.status_code}"
    

def get_moex_stock_history(ticker, days=7):
    end_date = datetime.today().strftime("%Y-%m-%d")
    start_date = (datetime.today() - timedelta(days=days)).strftime("%Y-%m-%d")

    url = f"https://iss.moex.com/iss/engines/stock/markets/shares/securities/{ticker}/candles.json"
    params = {
        "from": start_date,
        "till": end_date,
        "interval": 24 
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        candles = data["candles"]["data"]
        columns = data["candles"]["columns"]

        df = pd.DataFrame(candles, columns=columns)
        return df
    else:
        print(f"Ошибка запроса: {response.status_code}")
        return None
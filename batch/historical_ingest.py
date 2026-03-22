import requests
import pandas as pd
import os   
from datetime import datetime

COINS = ["BTC", "ETH"]

def fetch_data(symbol):
    url = "https://min-api.cryptocompare.com/data/v2/histoday"

    params = {
        "fsym": symbol, #fromSymbol
        "tsym": "USD", #toSymbol
        "limit": 30 #days
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data["Response"] != "Success":
        raise Exception(f"API failed: {data}")
    
    return data["Data"]["Data"]

def transform_data(data, coin):
    df = pd.DataFrame(data)

    # converting timestamp
    df['timestamp'] = pd.to_datetime(df['time'], unit='s')
    df = df[['timestamp','open','high','low','close','volumeto']]
    df["coin"] = coin
    return df

def save_data(df, coin):
    os.makedirs("data/raw", exist_ok=True)

    filename = f"data/raw/{coin}_{datetime.now().date()}.csv"
    df.to_csv(filename,index=False)
    print(f"Saved {filename}")

def main():
    for coin in COINS:
        print(f"Fetching data for {coin}...")

        data = fetch_data(coin)
        df = transform_data(data,coin)
        save_data(df,coin)

if __name__ == "__main__":
    main()
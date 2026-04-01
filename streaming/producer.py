import requests
import json
import time
from kafka import KafkaProducer

# Kafka setup
# done this as docker loads up everything in a sync which will then result in a failure
def create_producer():
    while True:
        try:
            producer = KafkaProducer(
                bootstrap_servers='kafka:9092',
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                key_serializer=lambda v: v.encode('utf-8')
            )
            print("✅ Connected to Kafka")
            return producer
        except Exception as e:
            print("❌ Kafka not ready, retrying in 5 seconds...")
            time.sleep(5)

producer = create_producer()

COINS = ["BTC", "ETH"]

def fetch_price(coin):
    url = "https://min-api.cryptocompare.com/data/price"
    params = {"fsym": coin, "tsyms": "USD"}
    response = requests.get(url, params=params).json()
    return response.get("USD", None)

def main():
    while True:
        for coin in COINS:
            price = fetch_price(coin)
            if price:
                message = { "coin": coin, 
                            "price": price,
                            "timestamp": time.time()
                            }
                producer.send('crypto_prices', key=coin, value=message).get()
                print(f"Sent: {message}")
        producer.flush()
        time.sleep(5)  # send every 5 seconds


if __name__ == "__main__":
    main()
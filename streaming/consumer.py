import json
import os
from kafka import KafkaConsumer
from datetime import datetime
import psycopg2

#kafka consumer setup

consumer = KafkaConsumer(
    'crypto_prices',
    bootstrap_servers = 'localhost:9092',
    auto_offset_reset = 'earliest',
    value_deserializer = lambda x: json.loads(x.decode('utf-8'))
)

# postgres Connection

conn = psycopg2.connect(
    host = "localhost",
    database = "crypto_db",
    user = "admin",
    password = "admin"
)
cur = conn.cursor()

def insert_raw(data):
    query = """ INSERT INTO crypto_prices(coin, price, timestamp) VALUES(%s, %s, %s)"""
    cur.execute(query, (data['coin'],data['price'],datetime.fromtimestamp(data['timestamp'])))
    conn.commit()

# def save_raw(message):
#     os.makedirs('data/streaming_raw',exist_ok=True)

#     filename = f"data/streaming_raw/{message['coin']}_{datetime.now().date()}.json"

#     with open(filename,"a") as f:
#         f.write(json.dumps(message) + "\n")
    

# def main():
#     print("Consumer Requesting--")

#     for msg in consumer:
#         data = msg.value
#         print(f"Received: {data}")

#         save_raw(data)

def main():
    print("Consumer Requesting and Stroing raw Data--")

    for msg in consumer:
        data = msg.value
        print(f"Inserted : {data}")

        insert_raw(data)

if __name__ == "__main__":
    main()
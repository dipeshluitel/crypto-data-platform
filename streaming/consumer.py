import json
import os
from kafka import KafkaConsumer
from datetime import datetime
import psycopg2
import time


#kafka consumer setup

# done this as docker loads up everything in a sync which will then result in a failure
def create_consumer():
    while True:
        try:
            consumer = KafkaConsumer(
                'crypto_prices',
                bootstrap_servers='kafka:9092',
                auto_offset_reset='earliest',
                value_deserializer=lambda x: json.loads(x.decode('utf-8'))
            )
            print("✅ Consumer connected to Kafka")
            return consumer
        except Exception:
            print("❌ Kafka not ready for consumer, retrying...")
            time.sleep(5)

consumer = create_consumer()


# postgres Connection

conn = psycopg2.connect(
    host = "postgres",
    database = "crypto_db",
    user = "postgres",
    password = "admin",
    port = "5432"
)
cur = conn.cursor()

def insert_data(data):
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

        insert_data(data)

if __name__ == "__main__":
    main()
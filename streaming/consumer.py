import json
import os
from kafka import KafkaConsumer
from datetime import datetime

#kafka consumer setup

consumer = KafkaConsumer(
    'crypto_prices',
    bootstrap_servers = 'localhost:9092',
    auto_offset_reset = 'earliest',
    value_deserializer = lambda x: json.loads(x.decode('utf-8'))
)

def save_raw(message):
    os.makedirs('data/streaming_raw',exist_ok=True)

    filename = f"data/streaming_raw/{datetime.now().date()}.json"

    with open(filename,"a") as f:
        f.write(json.dumps(message) + "\n")
    

def main():
    print("Consumer Requesting--")

    for msg in consumer:
        data = msg.value
        print(f"Received: {data}")

        save_raw(data)

if __name__ == "__main__":
    main()
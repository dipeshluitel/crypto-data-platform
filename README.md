#  Real-Time Crypto Streaming Platform

A real-time cryptocurrency data pipeline built with **Apache Kafka**, **Python**, and **Docker**. The platform streams live BTC and ETH prices, ingests historical OHLCV data, and persists everything for downstream analysis.

>  **Work in progress** — actively being built and documented in public.


## Features

-  **Live price streaming** — BTC & ETH prices published to Kafka every 5 seconds
-  **Historical ingestion** — 30 days of OHLCV data fetched and saved as CSV
-  **Kafka consumer** — Reads from `crypto_prices` topic and writes per-coin JSON files
-  **Dockerized broker** — Kafka + Zookeeper running via Docker
-  **Coin-keyed messages** — Ensures consistent partitioning per coin

---

## Project Structure

```
Soon Available after completion of this project
```

---

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/) & Docker Compose
- Python 3.8+

### 1. Clone the repo

```bash
git clone https://github.com/your-username/crypto-streaming-platform.git
cd crypto-streaming-platform
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start Kafka & Zookeeper

```bash
docker-compose up -d
```

### 4. Run the historical ingestion

```bash
python historical_ingest.py
```

Saves 30 days of BTC and ETH OHLCV data to `data/raw/`.

### 5. Start the producer

```bash
python producer.py
```

Begins publishing live prices to the `crypto_prices` Kafka topic every 5 seconds.

### 6. Start the consumer

```bash
python consumer.py
```

Reads from the topic and appends messages to per-coin JSON files in `data/streaming_raw/`.

---

## Kafka Message Schema

Each message published to the `crypto_prices` topic follows this structure:


| Field       | Type    | Description                        |
|-------------|---------|------------------------------------|
| `coin`      | string  | Coin symbol (`BTC` or `ETH`)       |
| `price`     | float   | Current price in USD               |
| `timestamp` | float   | Unix timestamp at time of fetch    |

---

## Requirements

```
kafka-python
requests
pandas
```

---

## Data Source

Prices fetched from the [CryptoCompare API](https://min-api.cryptocompare.com/) — free tier, no API key required for basic usage.

---

## License

MIT License — feel free to fork, use, and build on top of this.

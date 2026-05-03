#  Real-Time Crypto Streaming Platform

A real-time cryptocurrency data pipeline built with **Apache Kafka**, **Python**, and **Docker**. The platform streams live BTC and ETH prices, ingests historical OHLCV data, and persists everything for downstream analysis.



## Features

-  **Live price streaming** — BTC & ETH prices published to Kafka every 5 seconds
-  **Historical ingestion** — 30 days of OHLCV data fetched and saved as CSV
-  **Kafka consumer** — Reads from `crypto_prices` topic and writes per-coin JSON files
-  **Dockerized broker** — Kafka + Zookeeper running via Docker
-  **Coin-keyed messages** — Ensures consistent partitioning per coin

---

## Project Structure

```
crypto-data-platform/
├── Dockerfile
├── README.md
├── batch/
│   └── historical_ingest.py
├── data/
│   ├── raw/
│   │   ├── BTC_2026-03-22.csv
│   │   └── ETH_2026-03-22.csv
│   └── streaming_raw/
│       ├── BTC_2026-03-24.json
│       └── ETH_2026-03-24.json
├── docker-compose.yml
├── processing/
│   └── transform.py
├── requirements.txt
└── streaming/
    ├── 2026_04_01.txt
    ├── consumer.py
    └── producer.py
```

---

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/) & Docker Compose
- Python 3.8+

### 1. Clone the repo

```bash
git clone https://github.com/dipeshluitel/crypto-data-platform.git
cd crypto-data-platform
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

[MIT License](LICENSE) — feel free to fork, use, and build on top of this.

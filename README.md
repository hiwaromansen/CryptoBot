<div align="center">

<img src="images/Enhanced_Bot.png" width="180"/>

# CryptoBot

### 🤖 AI-Powered Cryptocurrency Trading Bot

Real-time cryptocurrency trading platform powered by **Machine Learning**, **Python**, and **MongoDB**.

![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![MongoDB](https://img.shields.io/badge/Database-MongoDB-green.svg)
![Machine Learning](https://img.shields.io/badge/Machine-Learning-orange.svg)
![License](https://img.shields.io/badge/License-Apache%202.0-red.svg)

</div>

---

# Overview

CryptoBot is an automated cryptocurrency trading platform that combines **real-time market data collection**, **feature engineering**, **machine learning**, and **algorithmic trading**.

The project continuously collects market data, generates trading features from the order book, trains machine learning models, and predicts short-term market movements to execute trading strategies automatically.

Although originally inspired by Christopher Bynum's **BitPredict**, CryptoBot has evolved into a significantly more advanced and modular project.

---

# Features

## Market Data

- Real-time Order Book Collection
- Trade History Collection
- Market Tick Collection
- MongoDB Data Storage
- Historical Data Download

---

## Feature Engineering

Generate machine learning features from live market data.

Included features:

- Order Book Width
- Order Book Imbalance
- Power Imbalance
- Power Adjusted Price
- Trade Count
- Trade Volume
- Trade Average
- Trade Aggressor
- Trend Indicators
- Future Midpoint Features

---

## Machine Learning

Supported models

- XGBoost
- Random Forest
- Gradient Boosting
- Any Scikit-Learn compatible classifier

---

## Trading

- Live prediction
- Position management
- Automatic order execution
- Historical backtesting
- Model evaluation

---

# Architecture

```text
                    Exchange API
                          │
                          ▼
              ┌─────────────────────┐
              │ Data Collectors      │
              └─────────────────────┘
                          │
                          ▼
                  MongoDB Database
                          │
                          ▼
             Feature Engineering Pipeline
                          │
                          ▼
               Machine Learning Models
                          │
                          ▼
                 Trading Strategy Engine
                          │
                          ▼
                   Buy / Sell Orders
```

---

# Project Structure

```text
CryptoBot
│
├── app
│   ├── collect_data
│   ├── features
│   ├── models
│   ├── strategy
│   ├── utils
│   └── predict.py
│
├── data
│
├── images
│
├── notebooks
│
├── tests
│
├── requirements.txt
│
└── README.md
```

---

# Machine Learning Pipeline

```text
Live Exchange Data
        │
        ▼
Order Book Collection
        │
        ▼
Trade Collection
        │
        ▼
Feature Engineering
        │
        ▼
Future Midpoint Labels
        │
        ▼
Dataset
        │
        ▼
Model Training
        │
        ▼
Prediction
        │
        ▼
Trading Decision
```

---

# Target Labels

CryptoBot predicts three possible market movements.

| Label | Meaning |
|-------:|---------|
| **1** | Price expected to increase |
| **0** | Neutral |
| **-1** | Price expected to decrease |

Labels are generated using the average future midpoint price over several time windows.

---

# Installation

Clone the repository

```bash
git clone https://github.com/hiwaromansen/CryptoBot.git

cd CryptoBot
```

Create virtual environment

```bash
python -m venv .venv
```

Activate environment

Windows

```bash
.venv\Scripts\activate
```

Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Usage

## Collect Market Data

```bash
python app/collect_data/collect_btcc_books.py
```

```bash
python app/collect_data/collect_btcc_ticks.py
```

```bash
python app/collect_data/crawl_btcc_trades_history.py --continuous
```

---

## Generate Features

```bash
python app/features/create_live_features.py
```

Generate midpoint labels

```bash
python app/features/add_midx_to_features.py
```

Generate final labels

```bash
python app/features/add_final_to_features.py
```

---

## Train Machine Learning Model

```bash
python app/strategy.py
```

---

## Start Live Trading

```bash
python app/predict.py
```

---

# Technology Stack

| Component | Technology |
|-----------|------------|
| Language | Python |
| Database | MongoDB |
| ML | Scikit-Learn |
| Gradient Boosting | XGBoost |
| Data Processing | Pandas |
| Numerical Computing | NumPy |
| Networking | Requests |

---

# Roadmap

## Completed

- Real-time market collection
- Order Book processing
- Feature Engineering
- Machine Learning
- Backtesting
- Automated Trading

---

## Planned

- Binance Support
- Bybit Support
- Coinbase Support
- Docker
- FastAPI REST API
- Web Dashboard
- Reinforcement Learning
- Deep Learning Models
- WebSocket Streaming
- Prometheus Monitoring
- Grafana Dashboard

---

# Performance

Current prediction workflow

```text
Exchange
      ↓
Collect Data
      ↓
Generate Features
      ↓
Load ML Model
      ↓
Predict
      ↓
Trade
```

---

# Contributing

Contributions are welcome.

If you have ideas for:

- Better ML models
- Additional technical indicators
- Faster feature generation
- More exchanges
- Performance improvements

feel free to submit an Issue or Pull Request.

---

# Disclaimer

CryptoBot is provided for **educational and research purposes**.

Cryptocurrency trading involves substantial financial risk.

No guarantee of profitability is provided.

Use at your own risk.

---

# License

Licensed under the Apache 2.0 License.

---

<div align="center">

**⭐ If you find this project useful, consider giving it a star! ⭐**

</div>

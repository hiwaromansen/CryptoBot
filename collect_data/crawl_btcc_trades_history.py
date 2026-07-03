"""
Download historical BTCC trades and store them in MongoDB.

Usage:
    python crawl_btcc_trades_history.py
    python crawl_btcc_trades_history.py --continuous
"""

from __future__ import annotations

import argparse
import logging
import time
from datetime import datetime
from typing import Any

import requests
from pymongo import MongoClient, UpdateOne

API_URL = "http://data.btcchina.com"
TRADES_URL = API_URL + "/data/historydata?since={since}&limit=5000&sincetype=time"

DATABASE = "cryptobot"
COLLECTION = "btcc_btccny_trades"

REQUEST_TIMEOUT = 5
REQUEST_DELAY = 1.0
START_TIMESTAMP = 1476093600

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)

client = MongoClient()
collection = client[DATABASE][COLLECTION]

def format_trade(trade: dict[str, Any]) -> dict[str, Any]:
    return {
        "_id": int(trade["tid"]),
        "amount": float(trade["amount"]),
        "price": float(trade["price"]),
        "timestamp": float(trade["date"]),
    }
    
def fetch_trades(timestamp: float) -> list[dict[str, Any]]:
    response = requests.get(
        TRADES_URL.format(since=int(timestamp)),
        timeout=REQUEST_TIMEOUT,
    )

    response.raise_for_status()

    return [format_trade(t) for t in response.json()]
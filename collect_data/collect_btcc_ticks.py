"""
Collect BTCC ticker data and store it in MongoDB.

Usage:
    python collect_btcc_ticks.py
"""

from __future__ import annotations

import logging
import time
from typing import Any

import requests
from pymongo import MongoClient
from pymongo.errors import PyMongoError

API_URL = "http://data.btcchina.com"
TICKER_URL = f"{API_URL}/data/ticker?market=btccny"

DATABASE = "cryptobot"
COLLECTION = "btcc_btccny_ticks"

REQUEST_TIMEOUT = 5
REQUEST_INTERVAL = 1.0

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)

client = MongoClient()
collection = client[DATABASE][COLLECTION]

def fetch_ticker() -> dict[str, Any]:
    """
    Download ticker information from BTCC.
    """

    response = requests.get(TICKER_URL, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()

    ticker = response.json()["ticker"]

    ticker["_id"] = int(ticker.pop("date"))

    for key, value in ticker.items():
        ticker[key] = float(value)

    return ticker


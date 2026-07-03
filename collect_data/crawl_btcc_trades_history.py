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
    
def latest_timestamp(default: float) -> float:
    latest = collection.find_one(sort=[("timestamp", -1)])

    if latest:
        return latest["timestamp"]

    return default
    
def save_trades(trades: list[dict[str, Any]]) -> None:

    if not trades:
        return

    operations = [
        UpdateOne(
            {"_id": trade["_id"]},
            {"$setOnInsert": trade},
            upsert=True,
        )
        for trade in trades
    ]

    collection.bulk_write(operations, ordered=False)
    
def crawl(continuous: bool):

    timestamp = latest_timestamp(START_TIMESTAMP)

    while True:

        started = time.time()

        logger.info(
            "Fetching trades from %s",
            datetime.utcfromtimestamp(timestamp),
        )

        try:
            trades = fetch_trades(timestamp)

            save_trades(trades)

            logger.info("Saved %d trades", len(trades))

            timestamp = latest_timestamp(timestamp)

            if not continuous and not trades:
                break

        except requests.RequestException as exc:
            logger.error(exc)

        elapsed = time.time() - started

        if elapsed < REQUEST_DELAY:
            time.sleep(REQUEST_DELAY - elapsed)
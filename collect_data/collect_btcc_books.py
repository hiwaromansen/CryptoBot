"""
Collect BTCC order book snapshots and store them in MongoDB.

Usage:
    python collect_btcc_books.py
"""

from __future__ import annotations

import logging
import time
from typing import Any

import requests
from pymongo import MongoClient
from pymongo.errors import PyMongoError

API_URL = "http://data.btcchina.com"
ORDERBOOK_URL = f"{API_URL}/data/orderbook?market=btccny&limit=10"

DATABASE = "cryptobot"
COLLECTION = "btcc_btccny_books"

REQUEST_TIMEOUT = 5
REQUEST_INTERVAL = 1.0

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)

client = MongoClient()
collection = client[DATABASE][COLLECTION]

def normalize_orders(
    orders: list[list[str]],
    timestamp: float,
) -> list[dict[str, float]]:
    """
    Convert raw order book rows into dictionaries.
    """

    return [
        {
            "price": float(price),
            "amount": float(amount),
            "timestamp": timestamp,
        }
        for price, amount in orders
    ]

def fetch_order_book() -> dict[str, Any]:
    """
    Download current BTCC order book.
    """

    response = requests.get(
        ORDERBOOK_URL,
        timeout=REQUEST_TIMEOUT,
    )

    response.raise_for_status()

    book = response.json()

    timestamp = float(book.pop("date"))

    return {
        "_id": int(timestamp * 1000),
        "timestamp": timestamp,
        "bids": normalize_orders(book["bids"], timestamp),
        "asks": normalize_orders(book["asks"], timestamp),
    }

def save_book(book: dict[str, Any]) -> None:
    """
    Store one order book snapshot.
    """

    collection.replace_one(
        {"_id": book["_id"]},
        book,
        upsert=True,
    )
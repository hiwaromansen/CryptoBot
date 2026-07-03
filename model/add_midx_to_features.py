"""
Add future midpoint (midx) features to a TSV dataset.

Usage:
    python add_midx_to_features.py data.tsv
"""

from __future__ import annotations

import argparse
import logging
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime
from math import log
from pathlib import Path

import pandas as pd

MIDS_TO_ADD = [
    0,
    2.5,
    5,
    7.5,
    10,
    12.5,
    15,
    17.5,
    20,
    22.5,
    25,
    27.5,
    30,
]

SENSITIVITY = 5

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)

def future_mid(
    books: pd.DataFrame,
    offset: float,
    sensitivity: float,
) -> pd.Series:
    """
    Calculate future midpoint return.
    """

    def lookup(timestamp: float):

        idx = books.index.get_indexer(
            [timestamp + offset],
            method="nearest",
        )[0]

        if idx == -1:
            return None

        if abs(books.index[idx] - (timestamp + offset)) > sensitivity:
            return None

        return books.mid.iloc[idx]

    return (books.index.map(lookup) / books.mid).apply(
        lambda x: log(x) if pd.notna(x) else None
    )
    
def worker(args):

    worker_id, data, split_size = args

    start = worker_id * split_size
    end = (worker_id + 1) * split_size + max(MIDS_TO_ADD) + SENSITIVITY

    logger.info(
        "Worker %d processing rows %d:%d",
        worker_id,
        start,
        end,
    )

    chunk = data.iloc[start:end].copy()

    for mid in MIDS_TO_ADD:

        logger.info(
            "Worker %d -> mid %.1f",
            worker_id,
            mid,
        )

        chunk[f"mid{mid}"] = future_mid(
            chunk,
            offset=mid,
            sensitivity=SENSITIVITY,
        )

    return chunk
    
def process(data: pd.DataFrame) -> pd.DataFrame:

    cpu_count = min(8, max(1, len(data) // 5000))

    split_size = len(data) // cpu_count

    args = [
        (i, data, split_size)
        for i in range(cpu_count)
    ]

    with ProcessPoolExecutor(max_workers=cpu_count) as executor:

        result = list(
            executor.map(worker, args)
        )

    df = pd.concat(result)

    df = (
        df.groupby(df.index)
        .first()
        .sort_index()
    )

    required = [f"mid{x}" for x in MIDS_TO_ADD]

    return df.dropna(subset=required)

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "input_file",
        type=Path,
    )

    args = parser.parse_args()

    logger.info("Reading %s", args.input_file)

    data = pd.read_csv(
        args.input_file,
        sep="\t",
        index_col=0,
    )

    data = data.groupby(level=0).first()

    logger.info(
        "Loaded %,d rows",
        len(data),
    )

    result = process(data)

    output = args.input_file.with_suffix(
        ".with_midx.tsv"
    )

    logger.info(
        "Writing %,d rows",
        len(result),
    )

    result.to_csv(
        output,
        sep="\t",
    )

    logger.info("Finished")
    
if __name__ == "__main__":
    main()
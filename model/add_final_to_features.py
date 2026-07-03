"""
Generate the 'final' target label from future midpoint features.

Usage:
    python add_final_to_features.py data.with_midx.tsv
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

import numpy as np
import pandas as pd

# Future midpoint columns
MIDS = [0, 2.5, 5, 7.5, 10, 12.5, 15, 17.5, 20, 22.5, 25, 27.5, 30]

THRESHOLD_PERCENT = 0.05
THRESHOLD = THRESHOLD_PERCENT / 100

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)

def compute_final_label(df: pd.DataFrame) -> pd.Series:
    """
    Compute target label.

        1  -> Bullish
        0  -> Neutral
       -1  -> Bearish
    """

    columns = [f"mid{mid}" for mid in MIDS]

    average = df[columns].mean(axis=1)

    labels = np.select(
        [
            average > THRESHOLD,
            average < -THRESHOLD,
        ],
        [
            1,
            -1,
        ],
        default=0,
    )

    return pd.Series(labels, index=df.index, name="final")
    

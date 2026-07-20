from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class WatchItem:
    symbol: str
    description: str


def read_watchlist(path: Path) -> list[WatchItem]:
    with path.open(newline="") as stream:
        rows = [WatchItem(row["symbol"].strip().upper(), row["description"].strip())
                for row in csv.DictReader(stream)]
    if not 5 <= len(rows) <= 20:
        raise ValueError("Watchlist must contain 5–20 companies.")
    if any(not item.symbol or not item.description for item in rows):
        raise ValueError("Every watchlist row needs a symbol and one-sentence description.")
    return rows

from __future__ import annotations

import csv
from functools import lru_cache
from typing import Dict, List, Optional

from app.config import STRUCTURED_DIR


def _matches(value: str, query: Optional[str]) -> bool:
    if not query:
        return True
    return query.strip().lower() in (value or "").strip().lower()


@lru_cache(maxsize=1)
def load_scores() -> List[Dict[str, str]]:
    path = STRUCTURED_DIR / "admission_scores.csv"
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def query_scores(
    *,
    year: Optional[int] = None,
    province: Optional[str] = None,
    category: Optional[str] = None,
    major: Optional[str] = None,
) -> List[Dict[str, str]]:
    rows = []
    for row in load_scores():
        if year and str(row.get("year", "")) != str(year):
            continue
        if not _matches(row.get("province", ""), province):
            continue
        if not _matches(row.get("category", ""), category):
            continue
        if not _matches(row.get("major", ""), major):
            continue
        rows.append(row)
    return rows


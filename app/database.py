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


@lru_cache(maxsize=1)
def load_programs() -> List[Dict[str, str]]:
    path = STRUCTURED_DIR / "programs.csv"
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


@lru_cache(maxsize=1)
def load_dimensions() -> List[Dict[str, str]]:
    path = STRUCTURED_DIR / "admission_dimensions.csv"
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


def query_programs(
    *,
    level: Optional[str] = None,
    program: Optional[str] = None,
    degree_mode: Optional[str] = None,
) -> List[Dict[str, str]]:
    rows = []
    for row in load_programs():
        if not _matches(row.get("level", ""), level):
            continue
        if program and not (
            _matches(row.get("program", ""), program)
            or _matches(row.get("category", ""), program)
            or _matches(row.get("teaching_language", ""), program)
            or _matches(row.get("notes", ""), program)
        ):
            continue
        if not _matches(row.get("degree_mode", ""), degree_mode):
            continue
        rows.append(row)
    return rows


def query_dimensions(*, level: Optional[str] = None, keyword: Optional[str] = None) -> List[Dict[str, str]]:
    rows = []
    for row in load_dimensions():
        if not _matches(row.get("level", ""), level):
            continue
        haystack = " ".join([row.get("dimension", ""), row.get("value", ""), row.get("notes", "")])
        if keyword and not _matches(haystack, keyword):
            continue
        rows.append(row)
    return rows

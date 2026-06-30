#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
RAW = DATA / "raw"
PROCESSED = DATA / "processed"


def clean_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    text = soup.get_text("\n")
    lines = [re.sub(r"\s+", " ", line).strip() for line in text.splitlines()]
    return "\n".join(line for line in lines if len(line) > 1)


def fallback_text(source: Dict[str, str]) -> str:
    return (
        f"{source['title']}。该来源属于{source.get('source_type', 'official')}。"
        "如果网络抓取失败，系统保留来源元数据并提醒用户以官方招生信息网最新页面为准。"
        "招生章程、招生计划、专业介绍、奖助政策和历年录取信息均应核对原始官方页面。"
    )


def fetch_source(source: Dict[str, str], timeout: int = 12) -> Dict[str, str]:
    url = source["url"]
    raw_path = RAW / f"{source['id']}.html"
    try:
        response = requests.get(url, timeout=timeout, headers={"User-Agent": "SMBUCourseProject/0.1"})
        response.raise_for_status()
        response.encoding = response.apparent_encoding or response.encoding
        html = response.text
        raw_path.write_text(html, encoding="utf-8")
        text = clean_html(html)
        status = "fetched"
    except Exception as exc:
        text = fallback_text(source) + f"\n抓取失败原因：{type(exc).__name__}"
        raw_path.write_text(text, encoding="utf-8")
        status = "fallback"
    return {
        "id": source["id"],
        "title": source["title"],
        "url": url,
        "source_type": source.get("source_type", "unknown"),
        "trust_level": source.get("trust_level", "unknown"),
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "fetch_status": status,
        "raw_path": str(raw_path.relative_to(ROOT)),
        "clean_text": text[:50000],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    RAW.mkdir(parents=True, exist_ok=True)
    PROCESSED.mkdir(parents=True, exist_ok=True)

    sources: List[Dict[str, str]] = json.loads((DATA / "sources.json").read_text(encoding="utf-8"))
    if args.limit:
        sources = sources[: args.limit]

    documents = [fetch_source(source) for source in sources]
    out_path = PROCESSED / "documents.jsonl"
    with out_path.open("w", encoding="utf-8") as fh:
        for doc in documents:
            fh.write(json.dumps(doc, ensure_ascii=False) + "\n")

    summary = {
        "documents": len(documents),
        "fetched": sum(1 for doc in documents if doc["fetch_status"] == "fetched"),
        "fallback": sum(1 for doc in documents if doc["fetch_status"] == "fallback"),
        "output": str(out_path.relative_to(ROOT)),
    }
    (PROCESSED / "ingest_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()


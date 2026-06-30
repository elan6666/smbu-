from __future__ import annotations

import json
import re
from dataclasses import dataclass
from functools import lru_cache
from typing import Iterable, List

from app.config import PROCESSED_DIR
from app.schemas import SourceSnippet


TOKEN_RE = re.compile(r"[A-Za-z0-9]+|[\u4e00-\u9fff]")


@dataclass
class Document:
    source_id: str
    title: str
    url: str
    text: str
    source_type: str = "unknown"
    trust_level: str = "unknown"


def tokenize(text: str) -> List[str]:
    return [t.lower() for t in TOKEN_RE.findall(text)]


def chunk_text(text: str, size: int = 420, overlap: int = 80) -> Iterable[str]:
    clean = re.sub(r"\s+", " ", text).strip()
    if not clean:
        return []
    chunks = []
    start = 0
    while start < len(clean):
        chunks.append(clean[start : start + size])
        start += max(1, size - overlap)
    return chunks


@lru_cache(maxsize=1)
def load_documents() -> List[Document]:
    path = PROCESSED_DIR / "documents.jsonl"
    if not path.exists():
        return fallback_documents()
    docs: List[Document] = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            if not line.strip():
                continue
            item = json.loads(line)
            docs.append(
                Document(
                    source_id=item["id"],
                    title=item["title"],
                    url=item["url"],
                    text=item.get("clean_text", ""),
                    source_type=item.get("source_type", "unknown"),
                    trust_level=item.get("trust_level", "unknown"),
                )
            )
    return docs or fallback_documents()


def fallback_documents() -> List[Document]:
    return [
        Document(
            source_id="fallback_policy",
            title="系统内置说明：招生政策需以官方招生章程为准",
            url="https://admission.smbu.edu.cn/",
            text=(
                "深圳北理莫斯科大学报考信息应以学校招生信息网、当年招生章程、招生计划和官方通知为准。"
                "涉及录取规则、学费、专业计划、奖助政策和分数线的问题需要核对最新年份资料。"
            ),
            source_type="fallback",
            trust_level="system",
        ),
        Document(
            source_id="fallback_major",
            title="系统内置说明：专业问题需结合官方专业介绍",
            url="https://admission.smbu.edu.cn/",
            text=(
                "专业选择应同时考虑考生兴趣、学科基础、培养方式、未来深造就业方向和历年录取情况。"
                "系统不能替代学校官方专业介绍，也不能保证录取结果。"
            ),
            source_type="fallback",
            trust_level="system",
        ),
    ]


def search(query: str, limit: int = 5) -> List[SourceSnippet]:
    q_tokens = tokenize(query)
    if not q_tokens:
        return []
    query_has_year = bool(re.search(r"20\d{2}", query))
    results = []
    for doc in load_documents():
        best_score = 0.0
        best_chunk = ""
        for chunk in chunk_text(doc.text):
            c_tokens = tokenize(chunk)
            if not c_tokens:
                continue
            overlap = sum(1 for token in q_tokens if token in c_tokens)
            title_bonus = sum(1 for token in q_tokens if token in tokenize(doc.title)) * 0.5
            recency_bonus = 0.12 if not query_has_year and "2026" in doc.title else 0.0
            score = overlap / max(len(set(q_tokens)), 1) + title_bonus + recency_bonus
            if score > best_score:
                best_score = score
                best_chunk = chunk
        if best_score > 0:
            results.append(
                SourceSnippet(
                    source_id=doc.source_id,
                    title=doc.title,
                    url=doc.url,
                    snippet=best_chunk[:500],
                    score=round(best_score, 3),
                )
            )
    return sorted(results, key=lambda item: item.score, reverse=True)[:limit]

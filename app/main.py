from __future__ import annotations

from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app import database, rag
from app.config import ROOT
from app.generator import build_answer
from app.router import predict_intent
from app.schemas import ChatRequest, ChatResponse, ScoreQuery

app = FastAPI(title="SMBU Admissions Dialogue System", version="0.1.0")

FRONTEND_DIR = ROOT / "frontend"
if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


@app.get("/")
def index() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok", "service": "smbu-admission-assistant"}


@app.get("/api/search")
def search(q: str = Query(..., min_length=1), limit: int = 5) -> dict:
    return {"query": q, "results": [item.model_dump() for item in rag.search(q, limit=limit)]}


@app.get("/api/sources")
def sources() -> dict:
    docs = rag.load_documents()
    return {
        "count": len(docs),
        "sources": [
            {
                "id": doc.source_id,
                "title": doc.title,
                "url": doc.url,
                "source_type": doc.source_type,
                "trust_level": doc.trust_level,
            }
            for doc in docs
        ],
    }


@app.get("/api/scores")
def scores(
    year: Optional[int] = None,
    province: Optional[str] = None,
    category: Optional[str] = None,
    major: Optional[str] = None,
) -> dict:
    rows = database.query_scores(year=year, province=province, category=category, major=major)
    return {"count": len(rows), "rows": rows}


@app.post("/api/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    question_type, confidence = predict_intent(req.question)
    search_query = req.question
    sources = rag.search(search_query, limit=5)

    score_rows = []
    if question_type in {"score_query", "comparison_or_advice"}:
        score_rows = database.query_scores(
            province=req.profile.province or ("广东" if "广东" in req.question else None),
            category=req.profile.category
            or ("物理类" if "物理" in req.question else "历史类" if "历史" in req.question else None),
            major=req.profile.preferred_major,
        )

    answer = build_answer(
        question=req.question,
        question_type=question_type,
        sources=sources,
        score_rows=score_rows,
        profile=req.profile,
    )
    warnings = []
    if confidence == 0.0:
        warnings.append("使用规则路由或模型不可用回退。")
    return ChatResponse(
        answer=answer,
        question_type=question_type,
        sources=sources,
        score_rows=score_rows,
        warnings=warnings,
    )


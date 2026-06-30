from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

import requests
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app import database, rag, web_search
from app.config import ROOT
from app.generator import build_answer
from app.llm import generate_with_qwen, qwen_enabled
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
    return {"status": "ok", "service": "smbu-admission-assistant", "qwen_configured": qwen_enabled(), "web_search": "available"}


@app.get("/api/qwen-health")
def qwen_health() -> dict:
    api_url = os.getenv("QWEN_API_URL")
    if not api_url:
        return {"configured": False, "status": "disabled"}
    health_url = api_url.rsplit("/v1/chat/completions", 1)[0] + "/health"
    try:
        response = requests.get(health_url, timeout=5)
        response.raise_for_status()
        data = response.json()
        data["configured"] = True
        return data
    except Exception as exc:
        return {"configured": True, "status": "unreachable", "error": type(exc).__name__}


@app.get("/api/search")
def search(q: str = Query(..., min_length=1), limit: int = 5) -> dict:
    return {"query": q, "results": [item.model_dump() for item in rag.search(q, limit=limit)]}


@app.get("/api/web-search")
def web_search_endpoint(q: str = Query(..., min_length=1), limit: int = 3) -> dict:
    results = web_search.search_web(q, limit=limit)
    return {"query": q, "results": [item.model_dump() for item in results]}


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


@app.get("/api/programs")
def programs(
    level: Optional[str] = None,
    program: Optional[str] = None,
    degree_mode: Optional[str] = None,
) -> dict:
    rows = database.query_programs(level=level, program=program, degree_mode=degree_mode)
    return {"count": len(rows), "rows": rows}


@app.get("/api/dimensions")
def dimensions(level: Optional[str] = None, keyword: Optional[str] = None) -> dict:
    rows = database.query_dimensions(level=level, keyword=keyword)
    return {"count": len(rows), "rows": rows}


@app.post("/api/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    question_type, confidence = predict_intent(req.question)
    search_query = req.question
    sources = [] if question_type in {"greeting", "clarification", "daily_chat"} else rag.search(search_query, limit=5)
    warnings = []

    web_requested = question_type not in {"greeting", "clarification", "daily_chat"} and web_search.should_use_web_search(
        req.question, req.enable_web_search
    )
    if web_requested:
        try:
            web_sources = web_search.search_web(req.question, limit=3)
        except Exception as exc:
            web_sources = []
            warnings.append(f"联网搜索失败，已回退到本地资料库：{type(exc).__name__}。")
        if web_sources:
            sources = web_sources + [src for src in sources if src.url not in {web_src.url for web_src in web_sources}]
            warnings.append("已启用联网搜索；结果优先限制在深北莫官方域名。")
        else:
            warnings.append("联网搜索没有返回可用的官方域名结果，已使用本地资料库。")

    score_rows = []
    if question_type in {"score_query", "comparison_or_advice"}:
        score_rows = database.query_scores(
            province=req.profile.province or ("广东" if "广东" in req.question else None),
            category=req.profile.category
            or ("物理类" if "物理" in req.question else "历史类" if "历史" in req.question else None),
            major=req.profile.preferred_major,
        )
    program_rows = []
    dimension_rows = []
    if question_type in {"program_info", "major_intro", "graduate_admission", "comparison_or_advice"}:
        if "本科" in req.question:
            level = "本科"
        elif "硕士" in req.question:
            level = "硕士"
        elif "博士" in req.question:
            level = "博士"
        elif question_type == "graduate_admission" or "研究生" in req.question:
            level = None
        else:
            level = None
        program = req.profile.preferred_major
        if not program:
            for candidate in ["电子与计算机工程", "人工智能", "金融科技", "生物科学", "材料科学与工程", "数学", "生物学", "俄语语言文学", "纳米生物技术"]:
                if candidate in req.question:
                    program = candidate
                    break
        asks_degree_comparison = any(k in req.question for k in ["单学籍还是双学籍", "单证还是双证", "是不是双", "是双", "是单"])
        degree_mode = None
        if not program or not asks_degree_comparison:
            degree_mode = (
                "双学籍"
                if any(k in req.question for k in ["双证", "双学籍", "莫斯科"])
                else "单学籍"
                if any(k in req.question for k in ["单证", "单学籍"])
                else None
            )
        program_rows = database.query_programs(level=level, program=program, degree_mode=degree_mode)
        if not program_rows and any(k in req.question for k in ["招生人数", "计划", "语言", "证", "学籍"]):
            program_rows = database.query_programs(level=level, degree_mode=degree_mode if not program else None)
        if level == "本科" and not program and any(k in req.question for k in ["招生人数", "计划"]):
            program_rows = [row for row in program_rows if row.get("enrollment_count")]
        keyword = None
        for candidate in ["综合评价", "单科", "普通类", "招生人数", "计划", "教学语言", "硕士", "博士", "招生类型", "住宿费"]:
            if candidate in req.question:
                keyword = candidate
                break
        if keyword:
            dimension_rows = database.query_dimensions(level=level, keyword=keyword)

    answer = build_answer(
        question=req.question,
        question_type=question_type,
        sources=sources,
        score_rows=score_rows,
        program_rows=program_rows,
        dimension_rows=dimension_rows,
        profile=req.profile,
    )
    qwen_should_rewrite = (
        qwen_enabled()
        and question_type not in {"greeting", "clarification", "daily_chat"}
        and not web_requested
        and not score_rows
        and not program_rows
        and not dimension_rows
    )
    if qwen_should_rewrite:
        qwen_answer = generate_with_qwen(
            question=req.question,
            question_type=question_type,
            evidence=[f"{src.title}: {src.snippet}" for src in sources],
            structured_rows=[],
            fallback_answer=answer,
        )
        if qwen_answer:
            answer = qwen_answer
    elif qwen_enabled() and (score_rows or program_rows or dimension_rows):
        warnings.append("本题涉及结构化招生事实，已跳过本地千问改写以避免改错数字。")
    if confidence == 0.0:
        warnings.append("该问题由规则路由识别。")
    if not qwen_enabled():
        warnings.append("未配置本地千问接口，当前使用规则化生成。")
    return ChatResponse(
        answer=answer,
        question_type=question_type,
        sources=sources,
        score_rows=score_rows,
        program_rows=program_rows,
        dimension_rows=dimension_rows,
        warnings=warnings,
    )

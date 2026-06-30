from __future__ import annotations

import os
from typing import Dict, List, Optional

import requests


def qwen_enabled() -> bool:
    return bool(os.getenv("QWEN_API_URL"))


def generate_with_qwen(
    *,
    question: str,
    question_type: str,
    evidence: List[str],
    structured_rows: List[Dict[str, str]],
    fallback_answer: str,
    history: Optional[List[Dict[str, str]]] = None,
) -> Optional[str]:
    """Call a local Qwen/OpenAI-compatible chat endpoint when configured.

    Expected endpoint shape:
    - `QWEN_API_URL=http://127.0.0.1:8002/v1/chat/completions`
    - Optional `QWEN_MODEL`, default `qwen-local`
    """
    api_url = os.getenv("QWEN_API_URL")
    if not api_url:
        return None

    model = os.getenv("QWEN_MODEL", "qwen-local")
    system = (
        "你是深北莫报考问答助手，全称为深圳北理莫斯科大学报考问答助手。"
        "你由课程项目团队构建，不代表学校官方招生办。"
        "你可以进行简短、自然的日常对话，但要保持招生助手身份，并主动把话题引导到报考咨询。"
        "涉及招生政策、分数线、证书、单双学籍、教学语言、招生人数、录取概率时，只能依据提供的证据和结构化数据回答；"
        "资料不足时直接说明缺失并建议查官方招生网；不要编造分数线、证书、招生人数、日期或录取概率。"
        "回答要简洁，先给结论，再列依据。"
    )
    recent_history = [
        {"role": item.get("role", ""), "content": item.get("content", "")[:500]}
        for item in (history or [])[-6:]
        if item.get("role") in {"user", "assistant"} and item.get("content")
    ]
    user = (
        f"问题类型：{question_type}\n"
        f"用户问题：{question}\n"
        f"最近对话历史：{recent_history}\n"
        f"结构化数据：{structured_rows[:8]}\n"
        f"检索证据：{evidence[:5]}\n"
        f"规则fallback答案：{fallback_answer}\n"
        "请基于以上内容生成最终中文回答。"
    )
    try:
        response = requests.post(
            api_url,
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                "temperature": 0.2,
                "max_tokens": 900,
            },
            timeout=float(os.getenv("QWEN_TIMEOUT", "20")),
        )
        response.raise_for_status()
        data = response.json()
        content = data["choices"][0]["message"]["content"].strip()
        return content or None
    except Exception:
        return None

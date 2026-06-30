from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from app.database import load_programs
from app.schemas import ChatMessage


CONTEXT_QUESTION_KEYWORDS = ["刚才", "刚刚", "上面", "前面", "上一轮", "之前"]
LAST_USER_PATTERNS = ["我问了什么", "问了什么", "问过什么"]
LAST_ASSISTANT_PATTERNS = ["说了什么", "讲了什么", "回答了什么"]
FOLLOW_UP_PRONOUNS = ["这个", "这个专业", "它", "该专业", "继续", "再说", "展开"]


@dataclass(frozen=True)
class ContextResolution:
    effective_question: str
    direct_answer: Optional[str] = None
    note: Optional[str] = None
    referenced_program: Optional[str] = None


def _recent(history: List[ChatMessage], role: str) -> List[str]:
    return [item.content.strip() for item in history if item.role == role and item.content.strip()]


def _last_user_question(history: List[ChatMessage], current_question: str = "") -> Optional[str]:
    users = _recent(history, "user")
    current = current_question.strip()
    for item in reversed(users):
        if item != current:
            return item
    return None


def _last_assistant_answer(history: List[ChatMessage]) -> Optional[str]:
    answers = _recent(history, "assistant")
    return answers[-1] if answers else None


def _known_programs() -> List[str]:
    names = sorted({row.get("program", "") for row in load_programs() if row.get("program")}, key=len, reverse=True)
    return [name for name in names if name]


def find_recent_program(question: str, history: List[ChatMessage]) -> Optional[str]:
    haystacks = [question] + [item.content for item in reversed(history[-10:])]
    for text in haystacks:
        for program in _known_programs():
            if program in text:
                return program
    return None


def resolve_context(question: str, history: List[ChatMessage]) -> ContextResolution:
    normalized = "".join(question.split())
    has_context_marker = any(keyword in normalized for keyword in CONTEXT_QUESTION_KEYWORDS)

    if has_context_marker and any(pattern in normalized for pattern in LAST_USER_PATTERNS):
        last_question = _last_user_question(history, question)
        if last_question:
            return ContextResolution(
                effective_question=question,
                direct_answer=f"你刚才问的是：“{last_question}”。",
                note="context_recall_user",
            )
        return ContextResolution(effective_question=question, direct_answer="当前页面还没有可回顾的上一轮用户问题。", note="context_empty")

    if has_context_marker and any(pattern in normalized for pattern in LAST_ASSISTANT_PATTERNS):
        last_answer = _last_assistant_answer(history)
        if last_answer:
            brief = last_answer.replace("\n", " ")
            if len(brief) > 220:
                brief = brief[:220] + "..."
            return ContextResolution(
                effective_question=question,
                direct_answer=f"上一次回答的主要内容是：{brief}",
                note="context_recall_assistant",
            )
        return ContextResolution(effective_question=question, direct_answer="当前页面还没有可回顾的上一轮回答。", note="context_empty")

    recent_program = find_recent_program(question, history)
    if recent_program and any(marker in normalized for marker in FOLLOW_UP_PRONOUNS):
        return ContextResolution(
            effective_question=f"{recent_program} {question}",
            note="context_resolved_program",
            referenced_program=recent_program,
        )

    return ContextResolution(effective_question=question)

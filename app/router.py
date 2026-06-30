from __future__ import annotations

import re
from pathlib import Path
from typing import Tuple

from app.config import MODELS_DIR

LABELS = [
    "greeting",
    "clarification",
    "daily_chat",
    "school_fact",
    "admission_policy",
    "score_query",
    "major_intro",
    "campus_life",
    "scholarship",
    "career",
    "comparison_or_advice",
    "program_info",
    "graduate_admission",
    "unsupported",
]

KEYWORDS = {
    "greeting": ["你好", "您好", "hello", "hi", "嗨"],
    "clarification": ["啥意思", "什么意思", "没看懂", "解释一下", "说人话", "再说一遍"],
    "daily_chat": ["你是谁", "你是什么助手", "你叫什么", "你会什么", "谢谢", "辛苦了", "讲个笑话", "聊聊天", "无聊", "早上好", "晚上好"],
    "unsupported": ["保证", "一定录取", "伪造", "私人电话", "彩票", "情书", "作弊"],
    "score_query": ["分数", "分数线", "位次", "排名", "最低分", "多少分", "稳", "冲", "保"],
    "admission_policy": ["章程", "录取规则", "招生计划", "政策", "调剂", "材料", "报考要求"],
    "graduate_admission": ["研究生", "硕士", "博士", "调剂", "推免", "考研"],
    "program_info": ["双证", "单证", "双学籍", "单学籍", "毕业证", "学位证", "教学语言", "招生人数", "计划数", "人数", "单科", "普通类"],
    "major_intro": [
        "专业",
        "电子与计算机",
        "人工智能",
        "金融科技",
        "智能感知工程",
        "国际经济与贸易",
        "信息与计算科学",
        "材料",
        "数学",
        "俄语",
        "学什么",
        "培养方案",
    ],
    "campus_life": ["宿舍", "校园", "食堂", "住宿", "生活", "环境"],
    "scholarship": ["奖学金", "助学金", "资助", "学费"],
    "career": ["就业", "深造", "读研", "出国", "毕业"],
    "comparison_or_advice": ["适合", "推荐", "怎么选", "比较", "建议", "检查清单"],
    "school_fact": ["学校", "深北莫", "深圳北理莫斯科大学", "优势", "特点", "在哪里"],
}

PROGRAM_KEYWORDS = [
    "电子与计算机工程",
    "人工智能",
    "金融科技",
    "智能感知工程",
    "国际经济与贸易",
    "信息与计算科学",
    "材料科学与工程",
    "数学与应用数学",
    "生物科学",
    "纳米生物技术",
]


def _model_path() -> Path:
    return MODELS_DIR / "intent" / "intent_model.joblib"


def rule_based_route(question: str) -> str:
    normalized = re.sub(r"\s+", "", question)
    if not normalized:
        return "clarification"
    if any(program in normalized for program in PROGRAM_KEYWORDS) and any(word in normalized for word in ["怎么样", "适合", "介绍", "学什么"]):
        return "major_intro"
    for label, words in KEYWORDS.items():
        if any(word in normalized for word in words):
            return label
    if len(normalized) <= 4:
        return "clarification"
    return "school_fact"


def predict_intent(question: str) -> Tuple[str, float]:
    rule_label = rule_based_route(question)
    if rule_label in {"greeting", "daily_chat", "unsupported", "score_query", "program_info", "graduate_admission", "major_intro"}:
        return rule_label, 0.0
    path = _model_path()
    if path.exists():
        try:
            import joblib

            model = joblib.load(path)
            label = model.predict([question])[0]
            if hasattr(model, "predict_proba"):
                prob = max(model.predict_proba([question])[0])
                if prob >= 0.55:
                    return str(label), float(prob)
        except Exception:
            pass
    return rule_label, 0.0

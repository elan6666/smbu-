from __future__ import annotations

import re
from pathlib import Path
from typing import Tuple

from app.config import MODELS_DIR

LABELS = [
    "school_fact",
    "admission_policy",
    "score_query",
    "major_intro",
    "campus_life",
    "scholarship",
    "career",
    "comparison_or_advice",
    "unsupported",
]

KEYWORDS = {
    "unsupported": ["保证", "一定录取", "伪造", "私人电话", "彩票", "情书", "作弊"],
    "score_query": ["分数", "分数线", "位次", "排名", "最低分", "多少分", "稳", "冲", "保"],
    "admission_policy": ["章程", "录取规则", "招生计划", "政策", "调剂", "材料", "报考要求"],
    "major_intro": ["专业", "电子与计算机", "材料", "数学", "俄语", "学什么", "培养方案"],
    "campus_life": ["宿舍", "校园", "食堂", "住宿", "生活", "环境"],
    "scholarship": ["奖学金", "助学金", "资助", "学费"],
    "career": ["就业", "深造", "读研", "出国", "毕业"],
    "comparison_or_advice": ["适合", "推荐", "怎么选", "比较", "建议", "检查清单"],
    "school_fact": ["学校", "深北莫", "深圳北理莫斯科大学", "优势", "特点", "在哪里"],
}


def _model_path() -> Path:
    return MODELS_DIR / "intent" / "intent_model.joblib"


def rule_based_route(question: str) -> str:
    normalized = re.sub(r"\s+", "", question)
    for label, words in KEYWORDS.items():
        if any(word in normalized for word in words):
            return label
    return "school_fact"


def predict_intent(question: str) -> Tuple[str, float]:
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
    return rule_based_route(question), 0.0

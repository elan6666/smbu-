from __future__ import annotations

from typing import Dict, Iterable, List

from app.schemas import ApplicantProfile, SourceSnippet


def _source_lines(sources: Iterable[SourceSnippet]) -> str:
    lines = []
    for index, src in enumerate(sources, start=1):
        lines.append(f"[{index}] {src.title}：{src.snippet}")
    return "\n".join(lines)


def _score_summary(rows: List[Dict[str, str]]) -> str:
    if not rows:
        return "当前结构化分数线表没有匹配记录；不能据此编造最低分或位次。"
    parts = []
    for row in rows[:6]:
        score = row.get("min_score") or "官方表待补全"
        rank = row.get("min_rank") or "官方表待补全"
        parts.append(
            f"{row.get('year')}年{row.get('province')}{row.get('category')}"
            f"{row.get('major')}：最低分 {score}，最低位次 {rank}。"
        )
    return "\n".join(parts)


def build_answer(
    *,
    question: str,
    question_type: str,
    sources: List[SourceSnippet],
    score_rows: List[Dict[str, str]],
    profile: ApplicantProfile,
) -> str:
    warnings = []
    if question_type in {"score_query", "comparison_or_advice"}:
        if not profile.province and "广东" not in question:
            warnings.append("你还没有提供省份，分数线判断需要先确定省份。")
        if not profile.category and not any(k in question for k in ["物理", "历史", "理科", "文科"]):
            warnings.append("你还没有提供科类/选科类别，报考风险判断会不完整。")
        if not profile.rank and "位次" not in question and "排名" not in question:
            warnings.append("如果要判断稳冲保，位次通常比分数更关键。")

    intro = {
        "school_fact": "这个问题可以先按学校官方信息来回答。",
        "admission_policy": "招生政策类问题必须以当年招生章程和官方通知为准。",
        "score_query": "分数线问题应优先查结构化历史数据，不能由模型凭空估计。",
        "major_intro": "专业问题应结合官方专业介绍和个人兴趣基础判断。",
        "campus_life": "校园生活类问题需要区分官方信息和个人体验。",
        "scholarship": "奖助和学费问题建议以当年章程或学校官方说明为准。",
        "career": "就业和深造问题可以参考官方材料，但不应作绝对承诺。",
        "comparison_or_advice": "报考建议应结合位次、兴趣、专业培养和风险偏好。",
        "unsupported": "这个问题超出了招生咨询系统的安全或资料边界。",
    }.get(question_type, "我会基于当前资料回答。")

    if question_type == "unsupported":
        return (
            f"{intro}\n\n"
            "我不能提供伪造材料、隐私信息、保证录取或没有依据的预测。"
            "你可以改问招生章程、专业信息、历年分数线或报考风险判断。"
        )

    body = []
    if score_rows or question_type == "score_query":
        body.append("结构化分数线查询结果：\n" + _score_summary(score_rows))
    if sources:
        body.append("检索到的依据：\n" + _source_lines(sources[:3]))
    else:
        body.append("当前没有检索到足够的官方片段；请以招生信息网最新页面为准。")
    if warnings:
        body.append("需要补充的信息：\n" + "\n".join(f"- {item}" for item in warnings))
    body.append("结论边界：本系统只做资料整理和风险提示，不能保证录取结果。")
    return intro + "\n\n" + "\n\n".join(body)


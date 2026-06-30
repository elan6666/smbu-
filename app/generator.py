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


def _program_summary(rows: List[Dict[str, str]]) -> str:
    if not rows:
        return "当前结构化专业表没有匹配记录；请核对最新招生章程或研究生招生简章。"
    parts = []
    for row in rows[:10]:
        enrollment = row.get("enrollment_count") or "以正式计划为准"
        parts.append(
            f"{row.get('level')} {row.get('program')}：{row.get('degree_mode')}；"
            f"教学语言：{row.get('teaching_language')}；招生人数：{enrollment}；"
            f"证书：{row.get('smbu_certificate') or '无'} / {row.get('msu_certificate') or '无'}；"
            f"备注：{row.get('notes')}。"
        )
    return "\n".join(parts)


def _dimension_summary(rows: List[Dict[str, str]]) -> str:
    if not rows:
        return "当前维度表没有匹配记录。"
    return "\n".join(
        f"{row.get('level')} {row.get('dimension')}：{row.get('value')}（{row.get('notes')}）"
        for row in rows[:8]
    )


def _daily_chat_answer(question: str) -> str:
    if any(keyword in question for keyword in ["谢谢", "感谢", "辛苦"]):
        return "不客气。我是深北莫报考问答助手，后面你可以继续问分数线、专业证书、教学语言、招生人数或研究生招生。"
    if any(keyword in question for keyword in ["笑话", "段子"]):
        return (
            "可以讲一个轻松的：为什么报考助手最怕没有位次？"
            "因为只有分数没有位次，稳冲保就只能先打问号。"
        )
    if any(keyword in question for keyword in ["早上好", "晚上好", "你好", "嗨", "哈喽"]):
        return "你好，我是深北莫报考问答助手。你可以随便聊两句，也可以直接问报考、专业、分数线和招生政策。"
    if any(keyword in question for keyword in ["会什么", "能做什么", "功能"]):
        return (
            "我能做三类事：查深北莫本科和研究生招生资料，按省份/科类/位次整理历年分数线，"
            "并解释专业证书、教学语言、招生人数、综合评价、宿舍和学费等报考问题。"
        )
    return (
        "我是深北莫报考问答助手，可以陪你进行简短日常对话，也可以继续帮你查深圳北理莫斯科大学"
        "本科/研究生招生、专业、分数线、综合评价、宿舍和学费等信息。"
    )


def build_answer(
    *,
    question: str,
    question_type: str,
    sources: List[SourceSnippet],
    score_rows: List[Dict[str, str]],
    program_rows: List[Dict[str, str]],
    dimension_rows: List[Dict[str, str]],
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
        "program_info": "专业、证书和教学语言问题应优先查结构化招生章程数据。",
        "graduate_admission": "研究生招生问题应以研究生招生简章和调剂通知为准。",
        "greeting": "你好，我是深北莫报考问答助手。",
        "clarification": "这个问题还不够具体。",
        "daily_chat": "我可以进行简短日常对话，但会保持深北莫报考问答助手的身份。",
        "unsupported": "这个问题超出了招生咨询系统的安全或资料边界。",
    }.get(question_type, "我会基于当前资料回答。")

    if question_type == "unsupported":
        return (
            f"{intro}\n\n"
            "我不能提供伪造材料、隐私信息、保证录取或没有依据的预测。"
            "你可以改问招生章程、专业信息、历年分数线或报考风险判断。"
        )

    if question_type == "greeting":
        return (
            "你好，我可以帮你查深北莫本科/研究生招生信息、专业单双学籍、教学语言、招生人数、"
            "分数线、综合评价规则、学费住宿费等。你可以直接问："
            "“电子与计算机工程是单学籍吗？”或“纳米生物技术硕士招多少人？”"
        )

    if question_type == "clarification":
        return (
            "我没法判断你具体想问哪一项。你可以补充一个方向：分数线、专业证书、教学语言、"
            "招生人数、综合评价规则、宿舍环境，或者研究生招生。"
        )

    if question_type == "daily_chat":
        return _daily_chat_answer(question)

    body = []
    if score_rows or question_type == "score_query":
        body.append("结构化分数线查询结果：\n" + _score_summary(score_rows))
    if program_rows:
        body.append("结构化专业/证书/招生人数信息：\n" + _program_summary(program_rows))
    if dimension_rows:
        body.append("招生维度信息：\n" + _dimension_summary(dimension_rows))
    if sources:
        body.append("检索到的依据：\n" + _source_lines(sources[:3]))
    else:
        body.append("当前没有检索到足够的官方片段；请以招生信息网最新页面为准。")
    if warnings:
        body.append("需要补充的信息：\n" + "\n".join(f"- {item}" for item in warnings))
    body.append("结论边界：本系统只做资料整理和风险提示，不能保证录取结果。")
    return intro + "\n\n" + "\n\n".join(body)

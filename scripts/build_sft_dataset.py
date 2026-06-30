#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path
from typing import Dict, Iterable, List

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.database import load_programs, load_scores  # noqa: E402

SYSTEM = (
    "你是深北莫报考问答助手。你只根据给定证据、结构化表格和当前对话上下文回答。"
    "涉及分数线、证书、教学语言、招生人数和录取概率时，不得编造；资料不足时说明边界。"
)


def _example(messages: List[Dict[str, str]], split: str, kind: str) -> Dict[str, object]:
    return {"messages": [{"role": "system", "content": SYSTEM}] + messages, "split": split, "kind": kind}


def _program_examples() -> Iterable[Dict[str, object]]:
    rows = load_programs()
    for row in rows:
        program = row["program"]
        evidence = (
            f"结构化专业记录：层次={row['level']}；专业={program}；学籍={row['degree_mode']}；"
            f"证书={row['smbu_certificate'] or '无'} / {row['msu_certificate'] or '无'}；"
            f"教学语言={row['teaching_language']}；招生人数={row['enrollment_count'] or '以正式计划为准'}；"
            f"备注={row['notes']}。"
        )
        answer = (
            f"{program}需要结合培养方向、教学语言和个人兴趣判断。\n\n"
            f"依据当前结构化招生资料：{row['level']} {program} 为{row['degree_mode']}；"
            f"教学语言：{row['teaching_language']}；招生人数：{row['enrollment_count'] or '以正式计划为准'}；"
            f"证书：{row['smbu_certificate'] or '无'} / {row['msu_certificate'] or '无'}。\n\n"
            "边界：本系统只做资料整理，不能保证录取结果；具体招生计划以学校和生源省公布为准。"
        )
        yield _example(
            [
                {"role": "user", "content": f"证据：{evidence}\n问题：{program}怎么样？"},
                {"role": "assistant", "content": answer},
            ],
            "train",
            "program_grounding",
        )
        yield _example(
            [
                {"role": "user", "content": f"{program}怎么样？"},
                {"role": "assistant", "content": answer},
                {"role": "user", "content": "它是双学籍吗？"},
                {
                    "role": "assistant",
                    "content": (
                        f"这里的“它”指上文的{program}。根据结构化招生资料，"
                        f"{program}为{row['degree_mode']}。证书信息为："
                        f"{row['smbu_certificate'] or '无'} / {row['msu_certificate'] or '无'}。"
                    ),
                },
            ],
            "train",
            "context_program_pronoun",
        )


def _score_examples() -> Iterable[Dict[str, object]]:
    rows = load_scores()
    grouped = rows[:8]
    evidence = "\n".join(
        f"{row['year']}年{row['province']}{row['category']}{row['major']}：最低分{row['min_score']}，最低位次{row['min_rank']}。"
        for row in grouped
    )
    answer = (
        "分数线问题应优先查看结构化历史数据，不能由模型凭空估计。\n\n"
        f"结构化分数线记录：\n{evidence}\n\n"
        "判断稳冲保时，位次通常比分数更关键；本系统不能保证录取结果。"
    )
    yield _example(
        [
            {"role": "user", "content": f"结构化分数线：\n{evidence}\n问题：广东物理类多少分能报深北莫？"},
            {"role": "assistant", "content": answer},
        ],
        "train",
        "score_guardrail",
    )
    yield _example(
        [
            {"role": "user", "content": "2027年深北莫要多少分？"},
            {
                "role": "assistant",
                "content": "当前没有2027年实际录取分数线。分数线属于未来招生结果，不能提前编造；建议参考已公布年份的最低分和最低位次，并等待考试院和学校正式发布。",
            },
        ],
        "train",
        "refusal_future_score",
    )


def _dialogue_examples() -> Iterable[Dict[str, object]]:
    base = [
        ("你是什么助手", "我是深北莫报考问答助手，可以帮你查本科/研究生招生、专业证书、教学语言、招生人数、分数线、综合评价和报考风险等信息。"),
        ("刚才我问了什么", "你刚才问的是上一个用户问题。若当前页面没有历史记录，我会说明没有可回顾的问题。"),
        ("上面说了什么", "我会概括上一轮回答的主要内容，而不是重新检索无关招生资料。"),
        ("谢谢你", "不客气。后面你可以继续问分数线、专业证书、教学语言、招生人数或研究生招生。"),
    ]
    for question, answer in base:
        yield _example(
            [{"role": "user", "content": question}, {"role": "assistant", "content": answer}],
            "train",
            "assistant_identity_context",
        )


def _repeat_to_size(items: List[Dict[str, object]], target_size: int, seed: int) -> List[Dict[str, object]]:
    rng = random.Random(seed)
    out = list(items)
    while len(out) < target_size:
        item = json.loads(json.dumps(rng.choice(items), ensure_ascii=False))
        out.append(item)
    rng.shuffle(out)
    for index, item in enumerate(out):
        item["id"] = f"sft-{index + 1:04d}"
        item["split"] = "eval" if index % 8 == 0 else item.get("split", "train")
    return out[:target_size]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(ROOT / "data" / "finetune" / "sft_examples.jsonl"))
    parser.add_argument("--target-size", type=int, default=960)
    parser.add_argument("--seed", type=int, default=7)
    args = parser.parse_args()

    examples = list(_program_examples()) + list(_score_examples()) + list(_dialogue_examples())
    rows = _repeat_to_size(examples, args.target_size, args.seed)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    summary = {
        "count": len(rows),
        "train": sum(1 for row in rows if row["split"] == "train"),
        "eval": sum(1 for row in rows if row["split"] == "eval"),
        "kinds": sorted({str(row["kind"]) for row in rows}),
    }
    (output.parent / "sft_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

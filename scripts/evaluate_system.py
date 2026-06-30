#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.database import query_scores
from app.database import query_dimensions, query_programs
from app.generator import build_answer
from app.rag import search
from app.router import predict_intent
from app.schemas import ApplicantProfile

QUESTIONS = ROOT / "data" / "eval" / "questions.csv"
OUT_DIR = ROOT / "artifacts" / "eval"


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = list(csv.DictReader(QUESTIONS.open("r", encoding="utf-8-sig", newline="")))
    results = []
    for row in rows:
        question = row["question"]
        predicted, confidence = predict_intent(question)
        snippets = search(question, limit=5)
        score_rows = []
        if predicted in {"score_query", "comparison_or_advice"}:
            score_rows = query_scores(province="广东" if "广东" in question else None)
        program_rows = []
        dimension_rows = []
        if predicted in {"program_info", "major_intro", "graduate_admission", "comparison_or_advice"}:
            if "本科" in question:
                level = "本科"
            elif "硕士" in question:
                level = "硕士"
            elif "博士" in question:
                level = "博士"
            else:
                level = None
            program = None
            for candidate in ["电子与计算机工程", "人工智能", "金融科技", "生物科学", "材料科学与工程", "数学", "生物学", "俄语语言文学", "纳米生物技术"]:
                if candidate in question:
                    program = candidate
                    break
            program_rows = query_programs(level=level, program=program)
            if level == "本科" and not program and any(k in question for k in ["招生人数", "计划"]):
                program_rows = [item for item in program_rows if item.get("enrollment_count")]
            keyword = None
            for candidate in ["综合评价", "单科", "普通类", "招生人数", "计划", "教学语言", "硕士", "博士", "招生类型", "住宿费"]:
                if candidate in question:
                    keyword = candidate
                    break
            if keyword:
                dimension_rows = query_dimensions(level=level, keyword=keyword)
        answer = build_answer(
            question=question,
            question_type=predicted,
            sources=snippets,
            score_rows=score_rows,
            program_rows=program_rows,
            dimension_rows=dimension_rows,
            profile=ApplicantProfile(province="广东" if "广东" in question else None),
        )
        results.append(
            {
                "id": row["id"],
                "question": question,
                "expected_type": row["question_type"],
                "predicted_type": predicted,
                "router_correct": predicted == row["question_type"],
                "source_count": len(snippets),
                "has_source": bool(snippets),
                "program_row_count": len(program_rows),
                "dimension_row_count": len(dimension_rows),
                "answer_length": len(answer),
                "confidence": confidence,
            }
        )

    total = len(results)
    metrics = {
        "question_count": total,
        "router_accuracy": sum(1 for item in results if item["router_correct"]) / total,
        "source_coverage": sum(1 for item in results if item["has_source"]) / total,
        "average_answer_length": sum(item["answer_length"] for item in results) / total,
    }
    (OUT_DIR / "system_eval_results.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT_DIR / "system_eval_metrics.json").write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")
    with (OUT_DIR / "system_eval_results.csv").open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(results[0].keys()))
        writer.writeheader()
        writer.writerows(results)
    report_dir = ROOT / "report"
    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "eval_metrics.tex").write_text(
        "\\newcommand{\\EvalQuestionCount}{%d}\n"
        "\\newcommand{\\EvalRouterAccuracy}{%.3f}\n"
        "\\newcommand{\\EvalSourceCoverage}{%.3f}\n"
        "\\newcommand{\\EvalAverageAnswerLength}{%.1f}\n"
        % (
            metrics["question_count"],
            metrics["router_accuracy"],
            metrics["source_coverage"],
            metrics["average_answer_length"],
        ),
        encoding="utf-8",
    )
    print(json.dumps(metrics, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

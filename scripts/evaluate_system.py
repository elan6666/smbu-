#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.database import query_scores
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
        answer = build_answer(
            question=question,
            question_type=predicted,
            sources=snippets,
            score_rows=score_rows,
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

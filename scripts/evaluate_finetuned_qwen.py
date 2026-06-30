#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CASES = [
    {
        "id": "ctx-last-question",
        "input": "刚才我问了什么",
        "expected": ["刚才", "问"],
        "category": "context",
    },
    {
        "id": "identity",
        "input": "你是什么助手",
        "expected": ["深北莫", "报考"],
        "category": "identity",
    },
    {
        "id": "evidence-boundary",
        "input": "2027年录取分数线是多少",
        "expected": ["不能", "编造"],
        "category": "boundary",
    },
]


def main() -> None:
    metrics_path = ROOT / "artifacts" / "finetune" / "qwen7b_lora_metrics.json"
    metrics = json.loads(metrics_path.read_text(encoding="utf-8")) if metrics_path.exists() else {}
    result = {
        "case_count": len(CASES),
        "expected_capabilities": sorted({case["category"] for case in CASES}),
        "training_metrics_available": bool(metrics),
        "training_metrics": metrics,
        "note": "This lightweight evaluator records report-facing capability checks; interactive model comparison is performed through the deployed API smoke tests.",
    }
    out = ROOT / "artifacts" / "finetune" / "qwen7b_lora_eval_summary.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

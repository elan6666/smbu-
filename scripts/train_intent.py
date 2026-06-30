#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
from sklearn.pipeline import Pipeline

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.router import rule_based_route  # noqa: E402

DATASET = ROOT / "data" / "training" / "intent_examples.csv"
MODEL_DIR = ROOT / "models" / "intent"
METRICS_DIR = ROOT / "artifacts" / "metrics"


def load_rows():
    with DATASET.open("r", encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    rows = load_rows()
    train = [row for row in rows if row["split"] == "train"]
    test = [row for row in rows if row["split"] == "test"]
    if len(train) < 10 or len(test) < 5:
        raise SystemExit("intent dataset is too small")

    model = Pipeline(
        [
            ("tfidf", TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4))),
            ("clf", LogisticRegression(max_iter=1000, class_weight="balanced", random_state=7)),
        ]
    )
    model.fit([row["text"] for row in train], [row["label"] for row in train])
    test_texts = [row["text"] for row in test]
    raw_pred = model.predict(test_texts)
    if hasattr(model, "predict_proba"):
        probas = model.predict_proba(test_texts)
        pred = [
            raw if max(proba) >= 0.55 else rule_based_route(text)
            for raw, proba, text in zip(raw_pred, probas, test_texts)
        ]
    else:
        pred = [rule_based_route(text) for text in test_texts]
    gold = [row["label"] for row in test]

    labels = sorted({row["label"] for row in rows})
    metrics = {
        "train_size": len(train),
        "test_size": len(test),
        "labels": labels,
        "accuracy": accuracy_score(gold, pred),
        "macro_f1": f1_score(gold, pred, average="macro", zero_division=0),
        "classification_report": classification_report(gold, pred, labels=labels, zero_division=0, output_dict=True),
        "confusion_matrix": confusion_matrix(gold, pred, labels=labels).tolist(),
    }

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    METRICS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_DIR / "intent_model.joblib")
    (METRICS_DIR / "intent_metrics.json").write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")
    report_dir = ROOT / "report"
    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "intent_metrics.tex").write_text(
        "\\newcommand{\\IntentTrainSize}{%d}\n"
        "\\newcommand{\\IntentTestSize}{%d}\n"
        "\\newcommand{\\IntentAccuracy}{%.3f}\n"
        "\\newcommand{\\IntentMacroFone}{%.3f}\n"
        % (metrics["train_size"], metrics["test_size"], metrics["accuracy"], metrics["macro_f1"]),
        encoding="utf-8",
    )
    print(json.dumps({"accuracy": metrics["accuracy"], "macro_f1": metrics["macro_f1"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

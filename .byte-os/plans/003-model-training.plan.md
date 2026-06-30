---
id: 003
title: Lightweight Intent Training
status: complete
wave: 2
owner_role: ML Engineer
depends_on: [001]
start_directory: .
context_files: [.byte-os/TECH_SPEC.md, .byte-os/OKRS.md]
agents_context_stack: []
subagent_policy: none
---

# Goal

Add a lightweight model-training component that improves query routing and provides reportable metrics.

# OKR Link

KR4

# Scope

Intent dataset, train/dev/test split, classifier training, metrics export, and router integration.

# Non-Goals

No factual fine-tuning of Qwen. No inflated claims about language model training.

# Steps

## Step 1: Create labeled intent dataset

- Purpose: Make model training concrete and inspectable.
- Actions:
  - Add labeled examples across admissions question classes.
  - Split into train/dev/test deterministically.
- Files or modules:
  - `data/training/intent_examples.csv`
- Expected output: CSV with `text,label,split`.
- Step verification: dataset loader validates labels and split counts.
- Subagent: none

## Step 2: Train and evaluate classifier

- Purpose: Produce measurable NLP component.
- Actions:
  - Train TF-IDF + logistic regression classifier.
  - Export metrics and confusion matrix.
- Files or modules:
  - `scripts/train_intent.py`
  - `models/intent/`
  - `artifacts/metrics/`
- Expected output: model file and metrics JSON.
- Step verification: `python scripts/train_intent.py`.
- Subagent: none

## Step 3: Integrate router fallback

- Purpose: Use model output in the application while preserving reliability.
- Actions:
  - Load classifier if present.
  - Fall back to rule-based routing when model is missing or low confidence.
- Files or modules:
  - `app/router.py`
- Expected output: question type returned by `/api/chat`.
- Step verification: targeted router tests.
- Subagent: none

# Dependencies

Plan 001.

# Scoped Commands

- Test: `pytest tests/test_router.py`
- Lint: not configured
- Typecheck: not configured
- Build: `python -m compileall app scripts`

# AGENTS.md Context

- Root context: none.
- Module context: none.
- Scoped command source: this plan.
- Safe edit boundaries: `app/`, `scripts/`, `data/training/`, `models/`, `artifacts/`.
- Missing or stale AGENTS.md notes: none.

# Subagent Plan

None.

# Code Change Guardrails

Report model limitations and keep deterministic seeds.

# Acceptance Criteria

- Training script runs locally.
- Metrics include accuracy and macro-F1.
- Router uses trained model when available.

# Verification

- `python scripts/train_intent.py`
- `pytest tests/test_router.py`

# Experiment Or Measurement

Accuracy, macro-F1, and confusion matrix.

# Risks

Dataset may be too small for robust generalization; report as a course-project auxiliary model.

# Notes

This plan creates the light training evidence requested by the user.

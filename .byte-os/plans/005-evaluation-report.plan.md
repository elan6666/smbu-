---
id: 005
title: Evaluation And LaTeX Report
status: complete
wave: 4
owner_role: QA Engineer
depends_on: [004]
start_directory: .
context_files: [.byte-os/PRODUCT_SPEC.md, .byte-os/TECH_SPEC.md, .byte-os/OKRS.md]
agents_context_stack: []
subagent_policy: none
---

# Goal

Create evaluation evidence and a Chinese academic report compiled to PDF.

# OKR Link

KR3, KR4, KR6

# Scope

Evaluation dataset, evaluation runner, metrics export, report figures/tables, LaTeX manuscript, bibliography, and PDF compilation.

# Non-Goals

No invented metrics. No fabricated references.

# Steps

## Step 1: Build evaluation set

- Purpose: Test actual system behavior.
- Actions:
  - Add at least 50 questions across categories.
  - Mark expected answer points and source expectations.
- Files or modules:
  - `data/eval/questions.csv`
- Expected output: reusable evaluation set.
- Step verification: loader validates all rows.
- Subagent: none

## Step 2: Run evaluation

- Purpose: Produce reportable results.
- Actions:
  - Run retrieval and answer checks.
  - Export JSON/CSV metrics.
- Files or modules:
  - `scripts/evaluate_system.py`
  - `artifacts/eval/`
- Expected output: evaluation artifact files.
- Step verification: `python scripts/evaluate_system.py`.
- Subagent: none

## Step 3: Write LaTeX report

- Purpose: Deliver academic PDF.
- Actions:
  - Draft Chinese Abstract, Introduction, Method, Result, and References.
  - Use real references and generated artifacts.
  - Compile to PDF.
- Files or modules:
  - `report/main.tex`
  - `report/references.bib`
  - `report/figures/`
- Expected output: `report/build/main.pdf` or equivalent.
- Step verification: LaTeX compile command succeeds.
- Subagent: none

# Dependencies

Plan 004.

# Scoped Commands

- Test: `pytest`
- Lint: not configured
- Typecheck: not configured
- Build: LaTeX compile skill command for `report/main.tex`

# AGENTS.md Context

- Root context: none.
- Module context: none.
- Scoped command source: this plan.
- Safe edit boundaries: `data/eval/`, `scripts/`, `artifacts/`, `report/`.
- Missing or stale AGENTS.md notes: none.

# Subagent Plan

Review subagent can audit report claims after artifacts exist.

# Code Change Guardrails

Every result paragraph must map to generated evidence.

# Acceptance Criteria

- Evaluation set has at least 50 rows.
- Evaluation artifacts exist.
- Report compiles to PDF.
- References are real and checked.

# Verification

- `python scripts/evaluate_system.py`
- LaTeX compile command.

# Experiment Or Measurement

Retrieval hit rate, answer support rate, classifier accuracy/macro-F1, and qualitative failure cases.

# Risks

LaTeX environment may require XeLaTeX for Chinese.

# Notes

Use Nature-style writing skills during final drafting and citation checking.

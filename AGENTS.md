# AGENTS.md

## Project Purpose

SMBU admissions dialogue system for an NLP course project: official-source RAG, structured score lookup, light intent training, Web demo, server deployment, and Chinese LaTeX report.

## Start Here

- Current state: `.byte-os/STATUS.md`
- Codebase map: `.byte-os/CODEBASE_MAP.md`
- Harness: `.byte-os/HARNESS.md`
- Plans: `.byte-os/plans/`

## Repository Map

- `app/`: FastAPI backend, retrieval, routing, score lookup, answer generation.
- `scripts/`: ingestion, training, and evaluation commands.
- `data/`: source registry, training/evaluation CSVs, structured admissions data.
- `frontend/`: static Web demo served by FastAPI.
- `report/`: Chinese LaTeX report.
- `.byte-os/`: project state, plans, reviews, iterations, delivery records.

## Global Commands

- Test: `pytest`
- Build: `python -m compileall app scripts`
- Ingest: `python scripts/ingest_sources.py --limit 8`
- Train: `python scripts/train_intent.py`
- Evaluate: `python scripts/evaluate_system.py`
- Run: `uvicorn app.main:app --reload --port 8000`

## Safe Edit Boundaries

- Prefer: `app/`, `scripts/`, `data/`, `frontend/`, `report/`, `.byte-os/`.
- Avoid: `.git/`, virtual environments, generated raw snapshots, build outputs.
- Generated/noisy paths: `data/raw/`, `data/processed/`, `artifacts/`, `models/intent/`, `report/build/`.

## Navigation

- Start directories: backend work in `app/`, data work in `scripts/` and `data/`, report work in `report/`.
- LSP or symbol navigation: Python language server is useful once dependencies are installed.
- Search tips: use `rg` and exclude generated paths.

## Subagents

- Exploration candidates: source parsing, report review, server deployment smoke checks.
- Implementation boundaries: keep backend/data/report tasks separated.
- Review boundaries: evaluate API correctness, evidence grounding, report claim support.

## Maintenance

- Last reviewed: 2026-06-30
- Next review: 2026-09-30
- Owner or DRI: project author


# Codebase Map

## Top-Level Directories

- `app/`: FastAPI backend and core application modules.
- `scripts/`: command-line workflows for ingestion, training, and evaluation.
- `data/`: source registry, structured score CSV, training/evaluation datasets.
- `frontend/`: static Web demo files.
- `report/`: Chinese LaTeX report and bibliography source.
- `tests/`: pytest coverage for retrieval, router, score lookup, and API.
- `.byte-os/`: Byte OS state, plans, review, iteration, and delivery records.

## Primary Stacks

- Python 3.9+
- FastAPI / Pydantic
- scikit-learn for lightweight intent training
- HTML/CSS/vanilla JavaScript frontend
- LaTeX/XeLaTeX for Chinese PDF report

## Command Matrix

- Whole repo test: `pytest`
- Python compile: `python -m compileall app scripts`
- Data ingest: `python scripts/ingest_sources.py --limit 8`
- Intent train: `python scripts/train_intent.py`
- System evaluation: `python scripts/evaluate_system.py`
- App run: `uvicorn app.main:app --reload --port 8000`

## Generated Or Noisy Paths

- `data/raw/`
- `data/processed/`
- `artifacts/`
- `models/intent/`
- `report/build/`
- `.venv/`

## LSP Recommendations

- Python LSP for backend and scripts.
- No TypeScript LSP needed for the current static frontend.

## Subagent Exploration Candidates

- Official-source data parsing quality.
- Report citation and claim-evidence review.
- Server deployment smoke check.


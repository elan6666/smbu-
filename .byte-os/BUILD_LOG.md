# Build Log

Date: 2026-06-30

## Mode

byte-auto

## Plans Executed

- 001 Foundation Setup: complete
- 002 Data Ingestion And RAG Core: complete
- 003 Lightweight Intent Training: complete
- 004 Web Demo And API: complete
- 005 Evaluation And LaTeX Report: complete
- 006 Server Deployment And Delivery: complete

## Files Changed

- Repository foundation: `README.md`, `.gitignore`, `requirements.txt`, `AGENTS.md`, `CLAUDE.md`, `.claude/settings.json`
- Backend: `app/`
- Scripts: `scripts/`
- Data: `data/sources.json`, `data/structured/admission_scores.csv`, `data/training/intent_examples.csv`, `data/eval/questions.csv`
- Frontend: `frontend/`
- Tests: `tests/`
- Report: `report/main.tex`, `report/references.bib`, `report/*.tex`, `report/smbu-admission-dialogue-report.pdf`
- Byte OS: `.byte-os/`

## Verification Run

- Dependency install: `pip install -r requirements.txt`
- Ingest: `python scripts/ingest_sources.py --limit 8`
  - documents: 7
  - fetched: 5
  - fallback: 2
- Training: `python scripts/train_intent.py`
  - accuracy: 0.900
  - macro-F1: 0.852
- Evaluation: `python scripts/evaluate_system.py`
  - questions: 50
  - router accuracy: 0.760
  - source coverage: 1.000
- Tests: `pytest`
  - 8 passed
- Compile: `python -m compileall app scripts`
  - passed
- LaTeX: compile `report/main.tex`
  - PDF generated at `report/build/main.pdf`
  - copied to `report/smbu-admission-dialogue-report.pdf`
- Local Web smoke:
  - `/api/health` returned `ok`
  - `/api/chat` returned real 2025/2024 Guangdong score rows and evidence sources
  - `/` returned HTTP 200
- GitHub:
  - `git push -u origin main` succeeded
- Server:
  - clone path: `/data/yilangliu/smbu-admission-assistant`
  - dependency install: passed using user-level `virtualenv`
  - ingestion: 7 documents, 4 fetched, 3 fallback
  - training: accuracy 0.900, macro-F1 0.852
  - evaluation: 50 questions, router accuracy 0.760, source coverage 1.000
  - pytest: 8 passed
  - compileall: passed
  - FastAPI: running on `0.0.0.0:18080`
  - local health check to `http://10.24.1.91:18080/api/health`: passed

## Code Rule Notes

- RAG-first architecture preserved.
- Light training is used for routing, not factual memory.
- Structured score data includes source notes and uncertainty boundaries.
- UI is intentionally simple: chat, profile, source panel, score rows.

## Subagents Used

None. Auto mode allowed subagents, but the initial build had shared contracts across backend, data, UI, and report, so sequential execution reduced merge risk.

## AGENTS.md Context Stack Used

- `AGENTS.md`
- `.byte-os/CODEBASE_MAP.md`
- `.byte-os/HARNESS.md`
- `.byte-os/AGENTS_AUDIT.md`

## Failures Or Blockers

- Port 8000 was occupied locally; local smoke used port 8001.
- Some official pages returned HTTP errors; fallback source records were preserved.
- Score rows use third-party score summary plus government news context where official school-structured rows were not directly available.

## OKR Impact

- KR1: source ingestion completed.
- KR2: structured score lookup completed for Guangdong sample rows.
- KR3: 50-question evaluation completed.
- KR4: lightweight router training completed.
- KR5: local Web demo completed; server verification pending.
- KR6: LaTeX PDF compiled.

## Next Wave

No required wave remains for v0. Optional v1: broader province data, dense embeddings, reranker, and report polish.

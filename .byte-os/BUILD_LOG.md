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
- Iteration 4 V1 Admissions Data Expansion And Dialogue Logic Repair: local complete

## Files Changed

- Repository foundation: `README.md`, `.gitignore`, `requirements.txt`, `AGENTS.md`, `CLAUDE.md`, `.claude/settings.json`
- Backend: `app/`, including program/dimension query endpoints and optional Qwen hook
- Scripts: `scripts/`
- Data: `data/sources.json`, `data/structured/admission_scores.csv`, `data/structured/programs.csv`, `data/structured/admission_dimensions.csv`, `data/training/intent_examples.csv`, `data/eval/questions.csv`, `data/eval/prospective_questions.csv`
- Frontend: `frontend/`
- Tests: `tests/`
- Report: `report/main.tex`, `report/references.bib`, `report/*.tex`, `report/smbu-admission-dialogue-report.pdf`
- Byte OS: `.byte-os/`
- Optional Qwen helper: `requirements-qwen.txt`, `scripts/serve_qwen_openai.py`

## V1 Verification Run

- Ingest: `python scripts/ingest_sources.py --limit 20`
  - documents: 13
  - fetched: 10
  - fallback: 3
- Training: `python scripts/train_intent.py`
  - accuracy: 0.9375
  - macro-F1: 0.8974
- Evaluation: `python scripts/evaluate_system.py`
  - questions: 58
  - router accuracy: 0.7586
  - source coverage: 1.000
  - average answer length: 1546.6
- Tests: `pytest`
  - 18 passed
- Compile: `python -m compileall app scripts`
  - passed
- LaTeX: compile `report/main.tex`
  - PDF generated at `report/build/main.pdf`
  - copied to `report/smbu-admission-dialogue-report.pdf`
- Local API smoke:
  - `你好`: greeting, no sources
  - `啥意思`: clarification, no sources
  - `电子与计算机工程是单学籍还是双学籍？`: one undergraduate program row, single学籍
  - `本科招生人数是多少？`: official boundary plus directly available 10-person foreign-language recommended row
  - `纳米生物技术硕士是英语教学吗，招多少人？`: English teaching, 15 students
  - `硕士有哪些专业和招生人数？`: 18 official 2026 master directions

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

- Product/data QA subagent `019f182e-9a00-7f90-a098-2d25db5dc8c8`: failed v1 readiness before fixes; findings recorded in `.byte-os/subagents/product-data-qa-019f182e-9a00.md`.
- Code QA subagent `019f182e-7d7c-7ad2-8d59-e49f48cdac19`: failed v1 readiness before fixes; findings recorded in `.byte-os/subagents/code-qa-019f182e-7d7c.md`.

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

Commit and push v1, redeploy server, attempt Qwen runtime, and run remote smoke.

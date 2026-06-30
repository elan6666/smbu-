# Iteration 4: Admissions Data Expansion And Dialogue Logic Repair

Date: 2026-06-30

## Evidence

- User screenshot showed that greetings such as `你好` and vague follow-ups such as `啥意思` were routed into retrieval and returned unrelated source dumps.
- Subagent review found the exact professional query `电子与计算机工程是单学籍还是双学籍？` could be polluted by broad `双学籍` matching.
- Subagent review also found that graduate enrollment counts were stale and that undergraduate enrollment counts needed explicit evidence boundaries.

## Changes

- Added structured undergraduate and graduate program data in `data/structured/programs.csv`.
- Added admissions dimension data in `data/structured/admission_dimensions.csv`.
- Replaced stale 2026 master rows with the 18 official master directions, including enrollment count, teaching language, certificate, tuition, and study notes.
- Added explicit greeting and clarification intents so small-talk and vague follow-ups no longer trigger RAG.
- Added `/api/programs` and `/api/dimensions` endpoints.
- Added `program_rows` and `dimension_rows` to `/api/chat`.
- Added optional local Qwen/OpenAI-compatible generation hook and helper service.
- Tightened RAG ordering so current-year official sources are preferred when the user does not specify a year.
- Tightened Qwen usage: the server can connect to local Qwen, but structured admissions facts skip model rewriting to prevent wrong enrollment counts or certificate wording.

## Verification

- `pytest`: 18 passed.
- `python -m compileall app scripts`: passed.
- `python scripts/train_intent.py`: accuracy 0.9375, macro-F1 0.8974.
- `python scripts/evaluate_system.py`: 58 questions, router accuracy 0.7586, source coverage 1.000, average answer length 1546.6.
- `python scripts/ingest_sources.py --limit 20`: 13 documents, 10 fetched, 3 fallback.
- LaTeX compile: passed; `report/smbu-admission-dialogue-report.pdf` regenerated.

## Smoke Questions

- `你好`: greeting, no sources, concise guidance.
- `啥意思`: clarification, no sources, asks user to specify a direction.
- `电子与计算机工程是单学籍还是双学籍？`: one program row, single学籍.
- `本科招生人数是多少？`: returns official boundary and only the directly available 10-person foreign-language recommended row.
- `纳米生物技术硕士是英语教学吗，招多少人？`: English teaching, 15 planned students.
- `硕士有哪些专业和招生人数？`: 18 official 2026 master directions.
